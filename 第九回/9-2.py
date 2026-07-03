# ============================================================
# 第9回 課題2：グラフからエッジを削除する
# ============================================================
# このプログラムでは、課題1の Graph クラスに無向エッジの削除機能
# (remove_undirected_edge) を追加する。
#
# ■ プログラムの全体構成：
#   1. Neighbor クラス: 隣接ノード1つ分の情報（課題1と同じ）
#   2. Graph クラス: ノード・エッジの追加 + エッジの削除機能を追加
#   3. メイン部分: グラフを構築 → 特定のエッジを削除 → 結果を表示
#
# ■ エッジ削除のアルゴリズム：
#
#   無向エッジの削除 = 両方向の有向エッジを削除すること。
#
#   例: A --[12号系統]-- B を削除する場合
#     1. Aの近傍リストから B(12号系統) を削除
#     2. Bの近傍リストから A(12号系統) を削除
#     3. エッジ数を1減らす
#
#   label指定なしの場合（label=None）:
#     A-B間の全エッジを削除する（複数路線があれば全て削除）
#     例: A-B間に 12号系統 と 15号系統 があれば両方削除
#
#   label指定ありの場合:
#     A-B間の指定ラベルのエッジだけを1本削除する
#     例: label='12号系統' → 12号系統だけ削除、15号系統は残る
#
# ■ 課題1との違い：
#   課題1: add_node, add_directed_edge, add_undirected_edge（追加のみ）
#   課題2: + remove_undirected_edge（エッジ削除を追加）
# ============================================================


# ============================================================
# Neighbor クラス（課題1と同じ）
# ============================================================
class Neighbor:
    def __init__(self, id, label):
        self.id = id  # 隣接ノードのID
        self.label = label  # 隣接ノードと接続するエッジのラベル（路線名）


# ============================================================
# Graph クラス — エッジ削除機能を追加
# ============================================================
class Graph:
    def __init__(self):
        self.node_list = {}  # グラフ上のノードリスト(辞書：key=ノードID, value=近傍リスト)
        self.num_nodes = 0  # グラフ上のノードの数
        self.num_edges = 0  # グラフ上のエッジの数

    def add_node(self, id):  # グラフにノードを追加するメソッド
        if id not in self.node_list:  # ノードリストにidのノードが無ければ
            self.node_list[id] = []  # 近傍リストを空で初期化
            self.num_nodes += 1  # ノードの数をインクリメント

    def add_directed_edge(self, sid, tid, label):  # グラフに有向エッジを追加するメソッド
        if sid not in self.node_list:  # 始点のノードが無ければ追加
            self.add_node(sid)
        if tid not in self.node_list:  # 終点のノードが無ければ追加
            self.add_node(tid)
        self.node_list[sid].insert(0, Neighbor(tid, label))  # 近傍リストの先頭に追加
        self.num_edges += 1  # エッジの数をインクリメント

    def add_undirected_edge(self, sid, tid, label):  # グラフに無向エッジを追加するメソッド
        self.add_directed_edge(sid, tid, label)  # sid → tid のエッジを追加
        self.add_directed_edge(tid, sid, label)  # tid → sid のエッジを追加
        self.num_edges -= 1  # 2回加算されたので1回引く（無向エッジは1本）

    # ----------------------------------------------------------
    # remove_undirected_edge: 無向エッジを削除するメソッド
    # ----------------------------------------------------------
    # 引数 sid: エッジの一端のノードID
    # 引数 tid: エッジの他端のノードID
    # 引数 label: 削除するエッジのラベル（None の場合は sid-tid 間の全エッジ削除）
    #
    # 【label=None の場合（全削除）】
    #   sid-tid 間のエッジを全て削除する。
    #
    #   処理手順:
    #     1. sidの近傍リストから tid に一致するNeighborを全て除外
    #        → リスト内包表記 [n for n in ... if n.id != tid] で実現
    #     2. 削除した数を計算（元の長さ - 新しい長さ）
    #     3. tidの近傍リストから sid に一致するNeighborを全て除外
    #     4. エッジ数を減らす
    #
    #   具体例:
    #     sid='A', tid='B' で、A-B間に 12号系統 と 15号系統 がある場合
    #     → Aの近傍から B(12号), B(15号) を両方削除
    #     → Bの近傍から A(12号), A(15号) を両方削除
    #     → エッジ数を2減らす
    #
    # 【label指定ありの場合（1本だけ削除）】
    #   sid-tid 間の指定ラベルのエッジを1本だけ削除する。
    #
    #   処理手順:
    #     1. sidの近傍リストを走査し、id==tid かつ label一致の最初の要素を pop
    #     2. tidの近傍リストを走査し、id==sid かつ label一致の最初の要素を pop
    #     3. エッジ数を1減らす
    #
    #   具体例:
    #     sid='A', tid='B', label='12号系統' の場合
    #     → Aの近傍から B(12号系統) を1つだけ削除（15号系統は残る）
    #     → Bの近傍から A(12号系統) を1つだけ削除
    #     → エッジ数を1減らす
    # ----------------------------------------------------------
    def remove_undirected_edge(self, sid, tid, label=None):
        if sid not in self.node_list or tid not in self.node_list:  # どちらかのノードが存在しなければ何もしない
            return

        if label is None:
            # --- label未指定: sid-tid間の全エッジを削除 ---
            original_len = len(self.node_list[sid])  # 削除前の近傍リストの長さを記録

            # リスト内包表記: tid以外のNeighborだけを残す新しいリストを作成
            # [n for n in リスト if 条件] → 条件を満たす要素だけを集めた新リスト
            self.node_list[sid] = [n for n in self.node_list[sid] if n.id != tid]

            removed_count = original_len - len(self.node_list[sid])  # 削除されたエッジの数を計算

            # 逆方向も同様に削除
            self.node_list[tid] = [n for n in self.node_list[tid] if n.id != sid]

            self.num_edges -= removed_count  # 削除したエッジ数分を減らす
        else:
            # --- label指定あり: 該当する1本だけ削除 ---

            # enumerate: リストの要素をインデックス付きで取り出す
            # enumerate([A, B, C]) → (0, A), (1, B), (2, C)
            for i, n in enumerate(self.node_list[sid]):  # sidの近傍リストを走査
                if n.id == tid and n.label == label:  # tid かつ label が一致する最初の要素
                    self.node_list[sid].pop(i)  # pop(i): i番目の要素を削除
                    break  # 1本だけ削除するので見つかったらループ終了

            for i, n in enumerate(self.node_list[tid]):  # tidの近傍リストを走査（逆方向）
                if n.id == sid and n.label == label:  # sid かつ label が一致する最初の要素
                    self.node_list[tid].pop(i)  # 逆方向のエッジも削除
                    break

            self.num_edges -= 1  # 無向エッジ1本分を減らす

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

    # --- エッジの削除 ---
    # ED01_1914 と ED01_1925 の間の M1号系統 のエッジを1本削除する
    # label='M1号系統' を指定しているので、この路線のエッジだけが削除される
    # 他の路線（15号系統、50号系統など）のエッジは残る
    bus_network.remove_undirected_edge('ED01_1914', 'ED01_1925', 'M1号系統')

    # --- 結果の表示 ---
    print('ノード(バス停)の数は{}個'.format(bus_network.get_num_nodes()))
    print('エッジ(バス停間のリンク)の数は{}個'.format(bus_network.get_num_edges()))
    bus_network.print_graph()
    fi.close()
