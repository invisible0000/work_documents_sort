import os
import pandas as pd
import shutil

# --- 설정 ---
CHUNK_FILE_PATH = 'manifest_chunks/chunk_001.csv'
ORGANIZED_ROOT_DIR = 'organized_files'
PROJECT_FULL_NAMES = {
    '알파': '알파 프로젝트', '브라보': '브라보 프로젝트', '찰리': '찰리 프로젝트', 
    '델타': '델타 기획', '에코': '에코 시스템', '폭스트롯': '폭스트롯 분석', 
    '골프': '골프 개발', '호텔': '호텔 설계', '인디아': '인디아 솔루션', 
    '줄리엣': '줄리엣 연구', '킬로': '킬로 보안', '리마': '리마 마케팅', 
    '마이크': '마이크 데이터', '노벰버': '노벰버 보고', '오스카': '오스카 TF', 
    '파파': '파파 계약', '퀘벡': '퀘벡 품질관리', '로미오': '로미오 영업', 
    '시에라': '시에라 재무', '탱고': '탱고 고객지원'
}
CATEGORIES = ['개발', '계약서', '기획서', '디자인', '보고서', '인사', '재무', '회의록', '마케팅']

def get_project_and_category_from_filename(filename):
    """파일 이름에서 프로젝트명과 카테고리를 추출 (Copilot의 휴리스틱 기반)"""
    
    found_project = "Uncategorized"
    found_category = "Etc"

    # 가장 긴 프로젝트 이름부터 확인하여 정확도 높임
    # 예: '골프 개발'이 '골프'보다 먼저 확인되도록
    sorted_projects = sorted(PROJECT_FULL_NAMES.keys(), key=len, reverse=True)

    for p_keyword in sorted_projects:
        # 파일명에서 공백과 밑줄을 제거하여 비교
        normalized_filename = filename.replace('_', '').replace(' ', '')
        normalized_p_name = PROJECT_FULL_NAMES[p_keyword].replace(' ', '')
        
        if normalized_p_name in normalized_filename:
            found_project = PROJECT_FULL_NAMES[p_keyword]
            break
    
    # 프로젝트를 못찾았을 경우, 키워드로 다시 한번 검색
    if found_project == "Uncategorized":
        for p_keyword in sorted_projects:
            if p_keyword in filename:
                found_project = PROJECT_FULL_NAMES[p_keyword]
                break

    for c in CATEGORIES:
        if c in filename:
            found_category = c
            break
            
    return found_project, found_category

def clean_filename(filename, project, category):
    """'Copy of', 'Final_' 등 불필요한 부분을 제거하고 파일명을 정리"""
    
    base, ext = os.path.splitext(filename)
    
    # 접두사 제거
    if base.startswith("Copy of "):
        base = base[8:]
    if base.startswith("Final_"):
        base = base[6:]

    # 파일명에서 프로젝트명, 카테고리명, '최종' 등 중복 정보 제거 시도
    base = base.replace(project.replace(' ', '_'), '')
    base = base.replace(project.replace(' ', ''), '')
    base = base.replace(category, '')
    base = base.replace('최종', '')
    base = base.replace('__', '_').strip('_')

    # 남은 부분이 숫자이거나 비어있으면, 원래 이름 일부를 사용
    if not base or base.isdigit():
       return f"{project}_{category}{ext}"
    else:
       return f"{project}_{category}_{base}{ext}"


def organize_files_from_chunk(chunk_path):
    """청크 파일을 읽어 파일을 정리하고, 결과를 다시 청크 파일에 업데이트"""
    if not os.path.exists(chunk_path):
        print(f"오류: 청크 파일 '{chunk_path}'를 찾을 수 없습니다.")
        return

    try:
        df = pd.read_csv(chunk_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"청크 파일 읽기 오류: {e}")
        return

    if 'new_path' not in df.columns: df['new_path'] = ''
    if 'status' not in df.columns: df['status'] = 'pending'

    for index, row in df.iterrows():
        if row.get('status') == 'processed':
            continue

        original_path = row['original_path']
        filename = row['file_name']

        if not os.path.exists(original_path):
            print(f"경고: 원본 파일 없음 '{original_path}', 건너뜁니다.")
            df.loc[index, 'status'] = 'error_not_found'
            continue

        project, category = get_project_and_category_from_filename(filename)
        new_dir = os.path.join(ORGANIZED_ROOT_DIR, project, category)
        
        cleaned_name = clean_filename(filename, project, category)
        new_path = os.path.join(new_dir, cleaned_name)

        try:
            os.makedirs(new_dir, exist_ok=True)
            
            # 파일이 이미 존재하면 이름에 번호를 붙임
            counter = 1
            temp_new_path = new_path
            while os.path.exists(temp_new_path):
                base, ext = os.path.splitext(new_path)
                temp_new_path = f"{base}_{counter}{ext}"
                counter += 1
            if temp_new_path != new_path:
                new_path = temp_new_path

            shutil.move(original_path, new_path)
            print(f"이동: '{original_path}' -> '{new_path}'")
            
            df.loc[index, 'new_path'] = new_path
            df.loc[index, 'status'] = 'processed'

        except Exception as e:
            print(f"오류: '{filename}' 이동 중 문제 발생 - {e}")
            df.loc[index, 'status'] = f'error_{e}'

    df.to_csv(chunk_path, index=False, encoding='utf-8-sig')
    print(f"'{chunk_path}' 처리를 완료하고 결과를 업데이트했습니다.")


if __name__ == "__main__":
    organize_files_from_chunk(CHUNK_FILE_PATH)
