# ============================================================
# 第11回 課題3：深さ優先探索（DFS）で全ノードを辿る
# ============================================================
# このプログラムでは、課題1で作成した GraphSearch クラスに、
# 深さ優先探索（DFS: Depth-First Search）で全ノードを訪問する
# search_with_DFS メソッドを追加する。
#
# ■ プログラムの全体構成：
#   1. def_graph.py から Graph クラスを読み込む
#   2. def_queue_stack.py から Stack, Queue クラスを読み込む
#   3. def_stop.py から Stop クラスを読み込む
#   4. GraphSearch クラス: BFS + DFS + trace_longest_path
#   5. メイン部分: ED01_1914 から DFS で探索し、最長パスを表示
#
#
# ================================================================
# ■ BFS（幅優先探索）と DFS（深さ優先探索）の違い
# ================================================================
#
# 【BFS（幅優先探索）— 課題1】
#   - キュー（FIFO）を使う
#   - スタートに近いノードから順に訪問する（波紋が広がるイメージ）
#   - 全ての隣接ノードを発見してからキューに入れ、先に入れたものから処理
#   - 結果: 浅く広く探索 → 最短経路が求まる
#
# 【DFS（深さ優先探索）— 課題3】
#   - スタック（LIFO）を使う
#   - 1つの方向に行けるところまで深く進み、行き止まりになったら戻る
#   - 隣接ノードを1つだけ選んで深く進み、戻れなくなったらバックトラック
#   - 結果: 深く狭く探索 → 同じグラフでも BFS とは異なるパスになる
#
# 【図解】
#
#   グラフ:     S
#              / \
#             A   B
#            / \   \
#           C   D   E
#
#   BFS の訪問順: S → A → B → C → D → E
#     （ホップ1の A, B を先に訪問 → ホップ2の C, D, E を後で訪問）
#
#   DFS の訪問順: S → A → C → D → B → E
#     （A に進んだら、A の先の C まで行く → C が行き止まりなので A に戻る
#      → A のもう1つの隣接 D に進む → D が行き止まりなので S に戻る
#      → S のもう1つの隣接 B に進む → B の先の E まで行く）
#
# 【データ構造の違い】
#
#   BFS:                         DFS:
#   キュー（FIFO）               スタック（LIFO）
#   enqueue → [A,B,C] → dequeue  push → [A,B,C] → pop
#   先に入れた A が先に出る       最後に入れた C が先に出る
#   → 幅優先（近い順）           → 深さ優先（深い方から）
#
#
# ================================================================
# ■ DFS でなぜスタックを使うのか？
# ================================================================
#
# DFS は「行き止まりになったら元の場所に戻る（バックトラック）」
# 必要がある。スタックは「最後に入れたものを最初に取り出す」ため、
# 直前に通った場所を記憶するのに最適。
#
# 【バックトラックの仕組み】
#
#   前進（push）:
#     新しいノードに進むたびにスタックに積む
#     stack = [S, A, C]  ← S から A を経由して C まで来た
#
#   後退（pop）:
#     行き止まりになったらスタックから取り出す
#     pop → C を取り出す → stack = [S, A]  ← A に戻る
#     A にまだ未訪問の隣接ノード D がある → push(D)
#     stack = [S, A, D]  ← A から D に進む
#
#   → スタックの中身が「現在地までの経路」を表している
#
#
# ================================================================
# ■ DFS のアルゴリズム（スタックを使った反復的実装）
# ================================================================
#
# 【使用するデータ構造】
#
#   stack: Stack オブジェクト — 現在の探索パスを記録
#     スタックの先頭（一番上）が現在位置を表す
#     push で前進、pop でバックトラック
#
#   visited: リスト — 訪問済みノードIDのリスト
#
#   parents: 辞書 — 各ノードへの到達経路を記録（BFS と同じ形式）
#
# 【アルゴリズムの流れ】
#
#   1. スタックに start を push、visited に start を追加
#   2. スタックが空でない間:
#      a. スタックの先頭を参照（peek）→ current
#         ※ pop ではなく peek（見るだけで取り出さない）
#         ※ stack.list[-1] で先頭を参照する
#      b. current の隣接ノードを走査
#      c. 未訪問の隣接ノードが見つかったら:
#         - visited に追加、parents に記録
#         - スタックに push（前進）
#         - break（1つだけ選んで深く進む）
#      d. 未訪問の隣接ノードがなければ:
#         - スタックから pop（バックトラック）
#   3. 全ノード訪問後、trace_longest_path で最長パスを表示
#
# 【BFS との違い（コードの差分）】
#
#   BFS:
#     queue = Queue()
#     queue.enqueue(start)
#     while not queue.is_empty():
#         current = queue.dequeue()        ← 取り出す
#         for neighbor in neighbors:
#             if not visited:
#                 queue.enqueue(neighbor)   ← 全ての未訪問隣接をキューに入れる
#
#   DFS:
#     stack = Stack()
#     stack.push(start)
#     while not stack.is_empty():
#         current = stack.list[-1]          ← 先頭を参照するだけ（取り出さない）
#         for neighbor in neighbors:
#             if not visited:
#                 stack.push(neighbor)       ← 1つだけ選んで push
#                 break                      ← ★ 1つだけ！（深く進む）
#         if not found:
#             stack.pop()                    ← ★ バックトラック
#
# 【具体例: 小さなグラフでの DFS 動作】
#
#   グラフ:     S
#              / \
#             A   B
#            / \
#           C   D
#
#   ステップ1: stack = [S], peek → S
#     隣接: [A, B]  → A が未訪問 → push(A)
#     stack = [S, A]
#
#   ステップ2: stack = [S, A], peek → A
#     隣接: [C, D]  → C が未訪問 → push(C)
#     stack = [S, A, C]
#
#   ステップ3: stack = [S, A, C], peek → C
#     隣接: [A]  → A は訪問済み → 未訪問なし → pop(C)
#     stack = [S, A]  ← C から A にバックトラック
#
#   ステップ4: stack = [S, A], peek → A
#     隣接: [C, D]  → C は訪問済み、D が未訪問 → push(D)
#     stack = [S, A, D]
#
#   ステップ5: stack = [S, A, D], peek → D
#     隣接: なし → pop(D)
#     stack = [S, A]  ← D から A にバックトラック
#
#   ステップ6: stack = [S, A], peek → A
#     隣接: [C, D]  → 全て訪問済み → pop(A)
#     stack = [S]  ← A から S にバックトラック
#
#   ステップ7: stack = [S], peek → S
#     隣接: [A, B]  → A は訪問済み、B が未訪問 → push(B)
#     stack = [S, B]
#
#   ステップ8: stack = [S, B], peek → B
#     隣接: なし → pop(B)
#     stack = [S]  ← B から S にバックトラック
#
#   ステップ9: stack = [S], peek → S
#     隣接: [A, B]  → 全て訪問済み → pop(S)
#     stack = []  ← 空になったので終了
#
#   訪問順: S → A → C → (戻) → D → (戻)(戻) → B
#   → 深さ優先で探索されている！
#
#
# ================================================================
# ■ BFS と DFS の結果の違い（バスネットワークの場合）
# ================================================================
#
# 【BFS（課題1）の結果】
#   府道横大路まで37ホップ
#   → BFS は「浅く広く」探索するため、最も遠い（最大ホップ）ノードでも
#     37ホップしかない。BFS のパスは最短経路なので、ホップ数は少ない。
#
# 【DFS（課題3）の結果】
#   中桂まで237ホップ
#   → DFS は「深く狭く」探索するため、1つの路線を延々と辿り続ける。
#     その結果、parents に記録されるパスは非常に長くなる。
#     DFS のパスは最短経路ではないため、同じノードでもホップ数が多い。
#
# ※ 訪問するノードの総数は同じ（全ノード）だが、
#   各ノードへのパス（parents に記録される経路）が異なる。
#
#
# ================================================================
# ■ 実行結果
# ================================================================
#
#   中桂まで237ホップ：立命館大学前 --[快速202号系統]--> 小松原児童公園前
#   --[快速202号系統]--> 衣笠校前 --[快速202号系統]--> 北野白梅町
#   --[10号系統]--> 府立体育館前 ...
#   → DFS なので BFS（37ホップ）とは大きく異なる結果になる
# ============================================================

