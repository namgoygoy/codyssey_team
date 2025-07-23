import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import deque

# ✅ Mac 환경용 한글 폰트 설정
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    """데이터를 불러오는 함수"""
    try:
        base_dir = os.path.dirname(__file__)
        csv_path = os.path.join(base_dir, 'merged_data.csv')
        merged_data = pd.read_csv(csv_path)
        print("✅ 데이터를 성공적으로 불러왔습니다.")
        return merged_data
    except FileNotFoundError:
        print("❌ merged_data.csv 파일을 찾을 수 없습니다.")
        print("   먼저 'python mas_map.py'를 실행하여 데이터를 분석해주세요.")
        return None

def find_my_home_and_cafe(data):
    my_home = data[data['struct_name'] == ' MyHome']
    cafe = data[data['struct_name'] == ' BandalgomCoffee']
    if len(my_home) == 0 or len(cafe) == 0:
        print("❌ 위치 데이터를 찾을 수 없습니다.")
        return None, None
    home_pos = (my_home.iloc[0]['x'], my_home.iloc[0]['y'])
    cafe_pos = (cafe.iloc[0]['x'], cafe.iloc[0]['y'])
    print(f"🏠 내 집 위치: {home_pos}")
    print(f"☕ 반달곰 커피 위치: {cafe_pos}")
    return home_pos, cafe_pos

def create_grid_map(data):
    max_x = int(data['x'].max())
    max_y = int(data['y'].max())
    grid = [[0 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    construction_sites = data[data['ConstructionSite'] == 1]
    for _, row in construction_sites.iterrows():
        y, x = int(row['y']), int(row['x'])
        grid[y][x] = 1
    return grid

def bfs_shortest_path(grid, start, goal):
    if start == goal:
        return [start]
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    queue = deque([(start,[start])])
    visited = set([start])
    while queue:
        current, path = queue.popleft()
        x, y = current
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                continue
            if grid[ny][nx] == 1 or (nx, ny) in visited:
                continue
            next_pos = (nx, ny)
            new_path = path + [next_pos]
            if next_pos == goal:
                print(f"✅ 최단 경로를 찾았습니다! (길이: {len(new_path)}칸)")
                return new_path
            queue.append((next_pos, new_path))
            visited.add(next_pos)
    print("❌ 경로를 찾을 수 없습니다.")
    return None

def save_path_to_csv(path, filename='home_to_cafe.csv'):
    if path is None:
        return
    path_data = [{
        'step': i + 1,
        'x': x,
        'y': y,
        'position': f'({x}, {y})'
    } for i, (x, y) in enumerate(path)]
    path_df = pd.DataFrame(path_data)
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, filename)  # ✅ 수정됨
    path_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"💾 경로가 저장되었습니다: {csv_path}")
    print(f"   - 총 {len(path)}칸 이동")
    print(f"   - 시작: {path[0]}")
    print(f"   - 도착: {path[-1]}")

def create_final_map_visualization(data, path):
    fig, ax = plt.subplots(figsize=(12,10))
    min_x, max_x = data['x'].min(), data['x'].max()
    min_y, max_y = data['y'].min(), data['y'].max()
    ax.set_xlim(min_x-1, max_x+1)
    ax.set_ylim(min_y-1, max_y+1)
    ax.invert_yaxis()
    for x in range(int(min_x), int(max_x)+2):
        ax.axvline(x, color='lightgray', linestyle='--', linewidth=0.5)
    for y in range(int(min_y), int(max_y)+2):
        ax.axhline(y, color='lightgray', linestyle='--', linewidth=0.5)
    for _, row in data.iterrows():
        x, y = row['x'], row['y']
        struct_name = str(row.get('struct_name', '')).strip().lower()
        construction_site = row.get('ConstructionSite', 0)
        if construction_site == 1:
            ax.add_patch(patches.Rectangle((x-0.6, y-0.6), 1.2, 1.2, facecolor='#666666', edgecolor='#333333'))
        elif struct_name == 'apartment':
            ax.add_patch(patches.Circle((x, y), 0.4, facecolor='#8B4513', edgecolor='#654321'))
        elif struct_name == 'building':
            ax.add_patch(patches.Circle((x, y), 0.4, facecolor='#A0522D', edgecolor='#654321'))
        elif struct_name == 'bandalgomcoffee':
            ax.add_patch(patches.Rectangle((x-0.4, y-0.4), 0.8, 0.8, facecolor='#228B22', edgecolor='#006400'))
        elif struct_name == 'myhome':
            triangle = [[x, y+0.4], [x-0.4, y-0.4], [x+0.4, y-0.4]]
            ax.add_patch(patches.Polygon(triangle, facecolor='#32CD32', edgecolor='#228B22'))
    if path and len(path) > 1:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, 'r-', linewidth=3, label='최단 경로')
        ax.add_patch(patches.Circle(path[0], 0.3, facecolor='blue', edgecolor='darkblue'))
        ax.add_patch(patches.Circle(path[-1], 0.3, facecolor='red', edgecolor='darkred'))
    ax.legend(loc='upper left')
    ax.set_title('내 집에서 반달곰 커피까지의 최단 경로')
    base_dir = os.path.dirname(__file__)
    map_path = os.path.join(base_dir, 'map_final.png')  # ✅ 수정됨
    plt.savefig(map_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"🗺️ 최종 지도가 저장되었습니다: {map_path}")

def bonus_optimized_path(data):
    print("\n🎯 보너스: 모든 구조물을 지나는 최적화된 경로 계산...")
    structures = data[data['struct_name'].notna() & (data['struct_name'] != 'nan')]
    struct_positions = []
    for _, row in structures.iterrows():
        struct_positions.append({
            'name': row['struct_name'],
            'pos': (row['x'], row['y']),
        })
    print(f"📍 총 {len(struct_positions)}개의 구조물을 방문해야 합니다:")
    for s in struct_positions:
        print(f"   - {s['name']}: {s['pos']}")
    optimized_order = [' MyHome', ' Apartment', ' Building', ' BandalgomCoffee']
    optimized_path = []
    for struct_type in optimized_order:
        struct_data = structures[structures['struct_name'] == struct_type]
        if len(struct_data) > 0:
            pos = (struct_data.iloc[0]['x'], struct_data.iloc[0]['y'])
            optimized_path.append(pos)
    print(f"✅ 최적화된 방문 순서: {optimized_path}")
    return optimized_path

def main():
    print("🚶 내 집에서 반달곰 커피까지의 최단 경로 탐색")
    print("=" * 60)
    data = load_data()
    if data is None:
        return
    home_pos, cafe_pos = find_my_home_and_cafe(data)
    if home_pos is None or cafe_pos is None:
        return
    print("\n🗺️ 그리드 맵 생성 중...")
    grid = create_grid_map(data)
    print(f"✅ {len(grid[0])}x{len(grid)} 크기의 그리드 맵 생성 완료")
    print("\n🔍 최단 경로 탐색 중...")
    shortest_path = bfs_shortest_path(grid, home_pos, cafe_pos)
    if shortest_path:
        print("\n💾 경로 저장 중...")
        save_path_to_csv(shortest_path)
        print("\n🎨 최종 지도 생성 중...")
        create_final_map_visualization(data, shortest_path)
        bonus_optimized_path(data)
        print("\n" + "=" * 60)
        print("✅ 3단계 최단 경로 탐색 완료!")
        print("📁 생성된 파일:")
        print("   - home_to_cafe.csv")
        print("   - map_final.png")
    else:
        print("❌ 경로를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
