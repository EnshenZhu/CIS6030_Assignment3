# <div style="text-align: center;">CIS6030 Information System</div>

## <div style="text-align: center;">Assignment 3</div>

## <div style="text-align: center;"> Enshen Zhu (1194726)</div>

****

### Before Start

1. Please install the PostgresSQL from the website
2. Set the database's administration password to "cis6030" (all lowercase)
3. Open the pgAdmin4 and create a database named as "Student_Admission"

### Question 1

1. All related code are inside the Question 1 folder
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
5. The final line of output ```Database connection closed.``` indicates that the database has been disconnected
   successfully.
