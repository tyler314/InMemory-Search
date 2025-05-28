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

### Design Choices
My main design choices revolved around the InMemoryDB class. I decided to make it a singleton, mostly to show that there should only be one instance of this database running at any time, since it's the central in-memory store.

I also had it inherit from Python's dict class. I did this partly to use Python's solid dictionary features. This let me make the modifications I needed while still using a familiar foundation.

Most of the business logic is packed into the InMemoryDB class itself. Outside of that, there are just some if-statements for error handling and a few method calls in routes.py. I kept main.py and routes.py separate to keep the codebase cleaner and better organized.

When it came to unit tests, I tried to be as thorough as possible, but I'm sure I've missed some edge cases. Hopefully, I'll find time to come back and add more tests soon.

Lastly, I used Pydantic to help normalize the documents being stored. It also came in handy for structuring the list of Document IDs that are returned by a couple of the API endpoints, ensuring the data format is consistent.