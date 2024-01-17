import requests

anime_id = "anime1"

response = requests.delete(f"http://localhost:5000/api/animes/{anime_id}")
print(response.status_code)
print(response.json())
