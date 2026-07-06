# ============================================================
# 第11回 課題2：最短パスを見つける
# ============================================================
# このプログラムでは、課題1で作成した GraphSearch クラスに、
# スタート地点から目的地までの最短パスを見つける
# find_shortest_path メソッドを追加する。
#
# ■ プログラムの全体構成：
#   1. def_graph.py から Graph クラスを読み込む
#   2. def_queue_stack.py から Queue クラスを読み込む
#   3. def_stop.py から Stop クラスを読み込む
#   4. GraphSearch クラス: BFS + find_shortest_path + trace_longest_path
#   5. メイン部分: ED01_1914 から ED01_4089 までの最短パスを出力
#
#
# ================================================================
# ■ 課題1（BFS で全ノード探索）との違い
# ================================================================
#
# 【課題1: search_with_BFS】
#   - 全ノードを訪問し終わってから trace_longest_path を呼ぶ
#   - 全ノードの中で最もホップ数が多い（最も遠い）パスを表示
#   - キューが空になるまでループを続ける
#
# 【課題2: find_shortest_path】
#   - 目的地（goal）に到達した時点で即座にパスを表示して終了
#   - 全ノードを訪問する必要がない → goalを見つけたらreturn
#   - BFS は近い順に訪問するため、最初に goal に到達したパスが最短
#
# 【コードの差分】
#
#   課題1 (search_with_BFS):
#     while not queue.is_empty():
#         current = queue.dequeue()
#         ... 隣接ノードを処理 ...
#     self.trace_longest_path(parents)  ← ループ後に呼ぶ
#
#   課題2 (find_shortest_path):
#     while not queue.is_empty():
#         current = queue.dequeue()
#         if current == goal:        ← ★ 目的地チェックを追加
#             ... パスを表示 ...
#             return                  ← ★ 見つかったら即終了
#         ... 隣接ノードを処理 ...
#
#
# ================================================================
# ■ なぜ BFS で最短パスが求まるのか？
# ================================================================
#
# BFS はスタート地点から「近い順」にノードを訪問する。
# つまり:
#   - 1ホップで行けるノードを全て訪問
#   - 次に2ホップで行けるノードを全て訪問
#   - 次に3ホップで行けるノードを全て訪問
#   - ...
#
# したがって、BFS で初めて goal に到達した時のパスは、
# 必ず最短（最小ホップ数）のパスになる。
#
# 【具体例】
#
#   グラフ:  S --[a]--> A --[b]--> B --[c]--> G（goal）
#            |                      ↑
#           [d]                    [e]
#            |                      |
#            C --------[f]-------> D
#
#   BFS の訪問順:
#     ホップ0: S
#     ホップ1: A, C      ← S の隣接
#     ホップ2: B, D      ← A, C の隣接
#     ホップ3: G          ← B の隣接（ここで goal に到達！）
#
#   パス: S → A → B → G（3ホップ）
#   ※ S → C → D → B → G（4ホップ）というパスもあるが、
#     BFS は近い順に訪問するので3ホップの方が先に見つかる
#
#
# ================================================================
# ■ find_shortest_path のアルゴリズム
# ================================================================
#
# 基本的な流れは search_with_BFS と同じ。違いは以下の2点:
#
# 【違い1: dequeue 後に goal チェック】
#   current = queue.dequeue() の後に:
#     if current == goal:
#         → パスを表示して return
#
# 【違い2: パスの復元方法】
#   trace_longest_path は全ノードの中から最長を選ぶが、
#   find_shortest_path は goal ノードから parents を辿って
#   スタート地点まで遡り、パスを直接構築する。
#
#   goal から遡る:
#     current = goal
#     path = "京都駅前"
#     parents[goal] = ('七条堀川', '快速9号系統')
#     → path = "七条堀川 --[快速9号系統]--> 京都駅前"
#     parents['七条堀川'] = ('堀川五条', '快速9号系統')
#     → path = "堀川五条 --[快速9号系統]--> 七条堀川 --[快速9号系統]--> 京都駅前"
#     ...（start に到達するまで繰り返す）
#
#
# ================================================================
# ■ 実行結果
# ================================================================
#
#   京都駅前まで12ホップ：立命館大学前 --[M1号系統]--> 桜木町
#   --[臨号系統]--> わら天神前 --[臨号系統]--> 北大路バスターミナル
#   --[臨号系統]--> 出町柳駅前 --[203号系統]--> 河原町今出川
#   --[102号系統]--> 堀川今出川 --[101号系統]--> 堀川丸太町
#   --[快速9号系統]--> 堀川御池 --[快速9号系統]--> 四条堀川
#   --[快速9号系統]--> 堀川五条 --[快速9号系統]--> 七条堀川
#   --[快速9号系統]--> 京都駅前
# ============================================================

from def_graph import Graph  # Graphクラスの読み込み
from def_queue_stack import Queue  # Queueクラスの読み込み（BFS にはキューが必要）
from def_stop import Stop  # Stopクラスの読み込み


