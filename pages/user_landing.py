import pandas as pd
import streamlit as st
from streamlit.components.v1 import html

# Set page config
st.set_page_config(
    page_title="F1 User Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"  
)

# Add custom CSS
def add_css():
    css = """
    <style>
    /* News Cards */
    .news-card {
        background-color: #cbcbcb;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    .news-card:hover {
        transform: translateY(-5px);
    }
    .news-card-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    .news-card-content {
        padding: 15px;
    }
    .news-card-title {
        color: #333;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .news-card-title a {
        color: #333;
        text-decoration: none;
    }
    .news-card-title a:hover {
        color: #D91E18;
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
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Main function for the landing page
def user_landing_page():
    add_css()  # Apply CSS styling

    st.title("🏎️ F1 User Dashboard")

    co1, co2, spacer, co3,  co4 = st.columns([1, 2, 4, 1, 1])
    with co1:
        if st.button('🪪 Profile'):
            st.switch_page("pages/profile.py")
    
    with co2:
        if st.button('⏱️ Lap-by-Lap Analysis'):
            st.switch_page("pages/lap_by_lap.py")

    with co3:
        if st.button('🤖AI Assistant'):
            st.switch_page("pages/AI_assistant.py")

    with co4:
        if st.button('💬 Chat Support'):
            st.switch_page("pages/chat_support.py")

    # Create layout with two columns
    col1, col2 = st.columns(2)

    # Column 1: Race Calendar and Driver Standings tabs
    with col1:
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["🏁 Race Calendar", "🏎️ Driver Standings", "🏆 Constructor Standings"])


        # Tab 1: Race Calendar
        with tab1:
            st.subheader("🏁 Race Calendar")

            # Data for the race calendar
            race_calendar = {
                "Grand Prix": [
                    "Bahrain", "Saudi Arabian", "Australian", "Japanese", "Chinese",
                    "Miami", "Emilia Romagna", "Monaco", "Canadian", "Spanish",
                    "Austrian", "British", "Hungarian", "Belgian", "Dutch",
                    "Italian", "Azerbaijan", "Singapore", 
                    "United States (Austin)", "Mexico City", "São Paulo",
                    "Las Vegas", "Qatar", "Abu Dhabi"
                ],
                "Circuit": [
                    "Bahrain International Circuit", "Jeddah Corniche Circuit", "Albert Park Circuit", "Suzuka International Racing Course", "Shanghai International Circuit",
                    "Miami International Autodrome", "Autodromo Enzo e Dino Ferrari", "Circuit de Monaco", "Circuit Gilles Villeneuve", "Circuit de Barcelona-Catalunya",
                    "Red Bull Ring", "Silverstone Circuit", "Hungaroring", "Circuit de Spa-Francorchamps", "Circuit Zandvoort",
                    "Autodromo Nazionale Monza", "Baku City Circuit", "Marina Bay Street Circuit",
                    "Circuit of the Americas", "Autódromo Hermanos Rodríguez", "Autódromo José Carlos Pace",
                    "Las Vegas Strip Circuit", "Lusail International Circuit", "Yas Marina Circuit"
                ],
                "Qualifying": [
                    "March 2", "March 9", "March 23", "April 6", "April 20",
                    "May 4", "May 18", "May 25", "June 8", "June 22",
                    "June 29", "July 6", "July 20", "July 27", "August 24",
                    "August 31", "September 14", "September 21",
                    "October 19", "October 26", "November 2", "November 22",
                    "November 30", "December 7"
                ],
                "Race": [
                    "March 3", "March 10", "March 24", "April 7", "April 21",
                    "May 5", "May 19", "May 26", "June 9", "June 23",
                    "June 30", "July 7", "July 21", "July 28", "August 25",
                    "September 1", "September 15", "September 22",
                    "October 20", "October 27", "November 3", "November 23",
                    "December 1", "December 8"
                ]
            }

            # Convert to DataFrame
            df = pd.DataFrame(race_calendar)

            # Display the table
            st.table(df)

        # Tab 2: Driver Standings
        with tab2:
            st.subheader("🏎️ Driver Standings")

            # Driver standings data
            driver_standings = {
                "Pos": list(range(1, 24)),
                "Driver": [
                    "Max Verstappen", "Lando Norris", "Charles Leclerc", "Oscar Piastri", "Carlos Sainz",
                    "George Russell", "Lewis Hamilton", "Sergio Perez", "Fernando Alonso", "Nico Hulkenberg",
                    "Pierre Gasly", "Yuki Tsunoda", "Lance Stroll", "Esteban Ocon", "Kevin Magnussen",
                    "Alexander Albon", "Daniel Ricciardo", "Oliver Bearman", "Franco Colapinto", "Zhou Guanyu",
                    "Liam Lawson", "Valtteri Bottas", "Logan Sargeant"
                ],
                "Nationality": [
                    "NED", "GBR", "MON", "AUS", "ESP", "GBR", "GBR", "MEX", "ESP", "GER",
                    "FRA", "JPN", "CAN", "FRA", "DEN", "THA", "AUS", "GBR", "ARG", "CHN",
                    "NZL", "FIN", "USA"
                ],
                "Car": [
                    "Red Bull Racing Honda RBPT", "McLaren Mercedes", "Ferrari", "McLaren Mercedes", "Ferrari",
                    "Mercedes", "Mercedes", "Red Bull Racing Honda RBPT", "Aston Martin Aramco Mercedes", "Haas Ferrari",
                    "Alpine Renault", "RB Honda RBPT", "Aston Martin Aramco Mercedes", "Alpine Renault", "Haas Ferrari",
                    "Williams Mercedes", "RB Honda RBPT", "Haas Ferrari", "Williams Mercedes", "Kick Sauber Ferrari",
                    "RB Honda RBPT", "Kick Sauber Ferrari", "Williams Mercedes"
                ],
                "Pts": [
                    429, 349, 341, 291, 272, 235, 211, 152, 68, 37,
                    36, 30, 24, 23, 16, 12, 12, 7, 5, 4,
                    4, 0, 0
                ]
            }

            # Convert to DataFrame
            df = pd.DataFrame(driver_standings).reset_index(drop=True)
            st.table(df)

            with tab3:
                st.subheader("🏆 Constructor Standings")

                # Constructor standings data
                constructor_standings = {
                    "Pos": list(range(1, 11)),
                    "Team": [
                        "McLaren Mercedes", "Ferrari", "Red Bull Racing Honda RBPT", "Mercedes",
                        "Aston Martin Aramco Mercedes", "Alpine Renault", "Haas Ferrari",
                        "RB Honda RBPT", "Williams Mercedes", "Kick Sauber Ferrari"
                    ],
                    "Pts": [
                        640, 619, 581, 446, 92, 59, 54, 46, 17, 4
                    ]
                }

                # Convert to DataFrame
                df_constructors = pd.DataFrame(constructor_standings)

                # Display the table
                st.table(df_constructors)

            
    with col2:
        st.subheader("📰 Latest News")
        news_articles = [
            {
                "image": "https://via.placeholder.com/300x200.png?text=F1+News",
                "title": "Hamilton Secures Pole Position in Thrilling Qualifying Session",
                "url": "#"
            },
            {
                "image": "https://media.formula1.com/image/upload/f_auto,c_limit,w_1440,q_auto/f_auto,c_fill,q_auto,w_1320,t_16by9Centre,g_faces,ar_16:9/fom-website/2023/Red%20Bull/RB20%20launch/SI202402140459_hires_jpeg_24bit_rgb",
                "title": "Red Bull Unveils Revolutionary New Aerodynamic Package",
                "url": "#"
            },
            {
                "image": "https://media.formula1.com/image/upload/f_auto,c_limit,w_960,q_auto/f_auto/q_auto/content/dam/fom-website/manual/Misc/2022manual/WinterFebruary/Ferrari/F1-75_JPG_SPONSOR_00004",
                "title": "Ferrari's Strategy Masterclass Leads to Double Podium Finish",
                "url": "#"
            },
            {
                "image": "https://via.placeholder.com/300x200.png?text=F1+News",
                "title": "Rookie Driver Makes Waves with Impressive Debut Performance",
                "url": "#"
            }
        ]

        for i in range(0, len(news_articles), 2):
            col1, col2 = st.columns(2)
            
            with col1:
                article = news_articles[i]
                st.markdown(f'''
                <div class="news-card">
                    <img src="{article['image']}" alt="News Image" class="news-card-image">
                    <div class="news-card-content">
                        <h3 class="news-card-title"><a href="{article['url']}">{article['title']}</a></h3>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
            
            if i + 1 < len(news_articles):
                with col2:
                    article = news_articles[i + 1]
                    st.markdown(f'''
                    <div class="news-card">
                        <img src="{article['image']}" alt="News Image" class="news-card-image">
                        <div class="news-card-content">
                            <h3 class="news-card-title"><a href="{article['url']}">{article['title']}</a></h3>
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)


# Run the app
if __name__ == "__main__":
    user_landing_page()
