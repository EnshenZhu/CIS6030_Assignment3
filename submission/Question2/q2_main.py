import psycopg2
import pandas as pd
import numpy as np
import time
import random

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split

from set_env.configuration import config


def connection():
    """Try to Connect to the PostgresSQL Server"""
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


def shutdown_db(conn, cur):
    """Shut down the communication with the PostgreSQL"""
    cur.close()

    if conn is not None:
        conn.close()
        print('Database disconnected.')


def user_prompt(reg_model, X_test, y_test):
    while True:
        user_input = int(input(
            "Press 1 to see a data validation from the test_dataset; Press 2 to check the overall performance of the "
            "linear regression model on all test dataset; Press 3 to enter your only admission profile and check the "
            "admission rate; Press 0 to exit"))
        if user_input == 0:
            print("Bye bye!")
            break
        elif user_input == 1:

            real_X = X_test.sample()  # get a tested admission profile
            the_idx = real_X.index.tolist()[0]
            real_y = y_test.loc[[the_idx]].iloc[0]  # get the corresponded admission rate of the admission profile

            predict_y = reg_model.predict(real_X.values)[0]

            print()
            print("The student profile is as follow:")

            print("GRE Score: %d | TOEFL Score: %d | University: %d | SOP: %.1f" % (
                real_X.iloc[0, 0], real_X.iloc[0, 1], real_X.iloc[0, 2], real_X.iloc[0, 3]))

            print(
                "LOR: %.1f | CGPA: %.2f | Research: %d" % (real_X.iloc[0, 4], real_X.iloc[0, 5], real_X.iloc[0, 6]))

            print("The predicted admission rate is %.2f" % predict_y)
            print("The real admission rate with linear regression is %.2f" % real_y)
            print()

        elif user_input == 2:
            """to do"""
            y_test_predict = reg_model.predict(X_test.values)
            r2_value = r2_score(y_test.values, y_test_predict)
            MSR = mean_squared_error(y_test.values, y_test_predict)
            print()
            print("By evaluating the linear regression model on all test dataset")
            print("The R^2 score between the real y_test and the predict y_test is %.4f" % r2_value)
            print("The Mean Square Error between the real y_test and the predict y_test is %.4f" % MSR)
            print()

        elif user_input == 3:
            gre_score = int(input("Enter GRE score: (the value should be an integer between 0 to 340"))

            toefl_score = int(input("Enter TOEFL score: (the value should be an integer between 0 to 120"))

            university_ranking = float(
                input("Enter University Rating: (the value should be a float number between 0 to "
                      "5)"))
            sop = float(input(
                "Enter the statement of purpose (the value should be a float "
                "number between 0 to 5)"))

            lor = float(input(
                "Enter the letter of recommendation strength (the value should be a float "
                "number between 0 to 5)"))

            cgpa = float(input(
                "Enter the undergraduate gpa (the value should be a float "
                "number between 0 to 10)"))

            research_experience = int(
                input("Enter the research experience (the value should be binary, either 0 or 1)"))

            input_data = np.array(
                [gre_score, toefl_score, university_ranking, sop, lor, cgpa, research_experience]).reshape(1, -1)

            admission_predict = reg_model.predict(input_data)[0]

            print()
            if admission_predict <= 1:
                print("The predicted admission rate with linear regression is %.2f" % admission_predict)
            else:
                print(
                    "The predicted admission rate with linear regression is %.2f. Since the predicted value is over "
                    "1, we will round it into 1, which means that this student is definitely accepted in admission "
                    "with the prediction" %
                    admission_predict)
            print()


def getData(cursor):
    sql_command1 = '''
                    SELECT COLUMN_NAME
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = N'student';
                    '''
    cursor.execute(sql_command1)
    column_name = [i[0] for i in cursor.fetchall()]

    sql_command2 = '''SELECT * from student;'''
    cursor.execute(sql_command2)

    raw_data = cursor.fetchall()

    df = pd.DataFrame(raw_data, columns=column_name)
    return df


def random_dataset_split(raw_data):
    # RECALL: the column 0 of the original pd.DataFrame is the serial number. We should not put it into the training
    X = raw_data.iloc[:, 1:8]  # 注意左闭右开
    y = raw_data.iloc[:, 8]

    # We split the training and testing data with the ratio of 90% vs 10%,
    # and use the current time as the seed for the random splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=int(time.time()))
    return X_train, X_test, y_train, y_test


def multiple_variable_linear_regression(cursor):
    basic_data = getData(cursor)
    X_train, X_test, y_train, y_test = random_dataset_split(basic_data)
    reg_model = LinearRegression().fit(X_train.values, y_train.values)

    score_reg = reg_model.score(X_train.values, y_train.values)

    coef_reg = reg_model.coef_

    intercept_reg = reg_model.intercept_
    print()
    print("Multivariable Linear Regression training finished.")
    print("The coefficient of determination is around %.4f" % score_reg)

    print("The linear regression model is y = %f*X0 + %f*X1 + %f*X2 + %f*X3 + %f*X4 + %f*X5 + %f*X6 + %f" % (
        coef_reg[0], coef_reg[1], coef_reg[2], coef_reg[3], coef_reg[4], coef_reg[5], coef_reg[6], intercept_reg))

    print()

    user_prompt(reg_model, X_test, y_test)  # add the interaction with the user


if __name__ == '__main__':
    connection_obj, cursor_obj = connection()
    multiple_variable_linear_regression(cursor_obj)
    shutdown_db(connection_obj, cursor_obj)