# ============================================================
# GraphSearch クラス — Graph を継承して BFS + 最短パス探索を追加
# ============================================================
class GraphSearch(Graph):
    def __init__(self):
        super().__init__()  # Graphクラスから継承したインスタンス変数の初期化
        self.busstops = {}  # バス停情報を格納するための辞書データ

    # ----------------------------------------------------------
    # search_with_BFS: 課題1と同じ（全ノードを BFS で訪問）
    # ----------------------------------------------------------
    def search_with_BFS(self, start):
        queue = Queue()
        parents = {start: None}
        visited = [start]
        queue.enqueue(start)
        while not queue.is_empty():
            current = queue.dequeue()
            if current not in self.node_list:
                print('{}のノードがグラフ上に存在しません。'.format(current))
                return
            neighbors = self.get_neighborhood(current)
            for neighbor in neighbors:
                if neighbor.id not in visited:
                    parents[neighbor.id] = (current, neighbor.label)
                    visited.append(neighbor.id)
                    queue.enqueue(neighbor.id)
        self.trace_longest_path(parents)

    # ----------------------------------------------------------
    # find_shortest_path: BFS で最短パスを見つけるメソッド
    # ----------------------------------------------------------
    # 引数 start: 開始ノードのID（文字列）
    # 引数 goal: 目的地ノードのID（文字列）
    #
    # 【search_with_BFS との違い】
    #   search_with_BFS: 全ノード訪問後に trace_longest_path
    #   find_shortest_path: goal に到達したら即座にパスを表示して終了
    #
    # 【なぜこれで最短パスになるのか】
    #   BFS はスタートに近い順にノードを訪問する。
    #   したがって、BFS で最初に goal に到達したパスが必ず最短。
    #   goal が見つかった時点で、それ以上探索を続ける必要はない。
    # ----------------------------------------------------------
    def find_shortest_path(self, start, goal):
        # --- 初期化（search_with_BFS と同じ） ---
        queue = Queue()  # BFS 用のキューを作成
        parents = {start: None}  # 経路情報の辞書
        visited = [start]  # 訪問済みリスト
        queue.enqueue(start)  # 開始ノードをキューに追加

        # --- BFS メインループ ---
        while not queue.is_empty():
            current = queue.dequeue()  # キューからノードを取り出す

            if current not in self.node_list:  # ノードが存在しなければエラー
                print('{}のノードがグラフ上に存在しません。'.format(current))
                return

            # ★ search_with_BFS との最大の違い: goal チェック ★
            if current == goal:  # 目的地に到達したらパスを表示
                # --- parents 辞書を逆順にたどってパスを復元 ---
                # goal から start まで1つずつ遡る
                #
                # 例: goal = ED01_4089（京都駅前）の場合
                #   parents[ED01_4089] = ('七条堀川のID', '快速9号系統')
                #   → current を七条堀川に移動
                #   parents[七条堀川のID] = ('堀川五条のID', '快速9号系統')
                #   → current を堀川五条に移動
                #   ...
                #   parents[ED01_1914] = None → ループ終了
                path = self.busstops[current].name  # 目的地のバス停名をパスに設定
                hops = 0  # ホップ数を初期化
                parent = parents[current]  # 目的地の1つ前の情報を取得
                while parent is not None:  # スタート地点に到達するまで遡る
                    current = parent[0]  # 1つ前のノードに移動
                    path = self.busstops[current].name + ' --[' + parent[1] + ']--> ' + path
                    # パスの先頭に「前のバス停 --[路線名]--> 」を連結
                    hops += 1  # ホップ数をカウント
                    parent = parents[current]  # さらに1つ前の情報を取得
                print('{}まで{}ホップ：{}'.format(self.busstops[goal].name, hops, path))
                return  # ★ パスを表示したら即終了（これ以上探索不要）

            # --- 隣接ノードの処理（search_with_BFS と同じ） ---
            neighbors = self.get_neighborhood(current)
            for neighbor in neighbors:
                if neighbor.id not in visited:  # 未訪問の隣接ノードのみ処理
                    parents[neighbor.id] = (current, neighbor.label)  # 経路情報を記録
                    visited.append(neighbor.id)  # 訪問済みに追加
                    queue.enqueue(neighbor.id)  # キューに追加

        # --- キューが空になっても goal に到達できなかった場合 ---
        print('{}から{}へのパスが見つかりませんでした。'.format(start, goal))

    # ----------------------------------------------------------
    # trace_longest_path: 課題1と同じ（最長パスを表示）
    # ----------------------------------------------------------
    def trace_longest_path(self, parents):
        max_hops = 0
        longest_path = ''
        furthest_dest = ''
        for dest in parents:
            current = dest
            path = self.busstops[current].name
            hops = 0
            parent = parents[current]
            while parent is not None:
                current = parent[0]
                path = self.busstops[current].name + ' --[' + parent[1] + ']--> ' + path
                hops += 1
                parent = parents[current]
            if hops > max_hops:
                max_hops = hops
                longest_path = path
                furthest_dest = dest
        print('{}まで{}ホップ：{}'.format(self.busstops[furthest_dest].name, max_hops, longest_path))


# ============================================================
# メインの実行部分
# ============================================================
if __name__ == '__main__':

    # --- 路線データの読み込みとグラフ構築 ---
    fi = open('kyotocitybus_line.dat', 'r', encoding='utf-8')
    bus_network = GraphSearch()
    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')
        bus_network.add_undirected_edge(items[0], items[1], items[3])

    # --- バス停データの読み込み ---
    fi2 = open('kyotocitybus_stop.dat', 'r', encoding='utf-8')
    lines = fi2.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')
        bus_network.busstops[items[0]] = Stop(items[0], items[1], items[2], items[3], items[4:])

    # --- 最短パスの探索 ---
    # ED01_1914（立命館大学前）から ED01_4089（京都駅前）までの最短パスを表示
    bus_network.find_shortest_path('ED01_1914', 'ED01_4089')
    fi.close()
    fi2.close()
