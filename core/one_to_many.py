#!/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *

psql_db = PostgresqlDatabase('orm1', user='prabhath')


class BaseModel(Model):

    class Meta:
        database = psql_db


class Authors(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100, unique=True)

    def __repr__(self):

        return "ID: {} Name: {}" .format(self.id, self.name)


class Books(BaseModel):
    id = PrimaryKeyField(null=False)
    title = CharField(max_length=100)
    author = ForeignKeyField(Authors, related_name='author_details')
    edition = CharField(max_length=100)
    year_written = SmallIntegerField()
    price = DecimalField()

    def __repr__(self):

        return "ID:{} title:{} author_id:{} edition:{} year_written: {} price: {}".format(
            self.id,
            self.title,
            self.author,
            self.edition,
            self.year_written,
            self.price
        )

content = [

    {"title": "Northanger Abbey", "author": "Austen, Jane", "year_written": 1814, "edition": "Penguin", "price": 18.2},
    {"title": "War and Peace", "author": "Tolstoy, Leo", "year_written": 1865, "edition": "Penguin", "price": 12.7},
    {"title": "Anna Karenina", "author": "Tolstoy, Leo", "year_written": 1875, "edition": "Penguin", "price": 13.5},
    {"title": "Huckleberry Finn", "author": "Twain, Mark", "year_written": 1865, "edition": "Penguin", "price": 5.76},
    {"title": "Roughing It", "author": "Twain, Mark", "year_written": 1872, "edition": "Penguin", "price": 6.25},
    {"title": "The Gilded Age", "author": "Twain, Mark", "year_written": 1873, "edition": "Penguin", "price": 13.84},
    {"title": "Oliver Twist", "author": "Dickens, Charles", "year_written": 1837, "edition": "Dover", "price": 3.75},
    {"title": "Tom Sawyer", "author": "Twain, Mark", "year_written": 1862, "edition": "Random House", "price": 7.75},
    {"title": "Pride and Prejudice", "author": "Austen, Jane", "year_written": 1813, "edition": "Dover Publications",
     "price": 15.2},
    {"title": "Mrs. Dalloway", "author": "Woolf, Virginia", "year_written": 1925, "edition": "Harcourt Brace",
     "price": 25},
    {"title": "Orlando", "author": "Woolf, Virginia", "year_written": 1928, "edition": "Harcourt Brace",
     "price": 12.36},
    {"title": "The Hours", "author": "Cunnningham, Michael", "year_written": 1999, "edition": "A Harvest Book",
     "price": 12.35},
    {"title": "Bleak House", "author": "Dickens, Charles", "year_written": 1870, "edition": "Random House",
     "price": 5.75},
    {"title": "A Room of One's Own", "author": "Woolf, Virginia", "year_written": 1922, "edition": "Penguin",
     "price": 29},
    {"title": "Harry Potter", "author": "Rowling, J.K.", "year_written": 2000, "edition": "Harcourt Brace",
     "price": 19.95},
    {"title": "One Hundred Years of Solitude", "author": "Marquez", "year_written": 1967,
     "edition": "Harper  Perennial", "price": 14.00},
    {"title": "Hamlet, Prince of Denmark", "author": "Shakespeare", "year_written": 1603, "edition": "Signet  Classics",
     "price": 7.95},
    {"title": "Lord of the Rings", "author": "Tolkien, J.R.", "year_written": 1937, "edition": "Penguin",
     "price": 27.45},
]


def populate():

    psql_db.create_tables([Authors, Books], safe=True)

    # creates authors table
    for con in content:
        author, created = Authors.get_or_create(name=con["author"])
        Books.create(
            title=con["title"],
            author=author,
            edition=con["edition"],
            year_written=con["year_written"],
            price=con["price"]
        )

    print("done")

if __name__ == "__main__":
    # populate()

    b = Books.get(title="Lord of the Rings")
    print(b.author)
    print()

    a = Authors.get(name="Woolf, Virginia")
    for i in a.author_details:
        print(i)
