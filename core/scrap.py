#!/usr/bin/python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests


def convert_to_dict(val):

    """
    :param val: list of book details
    :return: dict on book details

    takes in raw list and then converts it into
    dictionary.
    """

    track = dict()
    for i in range(0, len(val), 2):
        temp_val = val[i].split(":")[0].lower()
        track[temp_val] = val[i + 1]
    return track


def get_data():

    """
    :return: None

    Gets data from tables and then convert it into list.
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
    :return: tuple of book details and authors

    Takes in raw data cleans it and returns tuple.
    """

    books_data = get_data()
    altered_books_data = []
    authors_data = []

    for val in books_data:
        temp = []
        if len(val) > 8:
            prev = " ".join(val)
            for v in ["ISBN:", "Series:", "Author:", "Title:"]:
                prev, val = prev.split(v)
                temp.append(" ".join((i for i in val.split(" ") if i)))
                temp.append(v)
            books_dict = convert_to_dict(list(reversed(temp)))
            author_name = books_dict.pop("author")
            altered_books_data.append(books_dict)
            authors_data.append(author_name)
        elif len(val) == 8:
            books_dict = convert_to_dict(val)
            author_name = books_dict.pop("author")
            altered_books_data.append(books_dict)
            authors_data.append(author_name)
    return altered_books_data, authors_data


if __name__ == "__main__":
    books, author = clean_data()
    print(books[-1], author[-1])
