
from shiny.express import ui, render, input

with ui.sidebar():
    ui.input_selectize(
    "var", "펭귄 종을 선택해주세요.",
    choices = ["Adelie", "Gentoo", "Chinstrap"])
    ui.input_slider("slider1", "부리길이를 입력해주세요!", min=0, max=100,value=50 )

    @render.text   # render.code는 청크처럼 출력되고, render,text는 텍스트로 출력됨.
    def cal_depth():
        from matplotlib import pyplot as plt
        import seaborn as sns
        from palmerpenguins import load_penguins
        import pandas as pd
        # !pip install scikit-learn
        from sklearn.linear_model import LinearRegression

        penguins = load_penguins().dropna()
        penguins_dummies = pd.get_dummies(
                        penguins, 
                        columns=['species'],
                        drop_first=True)

        x = penguins_dummies[["bill_length_mm", "species_Chinstrap", "species_Gentoo"]]
        y = penguins_dummies["bill_depth_mm"]

        model = LinearRegression()
        model.fit(x, y)
        input_df = pd.DataFrame({
            "bill_length_mm" : [input.slider1()],
            "species" : pd.Categorical([input.var1()], categories = ['Adelie', 'Chinstrap', 'Gentoo'] )
        })
        input_df = pd.get_dummies(
            input_df, columns = ['species'], drop_first = True
        )
        y_hat = model.predict(input_df)
        y_hat = float(y_hat)
        return f'부리깊이 예상치 : {y_hat:.2f}'

@render.plot
def scatter():
    from palmerpenguins import load_penguins
    # 부리길이 vs 부리 깊이
    plt.rcParams.update({'font.family': 'Malgun Gothic'})
    sns.scatterplot(data=df, 
                    x="bill_length_mm", 
                    y="bill_depth_mm",
                    hue="species")
    plt.xlabel("부리길이")
    plt.ylabel("부리깊이")


    # 모델 학습
    model.fit(x, y)

    model.coef_  #[ 0.20044313, -1.93307791, -5.10331533]
    model.intercept_  # 10.565261622823751
    # Adelie 일 때 모델 : 0.2*bill_length_mm + 10.56
    # Chinstrap 일 때 모델 : 0.2* bill_length_mm -1.93*True + 10.56
    # Gentoo 일 때 모델 : 0.2*bill_length_mm -5.10*True + 10.56
    # 왜 범주마다 모델링 안하고, 더미로 만들어서 한 번에 모델링해?
    # 1. 연산량이 적어짐. 범주마다 모델링하면 범주 수만큼 모델 FIT을 해야하기 때문에 오래걸림.
    # 2. 통계적으로, 범주마다 모델링하면 각 범주에 해당하는 데이터 수마다 모델링이 되는데, 더미로 만들어서 한 번에 모델링하면
    #    총 데이터 수에 해당하는 모델이 만들어져서 계수 추정이 안정적임. (표본 수 N이 커지니까)


    regline_y=model.predict(x)



    # 그래프 그리기
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






import pandas as pd
x = pd.DataFrame({
    'bill_length_mm' : 15,
    'species_Chinstrap' : [False],  # boolen은 []로 묶어줘야 입력이 됨. 즉, 값 하나짜리도 []로 묶어줘야함.
    'species_Gentoo' : [False]
})

x = pd.DataFrame({
    'bill_length_mm' : 15,
    'species' : ['Adelie']
})
x
x['species'] = pd.Categorical(x['species'] , categories = ['Adelie', 'Chinstrap', 'Gentoo'] , ordered = True)
x_dummies = pd.get_dummies(
        x, 
        columns=['species'],
        drop_first=True
        )
x_dummies



x = pd.DataFrame({
    'bill_length_mm' : 15,
    'species' : pd.Categorical(['Adelie'], categories=['Adelie', 'Chinstrap', 'Gentoo'])
})
x_dummies = pd.get_dummies(
        x, 
        columns=['species'],
        drop_first=True
        )
x_dummies   # foundations -> calcuations

model.predict(x_dummies)

#try_y_hat = model.predict(x)

# 각 render 파트별로 변수를 공유하지 않음. 즉, model을 fit한 걸, 다른 render 파트에서 사용이 안됨.






