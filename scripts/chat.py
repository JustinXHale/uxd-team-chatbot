import sys
import requests
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Load embedding model
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
    return results

def call_ollama(prompt):
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that only answers questions using the team bios. "
                    "Do not make up facts or add your own knowledge. "
                    "If the bios don’t include the answer, say 'I don’t know based on the bios.' "
                    "Write your answer clearly and simply, like you are talking to someone in 5th grade. "
                    "Avoid long words or complicated explanations."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["message"]["content"].strip()

def main():
    print(" UXD Chatbot — Ask about your team (type '/exit' to quit)")
    while True:
        query = input("> ").strip()
        if query.lower() in ["/exit", "exit", "quit", "/quit"]:
            print("👋 Goodbye!")
            break
        elif query.lower() in ["/help", "help"]:
            print("Type a question about the team. Example: 'Who is a content designer?'\nType '/exit' to quit.")
            continue

        results = search_bios(query)
        if not results:
            print("No matching bios found.")
            continue

        # Handle full bio or summary-type queries
        if any(phrase in query.lower() for phrase in ["summary", "full bio", "bio of", "tell me about", "full markdown", "original bio"]):
            name_keywords = query.lower()
            for phrase in ["summary", "full bio", "bio of", "tell me about", "full markdown", "original bio"]:
                name_keywords = name_keywords.replace(phrase, "")
            name_keywords = name_keywords.strip().split()

            matched = None
            for r in results:
                name = r.payload.get("name", "").lower()
                if all(word in name for word in name_keywords):
                    matched = r
                    break

            if matched:
                payload = matched.payload
                name = payload.get("name", "Unknown")
                title = payload.get("title", "N/A")
                start_date = payload.get("start date", "Not listed")
                location = payload.get("location", "Unknown")
                team = payload.get("team", "Not listed")
                email = payload.get("email", "N/A")
                github = payload.get("github", "N/A")
                interests = payload.get("interests", [])
                fun_facts = payload.get("fun_facts", [])
                bio = payload.get("bio", "No bio available")
                image = payload.get("image", "N/A")

                interests_str = "\n  - " + "\n  - ".join(interests) if interests else "  - Not listed"
                fun_facts_str = "\n  - " + "\n  - ".join(fun_facts) if fun_facts else "  - None listed"

                print(f"\n📋 Full Bio for {name}\n")
                print(f" Name: {name}")
                print(f" Location: {location}")
                print(f" Start Date: {start_date}")
                print(f" Team: {team}")
                print(f" Email: {email}")
                print(f" GitHub: {github}")
                print(f" Interests: {interests_str}")
                print(f" Fun Facts: {fun_facts_str}\n")
                print(f" Bio: {bio}")
                print(f"🖼️ Image: {image}\n")
                continue

        # Otherwise, run RAG prompt to Ollama
        bios = []
        for r in results:
            name = r.payload.get("name", "Unknown")
            title = r.payload.get("title", "N/A")
            location = r.payload.get("location", "Unknown")
            bio = r.payload.get("bio", "")
            interests = r.payload.get("interests", [])
            fun_facts = r.payload.get("fun_facts", [])

            summary = (
                f"{name} is a {title} based in {location}.\n"
                f"Bio: {bio}\n"
                f"Interests: {', '.join(interests) if interests else 'Not listed'}.\n"
                f"fun_facts: {', '.join(fun_facts) if fun_facts else 'None listed.'}\n"
            )
            bios.append(summary)

        full_prompt = (
            f"Team bios:\n{''.join(bios)}\n\n"
            f"User question: {query}\n\n"
            f"Answer based only on the bios above:"
        )
        answer = call_ollama(full_prompt)
        print(answer)
        print()

if __name__ == "__main__":
    main()
