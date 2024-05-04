import os
from dotenv import load_dotenv
import mysql.connector


'''Pour MySQL : Nous avons utilisé des requêtes paramétrées dans les fonctions 
           pour éviter les attaques par injection SQL.'''



# Loading the environment variables from .env file
'''the env file is used for security purposes,
By not hardcoding your credentials into our application code, we reduce the risk of them being exposed. 
This is especially important if since our code will be stored in a public GitHub repository'''
load_dotenv()

# Getting the database credentials from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

# Creating a connection to the database
cnx = mysql.connector.connect(user=db_user, password=db_password,
                              host=db_host, database=db_name)

# Creating a cursor object
cursor = cnx.cursor()

# Function to execute SQL commands with parameterized queries
def execute_sql(sql, values=None):
    try:
        cursor.execute(sql, values)
        cnx.commit()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        cnx.rollback()

# Function to create Contacts table
def create_contacts_table():
    create_table = """
    CREATE TABLE IF NOT EXISTS Contacts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nom VARCHAR(255) NOT NULL,
        prenom VARCHAR(255) NOT NULL,
        adresse_email VARCHAR(255),
        numero_telephone VARCHAR(255) NOT NULL,
        numero_telephone_maison VARCHAR(255),
        adresse_postale VARCHAR(255),
        date_naissance DATE
    );
    """
    execute_sql(create_table)

# Function to make id column auto increment
def alter_table_id():
    alter_table_id = "ALTER TABLE Contacts MODIFY id INT AUTO_INCREMENT;"
    execute_sql(alter_table_id)

# Closing the cursor and connection
def close_connection():
    cursor.close()
    cnx.close()
