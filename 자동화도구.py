import sys
import json
import csv
from pathlib import Path

def main():
    # 1. 인자값 확인 (사용자가 키워드를 1개 입력했는지 검증)[cite: 2]
    if len(sys.argv) < 2:
        print("사용법: python solution.py <키워드>")
        print("예시: python solution.py 기본계획")
        sys.exit(1)

    keyword = sys.argv[1].strip()
    
    # 2. 파일 경로 설정
    current_dir = Path(__file__).parent
    json_path = current_dir / "조항데이터.json"
    output_filename = f"결과_{keyword}.csv"
    output_path = current_dir / output_filename

    # 3. 조항데이터.json 읽기[cite: 2]
    if not json_path.exists():
        print(f"[오류] '{json_path.name}' 파일을 찾을 수 없습니다.")
        sys.exit(1)

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except Exception as e:
        print(f"[오류] JSON 파일 읽기 실패: {e}")
        sys.exit(1)

    # 4. 본문에 키워드가 들어있는 조항 필터링[cite: 2]
    matched_articles = []
    for item in articles:
        # 본문 또는 제목에 키워드가 포함된 경우 추출 (요구사항: 본문 기준)
        if keyword in item.get("본문", "") or keyword in item.get("제목", ""):
            matched_articles.append(item)

    # 5. CSV 파일로 저장 (UTF-8 인코딩, 헤더: 조, 제목, 본문)[cite: 2]
    try:
        with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            # 헤더 작성
            writer.writerow(["조", "제목", "본문"])
            # 데이터 row 작성
            for item in matched_articles:
                writer.writerow([item.get("조"), item.get("제목"), item.get("본문")])
    except Exception as e:
        print(f"[오류] CSV 파일 저장 실패: {e}")
        sys.exit(1)

    # 6. 결과 건수 화면 출력[cite: 2]
    print(f"[OK] {len(matched_articles)}건 저장 결과 {output_filename}")

if __name__ == "__main__":
    main()