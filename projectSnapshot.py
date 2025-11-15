#!/usr/bin/env python3
"""
project_snapshot_full.py
------------------------------------------------------------
Creates a COMPLETE JSON snapshot of your project:
  - Full file structure (every folder, every file)
  - Full text content (UTF-8)
  - Base64 for binary files
  - Skips unnecessary folders (public, node_modules, docs, prisma/migrations)
"""

import os
import json
import base64
from pathlib import Path
from datetime import datetime

# =========================
# CONFIGURATION
# =========================

OUTPUT_DIR = r"C:\Users\ADMIN\Desktop\CodexSnapshot"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"project_snapshot_full_{timestamp}.json")

# ---- Directories to skip entirely (your request + defaults)
EXCLUDED_DIRS = {
    "node_modules",
    ".git",
    ".next",
    "public",
    "coverage",
    "dist",
    "build",
    "out",
    "tmp",
    "docs",
    "__pycache__",
    ".turbo",
    ".vscode",
    ".idea",
    "prisma/migrations",     # ❗ explicit skip
}

# ---- Max file size (None = unlimited)
MAX_FILE_SIZE_BYTES = None

# ---- Whether to include binary files (base64 encoded)
INCLUDE_BINARIES = True
BASE64_BINARY_CONTENT = True


# =========================
# HELPERS
# =========================

def is_excluded(path: Path) -> bool:
    """Check if this path should be skipped."""
    parts = {str(p).replace("\\", "/") for p in path.parts}
    full_path_str = str(path).replace("\\", "/")

    for exc in EXCLUDED_DIRS:
        if full_path_str.startswith(exc) or exc in parts:
            return True
    return False


def is_binary(data: bytes) -> bool:
    """Heuristic binary detection."""
    if b"\x00" in data[:800]:
        return True
    text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} |
                           set(range(0x20, 0x7F)))
    non_text = sum(c not in text_chars for c in data[:1000])
    return non_text > 0.30


# =========================
# EXECUTION
# =========================

snapshot = {
    "generatedAt": timestamp,
    "root": str(Path(".").resolve()),
    "files": []
}

root = Path(".").resolve()

for path in root.rglob("*"):
    # Skip directories
    if path.is_dir():
        if is_excluded(path.relative_to(root)):
            continue
        continue

    rel = path.relative_to(root)

    # Skip any file inside excluded folders
    if is_excluded(rel):
        continue

    # Skip by size if configured
    if MAX_FILE_SIZE_BYTES and path.stat().st_size > MAX_FILE_SIZE_BYTES:
        continue

    entry = {
        "path": str(rel),
        "ext": path.suffix.lower(),
        "sizeBytes": path.stat().st_size,
        "binary": False,
    }

    try:
        data = path.read_bytes()
    except Exception as e:
        entry["error"] = f"Could not read file: {e}"
        snapshot["files"].append(entry)
        continue

    # Detect binary
    if is_binary(data):
        entry["binary"] = True

        if INCLUDE_BINARIES and BASE64_BINARY_CONTENT:
            entry["content_base64"] = base64.b64encode(data).decode("utf-8")
        else:
            entry["content"] = None
    else:
        try:
            entry["content"] = data.decode("utf-8")
        except UnicodeDecodeError:
            entry["content"] = data.decode("latin-1", errors="replace")

    snapshot["files"].append(entry)


# =========================
# OUTPUT
# =========================

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(snapshot, f, indent=2, ensure_ascii=False)

print("✅ FULL snapshot created!")
print(f"📄 Saved to: {OUTPUT_FILE}")
print(f"📁 Files included: {len(snapshot['files'])}")
print(f"🗃️  Skipped directories: {', '.join(EXCLUDED_DIRS)}")
