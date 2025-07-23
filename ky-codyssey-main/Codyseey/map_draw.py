import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 한글 깨짐 및 음수 표현 문제 해결
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """mas_map.py에서 분석된 데이터를 불러오는 함수"""
    try:
        base_path = "/Users/lee/Desktop/codyssey by team/ky-codyssey-main/Codyseey"
        merged_data = pd.read_csv(f"{base_path}/merged_data.csv")
        area1_data = pd.read_csv(f"{base_path}/area1_data.csv")
        
        print("✅ mas_map.py에서 분석된 데이터를 성공적으로 불러왔습니다.")
        return merged_data, area1_data
    except FileNotFoundError as e:
        print(f"⚠️ mas_map.py에서 생성된 데이터 파일을 찾을 수 없습니다: {e}")
        print("   먼저 'python mas_map.py'를 실행하여 데이터를 분석해주세요.")
        return None, None

def process_data(merged_data, area1_data):
    """이미 처리된 데이터를 사용하는 함수"""
    if merged_data is None or area1_data is None:
        return None
    
    print("✅ 이미 분석된 데이터를 사용합니다.")
    return merged_data

def create_map_visualization(data):
    """지도 시각화를 생성하는 함수"""
    fig, ax = plt.subplots(figsize=(8, 8))
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()
    
    ax.set_xlim(min_x - 1, max_x + 1)
    ax.set_ylim(min_y - 1, max_y + 1)
    ax.invert_yaxis()  # (1,1)이 좌측 상단이 되도록

    for x in range(int(min_x), int(max_x) + 2):
        ax.axvline(x, color='lightgray', linestyle='--', linewidth=0.5)
    for y in range(int(min_y), int(max_y) + 2):
        ax.axhline(y, color='lightgray', linestyle='--', linewidth=0.5)

    for _, row in data.iterrows():
        x, y = row['x'], row['y']
        struct_name = str(row.get('struct_name', '')).strip()
        construction_site = row.get('ConstructionSite', 0)

        if construction_site == 1:
            rect = patches.Rectangle((x-0.6, y-0.6), 1.2, 1.2, facecolor='#666666', alpha=0.9, edgecolor='#333333', linewidth=2)
            ax.add_patch(rect)
        elif struct_name.lower() == 'apartment':
            circle = patches.Circle((x, y), 0.4, facecolor='#8B4513', alpha=1.0, edgecolor='#654321', linewidth=2)
            ax.add_patch(circle)
        elif struct_name.lower() == 'building':
            circle = patches.Circle((x, y), 0.4, facecolor='#A0522D', alpha=1.0, edgecolor='#654321', linewidth=2)
            ax.add_patch(circle)
        elif struct_name.lower() == 'bandalgomcoffee':
            rect = patches.Rectangle((x-0.4, y-0.4), 0.8, 0.8, facecolor='#228B22', alpha=1.0, edgecolor='#006400', linewidth=2)
            ax.add_patch(rect)
        elif struct_name.lower() == 'myhome':
            triangle = patches.Polygon([[x, y+0.4], [x-0.4, y-0.4], [x+0.4, y-0.4]], facecolor='#32CD32', alpha=1.0, edgecolor='#228B22', linewidth=2)
            ax.add_patch(triangle)

    legend_elements = [
        patches.Circle((0, 0), 0.4, facecolor='#8B4513', edgecolor='#654321', label='아파트'),
        patches.Circle((0, 0), 0.4, facecolor='#A0522D', edgecolor='#654321', label='빌딩'),
        patches.Rectangle((0, 0), 0.8, 0.8, facecolor='#228B22', edgecolor='#006400', label='반달곰 커피'),
        patches.Polygon([[0, 0.4], [-0.4, -0.4], [0.4, -0.4]], facecolor='#32CD32', edgecolor='#228B22', label='내 집'),
        patches.Rectangle((0, 0), 1.2, 1.2, facecolor='#666666', edgecolor='#333333', label='건설 현장')
    ]
    ax.legend(handles=legend_elements, loc='upper left')
    ax.set_title('반달곰 커피 지도')
    plt.savefig('map.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    print("🗺 반달곰 커피 지도 시각화 프로그램")
    print("=" * 60)
    print("📋 사용법:")
    print("   1. 먼저 'python mas_map.py'를 실행하여 데이터를 분석하세요")
    print("   2. 그 다음 이 프로그램을 실행하세요")
    print("=" * 60)
    
    merged_data, area1_data = load_data()
    if merged_data is not None:
        data = process_data(merged_data, area1_data)
        if data is not None:
            create_map_visualization(data)
        else:
            print("❌ 데이터 처리 중 오류가 발생했습니다.")
    else:
        print("❌ 데이터를 불러올 수 없습니다.")
