# project_snapshot_json.py
import os
import subprocess
import json
from datetime import datetime

# === CONFIG ===
OUTPUT_DIR = r"C:\Users\ADMIN\Desktop\CodexSnapshot"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"project_snapshot_{timestamp}.json")

# === Ensure repo ===
if not os.path.isdir(".git"):
    print("❌ This directory is not a git repository.")
    exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Utility to run git commands ===
def run_git(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout.splitlines()

# === Collect files ===
tracked = run_git("git ls-files")
untracked = run_git("git ls-files --others --exclude-standard")
all_files = sorted(set(tracked + untracked))

# === Read files safely ===
snapshot = []
for path in all_files:
    file_entry = {"path": path, "content": None}
    try:
        with open(path, "rb") as f:
            data = f.read()
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = data.decode("latin-1", errors="replace")
        file_entry["content"] = text
    except Exception as e:
        file_entry["content"] = f"⚠️ Could not read file: {e}"
    snapshot.append(file_entry)

# === Write to JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    json.dump(snapshot, out, ensure_ascii=False, indent=2)

print("✅ Project snapshot created successfully!")
print(f"📄 JSON file: {OUTPUT_FILE}")
print(f"📦 Total files captured: {len(snapshot)}")
