import pandas as pd
import streamlit as st
from streamlit.components.v1 import html
import mysql.connector

# Set page config
st.set_page_config(
    page_title="F1 User Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"  
)

cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )

def get_race_calendar():
    try:
        cnx = mysql.connector.connect(
        host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
        user="admin",
        password="amazonrds7245",
        database="bdia_team6_finalproject_db"
    )
        # Create cursor and execute query
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                `Grand Prix`,
                Venue,
                Dates
            FROM race_calendar
            ORDER BY STR_TO_DATE(Dates, '%M %d-%d')
        """)
        
        # Fetch all results
        results = cursor.fetchall()
        
        # Transform results into a dictionary for a DataFrame
        race_calendar = {
            "Grand Prix": [],
            "Venue": [],
            "Dates": []
        }
        
        for row in results:
            race_calendar["Grand Prix"].append(row['Grand Prix'])
            race_calendar["Venue"].append(row['Venue'])
            race_calendar["Dates"].append(row['Dates'])
            
        cursor.close()
        cnx.close()
        return race_calendar
        
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None


def get_driver_standings():
    try:
        cnx = mysql.connector.connect(
            host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
            user="admin",
            password="amazonrds7245",
            database="bdia_team6_finalproject_db"
        )
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT Pos, Driver, Nationality, Car, Pts
            FROM driver_standings
            ORDER BY CAST(Pos AS UNSIGNED)
        """)
        results = cursor.fetchall()
        driver_standings = {
            "Pos": [],
            "Driver": [],
            "Nationality": [],
            "Car": [],
            "Pts": []
        }
        for row in results:
            driver_standings["Pos"].append(row['Pos'])
            driver_standings["Driver"].append(row['Driver'])
            driver_standings["Nationality"].append(row['Nationality'])
            driver_standings["Car"].append(row['Car'])
            driver_standings["Pts"].append(row['Pts'])
        cursor.close()
        cnx.close()
        return driver_standings
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def get_constructor_standings():
    try:
        cnx = mysql.connector.connect(
        host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
        user="admin",
        password="amazonrds7245",
        database="bdia_team6_finalproject_db"
    )
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT Pos, Team, Pts
            FROM constructor_standings
            ORDER BY CAST(Pos AS UNSIGNED)
        """)
        results = cursor.fetchall()
        constructor_standings = {
            "Pos": [],
            "Team": [],
            "Pts": []
        }
        for row in results:
            constructor_standings["Pos"].append(row['Pos'])
            constructor_standings["Team"].append(row['Team'])
            constructor_standings["Pts"].append(row['Pts'])
        cursor.close()
        cnx.close()
        return constructor_standings
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return None

def fetch_news(team=None):
    cnx = mysql.connector.connect(
        host="bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com",
        user="admin",
        password="amazonrds7245",
        database="bdia_team6_finalproject_db"
    )
    cursor = cnx.cursor()
    
    try:
        if team:
            query = "SELECT team_name, news_title, news_link FROM news_articles WHERE team_name = %s"
            cursor.execute(query, (team,))
        else:
            query = "SELECT team_name, news_title, news_link FROM news_articles"
            cursor.execute(query)
        
        news_data = cursor.fetchall()
    except mysql.connector.Error as err:
        if err.errno == 1146:  # Table doesn't exist error
            st.error("The 'news' table does not exist in the database. Please create the table and try again.")
            news_data = []
        else:
            st.error(f"An error occurred: {err}")
            news_data = []
    finally:
        cursor.close()
        cnx.close()
    
    return news_data


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
    if "username" in st.session_state:
        st.write(f"Welcome {st.session_state.username}!")

    if "favorite_team" not in st.session_state:
            cursor = cnx.cursor()
            cursor.execute("SELECT favorite_team FROM login WHERE username = %s", (st.session_state.username,))
            result = cursor.fetchone()
            cursor.close()
            cnx.close()
            if result:
                st.session_state.favorite_team = result[0]
            else:
                st.session_state.favorite_team = None

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
            race_calendar = get_race_calendar()
    
            if race_calendar:
                # Convert to DataFrame
                df = pd.DataFrame(race_calendar)

                df.rename(
                    columns={
                        "Grand Prix": "Race",
                        "Venue": "Race Track",
                        "Dates": "Race Dates"
                    },
                    inplace=True
                )

                # Display the table
                st.table(df)

        # Tab 2: Driver Standings
        with tab2:
            st.subheader("🏎️ Driver Standings")

            driver_standings = get_driver_standings()

            if driver_standings:

                # Convert to DataFrame
                df1 = pd.DataFrame(driver_standings)

                df1.rename(
                    columns={
                        "Pos": "Position",
                        "Driver": "Driver Name",
                        "Nationality":"Nationality",
                        "Car": "Constructor Team",
                        "Pts": "Points"
                    },
                    inplace=True
                )

                # Display the table
                st.table(df1)    

        with tab3:
            st.subheader("🏆 Constructor Standings")

            constructor_standings = get_constructor_standings()

            if constructor_standings:

                # Convert to DataFrame
                df_constructors = pd.DataFrame(constructor_standings)

                df_constructors.rename(
                    columns={
                        "Pos": "Position",
                        "Team": "Constructor Team",
                        "Pts": "Points"
                    },
                    inplace=True
                )

                # Display the table
                st.table(df_constructors)


            
    with col2:
        st.subheader("📰 Latest News for Your Favorite Team")

        if st.session_state.favorite_team:
            # Fetch news data for the user's favorite team
            news_data = fetch_news(st.session_state.favorite_team)

            if news_data:
                # Format the news data
                news_articles = [
                    {
                        "image": f"https://via.placeholder.com/300x200.png?text={st.session_state.favorite_team}",
                        "title": news_title,
                        "url": news_link
                    }
                    for _, news_title, news_link in news_data
                ]

                # Display the news articles in a grid layout
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
            else:
                st.write(f"No news available for {st.session_state.favorite_team}.")
        else:
            st.write("Please set your favorite team in your profile to see team-specific news.")


# Run the app
if __name__ == "__main__":
    user_landing_page()
