import os
import yaml
import markdown
import re
import uuid
import argparse
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local Qdrant instance
client = QdrantClient(host="localhost", port=6333)

# Collection name
collection_name = "uxd-team-bios"

# CLI args parser
parser = argparse.ArgumentParser()
parser.add_argument("--reset", action="store_true", help="Reset Qdrant collection before embedding")
args = parser.parse_args()

# Optional: Reset the collection
if args.reset:
    print("⚠️ Resetting collection:", collection_name)
    client.delete_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
else:
    if not client.collection_exists(collection_name=collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

# Markdown to plain text
def markdown_to_text(md):
    text = markdown.markdown(md)
    text = re.sub(r"<[^>]+>", "", text)  # Strip HTML tags
    return text.strip()

# Load and parse markdown
def load_bio_markdown(file_path):
    with open(file_path, "r") as f:
        content = f.read()

    if content.startswith("---"):
        _, frontmatter, body = content.split("---", 2)
        data = yaml.safe_load(frontmatter)
    else:
        raise ValueError("Markdown file missing frontmatter")

    return data, markdown_to_text(body)

# Loop through all markdown files in bios/
bios_dir = Path("bios")

for md_file in bios_dir.glob("*/bio.md"):
    print(f"\n📄 Processing {md_file.name}...")

    try:
        data, text = load_bio_markdown(md_file)
        embedding_text = f"{data['title']} {data['bio']}"
        embedding = model.encode(embedding_text).tolist()

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "name": data["name"],
                "title": data["title"],
                "location": data["location"],
                "bio": data["bio"]
            }
        )

        client.upsert(collection_name=collection_name, points=[point])
        print(f"✅ Embedded and stored bio for {data['name']}")

    except Exception as e:
        print(f"❌ Failed to process {md_file.name}: {e}")
