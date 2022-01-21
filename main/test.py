import pymysql
import mysql
#
# try:
#     connection = pymysql.connect(
#         host='127.0.0.1',
#         port=3306,
#         user='root',
#         password='444745202',
#         database='shema_kurs',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     print("EEEEE")
# except Exception as ex:
#     print("Connection failed")
#     print(ex)

# import mysql.connector
# from mysql.connector import Error
# import eel
#
def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect( host='127.0.0.1',
                                        port=3306,
                                        user='root',
                                        password='444745202',
                                        database='shema_kurs',)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM live")

            row = cursor.fetchone()

            while row is not None:
                print(row)
                row = cursor.fetchone()

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()
#
# def query_with_fetchall():
#     """ Connect to MySQL database """
#     try:
#         conn = mysql.connector.connect( host='127.0.0.1',
#                                         port=3306,
#                                         user='root',
#                                         password='444745202',
#                                         database='shema_kurs',)
#         if conn.is_connected():
#             print('Connected to MySQL database')
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM live")
#
#             rows = cursor.fetchall()
#
#             print("Total Rows(s):",cursor.rowcount)
#             print(rows)
#             for row in rows:
#                 print(row)
#
#     except Error as e:
#         print(e)
#
#     finally:
#         cursor.close()
#         conn.close()
#
from mysql.connector import Error


def query_with_fetchall():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect( host='127.0.0.1',
                                        port=3306,
                                        user='root',
                                        password='444745202',
                                        database='kursowoi',)
        if conn.is_connected():
            print('Connected to MySQL database')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM main_news")

            rows = cursor.fetchall()

            print("Total Rows(s):",cursor.rowcount)
            print(rows)
            for row in rows:
                print(row)

    except Error as e:
        print(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    query_with_fetchall()

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import *
from .models import *




