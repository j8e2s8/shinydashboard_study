

# 소상공인시장진흥공단_전국 전통시장 현황_2015

예전에는 전통시장을 가면 편의시설이 부족해서 접근성이 떨어졌는데, 요즘에는 편의시설을 개선하려는 노력을 기울이고 있다. 1. 와이파이 설치 2. 건강한 식재료 (백년초 국수 등 + 지역 특색) 3. 공산품이 아니라 정성이 들어간 음식들 4. 저렴한 가격 + 온누리 상품권 사용가능 5. 쇼핑 후 차 한 잔의 여유를 위한 여가 공간 구비 (카페 등) 6. 1인 가구를 위한 음식

상품권 가맹점포 정보 https://www.sbiz.or.kr/sijangtong/nation/onnuri/onnuriMktList.do?menu_type_a=A&menu_cms=&menu_id=070400#shopPopBtn

데이터 출처 소상공인시장진흥공단_전국 전통시장 현황_2010 : https://www.data.go.kr/data/15102810/fileData.do 소상공인시장진흥공단_전국 전통시장 현황_20151231 : https://www.data.go.kr/data/15052836/fileData.do 소상공인시장진흥공단_시장 시설_20210928 : https://www.data.go.kr/data/15090651/fileData.do 소상공인시장진흥공단_전국 전통시장 현황_20230725 : https://www.data.go.kr/data/15012894/fileData.do 소상공인시장진흥공단_전국 전통시장 현황_20240719 : https://www.data.go.kr/data/15052837/fileData.do?recommendDataYn=Y

소상공인시장진흥공단_시장 서비스 정보_20210928 : https://www.data.go.kr/data/15090612/fileData.do


# 데이터 설명

```{python}
import pandas as pd
import numpy as np

market = pd.read_excel("traditionalmarket.xlsx")
market2 = market.copy()
market2.head()
```

현행 시장법상 시장은 상설시장과 정기시장으로 구분된다.

![상설 시장](상설시장%20이미지.jpg) 상설 시장 : 시장 개설 요건을 갖추고, 일정한 구역내에서 상시로 거래하는 영업장. ![정기 시장](정기시장%20이미지.jpg)

정기 시장 : 일정한 지역안에서 정기 또는 계절적으로 개설되는 시장. ![상설 시장과 5일장이 공존하는 시장](상설%20시장%20+%205일장%20이미지.jpg) 상설 시장과 5일장이 공존하는 시장 : 관광형 시장으로 탈바꿈한 시장. 5일 장날이 되면 주민, 관광객 등으로 인상한해를 이룬다.

데이터상 '시장유형'에 정기시장이 존재하면 '시장개설주기'가 5일장이라고 하는지 알아보고자 함.

https://wowmap.kr/market5 : 5일장 지도 (위치)



## 변수명 바꾸기

```{python}
market2 = market2.rename(columns={'시장명' : 'market_name',
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
market2.head()
```

잘 바뀐 것을 알 수 있다.



## 데이터 정보 알아보기

```{python}
market2.info()
```

8개가 범주컬럼이고, 2개가 수치 컬럼, 1개가 날짜컬럼임을 알 수 있다. (수치컬럼중 1개는 연도컬럼이라서, 우리가 분석해 볼 수 있는 수치 컬럼은 1개뿐이다.) 그리고 사용가능상품권(certificate)와 개설연도(year)에만 null값이 있다는 것을 알 수 있다.

각 컬럼의 범주 알아보기

```{python}
market2['market_name'].value_counts()
```

이름이 동일한 서로 다른 시장이 존재함.

```{python}
market2['type'].value_counts()
```

시장 유형은 3가지임.

```{python}
market2['address_road'].value_counts().head()
```

```{python}
market2['address_old'].value_counts().head()
```

주소가 동일한 시장이 있음

```{python}
market2['open_period'].value_counts()
```

정기 시장에 5일, 2일, 6일 있음.

```{python}
market2['certificate'].value_counts()
```

```{python}
market2['public_toilet'].value_counts()
```

```{python}
market2['parking_lot'].value_counts()
```

```{python}
market2['year'].value_counts().head()
```

