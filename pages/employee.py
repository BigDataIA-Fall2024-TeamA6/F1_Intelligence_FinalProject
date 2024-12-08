import streamlit as st
import pandas as pd
import json

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
            color: white;
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Users", "Transactions", "Support Tickets"])

    # Sample users data
    with tab1:
        st.header("User Directory")
        users_data = {
            'Name': ['Max Verstappen', 'Lewis Hamilton', 'Charles Leclerc'],
            'Username': ['maxv33', 'lewish44', 'charleslec16'],
            'Favorite Team': ['Red Bull Racing', 'Mercedes AMG', 'Ferrari']
        }
        users_df = pd.DataFrame(users_data)
        st.dataframe(users_df, use_container_width=True)

    # Transactions data
    with tab2:
        st.header("Transaction History")
        passes_data = {
            'Year': ['2024', '2024', '2024'],
            'Race': ['Yas Marina', 'Monaco GP', 'Silverstone'],
            'Cost ($)': [150, 200, 175],
            'No of Tickets': [10, 4, 2],
            'Total ($)': [1500, 800, 350],
            'Username': ['maxv33', 'lewish44', 'charleslec16']
        }
        transactions_df = pd.DataFrame(passes_data)
        st.dataframe(transactions_df, use_container_width=True)

    # Support tickets data
    with tab3:
        with st.container():
            col1, col2 = st.columns([1, 2])

            with col2:
                st.header("Support Tickets")
                tickets_data = {
                    'Complaint ID': ['F1-2024-001', 'F1-2024-002', 'F1-2024-003'],
                    'Issue Summary': ['Refund for Miami GP', 'Seating Change Request', 'Parking Pass Issue'],
                    'Chat History': [
                        '{"messages": [{"role": "user", "content": "Need refund for 5 tickets $100 each"}, {"role": "agent", "content": "Processing your refund request"}]}',
                        '{"messages": [{"role": "user", "content": "Need to change my seat"}, {"role": "agent", "content": "We can help with that"}]}',
                        '{"messages": [{"role": "user", "content": "Parking pass not received"}]}'
                    ],
                    'Username': ['Jon', 'Vismay', 'MaxV33'],
                    'Status': ['Pending ⏳', 'Approved ✅', 'In Progress 🔄']
                }
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
                    format_func=lambda x: f"{tickets_df.iloc[x]['Complaint ID']} - {tickets_df.iloc[x]['Issue Summary']}"
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
                    complaint_id = st.text_input("Complaint ID", selected_row['Complaint ID'])
                    issue_summary = st.text_input("Issue Summary", selected_row['Issue Summary'])
                    username = st.text_input("Username", selected_row['Username'])
                    status = st.selectbox(
                        "Status",
                        ['Pending ⏳', 'Approved ✅', 'In Progress 🔄'],
                        index=['Pending ⏳', 'Approved ✅', 'In Progress 🔄'].index(selected_row['Status'])
                    )
                    
                    # Add save button for changes
                    if st.button("Save Changes"):
                        # Update the data in the DataFrame (or your database)
                        tickets_df.at[st.session_state.selected_index, 'Complaint ID'] = complaint_id
                        tickets_df.at[st.session_state.selected_index, 'Issue Summary'] = issue_summary
                        tickets_df.at[st.session_state.selected_index, 'Username'] = username
                        tickets_df.at[st.session_state.selected_index, 'Status'] = status

                        st.success("Changes saved successfully!")
                    
                    # Close the styled div
                    st.markdown('</div>', unsafe_allow_html=True)
                    
if __name__ == "__main__":
    main()