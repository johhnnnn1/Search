from elasticsearch import Elasticsearch
import os

# Define the Elasticsearch endpoint and API key
es_endpoint = "https://your-elasticsearch-endpoint"
api_key_id = os.getenv("YOUR_API_KEY_ID")
api_key_secret = os.getenv("YOUR_API_KEY_SECRET")

# Initialize the Elasticsearch client with API key authentication
client = Elasticsearch(
    hosts=[es_endpoint],
    api_key=(api_key_id, api_key_secret)
)

# Define the index settings and mappings for anime
anime_index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "Title": {"type": "text"},
            "Genres": {"type": "keyword"},
            "Studio": {"type": "keyword"},
            "Description": {"type": "text"},
            "ReleaseDate": {"type": "date"}
            # Add other fields as needed
        }
    }
}

# Create the "anime" index
anime_index_name = "anime"

if not client.indices.exists(index=anime_index_name):
    client.indices.create(index=anime_index_name, body=anime_index_settings)
    print(f"Index '{anime_index_name}' created successfully.")
else:
    print(f"Index '{anime_index_name}' already exists.")

# Close the Elasticsearch client when done
client.close()