```{python}
import seaborn as sns
import matplotlib.pyplot as plt

year_group_count = market2.groupby('year').agg(year_count= ('year', 'count'))

plt.clf()
sns.lineplot(data=year_group_count, x='year', y='year_count')
plt.show()
```

```{python}
market2['data_date'].value_counts()
```


#------------------------------

## 점포수 요약 정보 알아보기

```{python}
market2[['store_count']].describe()
```

점포수 위주로 봤을 때, 25%, 75% 기준으로 점포 사이즈를 나누는 것이 합리적으로 보인다. samll : 50개 미만 medium : 50개 이상 134개 미만 large : 134개 이상 3가지의 범주로 나누고자 한다.

## 범주화 1 : 점포수로 범주화하기

```{python}
market2 = market2.assign(market_scale = np.where(market2["store_count"] >= 134, "large", 
                                        np.where(market2["store_count"] >= 50, "medium", "small")))
market2.head()
```

점포수대로 범주화가 잘 되어진 것으로 보인다.

```{python}
import matplotlib.pyplot as plt
plt.clf()
market2['market_scale'].value_counts().plot.bar(rot=0)
plt.show()
```

## 범주화 2 : 편의시절(공중화장실, 주차장) 보유 여부에 따라 시장을 범주화하기.

```{python}
market2['level'] = np.where((market2['public_toilet'] == 'Y') & (market2['parking_lot'] == 'Y'), 'high', 
                   np.where((market2['public_toilet'] == 'N') & (market2['public_toilet'] == 'N') , 'low', 'intermediate'))
market2.head()
```

편의시절(공중화장실, 주차장) 보유 여부에 따라 시장의 편의성이 얼마나 좋은지 범주화 해보고자 한다.

(공중화장실 Y, 주차장 Y) -\> high (공중화장실 Y, 주차장 N) -\> intermediate (공중화장실 N, 주차장 Y) -\> intermediate (공중화장실 N, 주차장 N) -\> low

```{python}
import matplotlib.pyplot as plt
plt.clf()
market2['level'].value_counts().plot.bar(rot=0)
plt.show()
```

대다수의 시장이 편의시설이 잘 구비되어 있음을 알 수 있다.

Y의 현황을 파악하기 위해서, N은 null값으로 만들기 -\> market3 데이터프레임으로 함. N 갯수 알아보기

```{python}
market2['public_toilet'].value_counts()
```

```{python}
market2['parking_lot'].value_counts()
```

온누리 상품권은 사용안하는 곳은 null값이니까 그대로 count 쓰면 쓰는 곳만 세어짐 공중화장실, 주차장은 Y/N 이므로, Y만 세려면 Y만 세어줘야 함.

## 범주별 데이텨 현황 알아보기 

```{python}
market3 = market2.copy()
import numpy as np
market3.loc[market3['public_toilet']=='N', 'public_toilet'] = np.nan
market3['public_toilet'].isna().sum()

market3.loc[market3['parking_lot']=='N', 'parking_lot'] = np.nan
market3['parking_lot'].isna().sum()


pd.set_option('display.max_columns', None)
group_df = market3.groupby(['type','market_scale']).agg(market_count= ('market_name','count')
                                                       , certificate_count = ('certificate', 'count')
                                                       , public_toilet_count = ('public_toilet', 'count')
                                                       , parking_lot_count = ('parking_lot', 'count'))
group_df

```

5일장 중에서 점포수가 많은 시장은 15곳 밖에 안 됨. 대부분 small에 해당함. 따라서 5일장만 열리는 곳은 소규모로 진행되는 시장임. 즉 외부 관광객이 간다기 보다는 지역 현지인들이 이용할 것으로 보임. 라고 생각을 했지, 5일장 블로그 봐보니까 관광지라면 관광객도 갈 법한 점포들도 있었음.


## 범주별 데이텨 현황 알아보기 
```{python}
group_df = market3.groupby(['type','market_scale','level']).agg(market_count= ('market_name','count')
                                                       , certificate_count = ('certificate', 'count')
                                                       , public_toilet_count = ('public_toilet', 'count')
                                                       , parking_lot_count = ('parking_lot', 'count'))
group_df['certificate_pct']= round(group_df['certificate_count']/group_df['market_count']*100,1)
group_df['public_toilet_pct']=round(group_df['public_toilet_count']/group_df['market_count']*100,1)
group_df['parking_lot_pct']=round(group_df['parking_lot_count']/group_df['market_count']*100,1)
group_df
```

