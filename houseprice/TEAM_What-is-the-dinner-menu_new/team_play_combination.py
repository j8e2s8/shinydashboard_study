# 라이브러리 불러오기
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
market_raw = pd.read_excel("data/traditionalmarket.xlsx")
market = market_raw.copy()
pop_raw = pd.read_excel('data/pop_2015.xlsx', thousands = ',') #쉼표 없애주고 숫자로 바꿔줌.
pop = pop_raw.copy()

# 데이터 전처리 1
pop = pop.iloc[1:18,[0,1,3,4,5,6,7,8,9,10,11,12,13]]
pop = pop.reset_index().iloc[:,1:]

# 변수명 변경
market = market.rename(columns={'시장명' : 'market_name',
                              '시장유형' : 'type',
                              '소재지도로명주소' : 'address_road',
                              '시장개설주기' : 'open_period',
                              '소재지지번주소' : 'address_old',
                              '점포수' : 'store_count',
                              '사용가능상품권' : 'certificate',
                              '공중화장실 보유여부' : 'public_toilet',
                              '주차장 보유여부' : 'parking_lot',
                              '개설년도' : 'year' ,
                              '데이터기준일자' : 'data_date'})

pop = pop.rename(columns={'행정기관' : 'region',
                          '총 인구수' : 'total_pop',
                          '0~9세' : '0~9',
                          '10~19세' : '10~19',
                          '20~29세' : '20~29',
                          '30~39세' : '30~39',
                          '40~49세' : '40~49',
                          '50~59세' : '50~59',
                          '60~69세' : '60~69',
                          '70~79세' : '70~79',
                          '80~89세' : '80~89',
                          '90~99세' : '90~99',
                          '100세 이상' : '100_over',
                          })

#이쯤에서 데이터 프레임 보여주면 좋을듯_정은서

# 데이터 전처리 2
region = pop['region'] #행정기관 빼내기
pop = pop.iloc[:,1:].astype(int) #행정기관 빼고 나머지 열을 정수로 바꿈.
pop = pd.concat([region, pop], axis = 1) #빼낸 행정기관을 다시 합침
pop.info()

# 행정명 똑같이 수정 후 띄어쓰기 지우기.
pop['region'] = pop['region'].str.replace('세종특별자치시','세종특별시') 
pop['region'] = pop['region'].str.replace('제주특별자치도','제주도')
pop['region'] = pop['region'].str.replace('  ','')

# market 데이터에서 지역 명 열(변수) 추가하기
market['region'] = market["address_road"].str.split(' ').str[0]

# 인구 연령 범주 인구수 열(변수) 추가하기
pop['under20'] = pop['0~9'] + pop['10~19']
pop['2050'] = pop['20~29'] + pop['30~39'] + pop['40~49'] + pop['50~59']
pop['over60'] = pop['60~69'] + pop['70~79'] + pop['80~89'] + pop['90~99'] + pop['100_over']

# 지역별 데이터 프레임 만들기
market_region = market.groupby('region', as_index = False)\
      .agg(market_count = ('market_name', 'count'),
           store_sum = ('store_count', 'sum'))

pop_region = pop[['region', 'total_pop', 'under20', '2050', 'over60']]

market_pop = pd.merge(market_region, pop_region, how='left', on='region')
market_pop.head()

# 있는 값들로 계산할 수 있는 열(변수) 추가
market_pop['pct_under20'] = round(market_pop['under20'] / market_pop['total_pop'] * 100, 2) #미성년자 비율 추가 + 소숫점 정리리
market_pop['pct_2050'] = round(market_pop['2050'] / market_pop['total_pop'] * 100, 2)
market_pop['pct_over60'] = round(market_pop['over60'] / market_pop['total_pop'] * 100, 2)

market_pop['pct_over60_mean'] = np.where(market_pop['pct_over60'] >= market_pop['pct_over60'].mean(),
                              'UP', 'DOWN') # 60대 이상 비율의 평균을 구한 뒤 그것보다 높거나 낮다는것 표시.

market_pop['pop_per_market'] = round(market_pop['total_pop'] / market_pop['market_count'], 1) #인구 수 / 시장 수, 소숫점 정리.
market_pop['pop_per_store'] = round(market_pop['total_pop'] / market_pop['store_sum'], 1)
market_pop['old_per_market'] = round(market_pop['over60'] / market_pop['market_count'], 1)
market_pop['old_per_store'] = round(market_pop['over60'] / market_pop['store_sum'], 1)


# 기타 등등 코드

# 엑셀로 빼보기
market_pop.to_excel(excel_writer = 'market_pop.xlsx', index=False)

# 데이터 프레임 출력 제한 설정정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
market_pop

# 출력 제한 다시 되돌리기
pd.reset_option('display.max_rows')
pd.reset_option('display.max_columns')
