from PyQt5 import QtWidgets, QtCore, QtGui
import app.controllers.contact_controller as contact_controller

# Custom QLabel for round image display
class RoundImageLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(RoundImageLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignCenter)  # Align image to center
        self.setScaledContents(True)
        self.default_photo_path = "C:/Users/HP/Desktop/my_contact_manager/app/views/default_photo.jpg"
        self.load_default_photo()

    # Load default photo
    def load_default_photo(self):
        default_pixmap = QtGui.QPixmap(self.default_photo_path)
        if default_pixmap.isNull():
            print(f"Default photo not found: {self.default_photo_path}")
        else:
            print(f"Default photo found: {self.default_photo_path}")
            rounded = QtGui.QPixmap(default_pixmap.size())
            rounded.fill(QtCore.Qt.transparent)
            painter = QtGui.QPainter(rounded)
            path = QtGui.QPainterPath()
            path.addEllipse(0, 0, default_pixmap.width(), default_pixmap.height())
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, default_pixmap)
            painter.end()
            self.setPixmap(rounded)

# Dialog for displaying contact details
class ContactDetailsDialog(QtWidgets.QDialog):
    def __init__(self, contact_id):
        super(ContactDetailsDialog, self).__init__()
        self.contact_id = contact_id
        self.contact = contact_controller.get_contact_by_id(contact_controller.cursor, contact_controller.collection, self.contact_id)
        self.setWindowTitle(f"Contact Details: {self.contact.get('nom', '')} {self.contact.get('prenom', '')}")
        self.setWindowIcon(QtGui.QIcon("C:/Users/HP/Desktop/my_contact_manager/app/views/add-user.png"))

        # Widgets
        self.photo_label = RoundImageLabel()
        self.photo_label.setFixedSize(150, 150)  # Set the size of the round image label
        self.photo_label.setStyleSheet("border: 2px solid black; border-radius: 75px;")  # Round border

        # Load the photo if available, otherwise load the default photo
        photo_path = self.contact.get('photos', [])
        if photo_path:
            pixmap = QtGui.QPixmap(photo_path[0])
            if pixmap.isNull():
                print("Selected photo is null, loading default photo...")
                self.photo_label.load_default_photo()
            else:
                resized_pixmap = pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                rounded = QtGui.QPixmap(resized_pixmap.size())
                rounded.fill(QtCore.Qt.transparent)
                painter = QtGui.QPainter(rounded)
                path = QtGui.QPainterPath()
                path.addEllipse(0, 0, resized_pixmap.width(), resized_pixmap.height())
                painter.setClipPath(path)
                painter.drawPixmap(0, 0, resized_pixmap)
                painter.end()
                self.photo_label.setPixmap(rounded)

        self.nom_label = QtWidgets.QLabel("Family Name*")
        self.nom_text = QtWidgets.QLineEdit(self.contact.get('nom', ''))
        self.prenom_label = QtWidgets.QLabel("First Name*")
        self.prenom_text = QtWidgets.QLineEdit(self.contact.get('prenom', ''))
        self.adresse_email_label = QtWidgets.QLabel("Mail Adress")
        self.adresse_email_text = QtWidgets.QLineEdit(self.contact.get('adresse_email', ''))
        self.numero_telephone_label = QtWidgets.QLabel("Phone Number*")
        self.numero_telephone_text = QtWidgets.QLineEdit(self.contact.get('numero_telephone', ''))
        self.numero_telephone_maison_label = QtWidgets.QLabel("Home Phone Number")
        self.numero_telephone_maison_text = QtWidgets.QLineEdit(self.contact.get('numero_telephone_maison', ''))
        self.adresse_postale_label = QtWidgets.QLabel("Home Address")
        self.adresse_postale_text = QtWidgets.QLineEdit(self.contact.get('adresse_postale', ''))
        self.date_naissance_label = QtWidgets.QLabel("Birthday")
        self.date_naissance_text = QtWidgets.QLineEdit(str(self.contact.get('date_naissance', '')))
        self.notes_label = QtWidgets.QLabel("Notes")
        self.notes_text = QtWidgets.QTextEdit(self.contact.get('notes', ''))
        self.tags_label = QtWidgets.QLabel("Tags")
        self.tags_text = QtWidgets.QLineEdit(', '.join(self.contact.get('tags', '')))
        self.photos_label = QtWidgets.QLabel("Photos")
        self.photos_text = QtWidgets.QLineEdit(', '.join(self.contact.get('photos', '')))
        self.select_image_button = QtWidgets.QPushButton("Select Image")

        self.upcoming_events_label = QtWidgets.QLabel("Upcoming Events")
        self.upcoming_events_text = QtWidgets.QTextEdit('\n'.join([f"{event.get('date', '')}: {event.get('description', '')}" for event in self.contact.get('upcoming_events', [])]))

        # Buttons
        self.save_button = QtWidgets.QPushButton("Save")
        self.save_button.setIcon(QtGui.QIcon("save.png"))

        self.delete_button = QtWidgets.QPushButton("Delete")
        self.delete_button.setStyleSheet("QPushButton { background-color: #b30000; color: white; border: none; border-radius: 20px; padding: 6px 20px; } QPushButton:hover { background-color: #cd0000; }")
        self.delete_button.setIcon(QtGui.QIcon("delete.png"))

        # Layout
        layout = QtWidgets.QVBoxLayout()
        photo_layout = QtWidgets.QHBoxLayout()
        photo_layout.addWidget(QtWidgets.QWidget())  # Spacer
        photo_layout.addWidget(self.photo_label)
        photo_layout.addWidget(QtWidgets.QWidget())  # Spacer
        layout.addLayout(photo_layout)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow(self.nom_label, self.nom_text)
        form_layout.addRow(self.prenom_label, self.prenom_text)
        form_layout.addRow(self.adresse_email_label, self.adresse_email_text)
        form_layout.addRow(self.numero_telephone_label, self.numero_telephone_text)
        form_layout.addRow(self.numero_telephone_maison_label, self.numero_telephone_maison_text)
        form_layout.addRow(self.adresse_postale_label, self.adresse_postale_text)
        form_layout.addRow(self.date_naissance_label, self.date_naissance_text)
        form_layout.addRow(self.notes_label, self.notes_text)
        form_layout.addRow(self.tags_label, self.tags_text)
        form_layout.addRow(self.photos_label, self.photos_text)
        form_layout.addRow(self.select_image_button)
        layout.addLayout(form_layout)

        layout.addWidget(self.upcoming_events_label)
        layout.addWidget(self.upcoming_events_text)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect signals
        self.save_button.clicked.connect(self.save_contact)
        self.delete_button.clicked.connect(self.delete_contact)
        self.select_image_button.clicked.connect(self.select_image)

    # Saving contact
    def save_contact(self):
        contact = {
            'nom': self.nom_text.text(),
            'prenom': self.prenom_text.text(),
            'adresse_email': self.adresse_email_text.text(),
            'numero_telephone': self.numero_telephone_text.text(),
            'numero_telephone_maison': self.numero_telephone_maison_text.text(),
            'adresse_postale': self.adresse_postale_text.text(),
            'date_naissance': self.date_naissance_text.text(),
            'notes': self.notes_text.toPlainText(),
            'tags': self.tags_text.text().split(','),
            'photos': self.photos_text.text().split(','),
            'upcoming_events': [{'date': event.split(':')[0].strip(), 'description': event.split(':')[1].strip()} for event in self.upcoming_events_text.toPlainText().split('\n') if event.strip()]
        }
        contact_controller.update_contact(contact_controller.cnx, contact_controller.cursor, contact_controller.collection, self.contact_id, contact)
        QtWidgets.QMessageBox.information(self, "Success", "Contact updated successfully.")

    # Deleting contact
    def delete_contact(self):
        reply = QtWidgets.QMessageBox.question(self, 'Delete Contact', 'Are you sure you want to delete this contact?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            contact_controller.delete_contact(contact_controller.cnx, contact_controller.cursor, contact_controller.collection, self.contact_id)
            self.accept()

    # Selecting image
    def select_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.photos_text.setText(','.join(selected_files))
            # Load the selected image
            if selected_files:
                pixmap = QtGui.QPixmap(selected_files[0])
                if pixmap.isNull():
                    print("Selected photo is null, loading default photo...")
                    self.photo_label.load_default_photo()
                else:
                    resized_pixmap = pixmap.scaled(150, 150, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                    self.photo_label.setPixmap(resized_pixmap)
