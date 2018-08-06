import lyricsgenius as genius
import json


def getting_names():
    f = open("result.json", "r")
    inform = json.loads(
        f.read())
    f.close()
    names = []
    for i in inform:
        names.append(i["name"])
    search(names)


def search(names):
    api = genius.Genius('OjplsjHuJuBJiqa_KqAfUz12EaUXkd2ETQwTNf-9J82qcjYRLY7OCoIpJzDOmQtF')
    for i in names:
        artist = api.search_artist(i)
        file = artist.save_lyrics(format='json')
        write_file(file)

def write_file(file):
    for i in file:
        artist = i.artist
        title = i.title
        song = i.lyrics

        dict = {"artist": artist, "title": title, "text": song}

        a = i.artist.replace(" ", "_")
        t = i.title.replace(" ", "_")
        filename = a + "__" + t + ".json"

        f = open(filename, "w")
        json.dump(dict, f, ensure_ascii=False)
        f.close()


if __name__ == '__main__':
    getting_names()
