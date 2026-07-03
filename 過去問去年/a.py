class Actor:
    def __init__(self, name, movies):
        self.name = name
        self.movies = movies

    def count_movies(self):
        return len(self.movies)


movies_a = []

with open('actor_data.dat', 'r', encoding='utf-8') as fi:
    for line in fi:
        line = line.rstrip()
        items = line.split()


        name = items[0]
        movies = items[1:]

        movies_a.append(Actor(name, movies))


for actor in movies_a:
    message = '{}さんは{}本の作品に出演しています。'
    print(message.format(actor.name, actor.count_movies()))

# [問題文]
#  actor_data.dat というファイルを読み込み、
# 各行に書かれている俳優名と出演作品から、
# 「〇〇さんは△本の作品に出演しています。」
# と出力するプログラムを作成せよ。


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# class Actor:
# ［俳優（Actor）のデータをまとめるクラス（設計図）］
# これまでの課題の「Stop（バス停）」が「Actor（俳優）」に変わっただけです。
#
#     def __init__(self, name, movies):
#         self.name = name
#         self.movies = movies
#     ［初期化］
#     俳優の名前(name)と、出演作品のリスト(movies)をデータとして持たせます。
#
#     def count_movies(self):
#         return len(self.movies)
#     ［作品数を数えるメソッド（機能）］
#     len() を使って、リスト(movies)の中に入っている作品の個数を数えて返します。
#     以前の課題であった count_routes（路線の数を数える）と全く同じ仕組みです。
#
# movies_a = []
# ［俳優データを保存する空のリストを作る］
# クラスから作った俳優データを全てまとめるための空箱を用意します。
#
# with open('actor_data.dat', 'r', encoding='utf-8') as fi:
#     for line in fi:
# ［ファイルを開いて1行ずつ取り出す］
#
#         line = line.rstrip()
#         items = line.split()
#         ［見えないゴミを消して、空白で切り分ける］
#         例えば "渡辺謙 インセプション ラストサムライ" という行なら、
#         ['渡辺謙', 'インセプション', 'ラストサムライ'] というリスト(items)になります。
#
#         name = items[0]
#         movies = items[1:]
#         ［分かりやすいように変数に代入］
#         1番目のデータ（インデックス0）を名前(name)に、
#         2番目以降のすべてのデータ（インデックス1から最後まで）を作品リスト(movies)に分けます。
#
#         movies_a.append(Actor(name, movies))
#         ［クラスからインスタンスを生成し、リストに追加する］
#         Actor クラスの設計図を使って1人分の俳優データを作り、
#         それを最初に用意した空箱(movies_a)に追加します。
#
# === ここから出力処理 ===
#
# for actor in movies_a:
# ［リストから俳優データを1人ずつ取り出して繰り返す］
#
#     message = '{}さんは{}本の作品に出演しています。'
#     ［ひな形となる文字列］
#
#     print(message.format(actor.name, actor.count_movies()))
#     ［データを入れて画面に出力］
#     .format() を使って、左から順番に {} にデータを当てはめます。
#     1つ目：actor.name （俳優の名前）
#     2つ目：actor.count_movies() （先ほどクラスに定義した、作品数を数えるメソッドの実行結果）
# -----------------------------------------------------------------