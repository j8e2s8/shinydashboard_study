# shift + enter로는 안되고, 상단에 재생버튼을 눌러야됨.
#!pip install palmerpenguins

from shiny.express import input, render, ui

ui.input_selectize(
    "var", "Select variable",
    choices = ["bill_length_mm", "body_mass_g"]
)

@render.plot
def hist():
    from matplotlib import pyplot as plt   # 그림 그릴 때 필요한 패키지들을 def 안에 넣기
    from palmerpenguins import load_penguins

    df = load_penguins()
    df[input.var()].hist(grid=False)
    plt.xlabel(input.var())
    plt.ylabel("count")
