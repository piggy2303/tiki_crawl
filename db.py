from pymongo import MongoClient
from bson.json_util import loads, dumps
import json

myclient = MongoClient("mongodb://0.0.0.0:27017/")

mydb = myclient["tiki"]


def db_col_list_item():
    return mydb["list_item"]


def db_col_item_detail():
    return mydb["item_detail"]


def db_col_item_rating():
    return mydb["item_rating"]
