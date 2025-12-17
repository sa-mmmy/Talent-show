import mysql.connector

def create_database():
    try:
        # Connect to MySQL server
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )

        # Create a cursor object
        mycursor = mydb.cursor()

        # Execute SQL statement to create the database
        mycursor.execute("CREATE DATABASE bdddProject")

        print("Database created successfully")

    except mysql.connector.Error as e:
        print("Error:", e)

# Call the function to create the database
create_database()