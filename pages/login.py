import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Predefined credentials for simplicity
USER_CREDENTIALS = {
    "admin": "password123",
    "user1": "welcome2024",
    "Test": "1234",
}

st.set_page_config(
    page_title="F1 Pit Stop Login",
    initial_sidebar_state="collapsed"
)

def main():
    # F1 red background and custom styles
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FF1801;  /* F1 red color */
        }
        .stTextInput > div > div > input {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stButton > button {
            background-color: #FFFFFF;
            color: #FF1801;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #000000;
            color: #FFFFFF;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # F1 logo and title
    col1, spacer, col2 = st.columns([1, 1, 2])
    with col1:
        st.image("https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg", width=300)
    with col2:
        st.markdown("<h1 style='color: white;'>F1 Pit Login</h1>", unsafe_allow_html=True)

    # Create a card-like container for login
    with st.container():
        st.markdown(
            """
            <style>
            .login-container {
                background-color: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        username = st.text_input("Driver ID", key="uname")
        password = st.text_input("Pit Lane Password", type="password", key="pword")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Engine 🏁", key="login"):
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.success(f"Welcome to the race, {username}!")
                    st.session_state.username = username
                    st.switch_page("pages/user_landing.py")
                else:
                    st.error("Pit stop error! Invalid Driver ID or Password.")
        with col2:
            if st.button("Join the Team 🏎️", key="create_user"):
                st.switch_page("pages/create_user.py")

        st.markdown('</div>', unsafe_allow_html=True)

    # F1 trivia or quote
    st.markdown(
        """
        <div style="position: fixed; bottom: 10px; right: 10px; background-color: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 5px;">
        <i>"To finish first, you must first finish." - Michael Schumacher</i>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()