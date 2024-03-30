import pymysql

from settings import DATABASE_NAME, DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD

conn = pymysql.connect(host=DATABASE_HOST, user=DATABASE_USER, password=DATABASE_PASSWORD)
conn.cursor().execute('CREATE DATABASE `' + DATABASE_NAME + '`')
conn.close()
