from def_node import Node, print_linked_list

class Song:
    def __init__(self, name, artists):
        self.name = name
        self.artists = artists

songs = []
with open('song.dat', 'r', encoding='utf-8') as fi:
    lines = fi.readlines()

for i in range(1, len(lines)):
    line = lines[i].rstrip()
    if line == '':
        continue
    items = line.split(',')
    name = items[1]
    artists = items[2:]
    songs.append(Song(name, artists))

# L1: 先頭から4行目まで
top1 = None
for i in range(4):
    top1 = Node(songs[i], top1)

# L2: 5行目から7行目まで
top2 = None
for i in range(4, 7):
    top2 = Node(songs[i], top2)

p = top1.next          # L1の2番目の節
temp = p.next          # 2番目の節の後ろを退避
p.next = top2          # 2番目の節の後ろにL2を接続
q = top2
while q.next is not None:
    q = q.next
q.next = temp          # L2の末尾にL1の残りを接続

print("L1':")
print_linked_list(top1)


top2 = None
for i in range(4, 7):
    top2 = Node(songs[i], top2)

p = top2.next          # 中央の節
top2.next = p.next     # 中央を飛ばして連結
p.next = None          # 切り取ったノードを切断

print("L2':")
print_linked_list(top2)


