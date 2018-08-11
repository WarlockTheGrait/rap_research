import json
import os
# takes file result_songs.json (songs from last.fm) and list of songs from genius (genius_songs_filtered)
# result: {"l_name": entry["l_name"],
#          "g_name": entry["g_name"],
#          "number of songs genius": entry["number of songs genius"],
#          "number of songs last": item["number of songs last"],
#          "percent": (entry["number of songs genius"]/item["number of songs last"])*100}


def songs_from_last():
    f = open("result_songs.json", "r")
    inform = json.loads(f.read())
    f.close()
    names = []
    for item in inform:
        names.append(item["artist"])
    names = set(names)
    dict = []
    for name in names:
        counter = 0
        for item in inform:
            if (item["artist"] == name):
                counter += 1
        dict.append({"artist": name, "number of songs last": counter})
    songs_from_genius(dict)

def songs_from_genius(vac):
    # list of song-files
    directory = '/songs/genius' 
    names_of_files = os.listdir(directory)
    f = open("filtered_ratio.json", "r")
    inform = json.loads(f.read())
    f.close()

    dict = []
    for item in inform:
        dict.append({"l_name": item["l_name"], "g_name": item["g_name"]})
    # getting names of artists from song-files
    names_of_artists = []
    for item in names_of_files:
        file_name = item.split('__')
        clear_name = file_name[0].split("_(", maxsplit=1)[0]
        names_of_artists.append(clear_name)
        
    # counting number of songs for each artist
    number_of_songs = []
    for item in dict:
        counter = 0
        for name in names_of_artists:
            name = name.replace("_", " ")
            if (name == item["g_name"]):
                counter += 1
        number_of_songs.append({"l_name": item["l_name"], "g_name": item["g_name"], "number of songs genius": counter})
    
    # shaping result dictionary 
    result = []
    for item in vac:
        for entry in number_of_songs:
            if (item["artist"] == entry["l_name"]):
                result.append({"l_name": entry["l_name"],
                               "g_name": entry["g_name"],
                               "number of songs genius": entry["number of songs genius"],
                               "number of songs last": item["number of songs last"],
                               "percent": (entry["number of songs genius"]/item["number of songs last"])*100})
    f = open("genius_last_coating.json", "w")
    json.dump(result, f, ensure_ascii=False)
    f.close()


if __name__ == '__main__':
    songs_from_last()