비율만 뽑아서 봐보기

```{python}
group_df.iloc[:,[0,4,5,6]]
```

## 상설+정기 시장의 지역 봐보기

```{python}
market2.query('type == "상설+정기"').head()
```



## 지역별로 시장 수 알아보기 (삭제할지 보기)

```{python}
# pd.set_option('display.max_rows', None)
# market2['town_city'].value_counts().head()
```

## 관광형 상설+정기 시장이 있는 지역 알아보기 (삭제할지 보기)

```{python}
# market4 = market2.query('type == "상설+정기"')
# market4['town_city'].value_counts().head()
```

https://www.bigdata-culture.kr/bigdata/user/data_market/detail.do?id=359f0000-4129-11ec-a107-3b8bd6a15b10 관심있는 지역

## 점포수 크기에 따른 연령층 확인하기

#### 0\~19세 = 유소년

#### 20\~59세 = 성인

#### 60\~100세 이상 = 노인

## 2015년 12월 기준 인구조사 파일 불러오기

```{python}
pop = pd.read_excel('pop_2015.xlsx')
pop.head()
```

```{python}
subset = pop.iloc[1:18,[0,1,3,4,5,6,7,8,9,10,11,12,13]]
subset = subset.reset_index().iloc[:,1:]
subset
```

## 원본 숫자 안에 , 를 없애기 (문자열을 숫자열로 바꾸기)

```{python}
columns = subset.columns[1:]

for col in columns:
    subset[col] = subset[col].str.replace(',', '')
    subset[col] = pd.to_numeric(subset[col])

subset
```

## 각 지역마다 연령층 비율 계산하기

```{python}
subset['minor_ratio'] = round((subset.iloc[:,2]+subset.iloc[:,3])/subset.iloc[:,1]*100,2)
subset['youth_ratio'] = round((subset.iloc[:,4]+subset.iloc[:,5]+subset.iloc[:,6]+subset.iloc[:,7])/subset.iloc[:,1]*100,2)
subset['old_ratio'] = round((subset.iloc[:,8]+subset.iloc[:,9]+subset.iloc[:,10]+subset.iloc[:,11]+subset.iloc[:,12])/subset.iloc[:,1]*100,2)
subset
```

## subset에서 필요한 변수만 남기기

```{python}
subset2 = subset.iloc[:, [0,1,13,14,15]]
subset2 = subset2.rename(columns = {'행정기관' : 'region' , '총 인구수' : 'total_pop'})
subset2.head()
```

```{python}
subset2['region'] == '서울특별시  '
```

region 컬럼의 값이 '  ' 공백이 포함되어 있음을 알 수 있다. 이 상태에서 merge하면 merge가 안됨.

```{python}
subset2['region'] = subset2['region'].str.replace('세종특별자치시','세종특별시') 
subset2['region'] = subset2['region'].str.replace('제주특별자치도','제주도')
subset2['region'] = subset2['region'].str.replace('  ','')
subset2
```



# subset2 데이터 저장하기
```{python}
subset2.to_excel(excel_writer = 'subset2.xlsx', index=False)
```



## market2와 subset 데이터 조인을 위해서 market2의 address_new에서 시/도 값 분리해서 'region' 변수 만들기

```{python}
first_tokens=[]

for address in market2['address_road']:
    first_token = address.split()[0]
    first_tokens.append(first_token)
    
market2['region'] = first_tokens
market2.head()
```


## market2, subset2 두 데이터셋 조인 (비율에 대한 새로운 데이터 프레임 만들기)

```{python}
market_pop = pd.merge(market2, subset2, how='left', on='region')
market_pop.head()
```


## market2와 subset2 조인한 데이터셋 저장하기 (market_pop)
```{python}
market_pop.to_excel(excel_writer='market_pop.xlsx', index=False)
```



## 60대 이상인 인구가 많으면 시장 갯수가 많이 형성되었을 것이다. (마켓 카운터 갯수 데이터, 지역별 ratio 데이터 병합)

