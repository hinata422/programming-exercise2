from def_liststack import ListStack

s=ListStack()

s.push('Yeon-Seo Oh')
s.push('Yosuke Eguchi')
s.push('Zach Aguilar')
s.push('Zach Gilford')
s.push('Zachary Levi')
s.display()


message = '{}さん は {} 作品に出演しています。'
stop=s.pop()
while stop is not None:
    print(message.format(stop.name, stop.movies))
    stop=s.pop()

# [問題文]
# ListStack クラスを用いてスタックを作成し、
# 俳優データを PUSH してから、
# POP を使って全て取り出し、
# 取り出した順に表示せよ。


# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# from def_liststack import ListStack
# ［スタックの設計図を読み込む］
# 以前作成した「スタック」の機能を持つ ListStack クラスを読み込みます。
#
# s = ListStack()
# ［スタックの作成］
# 俳優データを積み上げるための空のスタック（s）を1つ用意します。
#
# s.push('Yeon-Seo Oh')
# ...
# s.push('Zachary Levi')
# ［データを順番に積み上げる（PUSH）］
# 5人分のデータを順番にスタックへ積んでいきます。
# スタックは「机に本を積む」ような構造なので、一番最後に PUSH した
# 'Zachary Levi' さんが、スタックの「一番上（先頭）」になります。
#
# s.display()
# ［スタックの状態を表示］
# 現在積まれているデータを、一番上のものから順番に確認のために表示します。
#
# === ここから「全て取り出して表示する」処理 ===
#
# message = '{}さん は {} 作品に出演しています。'
# ［ひな形］
#
# stop = s.pop()
# ［★最初に取り出す］
# まず、スタックの一番上にあるデータを 1 つ取り出し、変数 stop に入れます。
# （ここでは一番最後に積んだ 'Zachary Levi' さんが最初に出てきます）
#
# while stop is not None:
# ［スタックが空になるまで繰り返す］
# pop() をした結果、中身がなくなって None（空）が返ってくるまで処理を繰り返します。
#
#     print(message.format(stop.name, stop.movies))
#     ［取り出したデータの表示］
#     いま取り出した俳優さんの情報を画面に出力します。
#
#     stop = s.pop()
#     ［★次を取り出す］
#     ここがループを回すための重要なポイントです。
#     いま表示した人の「下」に積まれていた、次の人をスタックから取り出します。
#     これを繰り返すことで、上から下へと順番に全てのデータを取り出せます。
#
# 【スタックの動きのイメージ】
# 1. PUSH順: Yeon-Seo -> Yosuke -> Zach A. -> Zach G. -> Zachary
# 2. スタックの中身: [一番上: Zachary, Zach G., Zach A., Yosuke, 一番下: Yeon-Seo]
# 3. POP（取り出し）順: Zachary -> Zach G. -> Zach A. -> Yosuke -> Yeon-Seo
#
# このように、「後から入れたものが先に出てくる」のがスタックの最大の特徴です！
# -----------------------------------------------------------------