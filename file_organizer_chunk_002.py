import os
import pandas as pd
import shutil
import re

# --- 설정 ---
CHUNK_FILE_PATH = 'manifest_chunks/chunk_002.csv'
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
    """(개선된 로직) 파일 이름에서 프로젝트명과 카테고리를 더 정확하게 추출"""
    
    # 파일명 정규화 (공백, 밑줄 통일)
    normalized_filename = filename.replace('_', ' ').strip()
    
    found_project = "Uncategorized"
    found_category = "Etc"

    # 1. 프로젝트 찾기 (가장 긴 이름부터 매칭)
    # '골프 개발'이 '골프'보다 먼저 매칭되도록 정렬
    sorted_project_names = sorted(PROJECT_FULL_NAMES.values(), key=len, reverse=True)
    
    for p_name in sorted_project_names:
        if p_name in normalized_filename:
            found_project = p_name
            # 프로젝트명을 찾으면 파일명에서 해당 부분 제거하여 카테고리 검색 정확도 향상
            normalized_filename = normalized_filename.replace(p_name, '', 1)
            break

    # 2. 카테고리 찾기
    for c_name in CATEGORIES:
        if c_name in normalized_filename:
            found_category = c_name
            break
            
    return found_project, found_category

def clean_filename(filename, project, category):
    """(개선된 로직) 파일명을 더 깔끔하게 정리"""
    
    base, ext = os.path.splitext(filename)
    
    # 1. 접두사 제거
    if base.startswith("Copy of "): base = base[8:]
    if base.startswith("Final_"): base = base[6:]
    
    # 2. 프로젝트명, 카테고리명, 기타 불필요한 단어 제거
    # 정규식을 사용하여 단어 단위로 정확하게 제거
    base = re.sub(r'\b' + re.escape(project.replace(" ", "_")) + r'\b', '', base, flags=re.IGNORECASE)
    base = re.sub(r'\b' + re.escape(project.replace(" ", "")) + r'\b', '', base, flags=re.IGNORECASE)
    base = re.sub(r'\b' + re.escape(category) + r'\b', '', base, flags=re.IGNORECASE)
    base = re.sub(r'\b최종\b', '', base, flags=re.IGNORECASE)
    
    # 3. 남은 문자열 정리 (앞뒤 공백/밑줄, 중복 밑줄 제거)
    remaining_part = base.strip('_ ').replace('__', '_')
    
    # 4. 최종 파일명 조합
    if remaining_part and not remaining_part.isdigit():
        return f"{project}_{category}_{remaining_part}{ext}"
    else:
        # 남은 부분이 없거나 숫자 뿐이면, 고유번호를 붙여서 생성
        unique_id = re.search(r'(\d+)', filename)
        if unique_id:
            return f"{project}_{category}_{unique_id.group(1)}{ext}"
        else:
            # 고유번호도 없으면 임의의 번호 부여 (혹은 타임스탬프)
            return f"{project}_{category}{ext}"


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
            
            counter = 1
            temp_new_path = new_path
            while os.path.exists(temp_new_path):
                base, ext = os.path.splitext(new_path)
                temp_new_path = f"{base}_{counter}{ext}"
                counter += 1
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
