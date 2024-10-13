# 부리길이 vs 부리 깊이
from matplotlib import pyplot as plt
import seaborn as sns
from palmerpenguins import load_penguins
import pandas as pd

df = load_penguins()
plt.rcParams.update({'font.family': 'Malgun Gothic'})
sns.scatterplot(data=df, 
                x="bill_length_mm", 
                y="bill_depth_mm",
                hue="species")
plt.xlabel("부리길이")
plt.ylabel("부리깊이")

# !pip install scikit-learn
from sklearn.linear_model import LinearRegression

model = LinearRegression()
penguins=df.dropna()

penguins_dummies = pd.get_dummies(
    penguins, 
    columns=['species'],
    drop_first=True
    )

# x와 y 설정
x = penguins_dummies[["bill_length_mm", "species_Chinstrap", "species_Gentoo"]]
y = penguins_dummies["bill_depth_mm"]

# 모델 학습
model.fit(x, y)

model.coef_
model.intercept_

regline_y=model.predict(x)

import numpy as np
index_1=np.where(penguins['species'] == "Adelie")
index_2=np.where(penguins['species'] == "Gentoo")
index_3=np.where(penguins['species'] == "Chinstrap")

sns.scatterplot(data=df, 
                x="bill_length_mm", 
                y="bill_depth_mm",
                hue="species")
plt.plot(penguins["bill_length_mm"].iloc[index_1], regline_y[index_1], color="black")
plt.plot(penguins["bill_length_mm"].iloc[index_2], regline_y[index_2], color="black")
plt.plot(penguins["bill_length_mm"].iloc[index_3], regline_y[index_3], color="black")
plt.xlabel("부리길이")
plt.ylabel("부리깊이")
