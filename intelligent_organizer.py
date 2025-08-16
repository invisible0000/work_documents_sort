import os
import csv
import re
import shutil

TARGET_DIR = "test_workspace"
MANIFEST_FILE = "file_manifest.csv"
PROJECT_MAP = {
    "QT": "신제품 '퀀텀' 출시",
    "MK": "2025 3분기 마케팅 캠페인",
    "TF": "사내 업무 효율화 TF"
}
PROJECT_KEYWORDS = {
    "QT": "신제품 '퀀텀' 출시",
    "MK": "2025 3분기 마케팅 캠페인",
    "TF": "사내 업무 효율화 TF"
}

# Phase 2-1: 메타데이터 분석
pattern = re.compile(r"^\d{8}_([A-Z]{2,})_.*")
name_pattern_count = 0
content_hint_count = 0
other_count = 0

with open(MANIFEST_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    manifest = list(reader)
    for row in manifest:
        name = row["name"]
        content_hint = row["content_hint"]
        m = pattern.match(name)
        if m:
            name_pattern_count += 1
        elif any(keyword in content_hint for keyword in PROJECT_KEYWORDS.values()):
            content_hint_count += 1
        else:
            other_count += 1

print(f"[분석] 파일명 패턴 매칭: {name_pattern_count}개")
print(f"[분석] 콘텐츠 힌트 매칭: {content_hint_count}개")
print(f"[분석] 기타(미분류): {other_count}개")

# Phase 2-2: 지능형 정리 스크립트
moved_count = {v: 0 for v in PROJECT_MAP.values()}
moved_count["_Uncategorized"] = 0

for row in manifest:
    rel_path = row["path"]
    name = row["name"]
    ext = row["extension"]
    content_hint = row["content_hint"]
    src = os.path.join(os.getcwd(), rel_path)
    m = pattern.match(name)
    dest_dir = None
    if m:
        code = m.group(1)
        proj_name = PROJECT_MAP.get(code)
        if proj_name:
            dest_dir = os.path.join(TARGET_DIR, proj_name)
    elif any(keyword in content_hint for keyword in PROJECT_KEYWORDS.values()):
        for code, keyword in PROJECT_KEYWORDS.items():
            if keyword in content_hint:
                dest_dir = os.path.join(TARGET_DIR, keyword)
                break
    if not dest_dir:
        dest_dir = os.path.join(TARGET_DIR, "_Uncategorized")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    dest = os.path.join(dest_dir, name)
    if os.path.abspath(src) != os.path.abspath(dest):
        try:
            shutil.move(src, dest)
            print(f"[이동] {rel_path} -> {os.path.relpath(dest, TARGET_DIR)}")
            key = os.path.basename(dest_dir)
            if key in moved_count:
                moved_count[key] += 1
            else:
                moved_count[key] = 1
        except Exception as e:
            print(f"[오류] {rel_path} 이동 실패: {e}")

# Phase 3: 최종 결과 보고
print("\n[최종 결과 요약]")
for k, v in moved_count.items():
    print(f"{k}: {v}개 파일 정리됨")
