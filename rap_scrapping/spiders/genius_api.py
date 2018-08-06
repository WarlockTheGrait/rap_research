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
        function(file)


def function(file):
    print(file["songs"][0]["lyrics"])
    f = open("text.txt", 'a')
    f.write(file["songs"][0]["lyrics"])
    f.close()


if __name__ == '__main__':
    getting_names()
