import sys
from PyQt5 import QtWidgets
from app.views.list_contacts_view import MainPage
from app.views.add_contact_view import AddContactDialog
from app.views.contact_details_view import ContactDetailsDialog

if __name__ == "__main__":
    # Creating a QApplication instance
    app = QtWidgets.QApplication([])

    # Creating the main page widget for my application
    main_page = MainPage()

    # Displaying the main page widget
    main_page.show()

    # Starting the application event loop
    sys.exit(app.exec_())
