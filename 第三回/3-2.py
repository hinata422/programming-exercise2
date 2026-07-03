# StopクラスおよびStopインスタンスの定義をdef_stop.pyからインポート
from 第六回.def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku

# Nodeクラスの定義
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

# 連結リストの作成（末尾から順に作る）
top = Node(ryukoku)
top = Node(kyosan, top)
top = Node(kyodai, top)
top = Node(doshisha, top)
top = Node(ritsumeikan, top)

# 「京大正門前」を削除（先頭 or 中間どっちでも対応できるように）
if top.data.name == "京大正門前":
    top = top.next
else:
    p = top
    while p and p.next:
        if p.next.data.name == "京大正門前":
            p.next = p.next.next
            break
        p = p.next

# 出力
message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
p = top
while p is not None:
    print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
    p = p.next


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# （※インポート、Nodeクラスの定義、リストの作成までは前回と同じため割愛します。
# 　現在のリストは top ➔ [立命館] ➔ [同志社] ➔ [京大] ➔ [京産] ➔ [龍谷] です）
#
# === ここから「京大」を切り取る処理 ===
#
# if top.data.name == "京大正門前":
#     top = top.next
# ［パターンA：もし消したいデータが「一番先頭」だった場合］
# もし先頭が京大だった場合は、先頭の目印（top）を「次の車両」に付け替えるだけで、
# 先頭車両を切り離すことができます。今回は先頭は立命館なので、ここはスルーされます。
#
# else:
#     p = top
# ［パターンB：消したいデータが「2番目以降」にある場合］
# 探すための目印「p」を、まずは先頭（top＝立命館）にセットします。
#
#     while p is not None and p.next is not None:
#     ［リストの端っこに到達するまで順番に探す］
#
#         if p.next.data.name == "京大正門前":
#         ［★超重要：消したいデータの「1つ手前」で気づく］
#         p.data ではなく、p.next.data（次の箱の名前）を確認しています。
#         なぜなら、連結を切り離すには「1つ手前の箱から出ている矢印」を
#         繋ぎ変えないといけないからです。
#         （いま p が同志社だとすると、p.next は京大なので、ここで条件に一致します！）
#
#             p.next = p.next.next
#             ［★切り取りの真髄：矢印を「1つ飛ばし」で繋ぐ］
#             いま、p(同志社) の次は p.next(京大) に繋がっています。
#             そして、京大の次は p.next.next(京産) に繋がっています。
#             【変更前】 [同志社(p)] ➔ [京大(p.next)] ➔ [京産(p.next.next)]
#
#             この同志社の次(p.next)の矢印を、京大を飛び越えて、京産(p.next.next)に直接向けます。
#             【変更後】 [同志社(p)] -------------------➔ [京産(p.next.next)]
#                                  （孤立した京大）
#             これで京大はリストから外れました！誰も矢印を向けてくれないデータは、
#             Pythonが後で自動的にお掃除して消してくれます。
#
#             break
#             ［切り取ったら終了］
#             無事に切り取れたので、breakでこの探すループ（while文）から抜け出します。
#
#         p = p.next
#         ［まだ見つからなければ、次の箱へ進む］
#
# === ここから出力処理 ===
#
# message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
# p = top
# ［先頭（立命館）からスタート］
#
# while p is not None:
# ［箱がなくなるまで繰り返す］
# 前回のように print と p = p.next を何度も書かなくても、
# while文を使えば「p が None（空っぽ）になるまで」自動で繰り返してくれます。
#
#     print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
#     p = p.next
#     ［現在の箱を出力し、次の箱へ進む］
#     京大はすでに切り離されているので、立命館 ➔ 同志社 ➔ 京産 ➔ 龍谷 の順で表示されます。
# -----------------------------------------------------------------