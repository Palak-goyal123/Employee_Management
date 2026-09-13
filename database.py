import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Suhana@123",
    database="employee_management"
)

cursor = connection.cursor(dictionary=True)