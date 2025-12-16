import os
import yaml
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(BASE_DIR, "BucketList.md")

EXCLUDE_DIRS = {"Templates", "__pycache__"}
VALID_EXT = ".yaml"

entries = []

for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

    for file in files:
        if not file.endswith(VALID_EXT):
            continue

        file_path = os.path.join(root, file)

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception:
            continue

        if not isinstance(data, dict):
            continue

        # Resolve author/director gracefully
        creator = (
            data.get("author")
            or data.get("director")
            or "—"
        )

        status = data.get("status", {})

        entries.append({
            "id": data.get("id", ""),
            "title": data.get("title", ""),
            "type": data.get("type", ""),
            "category": data.get("category", ""),
            "genres": ", ".join(data.get("genres", [])),
            "creator": creator,
            "consumed": "Yes" if status.get("consumed") else "No",
            "completed": "Yes" if status.get("completed") else "No",
            "rating": data.get("meta", {}).get("rating", "—"),
        })

# Sort for stable output
entries.sort(key=lambda x: (x["type"], x["title"]))

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("# 📚 Bucket List\n\n")
    out.write("_Auto-generated from YAML entries_\n\n")
    out.write(f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n\n")

    if not entries:
        out.write("No entries found.\n")
    else:
        out.write(
            "| ID | Title | Type | Category | Genres | Author / Director | "
            "Consumed | Completed | Rating |\n"
        )
        out.write(
            "|----|-------|------|----------|--------|-------------------|"
            "----------|------------|--------|\n"
        )

        for e in entries:
            out.write(
                f"| {e['id']} | {e['title']} | {e['type']} | "
                f"{e['category']} | {e['genres']} | {e['creator']} | "
                f"{e['consumed']} | {e['completed']} | {e['rating']} |\n"
            )

print(f"[+] BucketList.md generated at: {OUTPUT_FILE}")

