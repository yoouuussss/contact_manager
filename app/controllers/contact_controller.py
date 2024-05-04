import mysql.connector
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.mysql_connection import *
from app.models.mongodb_connection import *

def create_contact(mysql_conn, mysql_cursor, mongo_collection, contact):
    """
    Creates a contact in the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Create in MySQL
        query = "INSERT INTO Contacts (nom, prenom, adresse_email, numero_telephone, numero_telephone_maison, adresse_postale, date_naissance) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (contact['nom'], contact['prenom'], contact['adresse_email'], contact['numero_telephone'], contact['numero_telephone_maison'], contact['adresse_postale'], contact['date_naissance'])
        mysql_cursor.execute(query, values)
        id = mysql_cursor.lastrowid  # get the id of the created contact

        # Commit the transaction
        mysql_conn.commit()

        # Create in MongoDB
        mongo_contact = {
            "contact_id": id,
            "notes": contact.get('notes', ''),
            "tags": contact.get('tags', []),
            "photos": contact.get('photos', []),
            "upcoming_events": contact.get('upcoming_events', [])
        }
        result = mongo_collection.insert_one(mongo_contact)
        print(f"MongoDB Insert Result: {result.inserted_id}")
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except pymongo.errors.PyMongoError as err:
        print(f"MongoDB Error: {err}")

def get_all_contacts(cursor, collection):
    """
    Retrieves all contacts from the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Get from MySQL
        cursor.execute("SELECT * FROM Contacts")
        mysql_contacts = cursor.fetchall()

        # Convert MySQL contacts to dictionaries
        mysql_contacts = [
            {
                "contact_id": contact[0],
                "nom": contact[1],
                "prenom": contact[2],
                "adresse_email": contact[3],
                "numero_telephone": contact[4],
                "numero_telephone_maison": contact[5],
                "adresse_postale": contact[6],
                "date_naissance": contact[7]
            }
            for contact in mysql_contacts
        ]

        # Get from MongoDB
        mongo_contacts = list(collection.find())

        # Merge the two lists
        contacts = mysql_contacts + mongo_contacts
        print(contacts)
        return contacts
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def get_contact_by_id(cursor, collection, id):
    """
    Retrieves a contact by its ID from the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Get from MySQL
        query = "SELECT * FROM Contacts WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        mysql_contact = cursor.fetchone()

        # Convert the MySQL contact to a dictionary
        mysql_contact_dict = dict(zip(cursor.column_names, mysql_contact))

        # Get from MongoDB
        mongo_contact = collection.find_one({"contact_id": id})

        # Merge the two dictionaries
        contact = {**mysql_contact_dict, **mongo_contact}
        print(contact)
        return contact
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def delete_contact(mysql_conn, cursor, collection, id):
    """
    Deletes a contact from the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Delete from MySQL
        query = "DELETE FROM Contacts WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        mysql_conn.commit()  # commit the transaction

        # Delete from MongoDB
        collection.delete_one({"contact_id": id})
    except mysql.connector.Error as err:
        print(f"Error: {err}")



def update_contact(mysql_conn, cursor, collection, id, contact):
    """
    Updates a contact in the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Update in MySQL
        query = "UPDATE Contacts SET nom = %s, prenom = %s, adresse_email = %s, numero_telephone = %s, numero_telephone_maison = %s, adresse_postale = %s, date_naissance = %s WHERE id = %s"
        values = (contact['nom'], contact['prenom'], contact['adresse_email'], contact['numero_telephone'], contact['numero_telephone_maison'], contact['adresse_postale'], contact['date_naissance'], id)
        cursor.execute(query, values)

        # Commit the transaction
        mysql_conn.commit()

        # Update in MongoDB
        mongo_contact = {
            "contact_id": id,
            "notes": contact.get('notes', ''),
            "tags": contact.get('tags', []),
            "photos": contact.get('photos', []),
            "upcoming_events": contact.get('upcoming_events', [])
        }
        collection.update_one({"contact_id": id}, {"$set": mongo_contact})
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def search_contact(mysql_cursor, mongo_collection, search_term):
    """
    Searches for a contact in the MySQL Contacts table and MongoDB Contacts collection.
    """
    try:
        # Search in MySQL
        query = "SELECT * FROM Contacts WHERE nom LIKE %s OR prenom LIKE %s"
        values = (f'{search_term}%', f'{search_term}%')  # Add '%' to the search term for a prefix search
        mysql_cursor.execute(query, values)
        mysql_results = mysql_cursor.fetchall()
        print(mysql_results)

        # Fetch the rest of the contact's information from MongoDB using the id
        merged_results = []
        for mysql_result in mysql_results:
            mysql_result_dict = dict(zip(mysql_cursor.column_names, mysql_result))  # Convert the tuple to a dictionary
            mongo_result = mongo_collection.find_one({"contact_id": mysql_result_dict['id']})  # Now you can access the 'id' field
            if mongo_result:
                merged_result = {**mysql_result_dict, **mongo_result}
                merged_results.append(merged_result)

        return merged_results
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except pymongo.errors.PyMongoError as err:
        print(f"MongoDB Error: {err}")
