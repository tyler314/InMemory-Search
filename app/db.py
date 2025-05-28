import re
from collections import defaultdict
from typing import List, Dict, Set, Any
from app.models import Document


class InMemoryDB(dict):
    _instance = None

    @staticmethod
    def tokenize(document: Document) -> List[str]:
        if not isinstance(document, Document):
            return []
        return re.findall(r"\w+", document.content.lower())

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._deleted_documents = dict()
            cls._instance._inverted_index = defaultdict(set)
        return cls._instance

    def __setitem__(self, doc_id: str, document: Document) -> None:
        if doc_id in self:
            self._remove_from_inverted_index(doc_id)
        self._add_to_inverted_index(doc_id, document)
        super().__setitem__(doc_id, document)

    def _add_to_inverted_index(self, doc_id: str, document: Document) -> None:
        token = InMemoryDB.tokenize(document)
        for word in token:
            self._inverted_index[word].add(doc_id)

    def _remove_from_inverted_index(self, doc_id: str) -> None:
        token = InMemoryDB.tokenize(self[doc_id])
        for word in token:
            self._inverted_index[word].discard(doc_id)

    def delete_document(self, key: str, default: Any = None) -> Document:
        if key in self:
            self._deleted_documents[key] = self[key]
            self._remove_from_inverted_index(key)
        return super().pop(key, default)

    def get_deleted_uids(self) -> List[str]:
        return list(self._deleted_documents.keys())

    def get_doc_ids_by_keyword(self, keyword: str) -> List[str]:
        return list(self._inverted_index.get(keyword.lower(), set()))

    def clear(self):
        super().clear()
        self._inverted_index.clear()
        self._deleted_documents.clear()
