# house price
from shiny.express import ui, render, input

with ui.sidebar():
    ui.input_selectize(
    "var", "Select variable",
    choices = ["MS_SubClass", "MS_Zoning"])


@render.plot
def hist():
    from matplotlib import pyplot as plt   # 그림 그릴 때 필요한 패키지들을 def 안에 넣기
    import seaborn as sns 
    import pandas as pd

    df = pd.read_csv("C:/Users/USER/Documents/LS 빅데이터 스쿨/shinydashboard/try/goodhouse.csv")  # 상대 경로 하면 에러 떴는데 절대 경로 하니까 됨.
    #df2 = df[input.var()].value_counts().sort_index()
    plt.clf()
    sns.countplot(df[input.var()])
    plt.ylabel(input.var())
    plt.xlabel("count")

