import psycopg2
import numpy as np
import pandas as pd
import matplotlib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

hostname = "localhost"
username = "postgres"
db_password = "cis6030"
database = "Student_Admission"


def connection():
    """Try to Connect to the PostgreSQL Server"""
    try:
        # conduct the connection
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host=hostname,
            user=username,
            password=db_password,
            dbname=database
        )
        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print('PostgreSQL database version:')
        conn.autocommit = True
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn, cur


def shutdown_db(conn, cur):
    """Shut down the communication with the PostgreSQL"""
    cur.close()

    if conn is not None:
        conn.close()
        print('Database connection closed.')


def multiple_variable_linear_regression():
    return None


def view_table_content(cursor):
    """View the table contents"""
    sql_command3 = '''SELECT * from student;'''
    cursor.execute(sql_command3)
    for i in cursor.fetchall():
        print(i)


if __name__ == '__main__':
    connection_obj, cursor_obj = connection()
    multiple_variable_linear_regression()
    shutdown_db(connection_obj, cursor_obj)
