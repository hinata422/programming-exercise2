
# 穴埋め問題用プログラム
# Stopクラスの定義
class Stop:
    def __init__(self, id, name, lat, lng): # 初期化メソッド
        self.id = id # インスタンス変数に値を代入
        self.name = name
        self.lat = lat
        self.lng = lng


# ここからメインの処理
# バス停IDがED01_1914、バス停の名称が立命館大学前、緯度が35.03497163、経度が135.72602961であるStopクラスのインスタンスritsumeikanを生成
ritsumeikan = Stop('ED01_1914', '立命館大学前', 35.03497163, 135.72602961)
doshisha = Stop('ED01_1922', '同志社前', 35.02913136, 135.76314762)
kyodai = Stop('ED01_1841', '京大正門前', 35.02548675, 135.7786403)
kyosan = Stop('ED01_2244', '京都産大前', 35.07182049, 135.75638731)

# Stopクラスの各インスタンスのインスタンス変数を表示
message = '{}(ID:{})のバス停の緯度経度は({},{})です。'
print(message.format(ritsumeikan.name, ritsumeikan.id, ritsumeikan.lat, ritsumeikan.lng))
print(message.format(doshisha.name, doshisha.id, doshisha.lat, doshisha.lng))
print(message.format(kyodai.name, kyodai.id, kyodai.lat, kyodai.lng))
print(message.format(kyosan.name, kyosan.id, kyosan.lat, kyosan.lng))