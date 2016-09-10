#!/usr/bin/python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests


def convert_to_dict(val):
    track = dict()
    for i in range(0, len(val), 2):
        temp_val = val[i].split(":")[0]
        track[temp_val] = val[i + 1]
    return track


def get_data():

    """
    :return:
    """

    soup = BeautifulSoup(
        requests.get("http://www.travelman.co.uk/list_of_titles.htm").text,
        'html.parser'
    )
    
    temp = []
    form = soup.find('form', {"name": "formTitles"})
    tables = form.find_all("table")
    for tb in tables[1:]:
        if tb.find("table"):
            for val in str(tb.find("table").text).strip().split("\n"):
                if val.split("\n")[0]:
                    temp.append(val.split("\n")[0])
        yield temp
        temp = []


def clean_data():

    """
    :return:
    """

    main_temp = get_data()
    main_main_temp = []

    for val in main_temp:
        temp = []
        if len(val) > 8:
            prev = " ".join(val)
            for v in ["ISBN:", "Series:", "Author:", "Title:"]:
                prev, val = prev.split(v)
                temp.append(" ".join((i for i in val.split(" ") if i)))
                temp.append(v)
            main_main_temp.append(convert_to_dict(list(reversed(temp))))
        elif len(val) == 8:
            main_main_temp.append(convert_to_dict(val))
    return main_main_temp


if __name__ == "__main__":
    data = clean_data()
    print(data[-1])
