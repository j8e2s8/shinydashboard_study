import pandas as pd
import numpy as np

# 데이터 불러오기
market = pd.read_excel("data/traditionalmarket.xlsx")

# 분석을 위한 복사본 만들기
market2 = market.copy()

# 엑셀의 변수 한글을 영어로 rename
market2 = market2.rename(columns = {"시장명"              : "market_name", 
                                    "시장유형"            : "type",
                                    "소재지도로명주소"    : "adress_road",
                                    "시장개설주기"        : "open_period",
                                    "소재지지번주소"      : "address_old",
                                    "점포수"              : "market_count",
                                    "사용가능상품권"      : "certificate",
                                    "공중화장실 보유여부" :"public_toilet",
                                    "주차장 보유여부"     : "parking_lot",
                                    "개설년도"            : "year",
                                    "데이터기준일자"      : "data_date"})
                                    
# 데이터의 정보 확인하기
market2.describe()
market2["public_toilet"].info()
market2["parking_lot"].info()
market2['market_count'].describe()

# 점포수에 따른 규모 크기를 설명해주는 변수 만들기
market2 = market2.assign(market_scale = np.where(market2["market_count"] >= 134, "large", 
                                        np.where(market2["market_count"] >= 50, "medium", "small")))

# 편의시설의 유무에 따른 레벨링 하기
market2['level'] = np.where((market2['public_toilet'] == 'Y') & (market2['parking_lot'] == 'Y'), 'high', 
                   np.where((market2['public_toilet'] == 'N') & (market2['public_toilet'] == 'N') , 'low', 'intermediate'))

# 확인 절차
market2.head()

# 그래프 그리기
import seaborn as sns
import matplotlib.pyplot as plt

# x축을 편의 시설 레벨
sns.countplot(data = market2, x = 'level', hue = 'level')
plt.show()

# 그래프 그리기 위한 df 생성
# 시장 유형와 규모 크기에 따른 그룹화 / 규모 크기 갯수 추가
df = market2.groupby(["type", "market_scale"], as_index = False) \
            .agg(market_count = ("market_scale", "count"))

# 규모 크기에 따른 내림차순
df.sort_values('market_count', ascending = False)

# 만든 df를 x축에 시장 유형, y축은 규모 크기에 따른 점포 갯수
sns.barplot(data = df, x = 'type', y = 'market_count', hue = 'market_scale')
plt.show()
plt.clf()
