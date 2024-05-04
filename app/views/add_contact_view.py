from PyQt5 import QtWidgets, QtGui, QtCore

# Dialog for adding a new contact
class AddContactDialog(QtWidgets.QDialog):
    def __init__(self):
        super(AddContactDialog, self).__init__()

        # Setting window properties
        self.setWindowTitle("Add Contact")
        self.setWindowIcon(QtGui.QIcon("C:/Users/HP/Desktop/my_contact_manager/app/views/plus.png"))

        # Widgets for adding contact details
        self.nom_label = QtWidgets.QLabel("Family Name*")
        self.nom_lineedit = QtWidgets.QLineEdit()
        self.prenom_label = QtWidgets.QLabel("First Name*")
        self.prenom_lineedit = QtWidgets.QLineEdit()
        self.adresse_email_label = QtWidgets.QLabel("Mail Address")
        self.adresse_email_lineedit = QtWidgets.QLineEdit()
        self.numero_telephone_label = QtWidgets.QLabel("Phone Number*")
        self.numero_telephone_lineedit = QtWidgets.QLineEdit()
        self.numero_telephone_maison_label = QtWidgets.QLabel("Home Phone Number")
        self.numero_telephone_maison_lineedit = QtWidgets.QLineEdit()
        self.adresse_postale_label = QtWidgets.QLabel("Home Address")
        self.adresse_postale_lineedit = QtWidgets.QLineEdit()
        self.date_naissance_label = QtWidgets.QLabel("Birthday")
        self.date_naissance_calendar = QtWidgets.QCalendarWidget()
        self.notes_label = QtWidgets.QLabel("Notes")
        self.notes_textedit = QtWidgets.QTextEdit()
        self.tags_label = QtWidgets.QLabel("Tags")
        self.tags_lineedit = QtWidgets.QLineEdit()
        self.photos_label = QtWidgets.QLabel("Photos")
        self.photos_lineedit = QtWidgets.QLineEdit()
        self.select_image_button = QtWidgets.QPushButton(QtGui.QIcon("icons/image.png"), "Select Image")
        self.upcoming_events_label = QtWidgets.QLabel("Upcoming Events")
        self.upcoming_events_dateedit = QtWidgets.QDateEdit()
        self.upcoming_events_description_lineedit = QtWidgets.QLineEdit()
        self.add_event_button = QtWidgets.QPushButton(QtGui.QIcon("icons/add.png"), "Add Event")
        self.upcoming_events_listwidget = QtWidgets.QListWidget()

        # Buttons
        self.add_button = QtWidgets.QPushButton(QtGui.QIcon("icons/add.png"), "Add")
        self.cancel_button = QtWidgets.QPushButton(QtGui.QIcon("icons/cancel.png"), "Cancel")

        # Layout
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.nom_label, self.nom_lineedit)
        layout.addRow(self.prenom_label, self.prenom_lineedit)
        layout.addRow(self.adresse_email_label, self.adresse_email_lineedit)
        layout.addRow(self.numero_telephone_label, self.numero_telephone_lineedit)
        layout.addRow(self.numero_telephone_maison_label, self.numero_telephone_maison_lineedit)
        layout.addRow(self.adresse_postale_label, self.adresse_postale_lineedit)
        layout.addRow(self.date_naissance_label, self.date_naissance_calendar)
        layout.addRow(self.notes_label, self.notes_textedit)
        layout.addRow(self.tags_label, self.tags_lineedit)
        layout.addRow(self.photos_label, self.photos_lineedit)
        layout.addRow(self.select_image_button)
        layout.addRow(self.upcoming_events_label, self.upcoming_events_listwidget)
        layout.addRow(self.upcoming_events_dateedit, self.upcoming_events_description_lineedit)
        layout.addRow(self.add_event_button)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)

        self.setLayout(layout)

        # Connect signals
        self.add_button.clicked.connect(self.add_contact)
        self.cancel_button.clicked.connect(self.reject)
        self.select_image_button.clicked.connect(self.select_image)
        self.add_event_button.clicked.connect(self.add_event)

        self.upcoming_events_listwidget.itemClicked.connect(self.remove_event)

        # Apply style
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
                border-radius: 40px;
                padding: 6px 10px;
            }
            QPushButton:hover{
                background-color: #467967;
            }
            QPushButton#cancel_button{
                background-color: #f44336;
            }
            QPushButton#cancel_button:hover{
                background-color: #d32f2f;
            }
        """
        self.setStyleSheet(style)

    # Adding contact
    def add_contact(self):
        if not self.validate_input():
            return

        contact = {
            'nom': self.nom_lineedit.text(),
            'prenom': self.prenom_lineedit.text(),
            'adresse_email': self.adresse_email_lineedit.text(),
            'numero_telephone': self.numero_telephone_lineedit.text(),
            'numero_telephone_maison': self.numero_telephone_maison_lineedit.text(),
            'adresse_postale': self.adresse_postale_lineedit.text(),
            'date_naissance': self.date_naissance_calendar.selectedDate().toString(QtCore.Qt.ISODate),
            'notes': self.notes_textedit.toPlainText(),
            'tags': self.tags_lineedit.text().split(','),
            'photos': self.photos_lineedit.text().split(','),
            'upcoming_events': [{'date': self.upcoming_events_listwidget.item(i).data(QtCore.Qt.UserRole), 'description': self.upcoming_events_listwidget.item(i).text()} for i in range(self.upcoming_events_listwidget.count())]
        }
        self.accept()
        return contact

    # Validating input
    def validate_input(self):
        # Required fields
        if not self.nom_lineedit.text() or not self.numero_telephone_lineedit.text():
            QtWidgets.QMessageBox.critical(self, "Error", "Family Name, First Name and Phone Number are obligatory.")
            return False

        # Validate phone number
        phone_number = self.numero_telephone_lineedit.text()
        if not (phone_number.startswith('05') or phone_number.startswith('06') or phone_number.startswith('07')) or len(phone_number) != 10:
            QtWidgets.QMessageBox.critical(self, "Error", "The phone number must start with 05, 06 or 07 and must contain 10 digits.")
            return False

        return True

    # Selecting image
    def select_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.photos_lineedit.setText(','.join(selected_files))

    # Adding event
    def add_event(self):
        date = self.upcoming_events_dateedit.date().toString(QtCore.Qt.ISODate)
        description = self.upcoming_events_description_lineedit.text()
        if date and description:
            event = QtWidgets.QListWidgetItem(f"{date}: {description}")
            event.setData(QtCore.Qt.UserRole, date)
            self.upcoming_events_listwidget.addItem(event)

    # Removing event
    def remove_event(self, item):
        self.upcoming_events_listwidget.takeItem(self.upcoming_events_listwidget.row(item))
