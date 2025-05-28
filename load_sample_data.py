import json
import requests

API_URL = "http://localhost:8000/documents"

with open("sample_data.json") as f:
    docs = json.load(f)

for doc in docs:
    response = requests.post(f"{API_URL}/{doc['doc_id']}", json={"content": doc["content"]})
    print(f"{doc['doc_id']}: {response.status_code}")
