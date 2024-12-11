import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(
    page_title="F1 Lap Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and proper styling
st.markdown("""
    <style>
    /* Dark theme */
    .main {
        color: white;
    }
    
    /* Header styling */
    .title {
        color: white;
        padding: 1rem 0;
    }
    
    /* Dropdown styling */
    .stSelectbox > div > div {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #9146FF;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #FF1801;
        color: white;
        border: none;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #D10000;
        color: #000000
    }
    
    /* Container styling */
    .visualization-container {
        border: 1px solid #FF1801;
        border-radius: 10px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Create two columns with proper ratio
col1, col2 = st.columns([1, 3])

with col1:
    
    col_home, col_spacer= st.columns([1, 2])
    with col_home:
        if st.button(" Home "):
            st.switch_page("pages/user_landing.py")

    st.markdown("## Lap by Lap Analysis")
    st.markdown("Select Grand Prix to analyse: ")

    # Year dropdown
    years = list(range(2024, 2020, -1))
    selected_year = st.selectbox("Select Year", years, key="year")
    
    # Grand Prix dropdown
    grand_prix_list = [
        "Bahrain", "Saudi Arabian", "Australian", "Japanese", "Chinese",
        "Miami", "Emilia Romagna", "Monaco", "Canadian", "Spanish",
        "Austrian", "British", "Hungarian", "Belgian", "Dutch",
        "Italian", "Azerbaijan", "Singapore", 
        "United States (Austin)", "Mexico City", "São Paulo",
        "Las Vegas", "Qatar", "Abu Dhabi"
    ]
    selected_gp = st.selectbox("Select Grand Prix", grand_prix_list, key="gp")
    
    # Action buttons
    st.button("Generate Analysis")
    st.button("Download Results")

with col2:
    st.markdown("## Analysis")
    
    st.markdown("""
        <div style='
            border: 2px solid #E10600;
            border-radius: 10px;
            padding: 20px;
            min-height: 400px;
            display: flex;
            justify-content: center;
            align-items: center;
        '>
            <h3>Lap Analysis Visualization Will Appear Here</h3>
        </div>
    """, unsafe_allow_html=True)