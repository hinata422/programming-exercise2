# 穴埋め問題用のプログラム（課題1の続き）
from def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku
from def_node import Node

class Stack:
    def __init__(self):
        self.top = None

    def display(self):
        print('======スタックの先頭======')
        message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
        p = self.top
        while p is not None:
            print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
            p = p.next
        print('======スタックの底======')

    def push(self, data):
        if(isinstance(data, Stop)):
            self.top = Node(data, self.top)
        else:
            print('Stopインスタンス以外はPUSHできません。')

    # --- 課題2で追加するpopメソッド ---
    def pop(self):
        if self.top is None:
            print('スタックが空でPOPできません。')
            return None
        else:
            popped_data = self.top.data
            self.top = self.top.next
            return popped_data

# --- 実行用コード ---
s = Stack()

s.push(ritsumeikan)
s.push(doshisha)
s.push(kyodai)
s.push(kyosan)
s.push(ryukoku)

message = '{}(ID:{})のバス停の緯度経度は({},{})です。'

while True:
    popped_stop = s.pop()
    
    if popped_stop is None:
        break
        
    print(message.format(popped_stop.name, popped_stop.id, popped_stop.lat, popped_stop.lng))


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# （※初期化、display、pushまでは前回と同じため割愛します）
#
#     def pop(self):
#     ［スタックからデータを「取り出す」機能（POP）］
#     スタックは「後入れ先出し」なので、取り出すときは常に「一番上（先頭 = top）」からです。
#
#         if self.top is None:
#             print('スタックが空でPOPできません。')
#             return None
#         ［スタックが空っぽの場合のエラー回避］
#         もし空っぽ（取り出すものがない）の時は、メッセージを出して None(空) を返します。
#
#         else:
#             popped_data = self.top.data
#             ［★手順1：取り出すデータを一時的に避難させる］
#             いきなり top を次に進めてしまうと、今の先頭データが迷子になってしまいます。
#             そのため、まずは一番上の箱のデータ(self.top.data)を popped_data という変数にコピーして保存しておきます。
#
#             self.top = self.top.next
#             ［★手順2：先頭の目印を「次」に付け替えて切り離す］
#             【変更前】 [龍谷(top)] ➔ [京産] ➔ [京大] ...
#             先頭の目印(top)を、龍谷の次(top.next = 京産)に移動させます。
#             【変更後】 [龍谷(切り離された)]     [京産(新top)] ➔ [京大] ...
#             これで一番上の箱（龍谷）がスタックから外れました！
#
#             return popped_data
#             ［手順3：避難させておいたデータを返す］
#             手順1で確保しておいた「龍谷」のデータを return で呼び出し元に渡します。
#
# # --- 実行用コード ---
# s = Stack()
# s.push(ritsumeikan) ... (中略) ... s.push(ryukoku)
# ［データの積み上げ］
# 立命館、同志社…と積み上げ、一番最後に「龍谷」をPUSHしました。
# つまり、現在のスタックは一番上が「龍谷」、一番下（底）が「立命館」になっています。
#
# while True:
# ［全部取り出すための無限ループ］
#
#     popped_stop = s.pop()
#     ［スタックの先頭から1つデータを取り出す］
#     先ほど作った pop メソッドを呼び出します。
#     1回目は一番上にある「龍谷」が取り出され、popped_stop に代入されます。
#     （同時に、スタック内の先頭は1つ下の「京産」に切り替わります）
#
#     if popped_stop is None:
#         break
#     ［終了条件］
#     すべてのデータを取り出し終えてスタックが空になると、popメソッドは None を返してきます。
#     その None を受け取ったら、break でこのループを終了します。
#
#     print(message.format(popped_stop.name, ...))
#     ［取り出したデータを出力］
#     一番最後にPUSHした「龍谷」から順に出力され、最初にPUSHした「立命館」が最後に出力されます。
#     （実行例の画像と同じ順番になりますね！）
# -----------------------------------------------------------------