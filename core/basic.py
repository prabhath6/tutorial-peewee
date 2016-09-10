#!/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *
from core.scrap import clean_data

psql_db = PostgresqlDatabase(
    'ORM',  # database nanme
    user='prabhath',  # user name
    password='',  # password
    host='localhost',  # hostname -> localhost or 127.0.0.1
)


# Define table
class Books(Model):

    id = PrimaryKeyField(null=False)
    title = CharField(max_length=100)
    author = CharField(max_length=100)
    series = CharField(max_length=50)
    isbn = CharField(max_length=100, unique=True)

    def __repr__(self):
        return "ID: {} Title: {} Author: {} Series: {} ISBN: {}".format(
            self.id,
            self.title,
            self.author,
            self.series,
            self.isbn
        )

    class Meta:
        database = psql_db
        db_table = "books"


# Insert Bulk records
def insert_data(books):

    # create table
    psql_db.create_table(Books, safe=True)  # check for table before creating

    with psql_db.atomic():

        # insert data
        for book in books:
            Books.create(**book)

    print("Done")


# Insert Single row
def insert_single_row(book):

    # create table
    psql_db.create_table(Books, safe=True)  # check for table before creating

    row = Books(
        title=book["title"],
        author=book["author"],
        series=book["series"],
        isbn=book["isbn"]
    )
    row.save()

    """
    alternate way
    row = Books.create(**row)
    """

    print("Created -> {}".format(row))


# Get single record
def get_single_row(isbn):

    """
    :param isbn: str of book isbn
    :return: None

    Prints whole based row based on isbn passed.

    NOTE:- Any attribute from books class can be used to get
    a row.
    """

    try:
        book = Books.get(Books.isbn == isbn)
    except Books.DoesNotExist:
        book = None

    if book:
        print(book)


# Get multiple records
def get_multiple_rows():

    """
    :return:
    """

    try:
        books = Books.select().where(Books.id <= 10)
        """
        alternate way of doing
        books = Books.select().limit(10)
        """
    except Books.DoesNotExist:
        books = None

    for book in books:
        print(book)


# Update Single record
def update_single_record():

    """
    updating single record.
    :return:
    """

    book = Books.get(Books.id == 1)
    print("Before: {}".format(book))
    book.author = book.author.upper()
    book.save()
    print("After: {}".format(Books.get(Books.id == 1)))


# Update Multiple record
def update_multiple_records():

    """
    updating multiple record.
    :return:
    """

    """
        for book in Books.select().where(Books.id <= 10):
            book.author = book.author.upper()
            book.save()

    Do not do this! Not only is this slow, but it is also vulnerable to race conditions
    if multiple processes are updating the counter at the same time.
    """

    # atomic updates
    for i in range(1, 11):
        book = Books.update(author=fn.Upper(Books.author)).where(Books.id == i)
        book.execute()

    for book in Books.select().where(Books.id <= 10):
        print(book)


# Single delete
def delete_single_record():

    """
    Delete single record.
    :return:
    """

    book = Books.get(Books.id == 1)
    book.delete_instance()
    print("Delete: {}".format(book))


# multiple delete
def delete_multiple_records():

    """
    delete multiple record.
    :return:
    """

    query = Books.delete().where(Books.id < 10)
    rows = query.execute()
    print("Delete: {} rows" .format(rows))


if __name__ == "__main__":

    books_, author_, total = clean_data()
    insert_data(total)  # bulk insert

    # data = {
    #     'isbn': '1-86092-004-7',
    #     'series': 'Comedy',
    #     'title': 'Goodbye to all Cats',
    #     'author': 'P. G. Wodehouse (1881-1975)'
    # }
    # insert_single_row(data)

    # get_single_row("1-86092-004-7")

    # get_multiple_rows()

    # update_single_record()

    # update_multiple_record()

    # delete_single_record()

    # delete_multiple_records()
