import csv
import random
import os

# --- 설정값 ---
TOTAL_FILES = 3000
OUTPUT_CSV_FILE = 'dummy_file_manifest.csv'
TARGET_DIRECTORY = 'test_environment' # 더미 파일들이 생성될 최상위 폴더

# --- 데이터 풀 ---
PROJECT_NAMES = [
    '알파 프로젝트', '브라보 프로젝트', '찰리 프로젝트', '델타 기획', '에코 시스템',
    '폭스트롯 분석', '골프 개발', '호텔 설계', '인디아 솔루션', '줄리엣 연구',
    '킬로 보안', '리마 마케팅', '마이크 데이터', '노벰버 보고', '오스카 TF',
    '파파 계약', '퀘벡 품질관리', '로미오 영업', '시에라 재무', '탱고 고객지원'
]

CATEGORIES = {
    '기획서': ['기획', '제안', '아이디어', '로드맵', '전략'],
    '보고서': ['결과', '분석', '실적', '현황', '리포트'],
    '계약서': ['계약', '협약', 'NDA', 'MOU', '법률'],
    '디자인': ['시안', '목업', 'UIUX', '스케치', '프로토타입'],
    '개발': ['코드', '소스', '빌드', '라이브러리', 'API'],
    '회의록': ['회의', '논의', '결정사항', '참석자', '안건'],
    '재무': ['예산', '지출', '견적서', '세금계산서', '인보이스'],
    '인사': ['채용', '평가', '이력서', '조직도', '휴가'],
    '마케팅': ['광고', '캠페인', '프로모션', '성과', '보도자료']
}

FILE_EXTENSIONS = {
    '기획서': ['.pptx', '.docx', '.pdf'],
    '보고서': ['.docx', '.pdf', '.xlsx'],
    '계약서': ['.pdf', '.docx', '.hwp'],
    '디자인': ['.jpg', '.png', '.ai', '.psd', '.sketch'],
    '개발': ['.zip', '.py', '.js', '.sql', '.java'],
    '회의록': ['.docx', '.txt', '.md'],
    '재무': ['.xlsx', '.pdf', '.csv'],
    '인사': ['.docx', '.pdf', '.xlsx'],
    '마케팅': ['.pptx', '.pdf', '.jpg']
}

# 혼란을 주기 위한 이름 형식
CONFUSING_NAME_FORMATS = [
    "{category}_{project}_최종",
    "보고자료_{date}",
    "외부자료_{project_short}",
    "백업_{date}_{category}",
    "임시_{random_word}",
    "정리필요_{category}",
    "Final_{category}_{project}",
    "Copy of {category}_{date}"
]

# --- 함수 정의 ---

def get_random_element(data_list):
    """리스트에서 무작위 요소를 반환"""
    return random.choice(data_list)

def generate_messy_filepath(project_name, category):
    """지저분한 파일 경로 및 이름을 생성"""
    # 50% 확률로 프로젝트 폴더에, 30%는 카테고리 폴더에, 20%는 루트에 생성
    rand_val = random.random()
    if rand_val < 0.5:
        path = os.path.join(TARGET_DIRECTORY, project_name.replace(' ', '_'))
    elif rand_val < 0.8:
        path = os.path.join(TARGET_DIRECTORY, category)
    else:
        path = TARGET_DIRECTORY

    # 30% 확률로 혼란스러운 이름 생성
    if random.random() < 0.3:
        date_str = f"2024{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
        project_short_name = project_name.split(' ')[0]
        random_word = random.choice(['자료', '문서', '파일', '보고'])
        name_format = get_random_element(CONFUSING_NAME_FORMATS)
        file_name_base = name_format.format(
            category=category,
            project=project_name.replace(' ', '_'),
            date=date_str,
            project_short=project_short_name,
            random_word=random_word
        )
    else:
        # 일반적인 이름 생성
        file_name_base = f"{project_name} {category}"

    # 파일명 중복을 피하기 위해 숫자 추가
    file_name_base += f"_{random.randint(100, 999)}"
    
    extension = get_random_element(FILE_EXTENSIONS[category])
    file_name = file_name_base + extension

    return path, file_name

def generate_manifest_file():
    """메인 함수: CSV 매니페스트 파일을 생성"""
    header = ['project_name', 'category', 'file_path', 'file_name', 'keywords']
    
    with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for _ in range(TOTAL_FILES):
            project = get_random_element(PROJECT_NAMES)
            category = get_random_element(list(CATEGORIES.keys()))
            
            path, name = generate_messy_filepath(project, category)
            
            # 파일 내용에 포함될 키워드 생성 (프로젝트명 + 카테고리 관련 키워드 2개)
            keywords = [project] + random.sample(CATEGORIES[category], 2)
            keywords_str = ', '.join(keywords)
            
            writer.writerow([project, category, path, name, keywords_str])

    print(f"'{OUTPUT_CSV_FILE}' 파일이 성공적으로 생성되었습니다. ({TOTAL_FILES}개 파일 정보)")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    generate_manifest_file()
