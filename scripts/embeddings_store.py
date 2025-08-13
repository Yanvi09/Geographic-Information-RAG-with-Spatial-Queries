# scripts/embeddings_store.py
import os
import json
import numpy as np
from typing import List, Dict
from pathlib import Path


class EmbeddingStore:
    """
    A minimal, offline-friendly embedding store that generates
    deterministic fake embeddings for demo purposes.
    """

    def __init__(self, storage_path: str = "embeddings_store.json"):
        self.storage_path = storage_path
        self.embeddings: Dict[str, List[float]] = {}
        self.metadata: Dict[str, Dict] = {}
        self.load()

    def _fake_generate_embedding(self, text: str) -> List[float]:
        """Generate a deterministic pseudo-embedding for offline demo."""
        np.random.seed(abs(hash(text)) % (2**32))  # stable per text
        return np.random.rand(512).tolist()  # 512-dim vector

    def add_text(self, identifier: str, text: str, meta: Dict = None) -> None:
        embedding = self._fake_generate_embedding(text)
        self.embeddings[identifier] = embedding
        if meta:
            self.metadata[identifier] = meta
        self.save()

    def search(self, query: str, top_k: int = 3):
        """Return top_k (identifier, score) tuples sorted by similarity."""
        if not self.embeddings:
            return []
        query_embedding = self._fake_generate_embedding(query)
        scores = [
            (identifier, self._cosine_similarity(query_embedding, emb))
            for identifier, emb in self.embeddings.items()
        ]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    @staticmethod
    def _cosine_similarity(vec1, vec2) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    def save(self) -> None:
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(
                {"embeddings": self.embeddings, "metadata": self.metadata},
                f,
                ensure_ascii=False,
                indent=2
            )

    def load(self) -> None:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.embeddings = data.get("embeddings", {})
                self.metadata = data.get("metadata", {})
        else:
            self.embeddings = {}
            self.metadata = {}


if __name__ == "__main__":
    # CLI mode: load textual_info.json into the store
    store = EmbeddingStore()
    data_file = Path("data/textual_info.json")

    if data_file.exists():
        with open(data_file, "r", encoding="utf-8") as f:
            records = json.load(f)
            for rec in records:
                text = f"{rec['title']}. {rec['description']}"
                store.add_text(rec["id"], text, meta=rec)
        print(f"✅ Loaded {len(records)} items into {store.storage_path}")
    else:
        print("⚠️ No data/textual_info.json found. Nothing to load.")
