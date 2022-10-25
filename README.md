# <div style="text-align: center;">CIS6030 Information System</div>

## <div style="text-align: center;">Assignment 3</div>

## <div style="text-align: center;"> Enshen Zhu (1194726)</div>

****

### Before Start

1. Please install the PostgresSQL from the website
2. Create an **env.ini** file as follows, and place it with all the question folders (Please do not put this file inside
   any of the folders)
   ```
   [postgresql]
   host = localhost
   dbname = Student_Admission
   user = postgres
   password = cis6030
   ```
3. Open the pgAdmin4 and create a database named as "Student_Admission"

### Question 1

1. All related code are inside the Question 1 folder.
2. This script is going to save the raw "Admission_Prediction.csv" file into the PostgresSQL server. You may run it by
   enter ```python q1_main.py``` inside the terminal.
3. On the first three lines of the output, you may find out the general version information about the PostgresSQL server
   used:
   ```
   Connecting to the PostgreSQL database...
   PostgreSQL database version:
   ('PostgreSQL 15.0, compiled by Visual C++ build 1914, 64-bit',)
   ```
4. The following lines shows the fetch results for all the data inside the created **student** table
   ```
   (1, 337, 118, 4, 4.5, 4.5, 9.65, 1, 0.92)
   (2, 324, 107, 4, 4.0, 4.5, 8.87, 1, 0.76)
   (3, 316, 104, 3, 3.0, 3.5, 8.0, 1, 0.72)
   (4, 322, 110, 3, 3.5, 2.5, 8.67, 1, 0.8)
   (5, 314, 103, 2, 2.0, 3.0, 8.21, 0, 0.65)
   ......
   ......
   ```
   By which each row shows the **Serial No. | GRE Score | TOEFL Score | University Rating | SOP | LOR | CGPA | Research
   |
   Chance of Admit** in sequence
5. The final line of output ```Database disconnected.``` indicates that the database has been disconnected
   successfully.

### Question 2

1. All related code are inside the Question 2 folder.
2. This script is going to do the LinearRegression in regard to the date from the "Admission_Prediction.csv" file.
   However, the script withdraw the data from the PostgresSQL rather than the original csv file.
3. This script splits the original dataset into the training and testing data. **It randomly take 90% of the original
   dataset into the training data, and the rest 10% into the testing data**.
4. When starting the script, the output will briefly report the training status as follow:
   ```
   Connecting to the PostgreSQL database...
   PostgreSQL database version:
   ('PostgreSQL 15.0, compiled by Visual C++ build 1914, 64-bit',)
   Multivariable linear regression training finished.
   ```
   Besides, it will report the numerical model of the linear regression:
   ```
   The linear regression model is y = 0.002127*X1 + 0.002555*X2 
   + 0.007459*X3 + -0.000584*X4 + 0.018436*X5 + 0.114668*X6 + 0.027368*X7 + -1.310231
   ```
   It will also report the coefficient of determination:
   ```
   The coefficient of determination is around 0.8285
   ```
   Since 0.8285 is a relatively high value in terms of 1; we assume that the trained multivariable linear regression
   model may have a high performance on predicting the output.
5. The program will also prompt the user to either **do the performance validation** of the trained model, or enter
   their own data to predict the admission rate.
   ```
   Press 1 to see a data validation from the test_dataset; 
   2 to enter your only admission profile and check the admission rate; 0 to exit
   ```
6. When pressing 1, the script will do the performance validation of the trained model, which randomly pick a row of
   data from the testing dataset, and compares **the real admission rate and the predicted admission
   rate**. For example:
   ```
   The student profile is as follow:
   GRE Score: 314 | TOEFL Score: 106 | University: 3 | SOP: 3.0
   LOR: 5.0 | CGPA: 8.90 | Research: 0
   The predicted admission rate is 0.76
   The real admission rate is 0.74
   ```
7. When pressing 2, the script will take the user input and predict the admission rate. For example, if we enter the
   folllowing information
   ```
   Enter GRE score: (the value should be an integer between 0 to 340>? 320
   Enter TOEFL score: (the value should be an integer between 0 to 120>? 110
   Enter University Rating: (the value should be a float number between 0 to 5)>? 4
   Enter the statement of purpose (the value should be a float number between 0 to 5)>? 4
   Enter the letter of recommendation strength (the value should be a float number between 0 to 5)>? 3
   Enter the undergraduate gpa (the value should be a float number between 0 to 10)>? 8.7
   Enter the research experience (the value should be binary, either 0 or 1)>? 1
   ```
   The output predicted admission rate is:
   ```
   The predicted admission rate is 0.76
   ```
8. Press 0 to exit the script.
   ```
   Bye bye!
   Database disconnected.
   ```