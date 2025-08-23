import os
import csv
import time

# --- 설정값 ---
MANIFEST_FILE = 'dummy_file_manifest.csv'
BASE_TARGET_DIR = 'test_environment' # 더미 파일이 생성될 기본 폴더

def create_dummy_files_from_manifest():
    """CSV 매니페스트를 읽어 더미 파일과 폴더를 생성합니다."""
    
    if not os.path.exists(MANIFEST_FILE):
        print(f"오류: '{MANIFEST_FILE}'을 찾을 수 없습니다.")
        print("먼저 'generate_manifest.py'를 실행하여 매니페스트 파일을 생성하세요.")
        return

    # test_environment 폴더가 없으면 생성
    if not os.path.exists(BASE_TARGET_DIR):
        os.makedirs(BASE_TARGET_DIR)
        print(f"'{BASE_TARGET_DIR}' 폴더를 생성했습니다.")

    with open(MANIFEST_FILE, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        # 파일 경로의 고유한 목록을 만들어 폴더를 한 번에 생성
        # reader가 이터레이터이므로 리스트로 변환하여 사용
        manifest_data = list(reader)
        unique_paths = set(row['file_path'] for row in manifest_data)

        for path in unique_paths:
            # file_path가 비어있지 않은 경우에만 폴더 생성
            if path and not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError as e:
                    print(f"폴더 생성 오류: {path}, 오류: {e}")
                    # 오류 발생 시 해당 경로는 건너뜀
                    continue
        
        print(f"{len(unique_paths)}개의 폴더 구조를 확인 및 생성했습니다.")
        
        # 파일 생성
        file_count = 0
        for row in manifest_data:
            try:
                file_full_path = os.path.join(row['file_path'], row['file_name'])
                
                # 파일 내용에 키워드 작성
                content = f"""
                이 문서는 테스트 목적으로 자동 생성되었습니다.
                
                주요 정보:
                - 프로젝트: {row['project_name']}
                - 카테고리: {row['category']}
                
                핵심 키워드:
                {row['keywords']}
                """
                
                with open(file_full_path, 'w', encoding='utf-8') as file:
                    file.write(content.strip())
                
                file_count += 1
                # 생성 과정을 시각적으로 보여주기 위해 짧은 지연 추가 (선택 사항)
                # time.sleep(0.001) 
                # print(f"생성 완료: {file_full_path}")

            except Exception as e:
                print(f"파일 생성 오류: {row['file_name']} 경로: {row['file_path']}, 오류: {e}")

    print(f"\n총 {file_count}개의 더미 파일 생성을 완료했습니다.")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    create_dummy_files_from_manifest()
