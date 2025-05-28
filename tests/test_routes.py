import pytest
from app.db import InMemoryDB
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_inmemory_db():
    db = InMemoryDB()
    db.clear()


class TestPostDocuments:
    def test_unprocessable_entity(self):
        response = client.post(
            "/documents/test456",
            json={
                "title": "Another Test",
            },
        )
        assert response.status_code == 422

    def test_valid(self):
        response = client.post("/documents/test456", json={"content": "Some content"})
        assert response.status_code == 200

    def test_overwrite_existing_document(self):
        document_id = "overwrite"
        client.post(f"/documents/{document_id}", json={"content": "initial content"})
        response = client.post(
            f"/documents/{document_id}", json={"content": "new content"}
        )
        assert response.status_code == 200
        # Ensure that new content appears in search
        search_result = client.get("/search?keyword=new").json()
        assert document_id in search_result["document_ids"]


class TestDeleteDocuments:
    def test_deleted_documents_list_matches_deleted(self):
        doc_ids = ["test123", "test456", "test789"]
        for doc_id in doc_ids:
            client.post(
                f"/documents/{doc_id}", json={"content": f"test content {doc_id}"}
            )
            client.delete(f"/documents/{doc_id}")

        response = client.get("/documents/deleted")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "document_ids" in data
        assert set(data["document_ids"]) == set(doc_ids)
        assert data["total"] == len(doc_ids)

    def test_deleted_documents_only_shows_deleted(self):
        deleted_ids = ["del4", "del5"]
        active_ids = ["keep1", "keep2"]

        for doc_id in deleted_ids:
            client.post(f"/documents/{doc_id}", json={"content": f"delete {doc_id}"})
            client.delete(f"/documents/{doc_id}")

        for doc_id in active_ids:
            client.post(f"/documents/{doc_id}", json={"content": f"keep {doc_id}"})

        response = client.get("/documents/deleted")
        assert response.status_code == 200
        result = response.json()
        returned_ids = set(result["document_ids"])

        assert set(deleted_ids) == returned_ids
        assert all(active_id not in returned_ids for active_id in active_ids)
        assert result["total"] == len(deleted_ids)

    def test_get_deleted_documents_when_none_deleted(self):
        client.post("/documents/edgecase1", json={"content": "testing"})
        response = client.get("/documents/deleted")
        assert response.status_code == 200
        assert response.json()["document_ids"] == []

    def test_delete_nonexistent_document(self):
        document_id = "doesnotexist"
        response = client.delete(f"/documents/{document_id}")
        assert response.status_code == 404
        assert response.json() == {
            "detail": {"error": "Document Not Found", "document_id": document_id}
        }

    def test_deleted_documents_do_not_appear_in_search(self):
        client.post("/documents/testdelete", json={"content": "searchable content"})
        client.delete("/documents/testdelete")
        result = client.get("/search?keyword=searchable").json()
        assert "testdelete" not in result


class TestSearchDocuments:
    doc_ids = ["test123", "test456", "test789"]

    def test_search_documents(self):
        for uid in self.doc_ids:
            client.post(f"/documents/{uid}", json={"content": f"test-content-{uid}"})
        document_ids = client.get("/search?keyword=test").json()
        assert len(document_ids) == len(self.doc_ids)

    def test_search_with_nonexistent_keyword(self):
        client.post("/documents/searchtest1", json={"content": "derp"})
        response = client.get("/search?keyword=nonexistent")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_search_matches_whole_word_only(self):
        client.post("/documents/wordtest", json={"content": "hockey  and baseball"})
        client.post("/documents/shouldskip", json={"content": "basketball and soccer"})
        result = client.get("/search?keyword=baseball").json()
        assert "wordtest" in result["document_ids"]
        assert "shouldskip" not in result["document_ids"]
