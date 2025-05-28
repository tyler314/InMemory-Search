## Run the app with Docker

```bash
docker-compose up
```

## Upload sample_data.json
```bash
python load_sample_data.py
```
### OR

## 1. Add or update a document
```bash
curl -X POST "http://localhost:8000/documents/spam1" \
     -H "Content-Type: application/json" \
     -d '{"content": "Spam spam spam spam. Lovely spam! Wonderful spam!"}'
```
### Example Response:
```json
{
  "status": "document added",
  "document_id": "spam1"
}
```

## 2. Delete a document from the active corpus
```bash
curl -X DELETE "http://localhost:8000/documents/spam1"
```
### Example Response:
```json
{
  "status":"deleted",
  "document_id":"spam1"
}
```


## 3. Return a list of all deleted document IDs
```bash
curl "http://localhost:8000/documents/deleted"
```
### Example Response:
```json
{
  "status":200,
  "total":1,
  "document_ids":["spam1"]
}
```

## 4. Return a list of document IDs that contain the keyword
```bash
curl "http://localhost:8000/search?keyword=spam"
```
### Example Response:
```json
{
  "status": 200,
  "total": 1,
  "document_ids": ["spam1"]
}
```