from def_graph import Graph  # Graphクラスの読み込み
from def_queue_stack import Stack, Queue  # StackクラスおよびQueueクラスの読み込み
from def_stop import Stop  # Stopクラスの読み込み


# ============================================================
# GraphSearch クラス — Graph を継承して BFS + DFS 探索機能を追加
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
    # search_with_DFS: 深さ優先探索で全ノードを訪問するメソッド
    # ----------------------------------------------------------
    # 引数 start: 深さ優先探索の開始ノードのID（文字列）
    #
    # 【BFS（search_with_BFS）との違い】
    #   BFS: キュー（FIFO）で全隣接ノードを入れて広く探索
    #   DFS: スタック（LIFO）で1つずつ深く進み、行き止まりで戻る
    #
    # 【ヒント（問題文より）】
    #   深さ優先探索は、後退操作でどのノードに戻ればいいか記憶するために、
    #   前進操作時にスタックに出発地のノードを格納する必要がある。
    # ----------------------------------------------------------
    def search_with_DFS(self, start):
        # --- 初期化 ---
        stack = Stack()  # 深さ優先探索用のスタックを作成
        # Stack() で LIFO（後入れ先出し）のスタックオブジェクトを生成
        # push で末尾に追加、pop で末尾から取り出す
        # → 直前に通ったノードを記憶し、バックトラックに使う

        parents = {start: None}  # 各ノードへの到達経路（BFS と同じ形式）
        visited = [start]  # 訪問済みリスト
        stack.push(start)  # スタックに開始ノードを追加
        # スタックの中身が「スタート地点から現在位置までの経路」を表す

        # --- DFS のメインループ ---
        while not stack.is_empty():  # スタックが空でない限り以下を繰り返す
            # スタックが空 ＝ 全ノードを訪問し、スタート地点までバックトラック完了

            current = stack.list[-1]  # スタックの先頭を参照（現在位置）
            # ★ BFS との違い: dequeue（取り出す）ではなく peek（参照するだけ）
            # stack.list[-1] はリストの末尾（＝スタックの一番上）を見るだけ
            # pop しないのは、未訪問の隣接ノードがあれば前進し、
            # なければ pop（バックトラック）するため、まず確認が必要だから

            if current not in self.node_list:
                print('{}のノードがグラフ上に存在しません。'.format(current))
                return

            neighbors = self.get_neighborhood(current)  # 現在位置の隣接ノードを取得

            # --- 未訪問の隣接ノードを1つ探す ---
            found = False  # 未訪問の隣接ノードが見つかったかどうかのフラグ
            for neighbor in neighbors:
                if neighbor.id not in visited:  # 訪問先候補が未訪問であれば
                    parents[neighbor.id] = (current, neighbor.label)
                    # parents に経路情報を記録（BFS と同じ）

                    visited.append(neighbor.id)
                    # 訪問済みリストに追加

                    stack.push(neighbor.id)  # 前進：訪問済みノードをスタックに追加
                    # ★ push することで、スタックの先頭（list[-1]）が新しいノードになる
                    # → 次のループで新しいノードが current になる（深く進む）

                    found = True
                    break  # ★ BFS との最大の違い: 1つだけ選んで深く進む
                    # BFS: 全ての未訪問隣接ノードをキューに入れる（幅優先）
                    # DFS: 最初の未訪問隣接ノードだけ選んでスタックに積む（深さ優先）
                    # → break で for ループを抜けて、すぐに while ループの先頭に戻る
                    # → 新しいノードの隣接ノードを探索する（＝深く進む）

            if not found:
                stack.pop()  # 後退：未訪問の隣接ノードがなければバックトラック
                # 現在位置の全隣接ノードが訪問済み ＝ 行き止まり
                # → pop でスタックから現在位置を取り除く
                # → スタックの新しい先頭（1つ前のノード）が current になる
                # → 1つ前のノードに戻って、そこの別の隣接ノードを探す
                #
                # 例: stack = [S, A, C] で C が行き止まり
                #     pop → stack = [S, A]
                #     次のループで current = A（A に戻る）
                #     A のまだ探索していない隣接ノード D を見つけて push(D)
                #     stack = [S, A, D]（D に前進）

        self.trace_longest_path(parents)  # 最長パスを表示

    # ----------------------------------------------------------
    # trace_longest_path: 課題1と同じ（最長パスを表示）
    # ----------------------------------------------------------
    # ※ BFS と DFS では parents の内容が異なるため、
    #   同じ trace_longest_path を使っても結果は異なる。
    #   BFS: 各ノードへの最短経路 → 最長でも37ホップ
    #   DFS: 深く進んだ経路 → 最長237ホップ
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

    # --- DFS の実行 ---
    # ED01_1914（立命館大学前）から全ノードを深さ優先探索し、最長パスを表示
    # ※ BFS（課題1）では37ホップだが、DFS では237ホップと大きく異なる
    bus_network.search_with_DFS('ED01_1914')
    fi.close()
    fi2.close()
