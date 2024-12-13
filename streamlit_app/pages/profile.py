import streamlit as st
import mysql.connector
import pandas as pd

def get_user_info(username):
    try:
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, fname, lname, username, user_type, favorite_team, created_at
            FROM login
            WHERE username = %s
        """, (username,))
        user_info = cursor.fetchone()
        cursor.close()
        cnx.close()
        return user_info
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_ticket_info(username):
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
            WHERE username = %s
        """, (username,))
        
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

def get_helpdesk_tickets(username):
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
            WHERE username = %s
        """, (username,))
        
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

def user_profile_page():
    st.markdown(
        """
        <style>
        .stButton>button {
            width: 30%;
            background-color: #FF1E00;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 10px;
        }

        /* Tab styling */
        [data-testid="stHorizontalBlock"] {
            padding: 10px;
            border-radius: 5px;
        }

        /* Style for tab container */
        .stTabs {
            border-bottom: 2px solid #D91E18;
        }

        /* Style for individual tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border: 1px solid #333;
            border-radius: 4px 4px 0 0;
            padding: 8px 16px;
            background-color: #D91E18;
            color: white;
        }

        /* Active tab styling */
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            border-bottom: 2px solid #D91E18;
            background-color: #000000;
        }

        /* Hover effect for tabs */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #ffffff;
            color: #D91E18;
            border-color: #D91E18;
        }

        /* Tab content panel */
        .stTabs [data-baseweb="tab-panel"] {
            padding: 15px;
            border: 1px solid #333;
            border-top: none;
            background-color: #000000;
        }

        /* Custom button styling */
        .stButton > button {
            width: 100%;  /* Makes button fill the column width */
            padding: 10px 15px;
            border-radius: 5px;
        }

        /* Style for AI Assistant and Chat Support buttons */
        [data-testid="stHorizontalBlock"] > div:nth-child(4) button,
        [data-testid="stHorizontalBlock"] > div:nth-child(5) button {
            background-color: #D91E18;
            color: white;
        }

        /* Hover effect for red buttons */
        [data-testid="stHorizontalBlock"] > div:nth-child(4) button:hover,
        [data-testid="stHorizontalBlock"] > div:nth-child(5) button:hover {
            background-color: #F12A21;
            color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    user_info = get_user_info(st.session_state.username)

    # Header with profile summary
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png", width=250)
    with col2:
        st.title("User Profile 🏎️")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🪪 Profile Info", "🎟️ F1 Passes", "📋 Support Tickets"])

    if user_info:
        with tab1:
            st.header("Personal Information")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Member Since:** {user_info['created_at'].strftime('%Y-%m-%d')}\n
                **Email:** {user_info['username']}\n
                **Name:** {user_info['fname']} {user_info['lname']}
                """)
            with col2:
                st.markdown(f"""
                **Favorite Team:** {user_info['favorite_team']}\n
                **User Type:** {user_info['user_type']}\n
                **User ID:** {user_info['id']}
                """)
    else:
        st.error("Failed to retrieve user information.")

    co1, co2 = st.columns([1,1])
    with co1:
        if st.button("Home", use_container_width=True):
            st.switch_page("pages/user_landing.py")   

    with co2:
        if st.button("Logout"):
            # Clear session state
            st.session_state.messages = []
            # Add confirmation message
            st.warning('Successfully logged out')
            # Rerun the app to reset the state
            st.switch_page("pages/login.py")

    with tab2:
        st.header("My F1 Passes")
        username = st.session_state.get("username")
        # Create a DataFrame for the passes table
        passes_data = fetch_ticket_info(username)

        if passes_data:
            df_transactions = pd.DataFrame(passes_data)

        
        # Display table with styling
        st.markdown("### Passes Summary")
        st.markdown("""
            <style>
            .dataframe {
                background-color: #2B2B2B;
                color: white;
                font-size: 14px;
            }
            .dataframe th {
                background-color: #FF1E00;
                color: white;
                text-align: center !important;
            }
            .dataframe td {
                text-align: center !important;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(df_transactions, hide_index=True, use_container_width=True)

    
    with tab3:
        st.header("Support Tickets")
        
        # Create sample ticket data with chat history
        tickets_data = tickets_data = get_helpdesk_tickets(username)
        
        # Display table with styling
        st.markdown("### Tickets Summary")
        st.markdown("""
            <style>
            .dataframe {
                background-color: #2B2B2B;
                color: white;
                font-size: 14px;
            }
            .dataframe th {
                background-color: #FF1E00;
                color: white;
                text-align: center !important;
                padding: 10px;
            }
            .dataframe td {
                text-align: center !important;
                padding: 8px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(tickets_data, hide_index=True, use_container_width=True)

if __name__ == "__main__":
    st.set_page_config(
        page_title="F1 Driver Profile",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="collapsed" 
    )
    user_profile_page()