class Stop:
    # （画像で見切れている、初期化の設定部分です）
    def __init__(self, id, name, lat, lng, routes):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.routes = routes

    def count_routes(self):  # count_routesメソッドを定義
        return len(self.routes)

# ここからメインの処理
fi = open('kyotocitybus_stop.dat', 'r', encoding='utf-8')
lines = fi.readlines()
stops = []
for line in lines:
    line = line.rstrip()
    items = line.split(' ')  # 1行を半角スペースで区切ってitemsリストに代入
    stops.append(Stop(items[0], items[1], float(items[2]), float(items[3]), items[4:]))
    # Stopオブジェクトをstopsリストに追加
fi.close()

stop = stops[-500]  # リストの最後から500番目のバス停データを取得
message = '{}(ID:{})のバス停には{}本の路線が通っています。'
print(message.format(stop.name, stop.id, stop.count_routes()))


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# class Stop:
#     # (中略) __init__ メソッドでバス停の基本データを受け取る設定をしています。
#
#     def count_routes(self):
#     ［路線の数を数えるメソッド（関数）の追加］
#     Stopクラスの中に、独自の機能（メソッド）を追加しました。
#     self.routes には ['12号系統', '15号系統'...] のように路線のリストが入っています。
#
#         return len(self.routes)
#         ［要素の数を返す］
#         len() はリストの中身の個数を数える命令です。
#         数えた結果を return（戻り値）として、このメソッドを呼び出した場所に返します。
#
# # ここからメインの処理
# fi = open('kyotocitybus_stop.dat', 'r', encoding='utf-8')
# lines = fi.readlines()
# stops = []
# ［ファイルを開き、中身を読み込み、空のリスト(stops)を用意する］
# （この部分はこれまでの課題と同じ流れです）
#
# for line in lines:
#     line = line.rstrip()
#     items = line.split(' ')
#     ［1行ずつ取り出して、改行を消し、半角スペースで切り分ける］
#
#     stops.append(Stop(items[0], items[1], float(items[2]), float(items[3]), items[4:]))
#     ［インスタンスの作成とリスト追加を1行で行う］
#     前回の課題では stop_id = items[0] のように一度変数に入れていましたが、
#     今回は直接 items[番号] を指定して Stop クラスのインスタンスを作っています。
#     そして、作ったインスタンスをそのまま stops.append() でリストに放り込んでいます。
#     少しコードが長く見えますが、慣れると変数を減らせてスッキリ書けるテクニックです。
#
# fi.close()
# ［ファイルを閉じる］
#
# stop = stops[-500]
# ［後ろから500番目のデータを取得］
# リスト(stops)のインデックスに -500 を指定し、後ろから500番目のバス停データを取り出します。
#
# message = '{}(ID:{})のバス停には{}本の路線が通っています。'
# ［ひな形となる文字列］
# 今回は3つの {} （穴）が用意されています。
#
# print(message.format(stop.name, stop.id, stop.count_routes()))
# ［データを入れて画面に出力］
# .format() を使って、左から順番に {} にデータを当てはめます。
# 1つ目：stop.name （バス停の名前）
# 2つ目：stop.id （バス停のID）
# 3つ目：stop.count_routes() ★ここがポイント！
# 　　　 単なる変数ではなく、先ほどクラスに自分で追加したメソッド（機能）を呼び出しています。
# 　　　 これにより、「路線のリスト」ではなく「路線の数」が計算されて文字として埋め込まれます。
# -----------------------------------------------------------------