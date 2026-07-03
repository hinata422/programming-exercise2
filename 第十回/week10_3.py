# ============================================================
# 第10回 課題3：グラフ上の指定された道を歩く
# ============================================================
# このプログラムでは、課題1の walk メソッドを改良し、
# 指定したラベル（路線名）のエッジだけを辿る walk_along_route メソッドを実装する。
#
# ■ プログラムの全体構成：
#   1. def_graph.py から Graph クラスを読み込む
#   2. GraphWalk クラス: Graph を継承し、walk_along_route メソッドを追加
#   3. メイン部分: グラフを構築して、快速202号系統だけを辿って5ステップ歩く
#
#
# ================================================================
# ■ 課題1, 2との違い
# ================================================================
#
# 【3つの walk の比較】
#
#   課題1 walk:
#     neighbors[0] を無条件に選ぶ → ループする可能性がある
#     選択基準: なし（先頭を選ぶだけ）
#
#   課題2 walk_without_loop:
#     未訪問の最初の隣接ノードを選ぶ → ループしない
#     選択基準: neighbor.id not in visited
#
#   課題3 walk_along_route:
#     指定ルートかつ未訪問の最初の隣接ノードを選ぶ → 特定路線だけを辿る
#     選択基準: neighbor.label == route AND neighbor.id not in visited
#
# 【なぜ未訪問チェックも必要なのか】
#   ラベルだけでフィルタすると、課題1と同様にループする可能性がある。
#   例: A --[快速202号系統]--> B --[快速202号系統]--> A → ループ！
#   → visited チェックを加えることで、同じ路線上でもループを防ぐ
#
#
# ================================================================
# ■ walk_along_route のアルゴリズム
# ================================================================
#
# 【コードの差分（課題2との違い）】
#
#   課題2 (walk_without_loop):
#     for neighbor in neighbors:
#         if neighbor.id not in visited:    ← 未訪問だけチェック
#             next_node = neighbor
#             break
#
#   課題3 (walk_along_route):
#     for neighbor in neighbors:
#         if neighbor.label == route and neighbor.id not in visited:
#             next_node = neighbor          ← ラベル一致 AND 未訪問
#             break
#
#   → 条件が1つ追加されただけ（neighbor.label == route）
#
# 【具体例: ED01_1914 から 快速202号系統 で 5ステップ】
#
#   ステップ1: current = ED01_1914
#     隣接ノード: [ED01_1936(快速202号系統), ED01_1925(M1号系統), ...]
#     ED01_1936 のラベル = 快速202号系統 → route と一致、かつ未訪問 → 選択！
#     → ED01_1936 へ移動
#
#   ステップ2: current = ED01_1936
#     隣接ノード: [ED01_1914(快速202号系統), ED01_1927(快速202号系統), ...]
#     ED01_1914: ラベル一致だが visited にある → スキップ
#     ED01_1927: ラベル一致かつ未訪問 → 選択！
#     → ED01_1927 へ移動
#
#   ステップ3: current = ED01_1927
#     → ED01_1883 へ移動（快速202号系統で未訪問）
#
#   ステップ4: current = ED01_1883
#     隣接ノード: [ED01_1882(10号系統), ED01_1930(快速202号系統), ...]
#     ED01_1882: ラベル = 10号系統 → route と不一致 → スキップ
#     ED01_1930: ラベル = 快速202号系統 → route と一致、かつ未訪問 → 選択！
#     → ED01_1930 へ移動
#     ※ 課題2では ED01_1882(10号系統) が選ばれたが、
#       課題3では路線フィルタにより ED01_1930(快速202号系統) が選ばれる
#
#   ステップ5: current = ED01_1930
#     → ED01_1742 へ移動（快速202号系統で未訪問）
#
#   結果: ED01_1914 --[快速202号系統]--> ED01_1936 --[快速202号系統]--> ED01_1927
#         --[快速202号系統]--> ED01_1883 --[快速202号系統]--> ED01_1930
#         --[快速202号系統]--> ED01_1742
#   → 全て快速202号系統のエッジだけを辿っている！
# ============================================================

from def_graph import Graph  # Graphクラスの読み込み


# ============================================================
# GraphWalk クラス — Graph を継承して指定ルートウォーク機能を追加
# ============================================================
class GraphWalk(Graph):

    # ----------------------------------------------------------
    # walk_along_route: 指定ルート（エッジラベル）だけを辿って歩くメソッド
    # ----------------------------------------------------------
    # 引数 start: ウォーク開始ノードのID（文字列）
    # 引数 step: 辿る隣接ノードの数（整数）
    # 引数 route: 辿るエッジのラベル（文字列、例: '快速202号系統'）
    #
    # 課題2との違い:
    #   walk_without_loop: visited にないノードを選ぶ
    #   walk_along_route: visited にない AND ラベルが route に一致するノードを選ぶ
    # ----------------------------------------------------------
    def walk_along_route(self, start, step, route):
        visited = [start]  # 開始地点のノードIDを訪問済みリストに追加
        parents = {start:None}  # 経路情報を格納する辞書（開始地点の直前はNone）
        current = start  # 現在地を開始地点に設定

        for i in range(step):  # step回、訪問を繰り返す
            if current not in self.node_list:  # 訪問中ノードがグラフに存在しなければ
                print('{}のノードがグラフ上に存在しません。'.format(current))
                return

            neighbors = self.get_neighborhood(current)  # 現在地の隣接ノードリストを取得

            # --- 指定ルートかつ未訪問の隣接ノードを探す ---
            # 課題2との違い: neighbor.label == route の条件が追加されている
            next_node = None  # 次の訪問先（見つからなければ None のまま）
            for neighbor in neighbors:  # 隣接ノードを先頭から順に走査
                if neighbor.label == route and neighbor.id not in visited:
                    # ↑ 2つの条件を AND で結合:
                    #   1. neighbor.label == route: エッジのラベルが指定ルートと一致
                    #   2. neighbor.id not in visited: まだ訪問していないノード
                    next_node = neighbor  # 両方の条件を満たすノードを次の訪問先に選択
                    break  # 最初に見つかったノードを選ぶのでループ終了

            if next_node is not None:  # 条件を満たす隣接ノードが見つかった場合
                visited.append(next_node.id)  # 訪問済みリストに追加
                parents[next_node.id] = (current, next_node.label)  # 経路情報を記録
                current = next_node.id  # 現在地を次の訪問先に更新
            else:  # 指定ルートの未訪問隣接ノードがない場合
                # エラーメッセージ形式: "{ルート名}では{開始ノード}から{ステップ数}ステップ分進むパスはありません。"
                print('{}では{}から{}ステップ分進むパスはありません。'.format(route, start, step))
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

    # --- 指定ルートウォークの実行 ---
    # ED01_1914 から 快速202号系統 のエッジだけを辿って 5ステップ分歩く
    bus_network.walk_along_route('ED01_1914', 5, '快速202号系統')
    fi.close()
