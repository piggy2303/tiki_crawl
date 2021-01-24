import requests
from bson.json_util import loads, dumps
import json
from db import (db_col_list_item,
                db_col_item_detail,
                db_col_item_rating)


def get_list_item(cat_id):
    print("doing", cat_id)

    limit = 1
    page = 1

    url = "https://tiki.vn/api/v2/products?limit="+str(limit)+"&aggregations=1&category=" + \
        str(cat_id)+"&page="+str(page)+"&urlKey=dien-thoai-may-tinh-bang"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    response = requests.get(url, headers=headers).json()
    print(len(response["data"]))
    page_max = int(response["paging"]["total"] / 300) + 1

    for i in range(1, page_max+1, 1):
        limit = 300
        page = i
        url = "https://tiki.vn/api/v2/products?limit="+str(limit)+"&aggregations=1&category=" + \
            str(cat_id)+"&page="+str(page) + \
            "&trackity_id=fc8d7cda-22ef-a07c-1866-17499b14b111"

        x = requests.get(url, headers=headers).json()
        try:
            print(url, len(x["data"]))

            for item in x["data"]:
                couting = db_col_list_item().count_documents(
                    {"id": {"$eq": item["id"]}})
                if couting == 0:
                    db_col_list_item().insert_one(item)
                else:
                    print("duplicate")
        except Exception as error:
            # print(url)
            error = str(error)
            print(error)


def get_list_rating(product_id):
    url = "https://tiki.vn/api/v2/reviews"

    params = {
        "product_id": product_id,
        "sort": "score%7Cdesc,id%7Cdesc,stars%7Call",
        "page": 1,
        "limit": 1,
    }

    headers = {
        "User-Agent": "PostmanRuntime/7.26.8"
    }
    response = requests.get(url, headers=headers, params=params).json()
    page_max = int(response["paging"]["total"] / 300) + 1

    for i in range(1, page_max+1, 1):
        params.update({
            "limit": 300,
            "page": i
        })
        x = requests.get(url, headers=headers, params=params).json()
        print(len(x["data"]))
        try:
            print(params, len(x["data"]))
            for item in x["data"]:
                couting = db_col_item_rating().count_documents(
                    {"id": {"$eq": item["id"]}})
                if couting == 0:
                    db_col_item_rating().insert_one(item)
                else:
                    print("duplicate")
        except Exception as error:
            # print(url)
            error = str(error)
            print(error)


find_log = db_col_list_item().find({})
for i in find_log:
    product_id = i['id']
    print(product_id)
    get_list_rating(product_id)


# dien tu dien lanh
# get_list_item(1789)
# phu kien
# get_list_item(1815)
# # laptop
# get_list_item(1846)
# get_list_item(4221)
