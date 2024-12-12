import os
import json
import boto3
import requests
import time
from dotenv import load_dotenv
from typing import Dict, Any, List

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

BASE_URL = "https://api.jolpi.ca/ergast/f1"

# Initialize S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

def fetch_data(endpoint: str, max_retries: int = 10, initial_delay: int = 5) -> Dict[str, Any] | None:
    """Fetch data from the API with more robust exponential backoff."""
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{endpoint}.json")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                print(f"Rate limit hit for {endpoint}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                if delay > 300:  # Cap delay at 5 minutes
                    delay = 300
            else:
                print(f"Error fetching {endpoint}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            time.sleep(delay)
            delay *= 2
    print(f"Exceeded maximum retries ({max_retries}) for {endpoint}")
    return None

def safe_get_data(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    Safely retrieve nested dictionary values with a default fallback.
    
    :param data: The dictionary to search
    :param keys: Nested keys to retrieve
    :param default: Default value if keys are not found
    :return: Retrieved value or default
    """
    for key in keys:
        try:
            data = data.get(key, {})
        except (AttributeError, TypeError):
            return default
    return data if data != {} else default

def process_season_data(season: int) -> Dict[str, Any]:
    """Fetch and consolidate all data for a specific season with improved error handling."""
    season_data = {
        "season": season,
        "races": [],
        "drivers": [],
        "constructors": [],
        "standings": {},
        "race_details": []
    }

    # Fetch Races
    races_endpoint = f"{BASE_URL}/{season}/races"
    races_data = fetch_data(races_endpoint)
    if races_data:
        races = safe_get_data(races_data, 'MRData', 'RaceTable', 'Races', default=[])
        season_data['races'] = races

    # Fetch Drivers
    drivers_endpoint = f"{BASE_URL}/{season}/drivers"
    drivers_data = fetch_data(drivers_endpoint)
    if drivers_data:
        drivers = safe_get_data(drivers_data, 'MRData', 'DriverTable', 'Drivers', default=[])
        season_data['drivers'] = drivers

    # Fetch Constructors
    constructors_endpoint = f"{BASE_URL}/{season}/constructors"
    constructors_data = fetch_data(constructors_endpoint)
    if constructors_data:
        constructors = safe_get_data(constructors_data, 'MRData', 'ConstructorTable', 'Constructors', default=[])
        season_data['constructors'] = constructors

    # Process each race in the season
    for race in races:
        round_number = race.get('round')
        race_info = {
            "round": round_number,
            "raceName": race.get('raceName'),
            "date": race.get('date'),
            "circuit": race.get('Circuit', {}),
            "results": None,
            "qualifying": None,
            "pitStops": None
        }

        # Fetch Race Results
        results_endpoint = f"{BASE_URL}/{season}/{round_number}/results"
        results_data = fetch_data(results_endpoint)
        if results_data:
            race_info['results'] = safe_get_data(results_data, 'MRData', 'RaceTable', 'Races', default=[])

        # Fetch Qualifying
        qualifying_endpoint = f"{BASE_URL}/{season}/{round_number}/qualifying"
        qualifying_data = fetch_data(qualifying_endpoint)
        if qualifying_data:
            race_info['qualifying'] = safe_get_data(qualifying_data, 'MRData', 'RaceTable', 'Races', default=[])

        # Fetch Pit Stops
        pitstops_endpoint = f"{BASE_URL}/{season}/{round_number}/pitstops"
        pitstops_data = fetch_data(pitstops_endpoint)
        if pitstops_data:
            race_info['pitStops'] = safe_get_data(pitstops_data, 'MRData', 'RaceTable', 'Races', 'PitStops', default=[])

        season_data['race_details'].append(race_info)

    # Fetch Driver Standings
    driver_standings_endpoint = f"{BASE_URL}/{season}/driverStandings"
    driver_standings_data = fetch_data(driver_standings_endpoint)
    if driver_standings_data:
        season_data['standings']['drivers'] = safe_get_data(driver_standings_data, 'MRData', 'StandingsTable', 'StandingsLists', default=[])

    # Fetch Constructor Standings
    constructor_standings_endpoint = f"{BASE_URL}/{season}/constructorStandings"
    constructor_standings_data = fetch_data(constructor_standings_endpoint)
    if constructor_standings_data:
        season_data['standings']['constructors'] = safe_get_data(constructor_standings_data, 'MRData', 'StandingsTable', 'StandingsLists', default=[])

    return season_data

def upload_to_s3(data: Dict[str, Any], key: str):
    """Upload JSON data to S3 with error handling."""
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=key,
            Body=json.dumps(data, indent=2),
            ContentType="application/json",
        )
        print(f"Uploaded to S3: {key}")
    except Exception as e:
        print(f"Error uploading {key} to S3: {e}")

def main():
    """Main function to fetch and upload data with improved error handling."""
    current_year = time.localtime().tm_year
    for season in range(2013, current_year + 1):
        try:
            print(f"Processing season: {season}")
            consolidated_season_data = process_season_data(season)
            
            # Upload consolidated season data to S3
            season_key = f"f1-data/{season}/{season}_season_data.json"
            upload_to_s3(consolidated_season_data, season_key)
            print(f"Uploaded consolidated data for season {season}")
            
            # Add a small delay between seasons to prevent overwhelming the API
            time.sleep(2)
        except Exception as e:
            print(f"Error processing season {season}: {e}")
            continue

if __name__ == "__main__":
    main()