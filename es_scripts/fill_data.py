from elasticsearch import Elasticsearch
import os

# Define the Elasticsearch endpoint and API key
es_endpoint = "https://anime.es.eastus2.azure.elastic-cloud.com"
api_key_id = os.getenv("API_KEY_ID")
api_key_secret = os.getenv("API_KEY_SECRET")

# Initialize the Elasticsearch client with API key authentication
client = Elasticsearch(
    hosts=[es_endpoint],
    api_key=(api_key_id, api_key_secret)
)

# Define sample anime data
anime_data = [
    {
        "ID": "anime1",
        "Title": "Bungou Stray Dogs",
        "Genres": ["Mystery", "Seinen", "Supernatural"],
        "Studio": "Bones",
        "Description": "Nakajima Atsushi was kicked out of his orphanage...",
        "ReleaseDate": "2016-04-07"
        # Add more anime data fields as needed
    },
    {
        "ID": "anime2",
        "Title": "Attack on Titan",
        "Genres": ["Action", "Drama", "Fantasy"],
        "Studio": "Wit Studio",
        "Description": "In a world where humanity resides within enormous walled...",
        "ReleaseDate": "2013-04-06"
        # Add more anime data fields as needed
    },
    # Add more anime data as needed
]

# Index the sample anime data into the "anime" index
index_name = "anime"
for anime in anime_data:
    client.index(index=index_name, body=anime)

# Close the Elasticsearch client when done
client.close()
