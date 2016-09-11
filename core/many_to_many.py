#!/usr/bin/python3
# -*- coding: utf-8 -*-

from peewee import *
import random

psql_db = PostgresqlDatabase('orm1', user='prabhath')

"""
One student can enroll any number of courses.
One Course can be enrolled by any number of users.
"""


class BaseModel(Model):
    class Meta:
        database = psql_db


class Student(BaseModel):
    name = CharField(max_length=100, unique=True)


class Course(BaseModel):
    name = CharField(max_length=100, unique=True)


class StudentCourse(BaseModel):
    student = ForeignKeyField(Student)
    course = ForeignKeyField(Course)


def populate():
    psql_db.create_tables([Student, Course, StudentCourse], safe=True)

    students = ["student1", "student2", "student3", "student4"]
    courses = ["python", "java", "DataStructures", "WebDevelopment", "OperatingSystems"]

    for course in courses:
        Course.create_or_get(name=course)

    for stud in students:
        s = Student.create(name=stud)
        Course.create_or_get(name=random.choice(courses))

        indexes = set()
        while len(indexes) < 2:
            indexes.add(random.randint(0, len(courses) - 1))

        indexes = list(indexes)
        course1 = Course.get(name=courses[indexes[0]])
        course2 = Course.get(name=courses[indexes[1]])

        StudentCourse.create(student=s, course=course1)
        StudentCourse.create(student=s, course=course2)

    print("done\n")


if __name__ == "__main__":

    # populate()

    # get all student for a particular course
    query = (Student
             .select()
             .join(StudentCourse)
             .join(Course)
             .where(Course.name == 'DataStructures'))

    for student in query:
        print(student.name)
    print()

    # get all courses a student took
    student_courses = (Course
                       .select()
                       .join(StudentCourse)
                       .join(Student)
                       .where(Student.name == 'student1'))

    for course in student_courses:
        print(course.name)
