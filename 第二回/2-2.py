class Stop:
    def __init__(self, id, name, lat, lng, routes):
        self.id = id
        self.name = name
        self.lat = float(lat)
        self.lng = float(lng)
        self.routes = routes

with open("kyotocitybus_stop.dat", "r", encoding="utf-8") as fi:
    lines = fi.readlines()

stop_list = []

for line in lines:
    line = line.strip()
    items = line.split()

    if len(items) < 5:
        continue

    stop_id = items[0]
    stop_name = items[1]
    lat = items[2]
    lng = items[3]
    routes = items[4:]

    stop = Stop(stop_id, stop_name, lat, lng, routes)
    stop_list.append(stop)

if len(stop_list) < 100:
    print("バス停の数が100個未満です。")
    a = stop_list[-1]
else:
    a = stop_list[-100]

message = '{}(ID:{})のバス停の緯度経度は({},{})です。{}のバスが停まります。'
print(message.format(a.name, a.id, a.lat, a.lng, ",".join(a.routes)))


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# class Stop:
# ［クラス（設計図）の定義］
# 「バス停（Stop）」という新しいデータの型（設計図）を作ります。
#
#     def __init__(self, id, name, lat, lng, routes):
#     ［初期化メソッド（コンストラクタ）］
#     このクラスから新しいバス停のデータ（インスタンス）を作るときに、
#     最初に必ず実行される設定用の関数です。self は「作られたデータ自身」を指します。
#
#         self.id = id
#         self.name = name
#         self.lat = float(lat)  # ← 課題のヒントの通り、文字から小数(float)に変換！
#         self.lng = float(lng)  # ← 同じく小数に変換！
#         self.routes = routes   # ← 今回新しく追加した、路線リスト(routes)の変数
#
# with open("kyotocitybus_stop.dat", "r", encoding="utf-8") as fi:
# ［ファイルを安全に開く（with文）］
# 以前の fi = open(...) と同じですが、with を使うと、
# このブロック（字下げされた部分）が終わった時に「自動でファイルを閉じて」くれます。
# 閉じ忘れを防げるので、Pythonではこの書き方が推奨されています。
#
#     lines = fi.readlines()
#     ［中身をすべて読み込む］
#
# stop_list = []
# ［バス停データを保存する空のリストを作る］
# クラスから作ったバス停データ（インスタンス）を全てまとめるための空箱を用意します。
#
# for line in lines:
# ［1行ずつ取り出して繰り返す］
#
#     line = line.strip()
#     ［見えないゴミを消す］（rstrip とほぼ同じで、両端の空白などを消します）
#
#     items = line.split()
#     ［空白で切り分ける］（split(' ') と同じ働きをします）
#
#     if len(items) < 5:
#         continue
#     ［エラー回避の処理］
#     もし切り分けたデータの数が5個未満（路線データ等がない行）だった場合、
#     continue で以下の処理をスキップし、次の行へ進みます。
#
#     stop_id = items[0]
#     stop_name = items[1]
#     lat = items[2]
#     lng = items[3]
#     routes = items[4:]
#     ［分かりやすいように変数に代入、路線は[4:]で切り出し］
#
#     stop = Stop(stop_id, stop_name, lat, lng, routes)
#     ［クラスからインスタンスを生成（実体化）］
#     先ほど定義した Stop クラスの設計図を使って、1つのバス停データ(stop)を作ります。
#
#     stop_list.append(stop)
#     ［リストに追加］
#     作ったバス停データを、最初に用意した空箱(stop_list)に追加していきます。
#
# if len(stop_list) < 100:
#     print("バス停の数が100個未満です。")
#     a = stop_list[-1]
# else:
#     a = stop_list[-100]
# ［後ろから100番目のデータを取得］
# リストの最後にアクセスするにはインデックスに -1 を指定しますが、
# -100 と書くことで「後ろから100番目」のデータを直接取り出せます。
# ここではデータ数が足りない場合のエラー回避も書いてあります。取り出したデータは変数 a に代入します。
#
# message = '{}(ID:{})のバス停の緯度経度は({},{})です。{}のバスが停まります。'
# ［ひな形となる文字列の作成］
# {} は後から文字を埋め込むための穴です。
#
# print(message.format(a.name, a.id, a.lat, a.lng, ",".join(a.routes)))
# ［データを入れて画面に出力］
# .format(...) を使うと、message の {} の部分に順番にデータがはめ込まれます。
# a.name のように書くことで、クラスの中の変数（インスタンス変数）にアクセスできます。
# 最後の路線のリスト(a.routes)は、",".join() を使ってカンマ区切りの文字列に直してはめ込んでいます。
# -----------------------------------------------------------------