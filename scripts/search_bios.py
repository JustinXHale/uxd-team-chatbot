from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance
from qdrant_client.http.models import SearchRequest
import sys
import warnings

# Can remove later just to reprove the deprecation warning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Collection name
collection_name = "uxd-team-bios"

def query_bios(question, top_k=3):
    # Turn the user question into an embedding vector
    query_vector = model.encode(question).tolist()

    # Use Qdrant's original search method (simple and works well locally)
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )

    print(f"\n🔍 Results for: '{question}'\n")
    if not results:
        print("No matching bios found.")
        return

    for r in results:
        name = r.payload.get("name", "Unknown")
        title = r.payload.get("title", "N/A")
        location = r.payload.get("location", "Unknown")
        bio = r.payload.get("bio", "No bio available")

        print(f"👤 {name} ({title})")
        print(f"📍 {location}")
        print(f"📝 {bio[:180]}...\n")  # Limit to 180 chars for clean output

if __name__ == "__main__":
    # Get the user's question from command-line arguments
    if len(sys.argv) < 2:
        print("❗️Please provide a search query.")
        print("Usage: python search_bios.py 'your question here'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    query_bios(question)
