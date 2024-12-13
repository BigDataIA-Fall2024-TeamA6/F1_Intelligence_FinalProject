import streamlit as st
import pandas as pd
import mysql

def fetch_login_data():
    try:
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                id, 
                fname, 
                lname, 
                username, 
                password, 
                user_type, 
                favorite_team, 
                created_at
            FROM login
        """)

        # Fetch all results
        results = cursor.fetchall()

        # Transform results into a dictionary for a DataFrame
        login_data = {
            "id": [],
            "fname": [],
            "lname": [],
            "username": [],
            "password": [],
            "user_type": [],
            "favorite_team": [],
            "created_at": []
        }

        for row in results:
            login_data["id"].append(row['id'])
            login_data["fname"].append(row['fname'])
            login_data["lname"].append(row['lname'])
            login_data["username"].append(row['username'])
            login_data["password"].append(row['password'])
            login_data["user_type"].append(row['user_type'])
            login_data["favorite_team"].append(row['favorite_team'] if row['favorite_team'] is not None else "")
            login_data["created_at"].append(row['created_at'])

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        return login_data
        
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None
        

import mysql.connector
import streamlit as st

def fetch_ticket_info():
    try:
        # Connect to the database
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        
        # Create a cursor to execute the query
        cursor = cnx.cursor(dictionary=True)

        # Execute query to fetch ticket info
        cursor.execute("""
            SELECT 
                ticket_id, username, Country, Venue, TicketDate1, TicketDate2, TicketDate3, TicketCount, TicketPrice
            FROM ticket_info
        """)
        
        # Fetch all results
        results = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # If no results found, show message
        if not results:
            st.write("No ticket information found.")
            return None

        # Return the ticket info
        return results
        
    except Exception as e:
        st.error(f"Database operation failed: {e}")
        return None

def get_helpdesk_tickets():
    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        
        # Create cursor and execute the query to fetch helpdesk tickets
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                hdticket_id,
                hdticket_summary,
                chat_history,
                username,
                hdticket_status
            FROM helpdesk_tickets
        """)
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Transform results into a dictionary for each ticket
        helpdesk_tickets = []
        
        for row in results:
            ticket = {
                "hdticket_id": row['hdticket_id'],
                "hdticket_summary": row['hdticket_summary'],
                "chat_history": row['chat_history'],  # This is a JSON string
                "username": row['username'],
                "hdticket_status": row['hdticket_status']
            }
            helpdesk_tickets.append(ticket)
        
        # Close the cursor and connection
        cursor.close()
        cnx.close()
        
        return helpdesk_tickets
    
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def update_ticket_status(ticket_id, status):
    try:
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        cursor = cnx.cursor()

        # SQL query to update the ticket status
        update_query = """
            UPDATE helpdesk_tickets
            SET hdticket_status = %s
            WHERE hdticket_id = %s
        """
        cursor.execute(update_query, (status, ticket_id))

        # Commit the transaction
        cnx.commit()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

    except Exception as e:
        st.error(f"Failed to update ticket status: {e}")

def main():
    st.set_page_config(page_title="F1 Employee Dashboard", initial_sidebar_state="collapsed", layout="wide" )
    co1, co2 = st.columns([6,1])
    with co1:
        st.title("F1 Employee Dashboard")
    with co2:
        if st.button("Logout"):
            # Clear session state
            st.session_state.messages = []
            # Add confirmation message
            st.warning('Successfully logged out')
            # Rerun the app to reset the state
            st.switch_page("pages/login.py")

    # Custom CSS for F1 theme
    st.markdown("""
        <style>
        
        .stTabs {
            background-color: #oooooo;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 0;
            background-color: transparent;
        }
        
        [data-testid="stTextInput"] > div > div > input {
            background-color: #f0f0f0;  /* Light gray background */
            color: black;  /* Black text */
        }
                
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.1);
            border: none;
            color: white;
            padding: 16px 32px;
            font-weight: 500;
            font-size: 16px;
            border-radius: 8px 8px 0 0;
            margin-right: 4px;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .stTabs [data-baseweb="tab-panel"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 0 8px 8px 8px;
            padding: 20px;
            color: white;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(255, 255, 255, 0.3);
            color: red;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Users", "Transactions", "Support Tickets"])

    # Sample users data
    with tab1:
        st.header("User Directory")

        users_data = fetch_login_data()
        users_df = pd.DataFrame(users_data)
        users_df.rename(
                    columns={
                        "Grand Prix": "Race",
                        "Venue": "Race Track",
                        "Dates": "Race Dates"
                    },
                    inplace=True
                )

        st.dataframe(users_df, use_container_width=True)

    # Transactions data
    with tab2:
        st.header("Transaction History")

        transactions_data = fetch_ticket_info()

        if transactions_data:
            df_transactions = pd.DataFrame(transactions_data)

            st.table(df_transactions)

    # Support tickets data
    with tab3:
        with st.container():
            col1, col2 = st.columns([1, 2])

            with col2:
                st.header("Support Tickets")

                tickets_data = get_helpdesk_tickets()

                if tickets_data:
                    tickets_df = pd.DataFrame(tickets_data)

                    

                # Add selection column
                if 'selected_index' not in st.session_state:
                    st.session_state.selected_index = None

                # Display the table
                st.dataframe(tickets_df, use_container_width=True)

                # Dropdown to select a row (alternative to checkboxes)
                selected_row_index = st.selectbox(
                    "Select a ticket to update:",
                    options=list(range(len(tickets_df))),
                    format_func=lambda x: f"{tickets_df.iloc[x]['hdticket_id']} - {tickets_df.iloc[x]['hdticket_summary']}"
                )

                # Update button
                if st.button("Update Selected Ticket"):
                    st.session_state.selected_index = selected_row_index

            with col1:
                st.markdown("""
                    <style>
                    .ticket-details {
                        background-color: #000000; /* Light blue-gray background */
                        padding: 20px;
                        border-radius: 10px;
                        margin-top: 20px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional shadow */
                    }
                    </style>
                    <div class="ticket-details">
                    """, unsafe_allow_html=True)

                # Show selected ticket details
                if st.session_state.selected_index is not None:
                    selected_row = tickets_df.iloc[st.session_state.selected_index]

                    st.subheader("Ticket Details")

                    # Wrap inputs inside the styled div
                    st.markdown('<div>', unsafe_allow_html=True)
                    
                    # Create text input fields for editing
                    complaint_id = st.text_input("Complaint ID", selected_row['hdticket_id'])
                    issue_summary = st.text_input("Issue Summary", selected_row['hdticket_summary'])
                    username = st.text_input("Username", selected_row['username'])
                    status = st.selectbox(
                        "Status",
                        ['Pending', 'Approved'],
                        index=['Pending', 'Approved'].index(selected_row['hdticket_status'])
                    )

                    
                    # Add save button for changes
                    if st.button("Save Changes"):
                        # Update the DataFrame
                        tickets_df.at[st.session_state.selected_index, 'hdticket_id'] = complaint_id
                        tickets_df.at[st.session_state.selected_index, 'hdticket_summary'] = issue_summary
                        tickets_df.at[st.session_state.selected_index, 'username'] = username
                        tickets_df.at[st.session_state.selected_index, 'hdticket_status'] = status

                        # Save changes to the database
                        update_ticket_status(complaint_id, status)

                        st.success("Changes saved successfully!")

                    st.markdown('</div>', unsafe_allow_html=True)
                    
if __name__ == "__main__":
    main()