import mysql.connector
from pymongo import MongoClient
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimediaWidgets, QtMultimedia
import sys

class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, users_data):
        super().__init__()
        self.setWindowTitle('Admin Window')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('color:black') 

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        for user_data in users_data:
            user_box = self.create_user_box(user_data)
            layout.addWidget(user_box)

    def create_user_box(self, user_data):
        # Create widgets for user data
        username_label = QtWidgets.QLabel('Username: ' + user_data['username'])
        email_label = QtWidgets.QLabel('Email: ' + user_data['email'])
        birthdate_label = QtWidgets.QLabel('Birthdate: ' + user_data['birthdate'].strftime('%Y-%m-%d'))

        # Create video player widget
        video_widget = QtMultimediaWidgets.QVideoWidget()
        player = QtMultimedia.QMediaPlayer()

        # Check if user_data['video'] is a bytes object
        if isinstance(user_data['video'], bytes):
            # Write the bytes to a temporary file
            temp_file = QtCore.QTemporaryFile()
            temp_file.open()
            temp_file.write(user_data['video'])
            temp_file.flush()

            # Get the file path of the temporary file
            file_path = temp_file.fileName()
            temp_file.close()

            # Set media content from the temporary file
            player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(file_path)))
        else:
            # Set media content from the file path
            player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(user_data['video'])))

        player.setVideoOutput(video_widget)
        player.play()

        # Set layout for user box
        user_box = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(user_box)
        layout.addWidget(username_label)
        layout.addWidget(email_label)
        layout.addWidget(birthdate_label)
        layout.addWidget(video_widget)
        layout.addStretch()

        # Set style for user box
        user_box.setStyleSheet("border: 1px solid black; padding: 10px;")

        return user_box

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

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Retrieve data from MySQL and MongoDB
    users_data = retrieve_users_data()

    # Create and show the admin window
    admin_window = AdminWindow(users_data)
    admin_window.setWindowIcon(QtGui.QIcon('pics/MicIcon.png'))
    admin_window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()