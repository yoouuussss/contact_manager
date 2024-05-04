# Importing required PyQt5 modules
from PyQt5 import QtWidgets, QtCore, QtGui

# Importing controllers and views
import app.controllers.contact_controller as contact_controller
from app.views.add_contact_view import AddContactDialog
from app.views.contact_details_view import ContactDetailsDialog

# Importing QIcon and QColor classes
from PyQt5.QtGui import QIcon, QColor

# Main page representing the contact list
class MainPage(QtWidgets.QWidget):
    def __init__(self):
        super(MainPage, self).__init__()

        # Setting window properties
        self.setWindowTitle("Contact Manager")
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowIcon(QIcon('C:/Users/HP/Desktop/my_contact_manager/app/views/telephone.png'))

        # Setting background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor("#f0f0f0"))
        self.setPalette(p)

        # Creating search bar widget
        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setFixedHeight(40)  # Setting the height of the search bar
        self.search_bar.setStyleSheet("QLineEdit { padding-left: 5px; }")
        self.search_bar.setPlaceholderText("Search...")

        # Creating add contact button widget
        self.add_contact_button = QtWidgets.QPushButton("Add Contact")
        self.add_contact_button.setFixedSize(120, 40)  # Setting the size of the add contact button

        # Creating contacts list widget
        self.contacts_list = QtWidgets.QListWidget()
        self.contacts_list_title = QtWidgets.QLabel("Contacts List")
        self.contacts_list_title.setStyleSheet("font-size: 24px;")

        # Layout
        main_layout = QtWidgets.QVBoxLayout()

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(self.add_contact_button)

        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.contacts_list_title)
        main_layout.addWidget(self.contacts_list)

        self.setLayout(main_layout)

        # Connecting signals
        self.search_bar.textChanged.connect(self.search_contacts)
        self.add_contact_button.clicked.connect(self.show_add_contact_dialog)
        self.contacts_list.itemDoubleClicked.connect(self.show_contact_details_dialog)

        # Populating contacts list with all contacts
        self.populate_contacts(contact_controller.get_all_contacts)

        # Applying style
        self.apply_style()

    # Applying style
    def apply_style(self):
        style = """
            QWidget{
                background-color: #f0f0f0;
            }
            QLineEdit, QTextEdit, QListView{
                background-color: #ffffff;
                border: 1px solid #c4c4c4;
            }
            QPushButton{
                background-color: #65a68f;
                color: white;
                border: none;
                border-radius: 0px;
                padding: 6px 10px;
            }
            QPushButton:hover{
                background-color: #467967; 
            }
            QPushButton#delete_button{
                background-color: #f44336;
            }
            QPushButton#delete_button:hover{
                background-color: #d32f2f;
            }
            QLabel{
                font-size: 16px;
                font-weight: bold;
                padding: 6px 10px;
            }
            QListView::item {
                border-bottom: 1px solid #eaeaea;  /* Lighter shade of gray separator */
                padding: 12px 0; /* Increase space between contacts */
                padding-left: 10px; /* Shift contacts to the right */
            }
            QListView::item:hover {
                background-color: #cde3ee; /* Light blue hover effect */
                color: black; /* Keep text white when hovering */
            }
            QListView::item:last {
                border-bottom: none;  /* No separator for the last item */
            }
        """
        self.setStyleSheet(style)

    # Populating contacts list
    def populate_contacts(self, contacts_func):
        contacts = contacts_func(contact_controller.cursor, contact_controller.collection)
        # Clearing the contacts list
        self.contacts_list.clear()

        # Adding contacts to the list widget
        for contact in contacts:
            name = f"{contact.get('nom', '')} {contact.get('prenom', '')}"
            item = QtWidgets.QListWidgetItem(name)
            item.setData(QtCore.Qt.UserRole, contact['contact_id'])  # Storing the contact ID in the item
            self.contacts_list.addItem(item)

    # Searching contacts
    def search_contacts(self, search_term):
        if search_term:
            results = contact_controller.search_contact(contact_controller.cursor, contact_controller.collection, search_term)
            self.populate_contacts(lambda cursor, collection: results)
        else:
            self.populate_contacts(contact_controller.get_all_contacts)

    # Showing add contact dialog
    def show_add_contact_dialog(self):
        dialog = AddContactDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            contact = dialog.add_contact()
            contact_controller.create_contact(contact_controller.cnx, contact_controller.cursor, contact_controller.collection, contact)
            self.populate_contacts(contact_controller.get_all_contacts)

    # Showing contact details dialog
    def show_contact_details_dialog(self, item):
        contact_id = item.data(QtCore.Qt.UserRole)
        dialog = ContactDetailsDialog(contact_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.populate_contacts(contact_controller.get_all_contacts)
