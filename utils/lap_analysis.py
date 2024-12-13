import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timezone
import boto3
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("S3_BUCKET_NAME_LAP")
AWS_REGION = os.getenv("AWS_REGION")

BASE_URL = "https://www.autosport.com"

KEYWORDS_CLASSES = {
    "mslt-msg__flag_checkered": "checkered_flag",
    "mslt-msg__safety_car": "safety_car",
    "mslt-msg__crash": "crash",
    "mslt-msg__flag_red": "red_flag",
    "mslt-msg__flag_green": "green_flag",
    "mslt-msg__penalty": "penalty",
    "mslt-msg__mechanical_problem": "mechanical_problem",
    "mslt-msg__trophy": "trophy",
    "mslt-msg__lights_out": "lights_out",
    "mslt-msg__lights_green": "green_lights"
}

# Grand Prix list
grand_prix_list = [
    "Bahrain", "Saudi", "Australian", "Japanese", "Chinese",
    "Miami", "Emilia Romagna", "Monaco", "Canadian", "Spanish",
    "Austrian", "British", "Hungarian", "Belgian", "Dutch",
    "Italian", "Azerbaijan", "Singapore", "Portuguese",
    "US", "United States", "Mexico", "Mexican", "Sao Paulo", "French",
    "Las Vegas", "Qatar", "Abu Dhabi", "Brazilian", "Styrian", "Turkish", "Imola"
]

def create_webdriver():
    """
    Create and configure Selenium WebDriver with optimized settings.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable images

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)  # Increased timeout
    driver.implicitly_wait(10)  # Increased implicit wait
    return driver

def parse_timestamp(timestamp_str):
    """
    Safely parse timestamp, returning a valid datetime or None
    """
    if not timestamp_str:
        return None

    try:
        # Try parsing with Z (UTC) timezone
        if timestamp_str.endswith('Z'):
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))

        # Try direct parsing
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        # If parsing fails, log and return None
        logger.warning(f"Invalid timestamp format: {timestamp_str}")
        return None

def get_race_links(driver):
    """
    Scrape race links from pages p=0 to p=13 where titles strictly end with 'Race' or 'Race day'.
    """
    links = []
    for page in range(14):  # Pages 0 to 13
        url = f"https://www.autosport.com/live/?p={page}"
        try:
            driver.get(url)
            time.sleep(3)  # Allow page content to load
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract links with titles strictly ending with 'Race' or 'Race day'
            page_links = []
            for a in soup.find_all('a', href=True, class_='ms-item'):
                title_tag = a.find('p', class_='ms-item__title')
                if title_tag:
                    title = title_tag.text.strip()
                    if title.lower().endswith("race") or title.lower().endswith("race day"):
                        page_links.append(BASE_URL + a['href'])

            if not page_links:
                logger.warning(f"No race links found on page {page}.")
            else:
                logger.info(f"Page {page}: Found {len(page_links)} race links.")

            links.extend(page_links)
            time.sleep(0.5)  # Slight delay before processing next page
        except Exception as e:
            logger.error(f"Error processing page {page}: {e}")

    return list(set(links))

def extract_country_name(title):
    """
    Extract the country name from the race title based on the predefined Grand Prix list.
    If 'US' or 'United States', save as 'US'.
    If 'Mexico' or 'Mexican', save as 'Mexico'.
    """
    for country in grand_prix_list:
        if country.lower() in title.lower():
            if country.lower() in ["us", "united states"]:
                return "US"
            if country.lower() in ["mexico", "mexican"]:
                return "Mexico"
            return country
    return "Unknown"


def scrape_race_content(driver, link):
    """
    Scrape race content with detailed keyword and non-keyword messages,
    including clicking 'Load more' button to get all content.
    """
    try:
        driver.get(link)

        # Keep clicking 'Load more' until no more content
        while True:
            try:
                # Find and click 'Load more' button
                load_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mslt-more__btn"))
                )
                load_more_button.click()

                # Small delay to allow content to load
                time.sleep(3)
            except Exception:
                # No more 'Load more' button found
                break

        # Parse the fully loaded page
        race_title = driver.title.strip()
        country_name = extract_country_name(race_title)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        messages = soup.find_all('div', class_="mslt-msg")

        all_messages = []

        for msg in messages:
            msg_classes = msg.get("class", [])
            time_tag = msg.find('time', class_='mslt-msg__time')
            comment_body = msg.find('div', class_='mslt-msg__body ms-article-content')

            if time_tag and comment_body:
                timestamp_str = time_tag.get('datetime', '').strip()
                parsed_time = parse_timestamp(timestamp_str)
                if not parsed_time:
                    continue

                # Determine event type
                event_type = "non_keyword_message"
                for k_class, k_event in KEYWORDS_CLASSES.items():
                    if k_class in msg_classes:
                        event_type = k_event
                        break

                message_entry = {
                    'time': parsed_time.isoformat(),
                    'event': event_type,
                    'comment': comment_body.text.strip()
                }
                all_messages.append(message_entry)

        # Sort messages by timestamp
        all_messages.sort(key=lambda x: parse_timestamp(x['time']))

        # Final structure for the race
        race_data = {
            "country": country_name,
            "race": all_messages
        }

        return race_title, race_data
    except Exception as e:
        logger.error(f"Failed to scrape {link}: {e}")
        return None, None

def sequential_scrape(driver, links):
    """
    Perform sequential scraping of links.
    """
    results = {}
    failed_links = []

    for link in links:
        try:
            race_title, race_data = scrape_race_content(driver, link)
            if race_data:
                results[race_title] = race_data
            else:
                failed_links.append(link)
                logger.warning(f"Failed to scrape link: {link}")
        except Exception as e:
            logger.error(f"Error processing link {link}: {e}")
            failed_links.append(link)

        time.sleep(0.5)  # Slightly increased delay between links

    # Save failed links
    with open("failed_links.json", "w", encoding="utf-8") as failed_file:
        json.dump(failed_links, failed_file, indent=4)

    return results

def upload_to_s3(file_path, bucket_name, object_name):
    """
    Upload a file to an S3 bucket.
    """
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"File {file_path} uploaded to S3 bucket {bucket_name} as {object_name}")
    except Exception as e:
        logger.error(f"Failed to upload {file_path} to S3: {e}")

def main():
    driver = None
    try:
        driver = create_webdriver()
        race_links = get_race_links(driver)
        logger.info(f"Total race links found: {len(race_links)}")

        all_race_data = sequential_scrape(driver, race_links)

        # Save race data with proper encoding
        local_file_path = "race_data.json"
        with open(local_file_path, "w", encoding='utf-8') as json_file:
            json.dump(all_race_data, json_file, indent=4, ensure_ascii=False)

        logger.info("Scraping completed and saved to race_data.json.")

        # Upload to S3
        upload_to_s3(local_file_path, AWS_BUCKET_NAME, "race_data.json")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
