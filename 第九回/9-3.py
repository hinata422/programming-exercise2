# ============================================================
# 第9回 課題3：グラフからノードを削除する
# ============================================================
# このプログラムでは、Graph クラスにノードの削除機能
# (remove_node) を追加する。
#
# ■ プログラムの全体構成：
#   1. Neighbor クラス: 隣接ノード1つ分の情報（課題1, 2と同じ）
#   2. Graph クラス: ノード・エッジの追加 + ノード削除機能を追加
#   3. メイン部分: グラフを構築 → 特定のノードを削除 → 結果を表示
#
# ■ ノード削除のアルゴリズム：
#
#   ノードを削除する = そのノード自体と、そのノードに接続する全エッジを削除する。
#
#   例: ノードB を削除する場合（A--B--C の構造）
#
#     削除前:
#       A: [Neighbor('B', '12号')]
#       B: [Neighbor('C', '15号'), Neighbor('A', '12号')]
#       C: [Neighbor('B', '15号')]
#
#     処理手順:
#       1. Bの近傍リストの長さ（= Bに接続するエッジ数 = 2）を記録
#       2. 他の全ノード（A, C）の近傍リストから B を削除
#          A: [Neighbor('B', '12号')] → A: [] （B を除外）
#          C: [Neighbor('B', '15号')] → C: [] （B を除外）
#       3. ノードリストから B を削除（del で辞書からキーごと削除）
#       4. ノード数を1減らす
#       5. エッジ数をBに接続していた分だけ減らす
#
#     削除後:
#       A: []
#       C: []
#       ノード数: 3→2, エッジ数: 2→0
#
# ■ 課題1, 2との違い：
#   課題1: add_node, add_directed_edge, add_undirected_edge（追加のみ）
#   課題2: + remove_undirected_edge（エッジ削除）
#   課題3: + remove_node（ノード削除 = ノード自体 + 接続エッジ全て削除）
# ============================================================


# ============================================================
# Neighbor クラス（課題1, 2と同じ）
# ============================================================
class Neighbor:
    def __init__(self, id, label):
        self.id = id  # 隣接ノードのID
        self.label = label  # 隣接ノードと接続するエッジのラベル（路線名）


