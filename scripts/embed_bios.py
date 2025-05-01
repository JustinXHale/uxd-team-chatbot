import os
import yaml
import markdown
import re
import uuid
import json
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
    print(f"⚠️ Resetting collection: {collection_name}")
    client.delete_collection(collection_name=collection_name)
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE),
    )
    try:
        os.remove(".embed_cache.json")
        print("🗑️ Removed .embed_cache.json to rescan all bios.")
    except FileNotFoundError:
        print("ℹ️ No .embed_cache.json found. All bios will be embedded fresh.")
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
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if content.startswith("---"):
        _, frontmatter, body = content.split("---", 2)
        data = yaml.safe_load(frontmatter)
    else:
        raise ValueError("Markdown file missing frontmatter")

    return data, markdown_to_text(body), content  # returning full raw content too

# Load embed cache or prepare for full embedding
embed_cache = {}
force_all = False
embed_cache_path = Path(".embed_cache.json")

if embed_cache_path.exists():
    with open(embed_cache_path) as f:
        embed_cache = json.load(f)
else:
    force_all = True
    print("📂 No .embed_cache.json found — embedding all bios.")

# Loop through all markdown files in bios/
bios_dir = Path("bios")
updated_cache = {}
embedded_count = 0

for md_file in bios_dir.glob("**/bio.md"):
    print(f"\n📄 Processing {md_file}...")

    # Check file modification time
    last_modified = os.path.getmtime(md_file)
    if not force_all and str(md_file) in embed_cache:
        if embed_cache[str(md_file)] == last_modified:
            print(f"⏩ Skipping {md_file.name}, unchanged.")
            continue

    try:
        data, text, raw_md = load_bio_markdown(md_file)
        embedding_text = f"{data['title']} {data['bio']}"
        embedding = model.encode(embedding_text).tolist()

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "name": data.get("name", ""),
                "title": data.get("title", ""),
                "start_date": data.get("start date", ""),
                "location": data.get("location", ""),
                "team": data.get("team", ""),
                "email": data.get("email", ""),
                "github": data.get("github", ""),
                "interests": data.get("interests", []),
                "fun_facts": data.get("fun_facts", []),
                "bio": data.get("bio", ""),
                "image": data.get("image", ""),
                "raw_md": raw_md  # <- full markdown included
            }
        )

        client.upsert(collection_name=collection_name, points=[point])
        updated_cache[str(md_file)] = last_modified
        embedded_count += 1
        print(f"✅ Embedded and stored bio for {data['name']}")

    except Exception as e:
        print(f"❌ Failed to process {md_file.name}: {e}")

# Save updated cache
with open(embed_cache_path, "w") as f:
    json.dump(updated_cache, f)

print(f"\n🔄 Done. {embedded_count} bio(s) embedded.")
