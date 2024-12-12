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

# Function to scrape driver standings
def scrape_driver_standings():
    url = "https://www.formula1.com/en/results/2024/drivers"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the standings table
    table = soup.find("table")  # Adjust selector if a specific class or ID is required
    if not table:
        print("Could not locate driver standings table on the website.")
        return pd.DataFrame()

    # Extract rows from the table
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]  # Extract headers

    data = []
    for row in rows[1:]:
        cells = row.find_all("td")
        row_data = []
        for i, cell in enumerate(cells):
            # For the driver column, exclude shortform (VER, etc.)
            if headers[i].lower() == "driver":
                span = cell.find("span", class_="tablet:hidden")
                if span:
                    span.extract()  # Remove the shortform element
                row_data.append(cell.text.strip())
            else:
                row_data.append(cell.text.strip())
        data.append(row_data)

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

# Function to scrape constructor standings
def scrape_constructor_standings():
    url = "https://www.formula1.com/en/results/2024/team"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the standings table
    table = soup.find("table")  # Adjust selector if a specific class or ID is required
    if not table:
        print("Could not locate constructor standings table on the website.")
        return pd.DataFrame()

    # Extract rows from the table
    rows = table.find_all("tr")
    headers = [th.text.strip() for th in rows[0].find_all("th")]  # Extract headers
    data = [
        [td.text.strip() for td in row.find_all("td")] for row in rows[1:]
    ]  # Extract data rows

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=headers)
    return df

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
            {', '.join([f"`{col}` TEXT" for col in df.columns])}
        );
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({placeholders})"
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

    # Scrape and load driver standings
    print("Scraping Driver Standings...")
    driver_standings_df = scrape_driver_standings()
    if not driver_standings_df.empty:
        load_to_rds(driver_standings_df, "driver_standings", connection)

    # Scrape and load constructor standings
    print("Scraping Constructor Standings...")
    constructor_standings_df = scrape_constructor_standings()
    if not constructor_standings_df.empty:
        load_to_rds(constructor_standings_df, "constructor_standings", connection)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()