# ============================================================
# Graph クラス — ノード削除機能を追加
# ============================================================
class Graph:
    def __init__(self):
        self.node_list = {}  # グラフ上のノードリスト(辞書：key=ノードID, value=近傍リスト)
        self.num_nodes = 0  # グラフ上のノードの数
        self.num_edges = 0  # グラフ上のエッジの数

    def add_node(self, id):  # グラフにノードを追加するメソッド
        if id not in self.node_list:
            self.node_list[id] = []
            self.num_nodes += 1

    def add_directed_edge(self, sid, tid, label):  # グラフに有向エッジを追加するメソッド
        if sid not in self.node_list:
            self.add_node(sid)
        if tid not in self.node_list:
            self.add_node(tid)
        self.node_list[sid].insert(0, Neighbor(tid, label))  # 近傍リストの先頭に追加
        self.num_edges += 1

    def add_undirected_edge(self, sid, tid, label):  # グラフに無向エッジを追加するメソッド
        self.add_directed_edge(sid, tid, label)  # sid → tid
        self.add_directed_edge(tid, sid, label)  # tid → sid
        self.num_edges -= 1  # 無向エッジは1本としてカウント

    # ----------------------------------------------------------
    # remove_node: グラフからノードを削除するメソッド
    # ----------------------------------------------------------
    # 引数 id: 削除するノードのID
    #
    # ノードを削除する際、そのノードに接続する全エッジも一緒に削除する必要がある。
    #
    # 【処理手順の詳細】
    #
    #   ステップ1: 削除するノードに接続するエッジの数を記録
    #     → self.node_list[id] のリスト長 = そのノードから出る全エッジ数
    #     （無向グラフでは、各エッジは双方向に記録されているため、
    #      この数がそのノードに関わるエッジの総数になる）
    #
    #   ステップ2: 他のノードの近傍リストから、削除対象ノードへの参照を除去
    #     → 全隣接ノードの近傍リストを走査し、idに一致するものを除外
    #     例: ノードB を削除する場合
    #       Aの近傍 [B, C, D] → [C, D]  （Bへの参照を除去）
    #       Cの近傍 [B, E]    → [E]     （Bへの参照を除去）
    #
    #   ステップ3: ノードリストからノード自体を削除
    #     → del self.node_list[id] で辞書からキーごと削除
    #
    #   ステップ4: ノード数を1減らす
    #
    #   ステップ5: エッジ数を減らす
    #     → ステップ1で記録した数だけ減らす
    #
    # 【具体例: ノードBを削除（A--B--C, B--D の構造）】
    #
    #   削除前:
    #     A: [B(12号)]           ノード数=4, エッジ数=3
    #     B: [D(51号), C(15号), A(12号)]
    #     C: [B(15号)]
    #     D: [B(51号)]
    #
    #   ステップ1: removed_edges = len(B の近傍) = 3
    #
    #   ステップ2: 各隣接ノードの近傍からBを除去
    #     A: [B(12号)] → A: []
    #     C: [B(15号)] → C: []
    #     D: [B(51号)] → D: []
    #
    #   ステップ3: ノードリストからBを削除
    #
    #   結果:
    #     A: []                  ノード数=3, エッジ数=0
    #     C: []
    #     D: []
    # ----------------------------------------------------------
    def remove_node(self, id):
        if id not in self.node_list:  # ノードが存在しなければ何もしない
            return

        # ステップ1: 削除するノードに接続するエッジの数を記録
        removed_edges = len(self.node_list[id])

        # ステップ2: 隣接ノードの近傍リストから、削除対象ノードへの参照を除去
        # リスト内包表記で、id に一致しない Neighbor だけを残す
        for neighbor in self.node_list[id]:  # 削除対象ノードの全隣接ノードを走査
            self.node_list[neighbor.id] = [n for n in self.node_list[neighbor.id] if n.id != id]
            # neighbor.id（例: A）の近傍リストから、id（例: B）を除外した新リストで上書き

        # ステップ3: ノードリストからノード自体を削除
        del self.node_list[id]  # 辞書からキーごと削除

        # ステップ4, 5: ノード数とエッジ数を減らす
        self.num_nodes -= 1  # ノード数を1減らす
        self.num_edges -= removed_edges  # 接続していたエッジ数分を減らす

    def get_node_list(self):  # 全ノードの辞書を返す
        return self.node_list

    def get_neighborhood(self, id):  # 指定ノードの近傍リストを返す
        if id in self.node_list:
            return self.node_list[id]
        else:
            return None

    def get_num_nodes(self):  # ノード数を返す
        return self.num_nodes

    def get_num_edges(self):  # エッジ数を返す
        return self.num_edges

    def print_graph(self):  # 隣接リストを全て表示するメソッド
        for id in self.get_node_list():
            for neighbor in self.get_neighborhood(id):
                print('{} is connected to {} by {}.'.format(id, neighbor.id, neighbor.label))


# ============================================================
# メインの実行部分
# ============================================================
if __name__ == '__main__':
    # --- データの読み込みとグラフ構築 ---
    fi = open('kyotocitybus_line.dat', 'r', encoding = 'utf-8')
    bus_network = Graph()
    lines = fi.readlines()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')
        bus_network.add_undirected_edge(items[0], items[1], items[3])

    # --- ノードの削除 ---
    # ED01_1914 のノード（バス停）をグラフから完全に削除する
    # このノードに接続する全てのエッジ（12号系統、15号系統、快速202号系統 等）も
    # 一緒に削除される
    bus_network.remove_node('ED01_1914')

    # --- 結果の表示 ---
    print('ノード(バス停)の数は{}個'.format(bus_network.get_num_nodes()))
    print('エッジ(バス停間のリンク)の数は{}個'.format(bus_network.get_num_edges()))
    bus_network.print_graph()
    fi.close()
