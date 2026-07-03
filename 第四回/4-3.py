# StopクラスおよびStopインスタンスのimport
from 第六回.def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku
# Nodeクラスの定義をdef_node.pyからインポート
from def_node import Node

class Queue:
    def __init__(self):
        self.top = None  # キューの先頭（出口）
        self.rear = None # キューの末尾（入口）

    def display(self):
        print('======キューの先頭======')
        message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
        p = self.top
        while p is not None:
            print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
            p = p.next
        print('======キューの末尾======')

    def enqueue(self, data):
        if isinstance(data, Stop):
            new_node = Node(data, None)
            
            if self.top is None:
                self.top = new_node
                self.rear = new_node
            else:
                self.rear.next = new_node
                self.rear = new_node
        else:
            print('Stopインスタンス以外はENQUEUEできません。')

    def dequeue(self):
        if self.top is None:
            print('キューが空でDEQUEUEできません。')
            return None
        else:
            dequeued_data = self.top.data
            self.top = self.top.next
            
            if self.top is None:
                self.rear = None
                
            return dequeued_data

# --- 実行用コード ---
q = Queue()

q.enqueue(1)
q.enqueue(ritsumeikan)
q.enqueue(doshisha)
q.enqueue(kyodai)
q.enqueue(kyosan)
q.enqueue(ryukoku)

q.display()

message = '{}(ID:{})のバス停の緯度経度は({},{})です。'

while True:
    dequeued_stop = q.dequeue()
    
    if dequeued_stop is None:
        break
        
    print(message.format(dequeued_stop.name, dequeued_stop.id, dequeued_stop.lat, dequeued_stop.lng))


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# class Queue:
#     def __init__(self):
#         self.top = None  # 先頭（出口：ここからデータが出ていく）
#         self.rear = None # 末尾（入口：ここからデータが入ってくる）
#     ［キューの初期化］
#     スタックと違い、行列には「先頭」と「最後尾」があるので、2つの目印を用意します。
#
#     def enqueue(self, data):
#     ［キューにデータを「並ばせる」機能（ENQUEUE）］
#
#         new_node = Node(data, None)
#         ［★手順1：新しいお客さん（箱）を作る］
#         後ろに並ぶので、この箱の次(next)は必ず None になります。
#
#         if self.top is None:
#             self.top = new_node
#             self.rear = new_node
#         ［★手順2-A：もし誰も並んでいなかった場合］
#         行列の「最初のお客さん」です。この人が「先頭(top)」であり、
#         同時に「最後尾(rear)」にもなるので、両方の目印をこの人に付けます。
#
#         else:
#             self.rear.next = new_node
#             self.rear = new_node
#         ［★手順2-B：すでに人が並んでいた場合］
#         【変更前】 [先頭] ➔ ... ➔ [いまの最後尾(rear) | next:None]
#         まず、今の最後尾の次(rear.next)を、新しい人に繋ぎます。
#         そして、最後尾の目印(rear)を、新しく繋いだ人に付け替えます。
#         【変更後】 [先頭] ➔ ... ➔ [元最後尾] ➔ [新しい最後尾(rear) | next:None]
#
#     def dequeue(self):
#     ［キューからデータを「呼び出す」機能（DEQUEUE）］
#
#         if self.top is None: ... (中略)
#         ［空っぽの時はエラー回避］
#
#         else:
#             dequeued_data = self.top.data
#             self.top = self.top.next
#             ［★手順1：先頭から順番に呼び出す］
#             ここはスタックの pop メソッドと全く同じです！
#             列の先頭からデータを確保し、先頭の目印(top)を「次の人」に付け替えます。
#
#             if self.top is None:
#                 self.rear = None
#             ［★手順2：行列が全員いなくなった時のケア］
#             最後の1人を呼び出して top が None になった場合、
#             rear（最後尾の目印）だけが虚空を指したまま残ってしまいます。
#             それを防ぐため、top が空になったら rear もリセットしてあげます。（素晴らしい気配りです！）
#
# # --- 実行用コード ---
# q.enqueue(ritsumeikan)
# q.enqueue(doshisha) ...
# ［データを順番に並ばせる］
# 先に ENQUEUE された立命館が「先頭」、後から来た同志社、京大…が「後ろ」に並びます。
# 最後に龍谷が来るので、龍谷が「最後尾」になります。
# 【キューの状態】 [出口] 立命館 ➔ 同志社 ➔ 京大 ➔ 京産 ➔ 龍谷 [入口]
#
# while True:
#     dequeued_stop = q.dequeue()
# ［順番に呼び出す］
# スタック（後入れ先出し）の時とは違い、先頭の立命館から順番に呼び出されます。
# 「入れた順番通りに出てくる」のがキューの最大の特徴です。
# -----------------------------------------------------------------