```{python}
market_pop['old_up'] = np.where(market_pop['old_ratio'] >= market_pop['old_ratio'].mean(), '1' ,'0')
market_pop['youth_up'] = np.where(market_pop['youth_ratio'] >= market_pop['youth_ratio'].mean(), '1' ,'0')
market_pop['minor_up'] = np.where(market_pop['minor_ratio'] >= market_pop['minor_ratio'].mean(), '1' ,'0')
market_pop.head()
```

#### 각 지역마다 60대 이상인 인구가 평균보다 큰지 작은지를 알아보고, 시장의 갯수가 얼마나 되는지 알아보기. (X)

```{python}
market_pop.groupby(['region','old_up']).agg(old_market_count = ('market_name', 'count'))
```

1인 것과 0인 것끼리 합쳐서 알아보기

```{python}
market_pop.groupby('old_up').agg(old_market_count = ('market_name', 'count'))
```

0 : 60대 이상인 인구가 평균보다 작은 곳의 시장 수는 778개 (경기도, 경상남도, 광주광역시, 대구광역시, 대전광역시, 서울특별시, 세종특별시, 울산광역시, 인천광역시, 제주도) 1 : 60대 이상인 인구가 평균보다 큰 곳의 시장 수는 661개 (강원도, 경상북도, 부산광역시, 전라남도, 전라븍도, 충청남도, 충청북도) 60대 이상인 인구가 평균보다 큰 곳의 시장 수가 아닌 곳보다 적다. 딱히 60대 이상인 인구가 많은 지역이 시장 수가 많다고는 볼 수 없다. 그럼에도 불구하고 60대 이상 인구가 전통시장에서 다른 연령대에 비해 돈을 많이 쓴다면, 해당 지역에서 시장 수가 많이는 없어도 돈을 많이 쓴다고 볼 수 있다. (해당 지역에서 대형마트 등 경쟁사가 적다면 당연히 전통시장에 몰릴 수도 있음.)

※ 지역별 점포수, 지역별 마켓수 따로 데이터 프레임 만들기, 인구 비율 데이터 프레임



```{python}
market_pop.groupby(['region','youth_up']).agg(old_market_count = ('market_name', 'count'))
```

```{python}
market_pop.groupby('youth_up').agg(old_market_count = ('market_name', 'count'))
```

0 : 20~50세 인구가 평균보다 작은 곳의 시장 수는 676개 (강원도, 경상남도, 경상북도, 세종특별시, 전라남도, 전라북도, 제주도, 충청남도, 충청북도) 
1 : 20~50세 인구가 평균보다 큰 곳의 시장 수는 763개 (경기도, 광주광역시, 대구광역시, 대전광역시, 부산광역시, 서울특별시, 울산광역시, 인천광역시) 
20~50세 인구가 평균보다 큰 곳의 시장 수가 아닌 곳보다 크다.

#### 

```{python}
level_group = market_pop.groupby(['old_up','level'],as_index=False).agg(market_count = ('market_name', 'count'))
level_group
```

60대 이상 인구가 평균보다 적은 지역에서의 level별 시장 수 : 395 / 300 / 83 60대 이상 인구가 평균보다 많은 지역에서의 level별 시장 수 : 435 / 178 / 48

```{python}
level_group2 = market_pop.groupby(['youth_up','level'],as_index=False).agg(market_count = ('market_name', 'count'))
level_group2
```

20~50세 인구가 평균보다 적은 지역에서의 level별 시장 수 : 501 / 145 / 30 
20~50세 인구가 평균보다 많은 지역에서의 level별 시장 수 : 329 / 333 / 101

젊은 인구가 많은 지역에서 low인 시장이 많다. -> 개선해야 젊은 인구가 많이 간다라고 가도 되나?

## 편의시설이 high 인데 인구 많은데야? 인구 많으면 편의시설 좋아?

```{python}
market_pop.query('level == "high"').groupby('region', as_index=False).agg(market_count=('market_name', 'count'),pop = ('total_pop', 'min')).sort_values('pop',ascending=False)
```                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
편의시설이 잘 되어있는 시장이 많은 주변으로 인구 수가 많이 형성되어있다고 보기 어려움.
