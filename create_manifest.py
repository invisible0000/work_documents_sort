import os
import csv

ROOT_DIR = "test_workspace"
MANIFEST_FILE = "file_manifest.csv"

# CSV 헤더: path, name, extension, content_hint
header = ["path", "name", "extension", "content_hint"]

rows = []

for dirpath, _, filenames in os.walk(ROOT_DIR):
    for fname in filenames:
        rel_dir = os.path.relpath(dirpath, os.getcwd())
        rel_path = os.path.join(rel_dir, fname).replace("\\", "/")
        ext = os.path.splitext(fname)[1]
        content_hint = ""
        if ext == ".txt":
            try:
                with open(os.path.join(dirpath, fname), "r", encoding="utf-8") as f:
                    content_hint = f.readline().strip()
            except Exception:
                content_hint = ""
        rows.append([
            rel_path,
            fname,
            ext,
            content_hint
        ])

with open(MANIFEST_FILE, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"{MANIFEST_FILE} 생성 완료. 총 {len(rows)}개 파일 기록.")
