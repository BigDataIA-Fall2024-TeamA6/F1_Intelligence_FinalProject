import os
import json
import boto3
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from typing import List, Dict, Any, Optional

# Load environment variables
load_dotenv()

# Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize OpenAI Embeddings
embeddings = OpenAIEmbeddings()


class F1DataEnhancedEmbedder:
    def __init__(self, index_name: str = "f1-data-index"):
        self.index_name = index_name
        self._create_index_if_not_exists()
        self.index = pc.Index(index_name)

    def _create_index_if_not_exists(self):
        try:
            if self.index_name not in [idx.name for idx in pc.list_indexes()]:
                pc.create_index(
                    name=self.index_name,
                    dimension=1536,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT)
                )
                print(f"Created Pinecone index: {self.index_name}")
            else:
                print(f"Pinecone index {self.index_name} already exists")
        except Exception as e:
            print(f"Error creating Pinecone index: {e}")

    def download_json_from_s3(self, season: int) -> Optional[Dict[str, Any]]:
        try:
            key = f"f1-data/{season}/{season}_season_data.json"
            response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)
            json_content = response['Body'].read().decode('utf-8')
            return json.loads(json_content)
        except Exception as e:
            print(f"Error downloading JSON for season {season}: {e}")
            return None

    def _generate_text_representation(self, data: Any, category: str, season: int) -> str:
        if isinstance(data, list):
            if category == "races":
                return f"Season {season} races: " + ", ".join(
                    f"{item.get('raceName', 'Unknown')} at {item.get('circuit', {}).get('circuitName', 'Unknown')} on {item.get('date', 'Unknown')}"
                    for item in data
                )
            elif category == "drivers":
                return f"Season {season} drivers: " + ", ".join(
                    f"{item.get('givenName', 'Unknown')} {item.get('familyName', 'Unknown')} ({item.get('nationality', 'Unknown')})"
                    for item in data
                )
            elif category == "constructors":
                return f"Season {season} constructors: " + ", ".join(
                    f"{item.get('name', 'Unknown')} ({item.get('nationality', 'Unknown')})"
                    for item in data
                )
        elif category == "race_results":
            return f"Race {data.get('raceName', 'Unknown')} ({data.get('date', 'Unknown')}): Winner - {data['Results'][0]['Driver']['givenName']} {data['Results'][0]['Driver']['familyName']} ({data['Results'][0]['Constructor']['name']})."
        elif category == "top_5_standings":
            standings = ", ".join(
                f"{result['Driver']['givenName']} {result['Driver']['familyName']} ({result['Constructor']['name']})"
                for result in data['Results'][:5]
            )
            return f"Top 5 Standings for {data.get('raceName', 'Unknown')}: {standings}."
        return "Unknown category."

    def _upsert_embedding(self, text: str, unique_id: str, category: str, season: int):
        """Create and upsert embeddings into Pinecone."""
        embedding = embeddings.embed_query(text)
        metadata = {
            'text': text,
            'category': category,
            'season': str(season),
            'data_type': 'item-level' if "race" in category else 'key-level'
        }
        self.index.upsert(vectors=[(unique_id, embedding, metadata)])
        print(f"Embedded: {unique_id}")

    def generate_key_level_embedding(self, season: int, data: Dict[str, Any]):
        """Create embeddings for key-level summaries."""
        key_categories = ["races", "drivers", "constructors", "standings"]
        for category in key_categories:
            content = data.get(category, [])
            text_representation = self._generate_text_representation(content, category, season)
            unique_id = f"{season}_{category}_summary"
            self._upsert_embedding(text_representation, unique_id, category, season)

    def generate_race_embeddings(self, season: int, races: List[Dict[str, Any]]):
        """Embed detailed race results."""
        for race in races:
            # Embed race winner
            if 'Results' in race:
                winner_text = self._generate_text_representation(race, "race_results", season)
                unique_id = f"{season}_race_{race['round']}_winner"
                self._upsert_embedding(winner_text, unique_id, "race_results", season)

                # Embed top 5 standings
                top_5_text = self._generate_text_representation(race, "top_5_standings", season)
                unique_id = f"{season}_race_{race['round']}_top5"
                self._upsert_embedding(top_5_text, unique_id, "top_5_standings", season)

    def generate_embeddings_for_season(self, season: int):
        """Generate embeddings for a season."""
        season_data = self.download_json_from_s3(season)
        if not season_data:
            print(f"No data found for season {season}")
            return

        print(f"Creating embeddings for season: {season}")
        # Key-level embeddings
        self.generate_key_level_embedding(season, season_data)

        # Race-level embeddings
        self.generate_race_embeddings(season, season_data.get("races", []))

    def batch_embed_seasons(self, start_year: int, end_year: int):
        """Batch process multiple seasons."""
        for season in range(start_year, end_year + 1):
            try:
                self.generate_embeddings_for_season(season)
                print(f"Completed embeddings for season {season}")
            except Exception as e:
                print(f"Error processing season {season}: {e}")


if __name__ == "__main__":
    embedder = F1DataEnhancedEmbedder()
    current_year = int(os.getenv('MAX_SEASON_YEAR', '2024'))
    embedder.batch_embed_seasons(2013, current_year)
