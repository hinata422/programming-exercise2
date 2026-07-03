# 穴埋め問題用のプログラム
# StopクラスおよびStopインスタンスのimport
from def_stop import Stop, ritsumeikan, doshisha, kyodai, kyosan, ryukoku
# Nodeクラスの定義をdef_node.pyからインポート
from def_node import Node

# Stackクラスの定義
class Stack:
    def __init__(self):
        self.top = None  # 連結リストの先頭を指すリストヘッドのインスタンス変数

    def display(self):  # スタック内の連結リストを表示するメソッド
        print('======スタックの先頭======')
        message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
        p = self.top  # 走査用変数pを連結リストの先頭に設定する
        while p is not None:  # 走査用変数pが連結リストの終端でない限り、以下の処理を繰り返す
            print(message.format(p.data.name, p.data.id, p.data.lat, p.data.lng))
            p = p.next  # 走査用変数pを次の節に一つ進める
        print('======スタックの底======')

    def push(self, data):  # PUSHメソッド
        if(isinstance(data, Stop)):  # PUSHするデータがStopインスタンスかどうか確認
            self.top = Node(data, self.top)  # 連結リストの先頭に節を挿入
        else:
            print('Stopインスタンス以外はPUSHできません。')

s = Stack()  # スタック(Stackインスタンス)を生成
s.display()  # 空のスタックを表示する
s.push(1)  # Stopインスタンス以外をpush
s.push(ritsumeikan)  # スタックにStopインスタンスをPUSHする
s.push(doshisha)
s.push(kyodai)
s.push(kyosan)
s.push(ryukoku)
s.display()  # スタックを表示する