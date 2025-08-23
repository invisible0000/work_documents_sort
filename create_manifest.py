import os
import csv

# --- 설정값 ---
TARGET_DIRECTORY = 'test_environment'
OUTPUT_MANIFEST_FILE = 'file_manifest.csv'

def create_file_manifest():
    """지정된 디렉토리의 모든 파일 목록을 CSV 매니페스트 파일로 생성합니다."""
    
    if not os.path.exists(TARGET_DIRECTORY):
        print(f"오류: '{TARGET_DIRECTORY}' 디렉토리를 찾을 수 없습니다.")
        print("먼저 'create_dummy_files.py'를 실행하여 테스트 환경을 구축하세요.")
        return

    header = ['original_path', 'file_name', 'new_path', 'status']
    
    # 'file_manifest.csv'가 이미 존재하면 덮어쓰기 전에 사용자에게 알림
    if os.path.exists(OUTPUT_MANIFEST_FILE):
        print(f"'{OUTPUT_MANIFEST_FILE}'가 이미 존재합니다. 내용을 덮어씁니다.")

    try:
        with open(OUTPUT_MANIFEST_FILE, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            file_count = 0
            for root, _, files in os.walk(TARGET_DIRECTORY):
                for file in files:
                    original_path = os.path.join(root, file)
                    # new_path와 status는 나중에 채워질 필드로, 일단 비워둠
                    writer.writerow([original_path, file, '', 'pending'])
                    file_count += 1
        
        print(f"총 {file_count}개의 파일 정보를 '{OUTPUT_MANIFEST_FILE}'에 성공적으로 저장했습니다.")

    except IOError as e:
        print(f"파일 쓰기 중 오류가 발생했습니다: {e}")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    create_file_manifest()
