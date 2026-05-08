from def_node import Node

class Actor:
    def __init__(self, name, movies):
        self.name=name
        self.movies=movies

    def count_movies(self):
        return len(self.movies)
    

movies_a=[]

with open('actor_data.dat', 'r', encoding='utf-8')as fi:
    lines=fi.readlines()
    for line in lines:
        line=line.rstrip()
        items=line.split()

        name=items[0]
        movies=items[1:]

        a=Actor(name, movies)
        movies_a.append(a)

top1=Node('Abbi Jacobson', None)
top1=Node('Abby Tang', top1)
top1=Node('Adrian Dunbar', top1)
top1=Node('Adriana Ugarte', top1)
top1=Node('Aidy Bryant', top1)

p=top1.next.next
top1.next.next=p.next
p.next=None

for actor in movies_a:
    message = '{}さんは{}本の作品に出演しています。'
    print(message.format(actor.name, actor.count_movies()))



#解説
#末尾からコードを書くのがポイント。その次に先頭を繋げる
#最後使わなくなったものにNoneを書く

# [問題文]
# actor_data.dat を読み込み、
# 各俳優の出演作品数を求め、
# 「〇〇さんは△本の作品に出演しています。」と出力せよ。
# # 単方向連結リストを作成し、
# 先頭から3番目のノードを削除せよ。


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# （※Actorクラスの定義と、actor_data.datからの読み込み処理は、
# 　1つ前の過去問と全く同じため割愛します。バッチリ書けています！）
#
# === ここから単方向連結リストの作成 ===
#
# top1=Node('Abbi Jacobson', None)
# top1=Node('Abby Tang', top1)
# top1=Node('Adrian Dunbar', top1)
# top1=Node('Adriana Ugarte', top1)
# top1=Node('Aidy Bryant', top1)
# ［5人分のリストを作成する］
# ご自身の解説コメントにある通り「末尾（一番最後）から作って、その前に繋げる」
# を繰り返すことでリストを作っています。
# 【完成したリストの状態】
# 1番目(先頭): Aidy Bryant (これが今の top1)
# 2番目: Adriana Ugarte (top1.next でアクセスできる)
# 3番目: Adrian Dunbar (top1.next.next でアクセスできる)
# 4番目: Abby Tang
# 5番目: Abbi Jacobson
#
# === ここから「先頭から3番目のノードを削除」する処理 ===
#
# p = top1.next.next
# ［手順1：削除したい「3番目」のノードに名札(p)を付ける］
# top1(1番目) -> next(2番目) -> next(3番目) と辿り、
# 3番目である「Adrian Dunbar」の箱に変数 `p` をセットします。
#
# top1.next.next = p.next
# ［手順2：2番目のノードの矢印を、4番目に繋ぎ変える（3番目を飛ばす）］
# 左辺 `top1.next.next` は、2番目(Adriana Ugarte)から出ている矢印（next）を指します。
# 右辺 `p.next` は、3番目(p)の次、つまり4番目(Abby Tang)を指します。
# これにより、2番目の矢印が、3番目(p)を飛び越えて、4番目に直接繋がります。
# 【この時点の状態】
# 1番目 ➔ 2番目 -----------------➔ 4番目 ➔ 5番目
# 　　　　　　　　　3番目(p) ➔ 4番目
# ※まだ3番目(p)から4番目への矢印が残っています。
#
# p.next = None
# ［手順3：切り離された3番目のノードの矢印を消す］
# ご自身の解説コメント「最後使わなくなったものにNoneを書く」の通りです！
# 3番目(p)から4番目に向かっていた矢印を None（空）にすることで、
# 3番目のノード「Adrian Dunbar」がリストから完全に切り離されます。
#
# === ここから出力処理 ===
#
# for actor in movies_a:
#     message = '{}さんは{}本の作品に出演しています。'
#     print(message.format(actor.name, actor.count_movies()))
# ［ファイルから読み込んだ俳優データの出力］
# 最初に作成した movies_a のリストから1人ずつデータを取り出し、画面に出力します。
# -----------------------------------------------------------------