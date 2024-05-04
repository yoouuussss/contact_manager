import os
from dotenv import load_dotenv
from pymongo import MongoClient


"""Pour MongoDB : L'authentification est déjà en place 
   et le chiffrement des données doit être activé dans la configuration du serveur MongoDB."""

# Loading the environment variables from .env file
load_dotenv()

# Getting the MongoDB connection string from environment variable
mongo_connection_string = os.getenv('MONGO_CONNECTION_STRING')

# Creating a connection to the database
client = MongoClient(mongo_connection_string)

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("MongoDB connection successful")
except Exception as e:
    print("MongoDB connection unsuccessful:", e)


# Accessing the 'contact_manager' database and the 'CONATCTS' collection
db = client['contact_manager']
collection = db['CONTACTS']

# Closing the connection
#client.close() 
