import json
import os
# filters songs by ratio for artists names
# found_clear.json contains names from last.fm and clear names (without translation) from genius.com,
# number of listeners and ratio for names from both sites


def getting_names():
    directory = '/home/songs'  # write your own path
    names_of_files = os.listdir(directory)
    names_of_artists = []
    for item in names_of_files:
        file_name = item.split('__')
        clear_name = file_name[0].split("_(", maxsplit=1)[0]
        names_of_artists.append(clear_name)
    names_of_artists = set(names_of_artists)  # artists names from genius.com
    selecting_names(names_of_artists)


def selecting_names(names_of_artists):
    ratio_threshold = 60  # changeable parameter
    file = open("found_clear.json", "r")
    inform = json.loads(file.read())
    file.close()
    mas = []
    for item in inform:
        for name in names_of_artists:
            name = name.replace("_", " ")
            if (name == item["g_name"] and item["ratio"] >= ratio_threshold):
                mas.append({"l_name": item["l_name"], "g_name": name, "ratio": item["ratio"],
                            "listeners": item["listeners"]})
    print(len(mas))
    f = open("filtered_ratio.json", "w")
    json.dump(mas, f, ensure_ascii=False)
    f.close()


if __name__ == '__main__':
    getting_names()
