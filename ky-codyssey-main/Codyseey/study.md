1️⃣ area_category 데이터프레임의 내용을 딕셔너리로 변환
category_dict = dict(zip(area_category['category'], area_category['struct']))
예시로, area_category.csv의 내용이 다음과 같다고 해볼게요:

category	struct
1	Apartment
2	Building
3	MyHome
4	BandalgomCoffee
이걸 zip()과 dict()를 이용해서 이렇게 바꿔요:

category_dict = {
    1: 'Apartment',
    2: 'Building',
    3: 'MyHome',
    4: 'BandalgomCoffee'
}

-----------------------

area_struct.csv에는 구조물 종류가 다음처럼 숫자 ID로만 되어 있어요:

x	y	category	area
1	1	1	100
2	2	2	80
이걸 봐서는 1, 2가 무엇을 의미하는지 알 수 없죠.
사람이 이해하려면 "Apartment", "Building"처럼 이름이 필요해요.

✅ map()으로 해결

위에서 만든 category_dict는 다음처럼 구조물 ID를 이름으로 바꾸는 딕셔너리입니다:

{1: 'Apartment', 2: 'Building', 3: 'MyHome', 4: 'BandalgomCoffee'}
.map(category_dict)는 category 값 하나하나에 대해 딕셔너리를 참고해서 대응되는 이름을 가져와 새로운 열에 넣어주는 작업이에요.

📌 정리하자면

코드	목적
category_dict = dict(zip(...))	category → struct 매핑표 생성
.map(category_dict)	숫자 ID를 이름으로 변환 (전처리 핵심)

이를 통해 분석, 가독 용이성 확보

# area_map과 area_struct를 x, y 좌표 기준으로 병합
merged_data = pd.merge(area_map, area_struct, on=['x', 'y'], how='inner')
    
# area 기준으로 정렬
merged_data = merged_data.sort_values('area')


---------------------------------

struct_detailed = merged_data.groupby('struct_name').agg({
    'area': ['count', 'nunique'],
    'x': ['mean', 'min', 'max'],
    'y': ['mean', 'min', 'max']
}).round(2)
📌 코드 설명 요약

역할	설명
groupby('struct_name')	구조물 이름(예: Apartment, Building 등)으로 묶기
.agg({...})	묶인 그룹에 대해 여러 통계 계산
.round(2)	소수점 둘째자리까지 반올림

---------------------------------

min_x, max_x = data['x'].min(), data['x'].max()
min_y, max_y = data['y'].min(), data['y'].max()
min과 max의 최대, 최소값을 구하기 
어디까지 그릴지 정하기 위해

ax.set_xlim(min_x - 1, max_x + 1)
ax.set_ylim(min_y - 1, max_y + 1)
x축과 y축에 여백을 주기 위해 좌우로 한칸씩 여유를  줌


--------------------------------


for x in range(int(min_x), int(max_x) + 2):
    ax.axvline(x, color='lightgray', linestyle='--', linewidth=0.5)
for y in range(int(min_y), int(max_y) + 2):
    ax.axhline(y, color='lightgray', linestyle='--', linewidth=0.5)

+ 2 하는 이유는 -1, +1 한 값까지 그리기 위해서



________________________________

for _, row in data.iterrows():
main() 함수에서 data 값을 받아서 iterrows 한줄씩 순회하는 코드
        
        x, y = row['x'], row['y']
        struct_name = str(row.get('struct_name', '')).strip()
        construction_site = row.get('ConstructionSite', 0)
if elif 문으로 어떤 도형을 그릴 것인지 판단하기 위한 변수들 설정


-------------------------------


    home_pos = (my_home.iloc[0]['x'], my_home.iloc[0]['y'])
    cafe_pos = (cafe.iloc[0]['x'], cafe.iloc[0]['y'])
    # 나의 집과 반달곰 커피 위치 출력하여 저장 


-------------------------------

| 상황                       | `if ... elif` | `if ...: continue` |
| ------------------------ | ------------- | ------------------ |
| 여러 가지 경우 중 한 가지만 선택해서 실행 | ✅ 적합          | ❌ 안 맞음             |
| 특정 조건을 **건너뛰고** 나머지 처리   | ❌ 부적합         | ✅ 적합               |

BFS는 "더 빠른 길이 이미 있다면 그 이상 탐색하지 않아도 된다"는 특징이 있기 때문에 continue가 중요해!
반면에 DFS는 경우의 수를 다 따져보는 게 목적이라 탐색 전략이 조금 다르지.

---------------------------

for보다 while문이 적합한 이유 
for문은 자료구조같은 것을 사용할 때에 append 되거나 할때에 반영하지 못함
반면 while문은 자료구조가 꽉차거나 비는 것을 기준으로 하여 반영 돰 따라서 while 문을 사용 

bfs 너비 우선 탐색은 같은 레벨의 모든 노드를 방문하고 다음 레벨로 진입
다음 레벨로 진입하기 위해서 다시 돌아가야 하므로 while문을 사용

DFS는 재귀함수를 통해 구현하는 반면 BFS는 덱이나 링크드 리스트를 활용해야 하다 보니 자료구조를 접할 수 있는 기회 였음
간선의 가중치가 동일 알 때에는 다익스트라보다는 BFS가 유리 하다고 함

큐 선입 선출 구조

----------------------------
