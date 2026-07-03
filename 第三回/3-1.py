from 第六回.def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

top = Node(ryukoku)
p = Node(kyosan)
p.next= top
top = p
p = None
top = Node(kyodai, top)
top = Node(doshisha, top)
top = Node(ritsumeikan, top)

message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
p = top
print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
p = p.next
print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
p = p.next
print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
p = p.next
print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
p = p.next
print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# from def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku
# ［他のファイルからデータを読み込む］
# 事前に用意されたバス停のデータ（インスタンス）を使えるように読み込んでいます。
#
# class Node:
#     def __init__(self, data, next=None):
#         self.data = data
#         self.next = next
# ［連結リストの「箱（ノード）」の設計図］
# この箱には2つのスペースがあります。
# 1つは自分自身のデータ（data）を入れるスペース。
# もう1つは「次の箱はどれか」を指し示す矢印（next）を入れるスペースです。
# next=None は、「もし次が指定されなかったら、矢印は空っぽ（None）にする」という設定です。
#
# === ここから連結リストを作っていく作業（後ろから前へ繋ぎます） ===
#
# top = Node(ryukoku)
# ［①一番後ろの箱（龍谷）を作る］
# 「龍谷」のデータが入った箱を作ります。次（next）の指定はないので、矢印はNoneです。
# この箱に「top（先頭）」という名札を付けます。
# 【今の状態】top ➔ [龍谷 | next:None]
#
# p = Node(kyosan)
# p.next= top
# top = p
# p = None
# ［②1つ前の箱（京産）を作り、先頭に割り込ませる（丁寧な4ステップ）］
# 1. p = Node(kyosan) : 「京産」の箱を作り、仮の名札「p」を付けます。
# 2. p.next = top     : 京産の次の矢印を、今のtop（龍谷）に向けます。これで2つが繋がりました。
# 3. top = p          : 先頭の目印「top」を、新しく先頭になった京産に付け替えます。
# 4. p = None         : 仮の名札「p」はもう使わないので剥がします。
# 【今の状態】top ➔ [京産 | next] ➔ [龍谷 | next:None]
#
# top = Node(kyodai, top)
# ［③さらに前の箱（京大）を作る（★便利な1行書き！）］
# 実はこの1行で、上の②の4行と全く同じこと（先頭への割り込み）をしています。
# Node()の2つ目のカッコ内に「いまのtop（＝京産）」を入れることで、
# 「データは京大で、次は『京産』を指している箱」を作り、同時にtop名札も付け替えています。
# 【今の状態】top ➔ [京大 | next] ➔ [京産 | next] ➔ [龍谷 | next:None]
#
# top = Node(doshisha, top)
# top = Node(ritsumeikan, top)
# ［④残りも同じように先頭に割り込ませる］
# ③の便利な書き方を使って、同志社、立命館もどんどん先頭に繋いでいきます。
# 【最終的な状態】
# top ➔ [立命館] ➔ [同志社] ➔ [京大] ➔ [京産] ➔ [龍谷]
#
# === ここから作ったリストを出力していく作業 ===
#
# message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
#
# p = top
# ［スタート地点を決める］
# 変数pに、一番先頭の箱（top ＝ 立命館）をセットします。
#
# print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
# ［現在の箱のデータを出力する］
# p（今は立命館）のデータを取り出して画面に表示します。
#
# p = p.next
# ［次の箱へ進む］
# p の場所を、現在の箱が指し示している「次の箱（＝同志社）」へ移動させます。
#
# print(...)
# p = p.next
# ［これを繰り返す］
# 表示する ➔ 次の箱へ進む ➔ 表示する ➔ 次の箱へ進む... と繰り返すことで、
# 繋がっているバス停のデータを順番に出力することができます。
# -----------------------------------------------------------------