import streamlit as st

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

    # Header with profile summary
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png", width=250)
    with col2:
        st.title("User Profile 🏎️")
        st.write("Welcome back, Max Verstappen!")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🪪 Profile Info", "🎟️ F1 Passes", "📋 Support Tickets"])

    with tab1:
        st.header("Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Member Since:** 2024\n
            **Email:** max@f1racing.com \n
            **Phone:** +1 234 567 8900
            """)
        with col2:
            st.markdown("""
            **Favorite Circuit:** Spa-Francorchamps\n
            **Favorite Team:** Red Bull Racing\n
            **Preferred Seat:** Grandstand
            """)

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
        
        # Create a DataFrame for the passes table
        passes_data = {
            'Year': ['2024', '2024', '2024'],
            'Race': ['Yas Marina', 'Monaco GP', 'Silverstone'],
            'Cost ($)': [150, 200, 175],
            'No of Tickets': [10, 4, 2],
            'Total ($)': [1500, 800, 350]
        }
        
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
        
        st.dataframe(passes_data, hide_index=True, use_container_width=True)

    
    with tab3:
        st.header("Support Tickets")
        
        # Create sample ticket data with chat history
        tickets_data = {
            'Ticket ID': ['#F1-2024-001', '#F1-2024-002', '#F1-2024-003'],
            'Issue Summary': ['Seating Change Request', 'Parking Pass Issue', 'Ticket Transfer'],
            'Chat History': [
                '{"messages": [{"role": "user", "content": "Need to change my seat"}, {"role": "agent", "content": "We can help with that"}]}',
                '{"messages": [{"role": "user", "content": "Parking pass not received"}]}',
                '{"messages": [{"role": "user", "content": "Want to transfer my ticket"}]}'
            ],
            'Created': ['2024-02-01', '2024-02-15', '2024-02-20'],
            'Status': ['Resolved ✅', 'In Progress 🔄', 'Pending ⏳']
        }
        
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