import lyricsgenius as genius
import json
from fuzzywuzzy import fuzz

# getting texts of songs from www.genius.com


def getting_names():
    f = open("result.json", "r")
    inform = json.loads(
        f.read())
    f.close()
    names = []
    for i in inform:
        names.append(i["name"])
    serch(names)


def serch(names):
    api = genius.Genius('OjplsjHuJuBJiqa_KqAfUz12EaUXkd2ETQwTNf-9J82qcjYRLY7OCoIpJzDOmQtF')
    for i in names:
        try:
            artist = api.search_artist(i, take_first_result=True)
            proc = fuzz.token_sort_ratio(i, artist.name)
            strin = "Last.fm name: " + i + " ; Genius name: " + artist.name + " ratio: " + str(proc) + "\n"
            f = open("result.txt", "a")
            f.write(strin)
            f.close()
            file = artist.songs
            function(file)
        except:
            f = open("result.txt", "a")
            f.write("Nothing found for artist: " + i + "\n")
            f.close()


def function(file):
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
