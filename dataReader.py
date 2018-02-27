from pymongo import MongoClient
from json import load

client_maker = MongoClient(host="127.0.0.1", port=27017)

database_name = "data"

data_file_path = "/root/dataFiles/dataCollection/{}.json"

def read_data_file(file_path):
    """
    read data from data file with type json
    :param file_path:
    :return: data_list
    """
    with open(file_path, "r") as f:
        data_list = load(f)
    return data_list


def save_data_into_mongodb(data_list, database_name, collection_name):
    """
    create mongodb client object to save data,
    :param data_list:
    :param database_name:
    :param collection_name:
    :return: none
    """
    mongo_client = client_maker[database_name][collection_name]
    # clear the collection but not drop the collection
    mongo_client.remove({})
    for data_dict in data_list:
        mongo_client.insert_one(data_dict)


def handle_data(data_name):
    # ensure data file name ,and use it as the mongodb collection name
    file_name = data_name

    data = read_data_file(file_path=data_file_path.format(file_name))

    save_data_into_mongodb(data_list=data, database_name=database_name, collection_name=file_name)


if __name__ == '__main__':
    handle_data(data_name="videos")
    handle_data(data_name="musics")
    handle_data(data_name="novels")
