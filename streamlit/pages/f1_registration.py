import streamlit as st
import mysql.connector
import bcrypt
import re

# Move set_page_config to the top of the script
st.set_page_config(page_title="F1 User Registration", page_icon="🏎️")

# Connect to the AWS RDS MySQL instance
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com',  
            user='admin',  
            password='amazonrds7245',  
            database='bdia_team6_finalproject_db' 
        )
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error connecting to MySQL Database: {e}")
        return None

# Function to validate email
def is_valid_email(email):
    # Basic email validation regex
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

# Function to check if username already exists
def username_exists(username):
    connection = create_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM login WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result is not None
    except mysql.connector.Error as e:
        st.error(f"Error checking username: {e}")
        return False

# Function to create a new user
def create_new_user(first_name, last_name, username, password, favorite_team):
    connection = create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # User type is set to "user"
        user_type = "user"

        # Insert new user into the 'login' table
        query = """
        INSERT INTO login (fname, lname, username, password, user_type, favorite_team)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            first_name, 
            last_name, 
            username, 
            hashed_password.decode('utf-8'), 
            user_type, 
            favorite_team
        ))
        
        # Commit the transaction and close the connection
        connection.commit()
        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as e:
        st.error(f"Database error: {e}")
        return False

# Function for the create new user page
def create_account_page():
    st.title("🏁 Create New F1 User Account")

    # F1 Teams List
    f1_teams = [
        "Red Bull Racing",
        "Ferrari",
        "Mercedes",
        "McLaren",
        "Alpine",
        "Aston Martin",
        "Alfa Romeo",
        "Haas F1 Team",
        "AlphaTauri",
        "Williams"
    ]

    # Input fields for account creation
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Email", placeholder="example@mail.com")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    favorite_team = st.selectbox("Choose Your Favorite F1 Team", f1_teams)

    col1, col2 = st.columns(2)

    with col1:
        # Submit button
        submit_button = st.button("Create Account")
        
        if submit_button:
            # Validation checks
            if not (first_name and last_name and username and password and confirm_password):
                st.error("All fields are required!")
            elif not is_valid_email(username):
                st.error("Please enter a valid email address!")
            elif username_exists(username):
                st.error("Username (email) already exists!")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long!")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            else:
                try:
                    # Attempt to create user
                    if create_new_user(first_name, last_name, username, password, favorite_team):
                        st.success(f"Account created for {first_name} {last_name} ({username}) as a User!")
                        st.balloons()
                    else:
                        st.error("Failed to create account. Please try again.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
    
    with col2:
        if st.button("Back to Login"):
            # Note: This assumes you have a login.py page in a 'pages' directory
            st.switch_page("pages/login.py")

# Run the account creation page
if __name__ == "__main__":
    create_account_page()