# src/rag_pipeline.py
import sys
import os
import time

# ----------------- Fix imports for scripts ----------------- #
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "scripts"))
from embeddings_store import EmbeddingStore

# ----------------- Import spatial queries ----------------- #
from spatial_queries import (
    point_in_polygon, nearest_feature, features_in_bbox,
    cities_gdf, rivers_gdf, cities_idx, rivers_idx
)

# ----------------- Utility functions ----------------- #
def slow_print(text, delay=0.02):
    """Print text with a small delay for a polished effect."""
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def divider():
    print("\n" + "-"*60 + "\n")

# ----------------- RAG Pipeline ----------------- #
class RAGPipeline:
    def __init__(self):
        self.store = EmbeddingStore("embeddings_store.json")
        slow_print("✅ Embedding store loaded successfully.")
        divider()

    def query(self, text):
        slow_print(f">> Sample Query: {text}\n")
        retrieved = self.store.search(text, top_k=5)
        results = []
        for identifier, score in retrieved:
            meta = self.store.metadata.get(identifier, {})
            title = meta.get("title", identifier)
            desc = meta.get("description", "")
            results.append((title, desc, score))
        return results

    def annotate_spatial(self, results, query):
        """Highlight nearest rivers or cities mentioned in query."""
        annotated = []
        query_lower = query.lower()
        for title, desc, score in results:
            highlight = ""
            # Check for city mentions
            for city in cities_gdf["name"]:
                if city.lower() in query_lower:
                    highlight = f"✅ Near {city}"
                    break
            # Check for river mentions if no city
            if not highlight:
                for river in rivers_gdf["name"]:
                    if river.lower() in query_lower:
                        highlight = f"✅ Close to {river}"
                        break
            annotated.append(f"{title}: {desc} (score: {score:.4f}) {highlight}".strip())
        return annotated

# ----------------- Main Execution ----------------- #
if __name__ == "__main__":
    divider()
    slow_print("🌐 Welcome to the Geographic RAG Demo\n", delay=0.01)
    
    query_text = input("Enter your query (e.g., 'rivers near Delhi'): ").strip()
    if not query_text:
        query_text = "Tell me about rivers in Asia near Delhi"

    pipeline = RAGPipeline()
    retrieved_results = pipeline.query(query_text)
    annotated_results = pipeline.annotate_spatial(retrieved_results, query_text)

    divider()
    slow_print(">> Generated Answer:", delay=0.01)
    slow_print("Answer based on retrieved context:\n", delay=0.01)
    for idx, ans in enumerate(annotated_results, 1):
        slow_print(f"{idx}. {ans}", delay=0.005)
    slow_print(f"\n(Query: {query_text})")
    divider()

    # ----------------- Spatial Tests ----------------- #
    slow_print(">> Test 1: Point in polygon (Delhi area):")
    cities_found = point_in_polygon(28.6139, 77.2090, cities_gdf, buffer=0.01)
    slow_print(str(cities_found))

    slow_print("\n>> Test 2: Nearest river to Delhi coordinates:")
    nearest_river, dist = nearest_feature(28.6139, 77.2090, rivers_gdf, rivers_idx)
    slow_print(str((nearest_river, dist)))

    slow_print("\n>> Test 3: Features in bounding box around Delhi:")
    bbox_features = features_in_bbox(28.5, 77.0, 28.7, 77.3, cities_gdf)
    slow_print(str(bbox_features))

    divider()
    slow_print("🏁 End of demo.!\n", delay=0.01)
