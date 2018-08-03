import langdetect as lang
import json
import os


def getting_songs():
    # getting names of songs
    directory = '/home/ruslan/Загрузки/genius_songs'
    files = os.listdir(directory)
    texts = []

    # getting texts of songs
    for item in files:
        try:
            f = open(directory + '/' + item, "r")
            inform = json.loads(
                f.read())
            f.close()
            texts.append(inform["text"])
        except:
            print(item)
    filtering_texts(files, texts, directory)


def filtering_texts(files, texts, directory):
    indices = []
    languages = []
    for item in texts:
        try:
            lan = lang.detect(item)
            if lan != 'ru':
                indices.append(texts.index(item))
                languages.append(lan)
        except:
            indices.append(texts.index(item))
    indices = set(indices)  # deleting repetitive elements
    deleting(files, directory, indices)


def deleting(files, directory, indices):
    deleted_files = []  # list of deleted files
    for item in indices:
        try:
            file_name = files[item]
            os.remove(directory + '/' + file_name)
            dict = {"file_name": file_name}
            deleted_files.append(dict)
        except:
            print(file_name)
    f = open("deleted_files.json", "w")
    json.dump(deleted_files, f, ensure_ascii=False)
    f.close()


if __name__ == '__main__':
    getting_songs()
