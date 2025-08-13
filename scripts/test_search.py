# scripts/test_search.py
from colorama import Fore, Style, init
from embeddings_store import EmbeddingStore


init(autoreset=True)


def test_embedding_store():
    store = EmbeddingStore()

    if not store.embeddings:
        print(Fore.YELLOW + "⚠️ No embeddings found. Run embeddings_store.py first.")
        return

    query = "Tell me about famous rivers in Asia."
    results = store.search(query, top_k=3)

    print(Fore.CYAN + "\n🔍 Search Query:" + Style.RESET_ALL, query)
    print(Fore.GREEN + "Top Matches:" + Style.RESET_ALL)
    for identifier, score in results:
        meta = store.metadata.get(identifier, {})
        title = meta.get("title", "Unknown")
        desc = meta.get("description", "")
        print(f"{Fore.MAGENTA}- {title} ({score:.4f})")
        print(f"  {Style.DIM}{desc}\n")


if __name__ == "__main__":
    test_embedding_store()
