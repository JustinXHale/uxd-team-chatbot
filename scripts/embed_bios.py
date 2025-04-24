import os
import yaml
import markdown
import re
import uuid
import argparse
import json
from pathlib import Path
from datetime import datetime
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

# Load cache of last embed times
cache_path = Path(".cache.json")
if cache_path.exists():
    with open(cache_path, "r") as f:
        cache = json.load(f)
else:
    cache = {}

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

# Loop through all bio.md files
bios_dir = Path("bios")
updated = 0

for md_file in bios_dir.glob("*/bio.md"):
    modified_time = md_file.stat().st_mtime
    last_cached = cache.get(str(md_file), 0)

    if modified_time <= last_cached:
        continue  # Skip unchanged files

    print(f"\n📄 Processing {md_file}...")

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
        cache[str(md_file)] = modified_time
        updated += 1
        print(f"✅ Embedded and stored bio for {data['name']}")

    except Exception as e:
        print(f"❌ Failed to process {md_file}: {e}")

# Save updated cache
with open(cache_path, "w") as f:
    json.dump(cache, f)

if updated == 0:
    print("\n📦 No new or updated bios to embed.")
else:
    print(f"\n🔄 Done. {updated} bio(s) embedded.")
