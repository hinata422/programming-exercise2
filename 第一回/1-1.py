# 穴埋め問題用プログラム
fi = open('kyotocitybus_stop.dat', 'r', encoding = 'utf-8')
lines = fi.readlines()
for line in lines:
    line = line.rstrip()
    items = line.split(' ')  # 1行を半角スペースで区切ってitems リストに代入
    print(','.join(items))  # カンマを区切り文字としてitemsリストの要素を連結
fi.close()

fi = open('kyotocitybus_stop.dat', 'r', encoding='utf-8')
lines = fi.readlines()
for line in lines:
    line = line.rstrip()
    items = line.split(' ')
    print(','.join(items))
fi.close()

# -----------------------------------------------------------------
# 【以下、各行の詳細な解説】
#
# fi = open('kyotocitybus_stop.dat', 'r', encoding='utf-8')
# ［ファイルを開く］
# 'kyotocitybus_stop.dat' というファイルを作業用に開きます。
# 'r' は「読み込みモード（Read）」の略です。
# encoding='utf-8' は日本語が文字化けするのを防ぐための設定です。
#
# lines = fi.readlines()
# ［中身をすべて読み込む］
# .readlines() は、開いたファイルの中身をすべて一気に読み込み、
# 「1行目」「2行目」と区切ったリスト（配列）にまとめる命令です。
#
# for line in lines:
# ［1行ずつ取り出して繰り返す］
# for 文を使って、まとめたデータ(lines)から1行ずつ順番に取り出します。
# 取り出したデータは変数 line に入り、行数分だけ下のインデントされた処理を繰り返します。
#
#     line = line.rstrip()
#     ［見えないゴミ（改行）を消す］
#     読み込んだ行の末尾には目に見えない「改行コード」が必ずついています。
#     そのままでは余分な改行が入るため、.rstrip() で末尾の改行や空白を削除します。
#
#     items = line.split(' ')
#     ［半角スペースで切り分ける］
#     .split(' ') は、半角スペースの場所で文字列を切り分ける命令です。
#     「101 京都駅前」が ['101', '京都駅前'] のようなバラバラのリストになります。
#
#     print(','.join(items))
#     ［カンマでくっつけて画面に出す］
#     ','.join(items) は、バラバラのリストをカンマ(,)で繋ぎ直す命令です。
#     ['101', '京都駅前'] が "101,京都駅前" というカンマ区切りの文字列になり、
#     それを print() で画面に表示します。
#
# fi.close()
# ［ファイルを閉じる］
# 処理が終わったら .close() で必ずファイルを閉じます。
# これを忘れると、動作が重くなったりデータ破損の原因になります。
# -----------------------------------------------------------------