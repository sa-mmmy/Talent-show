from PyQt5 import QtCore , QtGui , QtWidgets 
import sys 
import mysql.connector
from pymongo import MongoClient
from datetime import datetime

app=QtWidgets.QApplication(sys.argv)
w=QtWidgets.QWidget()
w.resize(400,400)
#w.move()
#w.SetGeometry(w,h,l,t) 
w.setWindowTitle('TALENT SHOW')
w.setStyleSheet('background-color:pink ;')
w.setWindowIcon(QtGui.QIcon('pics/MicIcon.png'))

intro=QtWidgets.QLabel('ALGERIA\'S ANNUAL TALENT SHOW 2024', w )
intro.setStyleSheet('font-family: Inter ;font-size:40px ;')
intro.move(550,75)

text =QtWidgets.QLabel('✨ Your Time to Shine! ✨',w)
text.setStyleSheet('font-family: Inter ;font-size:40px ;')
text.move(680,150)

text1=QtWidgets.QLabel(' Got talent? We want YOU! Step into the spotlight and show off your skills in our upcoming talent show. Sing, dance, perform magic—whatever your talent, the stage is yours. Don\'t miss this chance to dazzle and ',w)
text1.setStyleSheet('font-family: Inter ;font-size:20px ;')
text1.move(10,250)

text2=QtWidgets.QLabel('inspire.Join us and let your brilliance light up the room! 🌟🎶🌟',w) 
text2.setStyleSheet('font-family: Inter ;font-size:20px ;')
text2.move(600,280)



# Function to handle form submission
def submit_form():
    # Extract data from form fields
    username = username_edit.text()
    email = email_edit.text()
    birthdate = birthdate_edit.date().toString("yyyy-MM-dd")
    attachment_path = attachment_edit.text()

    # Store data in MySQL
    user_id = store_in_mysql(username, email, birthdate)

    # Store video attachment in MongoDB
    store_in_mongodb(user_id, attachment_path)

     # Clear form fields
    username_edit.clear()
    email_edit.clear()
    birthdate_edit.setDate(QtCore.QDate.currentDate())
    attachment_edit.clear()

    # Display success message
    QtWidgets.QMessageBox.information(w, "Success", "Form submitted successfully!")

# Function to store data in MySQL
def store_in_mysql(username, email, birthdate):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bdddProject"
    )

    mycursor = mydb.cursor()

    # Create a table if not exists
    mycursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), birthdate DATE)")

    # Insert data into the table
    sql = "INSERT INTO users (username, email, birthdate) VALUES (%s, %s, %s)"
    val = (username, email, birthdate)
    mycursor.execute(sql, val)

    mydb.commit()
    return mycursor.lastrowid

# Function to store data in MongoDB
def store_in_mongodb(user_id, attachment_path):
    # Connect to MongoDB (replace "localhost" and "27017" with your MongoDB host and port)
    client = MongoClient("localhost", 27017)

    # Select database
    db = client["talent_show"]

    # Create a new collection
    videos_collection = db["videos"]

    # Read video file and convert it to binary
    with open(attachment_path, "rb") as f:
        video_binary = f.read()

    # Insert video data into MongoDB
    video_data = {
        "user_id": user_id,
        "upload_date": datetime.now(),
        "video": video_binary
    }
    videos_collection.insert_one(video_data)


# Function to browse and select file
def browse_attachment():
    file_dialog = QtWidgets.QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(w, "Select Video File", "", "Video Files (*.mp4 *.avi)")
    attachment_edit.setText(file_path)


# Create form widgets
form_container = QtWidgets.QGroupBox("Talent Show Form", w)
form_container.setGeometry(550, 420, 700, 300)
form_container.setStyleSheet("QGroupBox { border: 2px solid gray; border-radius: 5px; margin-left: 10px; margin-right: 10px; }")

layout = QtWidgets.QVBoxLayout(form_container)

username_label = QtWidgets.QLabel('Username:')
layout.addWidget(username_label)
username_edit = QtWidgets.QLineEdit()
layout.addWidget(username_edit)

email_label = QtWidgets.QLabel('Email:')
layout.addWidget(email_label)
email_edit = QtWidgets.QLineEdit()
layout.addWidget(email_edit)

birthdate_label = QtWidgets.QLabel('Birthdate:')
layout.addWidget(birthdate_label)
birthdate_edit = QtWidgets.QDateEdit()
layout.addWidget(birthdate_edit)

attachment_label = QtWidgets.QLabel('Video Attachment:')
layout.addWidget(attachment_label)
attachment_edit = QtWidgets.QLineEdit()
layout.addWidget(attachment_edit)
attachment_button = QtWidgets.QPushButton('Browse')
layout.addWidget(attachment_button)
attachment_button.clicked.connect(browse_attachment)


submit_button = QtWidgets.QPushButton('Submit', w)
submit_button.setGeometry(850, 800, 100, 30)
submit_button.clicked.connect(submit_form)
submit_button.setStyleSheet('background-color:yellow;')




w.show()
app.exec_()
