from def_listqueue import ListQueue

class Song:
    def __init__(self, name, artists):
        self.name = name
        self.artists = artists
    def count_artists(self):
        return len(self.artists)

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

q = ListQueue()
for i in range(39, 45):
    q.enqueue(songs[i])


for i in range(3):
    q.dequeue()

q.display()

