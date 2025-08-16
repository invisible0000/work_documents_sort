# Python 파일 정리 프로젝트 전체 자동화 작업 지시서

## 🎯 최종 목표
파이썬 가상 환경을 설정하고, 대량의 테스트용 파일을 생성한 후, 이 파일들을 자동으로 분류하고 정리하는 파이썬 스크립트를 작성하여 실행하는 전체 과정을 자동화합니다.

---

### 1단계: 프로젝트 환경 설정 (가상 환경 생성)

1.  **가상 환경 생성**: 현재 프로젝트 루트에 `python -m venv .venv` 명령을 실행하여 `.venv`라는 이름의 파이썬 가상 환경을 만들어 주세요.
2.  **가상 환경 활성화**: 생성된 가상 환경을 활성화하는 터미널 명령어를 알려주세요. (사용자의 OS에 맞춰서 Windows 또는 macOS/Linux용 명령어를 제시)

---

### 2단계: 테스트 데이터 생성

1.  **가짜 파일 생성 스크립트 작성**: 아래의 파이썬 코드를 그대로 사용하여 `create_dummy_files.py` 라는 이름의 파일을 생성해 주세요. 이 스크립트는 `test_workspace` 폴더를 만들고 그 안에 3,000개의 가짜 파일을 생성하는 역할을 합니다.

    ```python
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
    ```

2.  **스크립트 실행**: `create_dummy_files.py` 파일 생성이 완료되면, 터미널에서 `python create_dummy_files.py` 명령을 실행하여 테스트용 파일들을 생성해 주세요.

---

### 3단계: 파일 정리 스크립트 작성 및 실행

1.  **정리 스크립트 생성**: 이제 `test_workspace` 폴더 내의 파일들을 정리할 `file_organizer.py` 스크립트를 **프로젝트 루트**에 생성해 주세요. 아래 지시사항을 따라 코드를 작성합니다.

    * **필수 라이브러리**: `os`, `shutil`, `re`
    * **타겟 디렉토리 변수**: 정리할 대상 폴더를 `TARGET_DIR = "test_workspace"` 로 명시적으로 지정합니다.
    * **프로젝트 맵 정의**: 아래 딕셔너리를 코드에 포함시켜 주세요.
        ```python
        PROJECT_MAP = {
            "QT": "신제품 '퀀텀' 출시",
            "MK": "2025 3분기 마케팅 캠페인",
            "TF": "사내 업무 효율화 TF"
        }
        ```
    * **로직 구현**:
        1. `TARGET_DIR` 내부의 모든 파일을 순회합니다.
        2. `^\d{8}_([A-Z]{2,})_.*` 정규표현식을 사용해 파일명에서 프로젝트 코드(예: "QT")를 추출합니다.
        3. 추출한 코드를 `PROJECT_MAP`에서 찾아, 이동할 폴더의 전체 이름(예: "신제품 '퀀텀' 출시")을 결정합니다.
        4. 목적지 폴더가 `TARGET_DIR` 내에 존재하지 않으면 새로 생성합니다.
        5. `shutil.move()`를 사용해 파일을 해당 목적지 폴더로 이동시킵니다.
        6. 정규식에 매칭되지 않는 파일들은 `TARGET_DIR` 내의 `_Uncategorized` 폴더로 이동시킵니다.
        7. 어떤 파일이 어디로 이동되었는지 터미널에 로그를 출력해 주세요. (예: `[이동] test.docx -> _Uncategorized/test.docx`)

2.  **정리 스크립트 실행**: `file_organizer.py` 작성이 완료되면, 터미널에서 `python file_organizer.py` 명령을 실행하여 파일 정리를 수행해 주세요.

---

### ✅ 최종 확인
모든 단계가 끝나면, `test_workspace` 폴더 안에 `신제품 '퀀텀' 출시`, `2025 3분기 마케팅 캠페인`, `사내 업무 효율화 TF`, `_Uncategorized` 등의 폴더가 생성되고 모든 파일이 각 폴더로 정리되어 있어야 합니다.