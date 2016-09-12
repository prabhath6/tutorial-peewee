#!/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *

psql_db = PostgresqlDatabase('orm1', user='prabhath')


class BaseModel(Model):
    class Meta:
        database = psql_db


class Voter(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=100)
    age = SmallIntegerField()


class Vote(BaseModel):
    user = ForeignKeyField(Voter, primary_key=True)
    candidate_name = CharField(max_length=50)


if __name__ == "__main__":

    psql_db.create_tables([Voter, Vote], safe=True)

    # create voter
    vot, status = Voter.create_or_get(name="Sam", age=25)

    # vote
    vote1 = Vote.create(user=vot, candidate_name="Hillary")
    #  vote2 = Vote.create(user=vot, candidate_name="Trump")

    """
    Second statement will result in IntegrityError: duplicate key value violates unique constraint "vote_pkey"
    as one user can cast only one vote.
    """

    print("done")
