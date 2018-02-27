# -*- coding:utf-8 -*-
# python version= python3.X
# code lines count about 40

import os
import json
import pandas as pd
from customTools.databaseHome import video_mongo_clinet, music_mongo_clinet, novel_mongo_clinet


def _read_data_from_mongoDB(aggregate_rule, mongo_collection):
    """
    this is a function to read data from mongodb database,
    search with aggregate
    :param aggregate_rule:          search rule
    :param mongo_collection:        the data collection
    :return: data list              all data in a list
    """
    # create collection cursor
    cursor = mongo_collection.aggregate(aggregate_rule)
    """
    read and append data into list by collection cursor
    data_list = list()
    while True:
        try:
            result = cursor.next()
        except Exception:
            break
        else:
            data_list.append(result)
    return data_list
    """
    # By coercion type conversion,it would be iterate the cursor automatic
    return list(cursor)


def _save_data_in_file(filename, data):
    # to save data in a json type file object
    file_path = "./dataCollection/{}.json".format(filename)
    with open(file_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def video_data_collection():
    """
    read video data from mongodb , and save as a json type file in dataCollection dir
    the aggregate rule is Reverse order query by adding time
    """
    search_rule = [{"$sort": {"addtime": -1}},
                   {"$project": {"_id": 0, "finger": 1, "intro": 1, "video": 1, "image": 1}}]

    data = _read_data_from_mongoDB(search_rule, video_mongo_clinet)

    _save_data_in_file(filename="videos", data=data)


def music_data_collection():
    search_rule = [{"$sort": {"played": -1}}, {"$project": {"_id": 0, "title": 1, "image": 1, "music": 1, "played": 1}},
                   {"$limit": 100}]
    data = _read_data_from_mongoDB(search_rule, music_mongo_clinet)

    _save_data_in_file(filename="musics", data=data)


def novel_data_collection():
    # get data from mongodb
    search_rule = [{"$project": {"_id": 0, "name": 1, "author": 1, "state": 1, "source": 1, "wordCount": 1,
                                 "recommend": 1, "intro": 1, "link": 1, "image": 1}}]
    data = _read_data_from_mongoDB(aggregate_rule=search_rule, mongo_collection=novel_mongo_clinet)

    # select different source data into different data list
    qidian_data = [i for i in data if i["source"] == "起点中文网"]
    chuangshi_data = [i for i in data if i["source"] == "创世中文网"]
    data_need_drop = []

    # find the repeat data
    for i in qidian_data:
        for d in chuangshi_data:
            if d["name"] == i["name"] and d["author"] == i["author"]:
                i["recommend"] += d["recommend"]
                i["link"] = {"qidian": i["link"], "chuangshi": d["link"]}
                data_need_drop.append(d)
        if type(i["link"]) is str:
            i["link"] = {"qidian": i["link"]}

    # drop the repeat data
    for i in data_need_drop:
        chuangshi_data.remove(i)

    # change the link data type in chuangshi data list
    for i in chuangshi_data:
        i["link"] = {"chuangshi": i["link"]}

    # extent the two list
    data = qidian_data + chuangshi_data

    # use pandas sort the all data by recommend value
    df = pd.DataFrame(data)
    df = df.sort_values(by="recommend", axis=0, ascending=False)

    # select top 100, and trans DataFrame type into list of python
    # key word "orient='records'" make data structure like this >> [{},{},{},....]
    df = df[:100]
    data = df.to_dict(orient='records')

    # save data as a json type file
    _save_data_in_file(filename="novels", data=data)


if __name__ == '__main__':
    video_data_collection()
    music_data_collection()
    novel_data_collection()
    pass


