import unittest
import mysql.connector
from pymongo import MongoClient
from bson.objectid import ObjectId
from app.models.mysql_connection import *
from app.models.mongodb_connection import *
from app.controllers.contact_controller import *

class TestContactFunctions(unittest.TestCase):
    def setUp(self):
        # Set up test data
        self.test_contact = {
            "nom": "Doe",
            "prenom": "John",
            "adresse_email": "john.doe@example.com",
            "numero_telephone": "123456789",
            "numero_telephone_maison": "987654321",
            "adresse_postale": "123 Street, City",
            "date_naissance": "1990-01-01",
            "notes": "Some notes",
            "tags": ["tag1", "tag2"],
            "photos": ["photo1.jpg", "photo2.jpg"],
            "upcoming_events": [
                {"date": "2024-01-01", "description": "Event 1"},
                {"date": "2024-02-01", "description": "Event 2"}
            ]
        }

        # Create test contact in MySQL and MongoDB
        create_contact(cnx, cursor, collection, self.test_contact)

        # Get the ID of the test contact
        self.test_contact_id = cursor.lastrowid

    def tearDown(self):
        # Delete test contact from MySQL and MongoDB
        delete_contact(cnx, cursor, collection, self.test_contact_id)

    def test_create_contact(self):
        # Test if contact was created successfully
        contacts = get_all_contacts(cursor, collection)
        self.assertTrue(self.test_contact_id in [contact["contact_id"] for contact in contacts])

    def test_get_all_contacts(self):
        # Test if all contacts are retrieved
        contacts = get_all_contacts(cursor, collection)
        self.assertTrue(len(contacts) > 0)

    def test_get_contact_by_id(self):
        # Test if contact is retrieved by ID
        contact = get_contact_by_id(cursor, collection, self.test_contact_id)
        self.assertEqual(contact["contact_id"], self.test_contact_id)

    def test_update_contact(self):
        # Update test contact
        updated_contact = self.test_contact.copy()
        updated_contact["nom"] = "Updated Name"
        update_contact(cnx, cursor, collection, self.test_contact_id, updated_contact)

        # Test if contact was updated successfully
        contact = get_contact_by_id(cursor, collection, self.test_contact_id)
        self.assertEqual(contact["nom"], "Updated Name")
    
    def test_delete_contact(self):
        # Delete the test contact
        delete_contact(cnx, cursor, collection, self.test_contact_id)

        # Test if contact is deleted
        contacts = get_all_contacts(cursor, collection)
        self.assertTrue(self.test_contact_id not in [contact["contact_id"] for contact in contacts])


if __name__ == '__main__':
    unittest.main()
