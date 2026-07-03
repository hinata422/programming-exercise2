# ============================================================
# 第10回 課題2：グラフ上を巡回せずに歩く
# ============================================================
# このプログラムでは、課題1の walk メソッドを改良し、
# 訪問済みのノードを再訪しない walk_without_loop メソッドを実装する。
#
# ■ プログラムの全体構成：
#   1. def_graph.py から Graph クラスを読み込む
#   2. GraphWalk クラス: Graph を継承し、walk_without_loop メソッドを追加
#   3. メイン部分: グラフを構築して、ループせずに5ステップ分歩く
#
#
# ================================================================
# ■ 課題1の walk との違い
# ================================================================
#
# 【課題1の問題点: ループしてしまう】
#   walk では neighbors[0]（先頭の隣接ノード）を無条件に選ぶため、
#   2つのノード間を行ったり来たりしてしまう。
#
#   例: ED01_1914 → ED01_1936 → ED01_1914 → ED01_1936 → ...
#       ↑ 同じ2ノード間を永遠にループ！
#
# 【課題2の改良点: 訪問済みノードをスキップ】
#   隣接ノードリストを走査し、visited に含まれていない（未訪問の）
#   最初のノードを次の訪問先に選ぶ。
#
#   例: ED01_1914 → ED01_1936 → ED01_1927 → ED01_1883 → ...
#       ↑ 毎回新しいノードに進む！
#
#
# ================================================================
# ■ walk_without_loop のアルゴリズム
# ================================================================
#
# 【課題1の walk との違い（コードの差分）】
#
#   課題1 (walk):
#     neighbors = self.get_neighborhood(current)
#     if neighbors != []:
#         next = neighbors[0]  ← 先頭を無条件に選ぶ
#
#   課題2 (walk_without_loop):
#     neighbors = self.get_neighborhood(current)
#     next_node = None
#     for neighbor in neighbors:        ← 隣接ノードを順に走査
#         if neighbor.id not in visited:  ← 未訪問かチェック
#             next_node = neighbor        ← 未訪問なら選択
#             break                       ← 最初の未訪問ノードで終了
#
# 【具体例: ED01_1914 から 5ステップ（ループなし）】
#
#   ステップ1: current = ED01_1914
#     隣接ノード: [ED01_1936(快速202号系統), ED01_1925(M1号系統), ...]
#     visited = [ED01_1914]
#     ED01_1936 は visited にない → 選択！
#     → ED01_1936 へ移動
#
#   ステップ2: current = ED01_1936
#     隣接ノード: [ED01_1914(快速202号系統), ED01_1927(快速202号系統), ...]
#     visited = [ED01_1914, ED01_1936]
#     ED01_1914 は visited にある → スキップ
#     ED01_1927 は visited にない → 選択！
#     → ED01_1927 へ移動
#
#   ステップ3: current = ED01_1927
#     ...ED01_1883 へ移動（未訪問の最初のノード）
#
#   ステップ4: current = ED01_1883
#     隣接ノード: [ED01_1882(10号系統), ED01_1930(快速202号系統), ...]
#     ED01_1882 は visited にない → 選択！
#     → ED01_1882 へ移動（快速202号系統ではなく10号系統になる）
#
#   ステップ5: current = ED01_1882
#     → ED01_1881 へ移動
#
#   結果: ED01_1914 --[快速202号系統]--> ED01_1936 --[快速202号系統]--> ED01_1927
#         --[快速202号系統]--> ED01_1883 --[10号系統]--> ED01_1882 --[10号系統]--> ED01_1881
#
#   ※ ステップ4で路線が変わるのは、ED01_1883 の隣接リストの先頭で
#     未訪問のノードが 10号系統 の ED01_1882 だったため
# ============================================================

from def_graph import Graph  # Graphクラスの読み込み


# ============================================================
# GraphWalk クラス — Graph を継承してループなしウォーク機能を追加
# ============================================================
class GraphWalk(Graph):

    # ----------------------------------------------------------
    # walk_without_loop: 訪問済みノードを避けて歩くメソッド
    # ----------------------------------------------------------
    # 引数 start: ウォーク開始ノードのID（文字列）
    # 引数 step: 辿る隣接ノードの数（整数）
    #
    # 課題1の walk との違い:
    #   walk: neighbors[0] を無条件に選ぶ → ループする可能性がある
    #   walk_without_loop: visited に含まれない最初の隣接ノードを選ぶ → ループしない
    # ----------------------------------------------------------
    def walk_without_loop(self, start, step):
        visited = [start]  # 開始地点のノードIDを訪問済みリストに追加
        parents = {start:None}  # 経路情報を格納する辞書（開始地点の直前はNone）
        current = start  # 現在地を開始地点に設定

        for i in range(step):  # step回、訪問を繰り返す
            if current not in self.node_list:  # 訪問中ノードがグラフに存在しなければ
                print('{}のノードがグラフ上に存在しません。'.format(current))
                return

            neighbors = self.get_neighborhood(current)  # 現在地の隣接ノードリストを取得

            # --- 未訪問の隣接ノードを探す ---
            # 課題1との最大の違い: neighbors[0] を無条件に選ぶのではなく、
            # for ループで隣接ノードを順に走査し、visited に含まれない最初のノードを選ぶ
            next_node = None  # 次の訪問先を格納する変数（見つからなければ None のまま）
            for neighbor in neighbors:  # 隣接ノードを先頭から順に走査
                if neighbor.id not in visited:  # 未訪問のノードかチェック
                    next_node = neighbor  # 未訪問なら次の訪問先として選択
                    break  # 最初に見つかった未訪問ノードを選ぶのでループ終了

            if next_node is not None:  # 未訪問の隣接ノードが見つかった場合
                visited.append(next_node.id)  # 訪問済みリストに追加
                parents[next_node.id] = (current, next_node.label)  # 経路情報を記録
                current = next_node.id  # 現在地を次の訪問先に更新
            else:  # 全ての隣接ノードが訪問済み（または隣接ノードがない）場合
                print('{}から{}ステップ分進むパスはありません。'.format(start, step))
                return

        # --- 訪問経路を文字列として表示 ---
        path = visited[0]  # 開始地点をpathに代入
        for v in visited[1:]:  # 2番目以降の訪問ノードを順に取得
            path = path + ' --[' + parents[v][1] +']--> ' + v  # 経路を連結
        print(path)


# ============================================================
# メインの実行部分
# ============================================================
if __name__ == '__main__':
    # --- データの読み込みとグラフ構築 ---
    fi = open('kyotocitybus_line.dat', 'r', encoding = 'utf-8')
    bus_network = GraphWalk()
    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')
        bus_network.add_undirected_edge(items[0], items[1], items[3])

    # --- ループなしウォークの実行 ---
    # ED01_1914 から 5ステップ分、訪問済みノードを避けて歩く
    bus_network.walk_without_loop('ED01_1914', 5)
    fi.close()
