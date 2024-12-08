import streamlit as st
import time

def get_ai_response(question):
    """
    Simulated AI response - Replace this with your actual AI code integration.
    """
    value = """
    ## F1 Racing Insights
    
    F1 racing is known for its high-speed thrills and cutting-edge technology. Here are some key aspects:

    1. **Top Teams**: Mercedes, Red Bull Racing, and Ferrari are consistently among the top performers[1].
    2. **Race Strategy**: Tire management and pit stop timing are crucial for success.
    3. **Advanced Technology**: F1 cars feature state-of-the-art aerodynamics and hybrid power units.
    4. **Global Championship**: The F1 season includes races across various countries and continents.
    5. **Driver Skills**: F1 drivers need exceptional reflexes, physical fitness, and mental focus.

    Remember, the sport is constantly evolving, with new regulations and technological advancements shaping each season.
    """
    return value

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    initialize_session_state()
            
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: #FFFFFF;
        }
        .stButton>button {
            width: 30%;
            background-color: #FF1E00;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton>button:hover {
            background-color: #DC0000;
        }
        .stTextInput>div>div>input {
            background-color: #2B2B2B;
            color: white;
        }
        .stMarkdown {
            color: #FFFFFF;
        }
        [data-testid="column"]:first-child {
        background-color: #15151E;
        padding: 20px;
        border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1,2])

    with col1:
        if st.button("Home"):
            st.switch_page("pages/user_landing.py")
        st.markdown("---")
        st.image("https://logodownload.org/wp-content/uploads/2016/11/formula-1-logo-7.png", width=200)

        st.markdown("### Pit Wall Services")
        st.markdown("""
        🎟️ **Ticket Booking Assistant**
        - Book your race tickets by specifying:
            - Grand Prix location
            - Number of tickets needed

        🏎️ **F1 Knowledge Base**
        - Access comprehensive F1 history
        - Learn about racing rules and regulations
        - Get technical insights about cars and teams

        📊 **Race Weekend Updates**
        - Latest Updates:
            - qualifying and race grid positions
            - Track conditions and weather updates

        ---
        """)

    with col2:
        st.title("F1 AI Chat Assistant 🏎️")
        
        # Create a container for chat messages
        chat_container = st.container()
        
        # Create the input prompt at the bottom
        prompt = st.chat_input("Your team radio message...")
        
        # Display chat messages in the container
        with chat_container:
            # Check if chat history is empty to show welcome message
            if len(st.session_state.messages) == 0:
                welcome_msg = "Hello! I'm your F1 AI Pit Engineer. Ask me anything about Formula 1!"
                st.session_state.messages.append({"role": "ai", "content": welcome_msg})
            
            # Display existing messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
            # Handle new messages
            if prompt:
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})

                with st.chat_message("assistant"):
                    with st.spinner("Analyzing telemetry..."):
                        response = get_ai_response(prompt)
                        st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    st.set_page_config(
        page_title="F1 AI Pit Engineer",
        page_icon="🏎️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()