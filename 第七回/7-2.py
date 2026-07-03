# ============================================================
# 第7回 課題2：最小値を取り出す
# ============================================================
# 課題1で作成した Heap クラスに、最小値を格納した根を削除して
# 取り出す delete_min メソッドと、ヒープ条件を回復するための
# shift_down メソッドを追加する。
#
# ■ delete_min（最小値の取り出し）のアルゴリズム：
#   1. 根（インデックス1）に格納されている最小値を保存する
#   2. ヒープの最後尾の要素を根に移動させる
#   3. 最後尾の要素をリストから削除し、サイズを1減らす
#   4. 根に移動した要素は大きな値の可能性が高いので、
#      shift_down で適切な位置まで押し下げる
#   5. 保存しておいた最小値を返す
#
#   【delete_min の動作イメージ】
#     例: ヒープ [_, 1, 3, 2, 5, 4, 6] から最小値を取り出す
#
#     初期状態:
#              1         ← これを取り出したい
#            /   \
#           3     2
#          / \   /
#         5   4 6
#
#     ステップ1: 根の値 1 を保存
#     ステップ2: 最後尾の 6 を根に移動 → [_, 6, 3, 2, 5, 4]
#              6         ← ヒープ条件を満たしていない！
#            /   \
#           3     2
#          / \
#         5   4
#
#     ステップ3: shift_down(1) で根を押し下げる
#       6 の子は 3 と 2 → 小さい方は 2 → 6 > 2 なので交換
#              2
#            /   \
#           3     6
#          / \
#         5   4
#
#       6 の子は（なし）→ 終了
#              2
#            /   \
#           3     6
#          / \
#         5   4
#
#     ステップ4: 保存した 1 を返す
#
# ■ shift_down のアルゴリズム：
#   1. 左の子が存在しなければ（葉ノード）終了
#   2. 左右の子のうち、小さい方を選ぶ
#   3. 選んだ子が自分より小さければ交換し、再帰的に続ける
#   4. 自分の方が小さければ何もせず終了
#
# ■ shift_up と shift_down の違い：
#   shift_up:   子 → 親の方向に上がる（insert時に使用）
#   shift_down: 親 → 子の方向に下がる（delete_min時に使用）
# ============================================================

# 課題2：最小値を取り出す
from def_stop import Stop  # Stopクラスの読み込み（バス停1件分のデータを表すクラス）
import sys  # 再帰呼び出し回数の上限を変更するためのモジュール
sys.setrecursionlimit(10000)  # 再帰呼び出し回数の上限を10,000回に変更


