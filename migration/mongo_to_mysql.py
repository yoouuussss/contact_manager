import json
import os
import mysql.connector
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import json_util


load_dotenv()
 #mongodb connection
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')
client= MongoClient(mongo_connection_string)

db = client['contact_manager']
mongo_collection = db['CONTACTS']

# Exporting MongoDB data to JSON file
with open('mongo_data.json', 'w') as f:
    json.dump(list(mongo_collection.find()), f, default=json_util.default)

#mysql connection
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

cnx = mysql.connector.connect(user=db_user, password=db_password,
                              host=db_host, database=db_name)

cursor = cnx.cursor()

with open('mongo_data.json', 'r') as f:
    data = json.load(f)

# Creating a separate table in MySQL to store migrated data from MongoDB
cursor.execute("""
    CREATE TABLE IF NOT EXISTS mongodb_data (
        oid VARCHAR(255),
        contact_id VARCHAR(255),
        notes VARCHAR(255),
        tags VARCHAR(255),
        photos VARCHAR(255),
        upcoming_events VARCHAR(255)
    )
""")

# Inserting data into the separate table
for record in data:
    cursor.execute("""
        INSERT INTO mongodb_data (oid, contact_id, notes, tags, photos, upcoming_events) 
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        record['_id']['$oid'], 
        record['contact_id'], 
        record['notes'], 
        str(record['tags']), 
        str(record['photos']), 
        str(record['upcoming_events'])
    ))

# Committing changes and close MySQL connection
cnx.commit()
cnx.close()
print("Data migrated successfully from MongoDB to MySQL.")
