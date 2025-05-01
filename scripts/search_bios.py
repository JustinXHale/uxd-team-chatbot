from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance
from qdrant_client.http.models import SearchRequest
import sys
import warnings

# Suppress deprecation warnings from Qdrant
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

# Collection name
collection_name = "uxd-team-bios"

def query_bios(question, top_k=3, show_summary=False):
    query_vector = model.encode(question).tolist()

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
        start_date = r.payload.get("start_date", "Not listed")
        location = r.payload.get("location", "Unknown")
        team = r.payload.get("team", "Not listed")
        email = r.payload.get("email", "N/A")
        github = r.payload.get("github", "N/A")
        bio = r.payload.get("bio", "No bio available")
        interests = r.payload.get("interests", [])
        fun_facts = r.payload.get("fun_facts", [])
        image = r.payload.get("image", "N/A")
        raw_md = r.payload.get("raw_md", "No raw markdown available")

        interests_str = ", ".join(interests) if interests else "Not listed"
        fun_facts_str = "; ".join(fun_facts) if fun_facts else "None provided"

        print(f" {name} ({title})")
        print(f" Location: {location}")
        print(f" Start Date: {start_date}")
        print(f" Team: {team}")
        print(f" Email: {email}")
        print(f" GitHub: {github}")
        print(f" Interests: {interests_str}")
        print(f" Fun Fact: {fun_facts_str}")
        print(f"📝 Bio Preview: {bio[:180]}...")
        print(f"🖼️ Image: {image}")

        if show_summary:
            summary = (
                f"\n📋 Summary:\n"
                f"{name} is a {title} at Red Hat. "
                f"They are located in {location} and part of the {team} team. "
                f"Their interests include {interests_str.lower()}. "
                f"Fun fact: {fun_facts_str}.\n\n"
                f"Bio:\n{bio}\n"
            )
            print(summary)

        # Optional: Print raw markdown if debugging
        # print(f"\n🧾 Raw Markdown:\n{raw_md}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❗️Please provide a search query.")
        print("Usage: python search_bios.py 'your question here'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    show_summary = any(keyword in question.lower() for keyword in ["summary", "full bio", "full markdown"])
    query_bios(question, show_summary=show_summary)
