import requests
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# AWS RDS Configuration from .env
RDS_HOST = os.getenv("RDS_HOST")
RDS_PORT = os.getenv("RDS_PORT", "3306")  # Default MySQL port
RDS_DB = os.getenv("RDS_DB")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")

# Function to establish a connection to the RDS database
def get_rds_connection():
    try:
        connection = mysql.connector.connect(
            host=RDS_HOST,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB,
            port=RDS_PORT
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Failed to connect to RDS: {e}")
        return None

# Function to scrape the race calendar
def scrape_race_calendar():
    url = "https://www.formula1.com/en/latest/article/fia-and-formula-1-announces-calendar-for-2025.48ii9hOMGxuOJnjLgpA5qS"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the table containing the race calendar
    table = soup.find("table", class_="mt-5 mb-10 w-full border border-gray20 rounded-[10px] overflow-hidden border-separate border-spacing-0 table-fixed")
    if not table:
        print("Could not locate the race calendar table on the website.")
        return pd.DataFrame()

    # Extract table rows
    rows = table.find("tbody").find_all("tr")

    # Prepare to store race details
    race_details = []

    # Loop through each row and extract the data
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 3:  # Ensure the row has the expected number of columns
            date = cells[0].text.strip()
            country = cells[1].text.strip()
            venue = cells[2].text.strip()

            # Append the details to the list
            race_details.append({
                "Grand Prix": country,  # Country maps to Grand Prix
                "Venue": venue,         # Venue remains Venue
                "Dates": date           # Date becomes Dates
            })

    # Convert to DataFrame
    return pd.DataFrame(race_details)

# Function to load DataFrame to AWS RDS
def load_to_rds(df, table_name, connection):
    if df.empty:
        print(f"DataFrame is empty. Cannot load {table_name} to RDS.")
        return

    try:
        cursor = connection.cursor()

        # Create table if not exists
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            `Grand Prix` TEXT,
            `Venue` TEXT,
            `Dates` TEXT
        );
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO {table_name} (`Grand Prix`, `Venue`, `Dates`) VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))

        connection.commit()
        print(f"Successfully loaded {table_name} into RDS.")
    except mysql.connector.Error as e:
        print(f"Failed to load {table_name} to RDS: {e}")
    finally:
        cursor.close()

# Main Function
def main():
    # Get RDS connection
    connection = get_rds_connection()
    if not connection:
        return

    # Scrape and load race calendar
    print("Scraping Race Calendar...")
    race_calendar_df = scrape_race_calendar()
    if not race_calendar_df.empty:
        load_to_rds(race_calendar_df, "race_calendar", connection)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
