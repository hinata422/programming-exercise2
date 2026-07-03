from 第六回.def_stop import Stop

# Nodeクラス
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

top = None

with open("kyotocitybus_stop.dat", encoding='utf-8') as f:
    for line in f:
        tokens = line.strip().split()
        if len(tokens) < 4:
            continue
        s = Stop(tokens[0], tokens[1], float(tokens[2]), float(tokens[3]), tokens[4:])
        top = Node(s, top)
        
message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
if top is not None:
    print(message.format(top.data.name, top.data.id, top.data.lat, top.data.lng))
else:
    print("topがNoneです！")


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# from def_stop import Stop
# class Node: ... (中略)
# ［クラスの準備］
# Stopクラス（バス停の設計図）と、Nodeクラス（連結リストの箱の設計図）を準備します。
#
# top = None
# ［★超重要：最初は「空っぽ」の先頭を用意する］
# まだデータを1つも読み込んでいないので、先頭の目印(top)は「何もない(None)」状態にしておきます。
#
# with open("kyotocitybus_stop.dat", encoding='utf-8') as f:
#     for line in f:
# ［ファイルを開いて1行ずつ取り出す］
#
#         tokens = line.strip().split()
#         if len(tokens) < 4:
#             continue
#         ［ゴミ取りと切り分け、エラー回避］
#         （前回まで items と呼んでいた変数を今回は tokens としていますね。同じ働きです）
#
#         s = Stop(tokens[0], tokens[1], float(tokens[2]), float(tokens[3]), tokens[4:])
#         ［Stopインスタンス（バス停データ）の作成］
#         切り分けたデータを使って、Stopクラスから1つのバス停データ(s)を作ります。
#
#         top = Node(s, top)
#         ［★最大のポイント：新しいデータを「先頭」に割り込ませる］
#         前回の課題であった「便利な1行書き」がここで大活躍しています！
#         Node(s, top) で「データは s(いま読み込んだバス停)、次は今の top」という箱を作ります。
#         そして、その新しく作った箱に top の名札を付け替えます。
#
#         【ループの中での動きのイメージ】
#         1行目(101 京都駅前)を読む：
#         　top ➔ [京都駅前 | next:None(最初のtop)]
#         2行目(102 烏丸七条)を読む：
#         　top ➔ [烏丸七条 | next] ➔ [京都駅前]
#         3行目(103 烏丸六条)を読む：
#         　top ➔ [烏丸六条 | next] ➔ [烏丸七条] ➔ [京都駅前]
#
#         このように「常に新しいデータを一番前に持ってくる（後入れ先出し）」という追加の仕方をしています。
#         そのため、ファイルの「最後の行」を読み込み終わったとき、そのデータが連結リストの「一番先頭(top)」になります。
#
# message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
# if top is not None:
# ［出力前のチェック］
# ファイルが空っぽでデータが1つも作られなかった場合（topがNoneのまま）のエラーを防ぎます。
#
#     print(message.format(top.data.name, top.data.id, top.data.lat, top.data.lng))
# ［先頭のデータを出力する］
# 課題の指示通り、「連結リストの先頭(top)」のデータを出力します。
# 先ほど説明した通り、常に先頭に追加し続けたため、ここには「ファイルの最後尾にあったバス停（京都駅八条口）」が入っています。
# -----------------------------------------------------------------