class Heap:  # Heapクラスの定義
    def __init__(self):
        self.list = [0]  # データを格納するリスト。0番目の要素は使わないため0を代入。
        self.size = 0    # 現在ヒープに格納されているデータの件数

    # --- 課題1から引き継いだメソッド ---

    def insert(self, data):
        # データをヒープに挿入するメソッド
        self.list.append(data)  # データをヒープの最後の要素の次に挿入
        self.size += 1  # ヒープサイズを1増やす
        self.shift_up(self.size)  # 挿入した要素をシフトアップする

    def shift_up(self, num):  # num番目の要素をシフトアップ
        # 親（num // 2）の経度が自分より大きければ交換し、再帰的に上に移動
        if num > 1 and self.list[num // 2].lng > self.list[num].lng:
            self.list[num], self.list[num // 2] = self.list[num // 2], self.list[num]
            self.shift_up(num // 2)

    # --- 課題2で追加するメソッド ---

    def delete_min(self):  # ヒープの最小値である根を削除するメソッド
        # 返り値: ヒープの根に格納されたデータ（Stopインスタンス）

        # ステップ1: 根（インデックス1）の値を保存
        # 最小ヒープなので、根は常に最小値を持つ
        min_val = self.list[1]  # 根（最小値）を取得

        # ステップ2: ヒープの最後尾の要素を根に移動
        # こうすることで、完全二分木の形を保ったままサイズを減らせる
        self.list[1] = self.list[self.size]  # ヒープの最後尾の要素を根に移動

        # ステップ3: 最後尾の要素をリストから削除し、サイズを減らす
        self.list.pop()  # リスト末尾の要素を削除（pop()は末尾を除去するメソッド）
        self.size -= 1  # ヒープサイズを1減らす

        # ステップ4: 根に移動した要素をシフトダウンしてヒープ条件を回復
        # size > 0 のチェックは、最後の1要素を削除した場合に
        # 空のヒープに対してシフトダウンしないようにするため
        if self.size > 0:
            self.shift_down(1)  # 根（インデックス1）からシフトダウン開始

        # ステップ5: 保存しておいた最小値を返す
        return min_val  # 削除した最小値を返す

    def shift_down(self, num):  # num番目のノードをシフトダウンするメソッド
        # num番目の要素を、ヒープ条件を満たす位置まで下に移動させる（再帰）
        # 引数 num: シフトダウンしたい要素のインデックス
        #
        # 処理の流れ：
        #   1. 子が存在しなければ終了（葉ノード）
        #   2. 左右の子のうち小さい方を見つける
        #   3. 小さい子が自分より小さければ交換して再帰

        # --- 子の存在チェック ---
        # 左の子のインデックスは num * 2
        # 左の子が存在しない（num * 2 > self.size）なら、このノードは葉なので終了
        if num * 2 > self.size:
            return

        # --- 小さい方の子を選ぶ ---
        if num * 2 + 1 > self.size:  # 右の子が存在しない場合
            # 左の子しかないので、左の子が比較対象
            min_child = num * 2  # 左の子のみ
        else:  # 両方の子が存在する場合
            # 左右の子の経度を比較し、小さい方のインデックスを min_child に格納
            if self.list[num * 2].lng < self.list[num * 2 + 1].lng:
                min_child = num * 2  # 左の子の方が小さい
            else:
                min_child = num * 2 + 1  # 右の子の方が小さい

        # --- 交換の判定と実行 ---
        # 小さい方の子が自分より小さければ、ヒープ条件に違反しているので交換
        if self.list[min_child].lng < self.list[num].lng:
            # 自分と小さい方の子を交換
            self.list[num], self.list[min_child] = self.list[min_child], self.list[num]
            # 交換先の位置（min_child）から再帰的にシフトダウンを続ける
            self.shift_down(min_child)
        # 自分の方が小さければ何もせずに終了（ヒープ条件を満たしている）

    def show_tree(self, num):
        # ヒープを横向きの木構造として表示する（再帰）
        if num <= self.size:
            self.show_tree(num * 2 + 1)  # 右の子を先に表示（画面上部に来る）
            i = num
            space = ''
            while i // 2 > 0:
                space += '  '
                i = i // 2
            print('{}{}:{}'.format(space, self.list[num].name, self.list[num].lng))
            self.show_tree(num * 2)  # 左の子を後に表示（画面下部に来る）

    def is_heap(self):
        # 全ノードがヒープ条件を満たしているか検証
        for i in range(self.size, 1, -1):
            if self.list[i].lng < self.list[i//2].lng:
                return False
        return True


# ============================================================
# メインの実行部分
# ============================================================
if __name__ == '__main__':
    # --- データの読み込みとヒープの構築 ---
    fi = open('allkyotobus_stop.dat', 'r', encoding='utf-8')
    lines = fi.readlines()
    heap = Heap()
    for line in lines:
        line = line.rstrip()
        items = line.split(' ')
        # insert でデータを1件ずつヒープに追加（課題1と同じ方法で構築）
        heap.insert(Stop(items[0], items[1], float(items[2]), float(items[3]), items[4:]))
    fi.close()

    # --- delete_min を3回実行 ---
    # 最小ヒープなので、delete_min は経度が最も小さい（=最も西にある）
    # バス停を順番に取り出す。
    # 1回目: 最西のバス停
    # 2回目: 2番目に西のバス停
    # 3回目: 3番目に西のバス停
    for i in range(3):
        stop = heap.delete_min()  # 最小値（最西のバス停）を取り出す
        # 取り出したバス停の名前・ID・緯度・経度を表示
        print('最西のバス停の{}(ID:{})の緯度経度は({}, {})です。'.format(stop.name, stop.id, stop.lat, stop.lng))
