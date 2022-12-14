import psycopg2
# from set_env.configuration import config

from configparser import ConfigParser


def config(filename='../env.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db_profile = {}
    if parser.has_section(section):
        all_params = parser.items(section)
        for single_param in all_params:
            db_profile[single_param[0]] = single_param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db_profile


def connection():
    """Try to Connect to the PostgreSQL Server"""
    try:
        parameters = config()

        # conduct the connection
        print('Connecting to the PostgreSQL database...')

        conn = psycopg2.connect(**parameters)
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


def drop_student_table(cursor):
    """Remove the student table if it is existed"""
    try:
        sql_drop_command = '''DROP TABLE student;'''
        cursor.execute(sql_drop_command)
    except Exception:
        pass


def shutdown_db(conn, cur):
    """Shut down the communication with the PostgreSQL"""
    cur.close()

    if conn is not None:
        conn.close()
        print('Database disconnected.')


def save_csv_to_db(conn, cursor):
    drop_student_table(cursor)

    # Create the schema
    sql_command1 = '''CREATE TABLE student(
                    Serial_Num int NOT NULL PRIMARY KEY,
                    GRE_Score int,
                    TOEFL_Score int,
                    University int,
                    SOP float,
                    LOR float,
                    CGPA float,
                    Research int,
                    Chance_of_Admin float
                    );
                    '''

    cursor.execute(sql_command1)

    # Execute the data insertion
    sql_command2 = '''COPY student(Serial_Num, GRE_Score, TOEFL_Score, University,SOP,LOR,CGPA,Research,Chance_of_Admin)
                    FROM 'D:\\Guelph_Master\\CIS6030 Information System\\CIS6030_Assignment\\CIS6030_Assignment3\\Question1\Admission_Predict_trimmed.csv'
                    DELIMITER ','
                    CSV HEADER;'''

    cursor.execute(sql_command2)

    conn.commit()


def view_table_content(cursor):
    """View the all table contents"""
    sql_command3 = '''SELECT * from student;'''
    cursor.execute(sql_command3)
    for i in cursor.fetchall():
        print(i)

    print()
    """View the table contents which toefl_score >100"""
    sql_command4 = '''SELECT * from student WHERE toefl_score >115 and gre_score>339;'''
    cursor.execute(sql_command4)
    for i in cursor.fetchall():
        print(i)


if __name__ == '__main__':
    connection_obj, cursor_obj = connection()
    save_csv_to_db(connection_obj, cursor_obj)
    view_table_content(cursor_obj)
    shutdown_db(connection_obj, cursor_obj)
