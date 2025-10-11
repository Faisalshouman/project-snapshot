# 🧠 Project Snapshot JSON Exporter

A simple, safe Python tool to extract **the full contents and structure** of a Git repository into a single `.json` file — ideal for:

- AI model training or fine-tuning  
- Project backups or code sharing  
- Offline code review or documentation generation  

---

## 🚀 Features
✅ Captures **tracked + untracked (not ignored)** files  
✅ Preserves **full file content** with UTF-8 encoding  
✅ Clear, AI-friendly JSON structure  
✅ Works on **Windows, macOS, and Linux**  
✅ No dependencies other than Python 3.8+

---

## 🧩 Example Output

```json
[
  {
    "path": "src/main.ts",
    "content": "import { NestFactory } from '@nestjs/core'..."
  },
  {
    "path": "package.json",
    "content": "{\n  \"name\": \"my-app\" ..."
  }
]

⚙️ Usage

Clone or download the repo

Run inside any Git project root:

```

python project_snapshot_json.py

```

Your snapshot file will appear in C:\Users\ADMIN\Desktop\CodexSnapshot (or your chosen directory)

🛠️ Configuration

You can edit:

```
OUTPUT_DIR = r"C:\Users\ADMIN\Desktop\CodexSnapshot"

```

to any desired output path.