import pandas as pd

def load_and_analyze_data():
    """데이터 파일들을 불러와서 분석하는 함수"""
    
    print("=" * 60)
    print("📂 1단계: 데이터 수집 및 분석")
    print("=" * 60)
    
    # 1. CSV 파일들 불러오기
    print("\n1️⃣ CSV 파일 불러오기...")
    try:
        base_path = "/Users/lee/Desktop/codyssey by team/ky-codyssey-main/Codyseey"
        area_map = pd.read_csv(f"{base_path}/area_map.csv")
        area_struct = pd.read_csv(f"{base_path}/area_struct.csv")
        area_category = pd.read_csv(f"{base_path}/area_category.csv")
        
        print("✅ 모든 CSV 파일을 성공적으로 불러왔습니다.")
    except FileNotFoundError as e:
        print(f"❌ 파일을 찾을 수 없습니다: {e}")
        return None
    
    # 2. 각 파일의 내용 출력 및 분석
    print("\n2️⃣ 각 파일 내용 분석...")
    
    print("\n📊 area_map.csv 분석:")
    print(f"   - 행 수: {len(area_map)}")
    print(f"   - 열 수: {len(area_map.columns)}")
    print(f"   - 열 이름: {list(area_map.columns)}")
    print("\n   처음 5행:")
    print(area_map.head())
    
    print("\n📊 area_struct.csv 분석:")
    print(f"   - 행 수: {len(area_struct)}")
    print(f"   - 열 수: {len(area_struct.columns)}")
    print(f"   - 열 이름: {list(area_struct.columns)}")
    print("\n   처음 5행:")
    print(area_struct.head())
    
    print("\n📊 area_category.csv 분석:")
    print(f"   - 행 수: {len(area_category)}")
    print(f"   - 열 수: {len(area_category.columns)}")
    print(f"   - 열 이름: {list(area_category.columns)}")
    print("\n   전체 내용:")
    print(area_category)
    
    print("\n3️⃣ 구조물 ID를 이름으로 변환...")
    
    category_dict = dict(zip(area_category['category'], area_category['struct']))
    area_struct['struct_name'] = area_struct['category'].map(category_dict)
    # -> category를 struct_name으로 매핑하여 딕셔너리 형태로 저장 이후 x,y를 기준으로 병합
    
    print("✅ 구조물 ID를 이름으로 변환 완료")
    print("\n   변환된 area_struct (처음 5행):")
    print(area_struct.head())
    
    # 4. 세 데이터를 하나의 DataFrame으로 병합
    print("\n4️⃣ 데이터 병합...")
    merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    merged_data = merged_data.sort_values('area')
    
    print("✅ 데이터 병합 및 정렬 완료")
    print(f"   - 병합된 데이터 행 수: {len(merged_data)}")
    print(f"   - 병합된 데이터 열 수: {len(merged_data.columns)}")
    print("\n   병합된 데이터 (처음 5행):")
    print(merged_data.head())
    
    # 5. area 1에 대한 데이터만 필터링
    print("\n5️⃣ area 1 데이터 필터링...")
    area1_data = merged_data[merged_data['area'] == 1]
    
    print(f"✅ area 1 데이터 필터링 완료")
    print(f"   - area 1 데이터 행 수: {len(area1_data)}")
    print("\n   area 1 데이터:")
    print(area1_data)
    
    # 6. 보너스: 구조물 종류별 요약 통계를 리포트로 출력
    print("\n6️⃣ 보너스: 구조물 종류별 요약 통계...")
    
    print("\n📈 전체 지역 구조물 종류별 통계:")
    struct_summary = merged_data['struct_name'].value_counts()
    print(struct_summary)
    
    print("\n📈 area 1 구조물 종류별 통계:")
    area1_struct_summary = area1_data['struct_name'].value_counts()
    print(area1_struct_summary)
    
    print("\n📊 구조물별 상세 통계:")
    struct_detailed = merged_data.groupby('struct_name').agg({
        'area': ['count', 'nunique'],
        'x': ['mean', 'min', 'max'],
        'y': ['mean', 'min', 'max']
    }).round(2)
    print(struct_detailed)
    
    return area1_data, merged_data

def main():
    """메인 함수"""
    print("☕ 반달곰 커피 데이터 분석 프로그램")
    print("=" * 60)
    
    # 데이터 분석 실행
    result = load_and_analyze_data()

    if result:
        area1_data, merged_data = result
        print("\n" + "=" * 60)
        print("✅ 1단계 데이터 수집 및 분석 완료!")
        print("=" * 60)
        print(f"📊 분석 결과:")
        print(f"   - 전체 데이터: {len(merged_data)}개 행")
        print(f"   - area 1 데이터: {len(area1_data)}개 행")
        print(f"   - 구조물 종류: {merged_data['struct_name'].nunique()}개")
    else:
        print("\n❌ 데이터 분석 중 오류가 발생했습니다.")

if __name__ == "__main__":
    main()
