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

message = '{}には{}組のアーティストが参加しています。'
for i in range(5):
    print(message.format(songs[i].name, songs[i].count_artists()))