# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 17:43:44 2019

Purpose:  Example illustrating connection to postgres database

@author: Graham
"""

import psycopg2
try:
    connection = psycopg2.connect(user="postgres",
                                  password="insight",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="test")
    cursor = connection.cursor()
    postgreSQL_select_Query = "select * from food"
    cursor.execute(postgreSQL_select_Query)
    print("Selecting rows from food table using cursor.fetchall")
    food_records = cursor.fetchall()

    print("Print each row and it's columns values")
    for row in food_records:
        print("Id = ", row[0], )
        print("Name = ", row[1])
        print("Is Fruit  = ", row[2], "\n")

    # try writing to the database
    postgres_insert_query = """ INSERT INTO food (NAME, IS_FRUIT)
                                VALUES (%s,%s)"""

    foods = {'orange': True, 'banana': True, 'apple': True,
             'beef': False, 'chicken': False, 'rice': False}

    for name, is_fruit in foods.items():
        print(name, is_fruit)
        record_to_insert = (name, is_fruit)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

except (Exception, psycopg2.Error) as error:
    print("PostgreSQL error:  ", error)
finally:
    # closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
