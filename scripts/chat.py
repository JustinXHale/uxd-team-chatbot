import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Qdrant
client = QdrantClient(host="localhost", port=6333)

collection_name = "uxd-team-bios"

def search_bios(question, top_k=3):
    query_vector = model.encode(question).tolist()
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k
    )

    # Optionally filter by name if mentioned in the query
    name_keywords = ["justin", "allison", "hale", "wolfe"]  # Add more team names here
    if any(word in question.lower() for word in name_keywords):
        filtered = []
        for r in results:
            name = r.payload.get("name", "").lower()
            if any(word in name for word in question.lower().split()):
                filtered.append(r)
        if filtered:
            results = filtered

    if not results:
        return "No matching bios found."

    responses = []
    for r in results:
        name = r.payload.get("name", "Unknown")
        title = r.payload.get("title", "N/A")
        location = r.payload.get("location", "Unknown")
        bio = r.payload.get("bio", "")
        image = r.payload.get("image", None)

        summary = (
            f"👤 {name} ({title})\n"
            f"📍 {location}\n"
            f"📝 {bio[:180]}..."
        )

        if image:
            summary += f"\n🖼️ {image}"

        responses.append(summary)

    return "\n\n".join(responses)


def main():
    print("💬 UXD Chatbot — Ask about your team (type '/exit' to quit)")
    while True:
        query = input("> ").strip()

        if query.lower() in ["/exit", "exit", "quit", "/quit"]:
            print("👋 Goodbye!")
            break
        elif query.lower() in ["/help", "help"]:
            print("Type a question about the team. Example: 'Who is a content designer?'\nType '/exit' to quit.")
            continue

        print()
        response = search_bios(query)
        print(response)
        print()

if __name__ == "__main__":
    main()
