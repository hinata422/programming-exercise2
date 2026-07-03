class ListQueue():
    def __init__(self):
        self.list = []  # データ格納用のインスタンス変数list(リスト)

    def count(self):
        return len(self.list)

    def enqueue(self, data):  # キューにデータを追加するメソッド
        self.list.append(data)

    def dequeue(self):  # キューからデータを取り出すメソッド
        if self.list == []:  # リストが空かどうか判定
            print('キューが空のため、これ以上DEQUEUEできません。')
            return None
        return self.list.pop(0)

    def display(self):  # キューの中身を先頭から表示するメソッド
        print('======キューの先頭======')
        for i in self.list:
            artist_names = '、'.join(i.artists)
            print('{} のアーティストは {} です。'.format(i.name, artist_names))
        print('======キューの末尾======\n')