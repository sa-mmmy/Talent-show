from PyQt5 import QtWidgets, QtGui
import mysql.connector
from pymongo import MongoClient
import sys
import Participants  # Import the last_try module

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Admin Login')
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet('background-color:pink;')
        self.setWindowIcon(QtGui.QIcon('pics/human-icon.webp'))

        # Create UI elements (username and password fields, login button, etc.)
        self.username_edit = QtWidgets.QLineEdit()
        self.password_edit = QtWidgets.QLineEdit()
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_button = QtWidgets.QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(QtWidgets.QLabel('Username:'))
        layout.addWidget(self.username_edit)
        layout.addWidget(QtWidgets.QLabel('Password:'))
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        # Dummy authentication logic (replace with your actual authentication mechanism)
        if username == 'admin' and password == 'password':
            # Retrieve data from MySQL and MongoDB
            users_data = retrieve_users_data()

            # Create and show the admin window
            self.admin_window = Participants.AdminWindow(users_data)
            self.admin_window.setWindowIcon(QtGui.QIcon('pics/MicIcon.png'))
            self.admin_window.show()

            self.close()  # Close the login window
        else:
            QtWidgets.QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')

def retrieve_users_data():
    try:
        # Connect to MySQL
        mysql_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="bdddproject"
        )

        # Query data from MySQL
        mysql_cursor = mysql_connection.cursor(dictionary=True)
        mysql_cursor.execute("SELECT * FROM users")
        mysql_records = mysql_cursor.fetchall()

        # Connect to MongoDB
        mongo_client = MongoClient("mongodb://localhost:27017/")
        mongo_db = mongo_client["talent_show"]
        mongo_collection = mongo_db["videos"]

        # Retrieve data from MongoDB and combine with MySQL data
        users_data = []
        for mysql_record in mysql_records:
            # Find corresponding MongoDB record based on id_user (mapped to user_id)
            mongo_record = mongo_collection.find_one({"user_id": mysql_record['id']})

            if mongo_record:
                # Combine data from MySQL and MongoDB
                user_data = {
                    'id': mysql_record['id'],
                    'username': mysql_record['username'],
                    'email': mysql_record['email'],
                    'birthdate': mysql_record['birthdate'],
                    'video': mongo_record.get('video', 'Not available')
                }
                users_data.append(user_data)

        return users_data

    except Exception as e:
        print("Error:", e)
        return []

# Create a QApplication instance
app = QtWidgets.QApplication([])

# Create login window and show it
login_window = LoginWindow()
login_window.show()

# Start the application event loop
sys.exit(app.exec_())