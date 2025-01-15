import sqlite3
import hashlib

#db setup
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

#create table if it doesnt exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    username TEXT NOT NULL UNIQUE,
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")
connection.commit()


def generate_username_and_id(limit=12):
    input_username = input("Enter wanted username: ").strip()
    
    if len(input_username) <= limit:
        #create user_id
        user_id = str(hash(input_username))[:8]  #first 8 digits of hash
        return input_username, user_id
    else:
        print("Username too long or invalid")
        return None, None


def generate_password(limit=12):
    password = input("Enter your password: ").strip()
    
    #very basic len check
    if len(password) <= limit:
        #hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password
    else:
        print("Password too long or invalid")
        return None


def store_user_in_db(username, user_id, hashed_password):
    #update db with values
    try:
        cursor.execute("INSERT INTO Users (username, user_id, password) VALUES (?, ?, ?)",
                       (username, user_id, hashed_password))
        connection.commit()
        print("User stored successfully!")
    except sqlite3.IntegrityError as e:
        print(f"Error storing user: {e}")


#main function
def main():
    username, user_id = generate_username_and_id()
    if username and user_id:
        hashed_password = generate_password()
        if hashed_password:
            store_user_in_db(username, user_id, hashed_password)
        else:
            print("Failed to generate password.")
    else:
        print("Failed to generate username and ID.")


if __name__ == "__main__":
    main()