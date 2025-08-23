import os
import pandas as pd

# --- 설정값 ---
SOURCE_MANIFEST = 'file_manifest.csv'
OUTPUT_DIR = 'manifest_chunks'
CHUNK_SIZE = 100  # 한 번에 처리할 파일 개수 (LLM 컨텍스트 크기 고려)

def split_manifest_to_chunks():
    """원본 매니페스트 파일을 작은 청크 파일들로 분할합니다."""
    
    # 1. 소스 파일 존재 여부 확인
    if not os.path.exists(SOURCE_MANIFEST):
        print(f"오류: 원본 매니페스트 파일 '{SOURCE_MANIFEST}'를 찾을 수 없습니다.")
        return

    # 2. 출력 디렉토리 생성
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"'{OUTPUT_DIR}' 디렉토리를 생성했습니다.")
    else:
        # 기존 청크 파일이 있다면 삭제하여 항상 새로운 상태에서 시작
        print(f"'{OUTPUT_DIR}' 디렉토리가 이미 존재합니다. 기존 청크 파일을 삭제합니다.")
        for f in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, f))

    # 3. pandas를 사용하여 CSV 파일 읽기
    try:
        df = pd.read_csv(SOURCE_MANIFEST)
    except Exception as e:
        print(f"'{SOURCE_MANIFEST}' 파일 읽기 중 오류 발생: {e}")
        return

    # 4. 데이터프레임을 정해진 크기로 분할하고 CSV로 저장
    num_chunks = (len(df) // CHUNK_SIZE) + (1 if len(df) % CHUNK_SIZE > 0 else 0)
    
    for i in range(num_chunks):
        start_row = i * CHUNK_SIZE
        end_row = start_row + CHUNK_SIZE
        chunk_df = df[start_row:end_row]
        
        chunk_filename = os.path.join(OUTPUT_DIR, f'chunk_{i+1:03d}.csv')
        chunk_df.to_csv(chunk_filename, index=False, encoding='utf-8-sig')
        
    print(f"총 {len(df)}개의 파일 정보를 {num_chunks}개의 청크 파일로 분할하여 '{OUTPUT_DIR}'에 저장했습니다.")

# --- 스크립트 실행 ---
if __name__ == "__main__":
    split_manifest_to_chunks()
