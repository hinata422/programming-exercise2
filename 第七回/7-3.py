# ============================================================
# 第7回 課題3：ヒープを作る（build_heap）
# ============================================================
# 課題1では insert を繰り返してヒープを構築したが、
# 課題3では build_heap メソッドを使い、与えられたリストから
# 直接ヒープを構築する。
#
# ■ 課題1（insert方式）と課題3（build_heap方式）の違い：
#
#   【insert方式（課題1）】
#     - データを1つずつ末尾に追加し、毎回 shift_up で押し上げる
#     - 計算量: O(n log n)（n個のデータそれぞれに O(log n) の shift_up）
#     - 挿入順にヒープが成長していくので、結果のヒープの形は挿入順に依存
#
#   【build_heap方式（課題3）— ボトムアップ構築】
#     - まずデータを全てリストに入れてから、ヒープ条件を回復する
#     - リストの後半（葉ノード）は子を持たないのでヒープ条件を自動的に満たす
#     - 最後の親ノード（size // 2）から根に向かって順に shift_down を適用
#     - 計算量: O(n)（insert方式の O(n log n) より高速！）
#
#   ※ 両方ともヒープ条件は満たすが、木の形（どのノードがどこに配置されるか）は
#     異なる場合がある
#
# ■ build_heap のアルゴリズム：
#
#   例: リスト [5, 3, 8, 1, 2] からヒープを構築する場合
#
#   ステップ0: リストをそのまま完全二分木として配置
#     self.list = [ダミー, 5, 3, 8, 1, 2]
#
#              5
#            /   \
#           3     8
#          / \
#         1   2
#
#   ステップ1: 最後の親ノード（size//2 = 5//2 = 2）から開始
#     shift_down(2): ノード3 の子は 1 と 2 → 最小は 1 → 3 > 1 → 交換
#              5
#            /   \
#           1     8
#          / \
#         3   2
#
#   ステップ2: shift_down(1): ノード5 の子は 1 と 8 → 最小は 1 → 5 > 1 → 交換
#              1
#            /   \
#           5     8
#          / \
#         3   2
#
#     交換後、shift_down は再帰的に続く:
#     shift_down(2): ノード5 の子は 3 と 2 → 最小は 2 → 5 > 2 → 交換
#              1
#            /   \
#           2     8
#          / \
#         3   5
#
#   → ヒープ完成！
#
# ■ なぜ build_heap は O(n) で済むのか：
#   - 葉ノード（約半分）は shift_down 不要
#   - 深い位置のノードほど shift_down の距離が短い
#   - 浅い位置のノード（根に近い）は数が少ない
#   - これらを合計すると O(n) になる
# ============================================================

# 課題3：ヒープを作る
from def_stop import Stop  # Stopクラスの読み込み（バス停1件分のデータを表すクラス）
import sys  # 再帰呼び出し回数の上限を変更するためのモジュール
sys.setrecursionlimit(10000)  # 再帰呼び出し回数の上限を10,000回に変更


