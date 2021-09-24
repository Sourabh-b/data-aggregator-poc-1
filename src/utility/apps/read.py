import json


def read_apps(read_from: str):
    file = open(read_from)
    contents_list = json.load(file)
    file.close()
    return contents_list
