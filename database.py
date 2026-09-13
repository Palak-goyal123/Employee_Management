import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()  # .env file se variables load karta hai

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor(dictionary=True)
