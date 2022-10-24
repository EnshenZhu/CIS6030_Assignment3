import psycopg2
import os.path

hostname = "localhost"
username = "postgres"
db_password = "cis6030"
database = "Student_Admission"

file_location = r"../assets/Admission_Predict_Ver1.1.csv"


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
    # close the communication with the PostgreSQL
    cur.close()

    if conn is not None:
        conn.close()
        print('Database connection closed.')


def save_csv_to_db(conn, cursor):
    sql_command1 = '''CREATE TABLE student6(
                    Serial_Num int NOT NULL PRIMARY KEY,
                    GRE_Score int,
                    TOEFL_Score int,
                    University int,
                    SOP float,
                    LOR float,
                    CGPA float,
                    Research int,
                    Chance_of_Admin float
                    );'''

    cursor.execute(sql_command1)

    sql_command2 = '''COPY student6(Serial_Num) FROM 'D:\Guelph_Master\CIS6030 Information System\CIS6030_Assignment\CIS6030_Assignment3\Question1\qtest.csv' DELIMITER ',' CSV HEADER;'''

    cursor.execute(sql_command2)

    conn.commit()


if __name__ == '__main__':
    connection_obj, cursor_obj = connection()
    save_csv_to_db(connection_obj, cursor_obj)
    shutdown_db(connection_obj, cursor_obj)
