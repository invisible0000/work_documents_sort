import os
import pandas as pd
import shutil
import re

# --- 설정 ---
CHUNK_FILE_PATH = 'manifest_chunks/chunk_003.csv'
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
    normalized_filename = filename.replace('_', ' ').strip()
    
    found_project = "Uncategorized"
    found_category = "Etc"

    sorted_project_names = sorted(PROJECT_FULL_NAMES.values(), key=len, reverse=True)
    
    for p_name in sorted_project_names:
        if p_name in normalized_filename:
            found_project = p_name
            normalized_filename = normalized_filename.replace(p_name, '', 1)
            break
    
    # '외부자료_골프' 같은 경우 프로젝트를 찾기 위한 추가 로직
    if found_project == "Uncategorized" and '외부자료' in filename:
         for p_key, p_value in PROJECT_FULL_NAMES.items():
             if p_key in filename:
                 found_project = p_value
                 break

    for c_name in CATEGORIES:
        if c_name in normalized_filename:
            found_category = c_name
            break
            
    return found_project, found_category

def clean_filename(filename):
    """가장 기본적인 파일명 정리 (나중에 규칙별로 세분화)"""
    base, ext = os.path.splitext(filename)
    # 간단한 접두사 및 공백 정리
    base = base.replace('Copy of ', '').replace('Final_', '').strip()
    return f"{base}{ext}"


def organize_files_from_chunk(chunk_path):
    """(3차 개선) 청크 파일을 읽어 새로운 규칙에 따라 파일을 정리"""
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

        new_dir = ''
        cleaned_name = clean_filename(filename)

        # --- 새로운 규칙 적용 ---
        # 1. 날짜 포함된 '보고자료' 처리
        date_match = re.search(r'보고자료_(\d{8})', filename)
        if date_match:
            date_str = date_match.group(1)
            year, month = date_str[:4], date_str[4:6]
            new_dir = os.path.join(ORGANIZED_ROOT_DIR, '_Dated_Logs', year, month)
        
        # 2. '정리필요' 또는 '임시' 파일 처리
        elif filename.startswith(('정리필요_', '임시_')):
            _, category = get_project_and_category_from_filename(filename)
            new_dir = os.path.join(ORGANIZED_ROOT_DIR, '_Review_Needed', category)

        # 3. '외부자료' 처리
        elif filename.startswith('외부자료_'):
            project, _ = get_project_and_category_from_filename(filename)
            new_dir = os.path.join(ORGANIZED_ROOT_DIR, '_External_Data', project)

        # 4. 기존 프로젝트 기반 분류
        else:
            project, category = get_project_and_category_from_filename(filename)
            new_dir = os.path.join(ORGANIZED_ROOT_DIR, project, category)
        
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