class Heap:  # Heapクラスの定義
    def __init__(self):
        self.list = [0]  # データを格納するリスト。0番目の要素は使わないため0を代入。
        self.size = 0    # 現在ヒープに格納されているデータの件数

    # --- 課題1のメソッド ---

    def insert(self, data):
        # データを1つずつヒープに挿入するメソッド（課題1で使用）
        self.list.append(data)
        self.size += 1
        self.shift_up(self.size)

    def shift_up(self, num):
        # num番目の要素を親方向に押し上げるメソッド（再帰）
        if num > 1 and self.list[num // 2].lng > self.list[num].lng:
            self.list[num], self.list[num // 2] = self.list[num // 2], self.list[num]
            self.shift_up(num // 2)

    # --- 課題2のメソッド ---

    def delete_min(self):
        # ヒープの最小値（根）を取り出して返すメソッド
        min_val = self.list[1]            # 根の値を保存
        self.list[1] = self.list[self.size]  # 最後尾を根に移動
        self.list.pop()                   # 最後尾を削除
        self.size -= 1                    # サイズを減らす
        if self.size > 0:
            self.shift_down(1)            # 根からシフトダウン
        return min_val

    def shift_down(self, num):
        # num番目の要素を子方向に押し下げるメソッド（再帰）
        # 左右の子のうち小さい方と比較し、自分より小さければ交換する

        # 左の子が存在しなければ（葉ノード）終了
        if num * 2 > self.size:
            return

        # 小さい方の子を選ぶ
        if num * 2 + 1 > self.size:  # 右の子が存在しない場合
            min_child = num * 2      # 左の子のみ
        else:                        # 両方の子が存在する場合
            if self.list[num * 2].lng < self.list[num * 2 + 1].lng:
                min_child = num * 2      # 左の子の方が小さい
            else:
                min_child = num * 2 + 1  # 右の子の方が小さい

        # 小さい方の子が自分より小さければ交換し、再帰的に続ける
        if self.list[min_child].lng < self.list[num].lng:
            self.list[num], self.list[min_child] = self.list[min_child], self.list[num]
            self.shift_down(min_child)

    # --- 課題3で追加するメソッド ---

    def build_heap(self, lst):  # 与えられたリストからヒープを構築するメソッド
        # 引数 lst: ヒープに格納するデータのリスト（Stopインスタンスのリスト）
        #
        # insert を繰り返す方法（課題1）とは異なり、
        # リスト全体を一度にセットしてから、ボトムアップに
        # shift_down を適用してヒープ条件を回復する。

        # ステップ1: ダミー(0) + データリストでヒープ用のリストを作成
        # [0] + lst で、インデックス0にダミー、インデックス1以降にデータが入る
        self.list = [0] + lst  # 0番目にダミーを置き、リストをそのまま格納

        # ステップ2: サイズをデータの件数に設定
        self.size = len(lst)

        # ステップ3: 最後の親ノードから根まで、ボトムアップに shift_down を適用
        #
        # なぜ size // 2 から始めるのか：
        #   - size // 2 は「最後尾のノード（size）の親」のインデックス
        #   - size // 2 + 1 以降のノードは全て葉（子を持たない）なので、
        #     shift_down する必要がない
        #   - 例: size=5 の場合、ノード3,4,5 は葉、ノード1,2 は内部ノード
        #         → ノード2 から 1 に向かって shift_down する
        #
        # range(self.size // 2, 0, -1) → size//2, size//2-1, ..., 2, 1
        for i in range(self.size // 2, 0, -1):
            self.shift_down(i)

    # --- 表示・検証メソッド ---

    def show_tree(self, num):
        # ヒープを横向きの木構造として表示する（再帰）
        # 右の子 → 自分 → 左の子 の順で表示
        if num <= self.size:
            self.show_tree(num * 2 + 1)  # 右の子の部分木を表示
            i = num
            space = ''
            while i // 2 > 0:           # 深さ分のインデントを計算
                space += '  '
                i = i // 2
            print('{}{}:{}'.format(space, self.list[num].name, self.list[num].lng))
            self.show_tree(num * 2)      # 左の子の部分木を表示

    def is_heap(self):
        # 全ノードがヒープ条件を満たしているか検証
        for i in range(self.size, 1, -1):
            if self.list[i].lng < self.list[i//2].lng:
                return False
        return True


# ============================================================
# メインの実行部分
# ============================================================
# 課題1との違い：
#   課題1: for文で insert を繰り返す → 1つずつ挿入してヒープを成長させる
#   課題3: まずリストにデータを全て読み込み → build_heap で一括構築
# ============================================================
if __name__ == '__main__':
    # --- データの読み込み ---
    fi = open('allkyotobus_stop.dat', 'r', encoding='utf-8')
    lines = fi.readlines()  # ファイル全体を行ごとのリストとして取得
    fi.close()  # ファイルを先に閉じる（以降は lines リストだけを使う）

    # --- データをリストに格納 ---
    # 課題1では読み込みながら insert していたが、
    # 課題3ではまず全データを Python のリストに格納する
    stop_list = []
    for line in lines:
        line = line.rstrip()  # 行末の改行を除去
        items = line.split(' ')  # スペースで分割
        # Stop インスタンスを生成してリストに追加
        stop_list.append(Stop(items[0], items[1], float(items[2]), float(items[3]), items[4:]))

    # --- build_heap でヒープを構築 ---
    # insert を繰り返す課題1とは異なる方法でヒープを構築する
    # 結果として得られるヒープの形は課題1とは異なるが、
    # ヒープ条件は同様に満たされる
    heap = Heap()
    heap.build_heap(stop_list)

    # --- 結果の表示 ---
    # ヒープ条件を満たしていれば木構造を表示
    # 根（最小値）は課題1と同じ下夜久野駅前だが、
    # 他のノードの配置は課題1と異なる
    if heap.is_heap():
        heap.show_tree(1)  # ヒープ全体を表示
