import psycopg2
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
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


def status_identify(value):
    if value == 1:
        return "Accepted"
    else:
        return "Rejected"


def user_prompt(reg_model, X_test, y_test):
    while True:
        user_input = int(input(
            "Press 1 to see a data validation from the test_dataset; Press 2 to check the overall performance (with a "
            "confusion matrix) of the logistic regression model on the test dataset. Press 3 to enter your only "
            "admission profile and check the admission rate; Press 0 to exit"))
        if user_input == 0:
            print("Bye bye!")
            break
        elif user_input == 1:

            print()

            real_X = X_test.sample()  # get a tested admission profile
            the_idx = real_X.index.tolist()[0]
            real_y = y_test.loc[[the_idx]].iloc[0]  # get the corresponded admission rate of the admission profile
            real_y_rounded = round(real_y)
            real_admission_status = status_identify(real_y_rounded)

            predict_y = reg_model.predict(real_X.values)[0]
            predict_admission_status = status_identify(predict_y)

            print("The student profile is as follow:")

            print("GRE Score: %d | TOEFL Score: %d | University: %d | SOP: %.1f" % (
                real_X.iloc[0, 0], real_X.iloc[0, 1], real_X.iloc[0, 2], real_X.iloc[0, 3]))

            print(
                "LOR: %.1f | CGPA: %.2f | Research: %d" % (real_X.iloc[0, 4], real_X.iloc[0, 5], real_X.iloc[0, 6]))

            print("The predicted admission case with logistic regression is %d. The predicted admission status: %s" % (
                predict_y, predict_admission_status))

            print("The real admission case is %.2f, which is normalized into %d. The real admission status: %s" % (
                real_y, real_y_rounded, real_admission_status))

            print()

        elif user_input == 2:
            print()

            y_test_predicted = reg_model.predict(X_test.values)
            y_test_round = np.round(y_test.values)

            accuracy = accuracy_score(y_test_round, y_test_predicted) * 100
            print("By evaluating the logistic regression model on all test dataset")
            print("The accuracy of the model is %.2f percents" % accuracy)

            c_m = confusion_matrix(y_test_round, y_test_predicted, labels=[1, 0])
            df_cm = pd.DataFrame(c_m, index=[i for i in ["Actually Accepted", "Actually Rejected"]],
                                 columns=[i for i in ["Predicted Accepted", "Predicted Rejected"]])
            plt.figure(figsize=(10, 7))
            sns.heatmap(df_cm, annot=True, cmap="crest")
            plt.savefig("confusion_matrix.png")
            plt.show()

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
            user_predict_admission_status = status_identify(admission_predict)

            print()
            print(
                "The predicted admission rate with logistic regression is %d. It predict the admission status is %s." % (
                    admission_predict, user_predict_admission_status))
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


def random_dataset_split(input):
    # RECALL: the column 0 of the original pd.DataFrame is the serial number. We should not put it into the training
    X = input.iloc[:, 1:8]  # ??????????????????
    y = input.iloc[:, 8]

    # We split the training and testing data with the ratio of 90% vs 10%,
    # and use the current time as the seed for the random splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=int(time.time()))
    return X_train, X_test, y_train, y_test


def logistic_regression(cursor):
    print()
    basic_data = getData(cursor)
    X_train, X_test, y_train, y_test = random_dataset_split(basic_data)

    """The next step is extremely important"""
    # Because in logistic regression, the output can only be discrete classes
    # We normalize the initial decimal output to 0 or 1 by rounding
    y_train_rounded, y_test_rounded = round(y_train), round(y_test)

    reg_model = LogisticRegression(random_state=0, max_iter=500).fit(X_train.values, y_train_rounded.values)
    print("Logistic Regression training finished.")

    score_reg = reg_model.score(X_train.values, y_train_rounded.values)
    print("The coefficient of determination is around %.4f" % score_reg)

    intercept = reg_model.intercept_[0]
    print("The interception is around %.4f" % intercept)

    coefficient_ls = reg_model.coef_[0]

    for idx, a_coefficient in enumerate(coefficient_ls):
        print("Column %d has the coefficient around %.4f" % (idx, a_coefficient))

    print()

    user_prompt(reg_model, X_test, y_test)  # add the interaction with the user


if __name__ == '__main__':
    connection_obj, cursor_obj = connection()
    logistic_regression(cursor_obj)
    shutdown_db(connection_obj, cursor_obj)
