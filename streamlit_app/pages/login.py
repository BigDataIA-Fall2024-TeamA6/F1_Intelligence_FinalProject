import streamlit as st
import requests

# Streamlit page configuration
st.set_page_config(
    page_title="F1 Pit Stop Login",
    initial_sidebar_state="collapsed",
)

# Validate user credentials via FastAPI
def validate_user(username, password):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/login/",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Invalid email or password.")
            return False
    except requests.ConnectionError:
        st.error("Unable to connect to FastAPI backend.")
        return False

def main():
    # Inline CSS for styling
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
        .login-container {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # F1 logo and title
    col1, spacer, col2 = st.columns([1, 1, 2])
    with col1:
        st.image("https://www.formula1.com/etc/designs/fom-website/images/f1_logo.svg", width=300)
    with col2:
        st.markdown("<h1 style='color: white;'>F1 Pit Login</h1>", unsafe_allow_html=True)

    # Login form
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)

        username = st.text_input("Driver ID (Email)", key="uname")
        password = st.text_input("Pit Lane Password", type="password", key="pword")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Start Engine 🏁", key="login"):
                # Validate user credentials
                user = validate_user(username, password)
                if user:
                    st.success(f"Welcome to the race, {user['fname']} {user['lname']}!")
                    # Store user details in session state
                    st.session_state.username = username
                    st.session_state.user_id = user["id"]
                    st.session_state.user_type = user["user_type"]
                    st.session_state.full_name = f"{user['fname']} {user['lname']}"
                    
                    # Redirect based on user type
                    if user["user_type"] == "admin":
                        st.switch_page("pages/employee.py")
                    else:
                        st.switch_page("pages/user_landing.py")
        with col2:
            if st.button("Join the Team 🏎️", key="create_user"):
                st.switch_page("pages/f1_registration.py")

        st.markdown('</div>', unsafe_allow_html=True)

    # F1 trivia or quote
    st.markdown(
        """
        <div style="position: fixed; bottom: 10px; right: 10px; background-color: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 5px;">
        <i>"To finish first, you must first finish." - Michael Schumacher</i>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
