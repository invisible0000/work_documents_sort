import os
import random
from datetime import datetime, timedelta

# --- 설정값 ---
ROOT_DIR = "test_workspace"
NUM_FILES = 3000
CHAOS_FACTOR = 0.3  # 30%의 파일은 루트 폴더에 생성 (무질서 비율)

# 프로젝트 정의
PROJECTS = {
    "QT": {
        "name": "신제품 '퀀텀' 출시",
        "keywords": ["신제품", "퀀텀", "기획", "로드맵", "스펙", "UI/UX"],
        "doc_types": ["기획안", "요구사항정의서", "디자인시안", "개발일정"]
    },
    "MK": {
        "name": "2025 3분기 마케팅 캠페인",
        "keywords": ["마케팅", "캠페인", "광고", "SNS", "성과", "ROI", "예산"],
        "doc_types": ["캠페인제안서", "광고시안", "결과보고서", "예산안"]
    },
    "TF": {
        "name": "사내 업무 효율화 TF",
        "keywords": ["자동화", "프로세스", "개선", "만족도", "설문"],
        "doc_types": ["개선안", "설문결과", "회의록", "발표자료"]
    }
}

FILE_EXTS = {
    "기획안": [".pptx", ".docx"], "요구사항정의서": [".docx"], "디자인시안": [".jpg", ".png"],
    "개발일정": [".xlsx"], "캠페인제안서": [".pdf"], "광고시안": [".jpg"], "결과보고서": [".xlsx"],
    "예산안": [".xlsx"], "개선안": [".docx"], "설문결과": [".xlsx"], "회의록": [".txt"], "발표자료": [".pptx"]
}

def create_files():
    if not os.path.exists(ROOT_DIR):
        os.makedirs(ROOT_DIR)
    print(f"'{ROOT_DIR}' 폴더에 {NUM_FILES}개의 가짜 파일 생성을 시작합니다...")
    for i in range(NUM_FILES):
        p_code = random.choice(list(PROJECTS.keys()))
        project = PROJECTS[p_code]
        doc_type = random.choice(project["doc_types"])
        ext = random.choice(FILE_EXTS.get(doc_type, [".txt"]))
        rand_date = datetime.now() - timedelta(days=random.randint(0, 365))
        date_str = rand_date.strftime("%Y%m%d")
        version = f"_v{random.randint(1, 3)}.{random.randint(0, 5)}" if random.random() > 0.3 else ""
        filename = f"{date_str}_{p_code}_{doc_type}{version}{ext}"
        content = f"이 문서는 '{project['name']}' 프로젝트의 '{doc_type}'입니다.\n주요 키워드: {', '.join(project['keywords'])}."
        # Chaos Factor 적용
        target_dir = ROOT_DIR
        if random.random() > CHAOS_FACTOR:
            project_folder = os.path.join(ROOT_DIR, project["name"])
            if not os.path.exists(project_folder):
                os.makedirs(project_folder)
            target_dir = project_folder
        try:
            with open(os.path.join(target_dir, filename), "w", encoding="utf-8") as f: f.write(content)
        except OSError: continue
    print("파일 생성이 완료되었습니다.")

if __name__ == "__main__":
    create_files()
