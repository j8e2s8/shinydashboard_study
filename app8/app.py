from shiny.express import input, render, ui
ui.page_opts(title="Page title")

with ui.sidebar():
    ui.input_selectize(
    "var", "Select variable",
    choices = ["bill_length_mm", "body_mass_g"])


with ui.nav_panel("Page 1"):
    @render.plot
    def hist():
        from matplotlib import pyplot as plt   # 그림 그릴 때 필요한 패키지들을 def 안에 넣기
        from palmerpenguins import load_penguins

        df = load_penguins()
        df[input.var()].hist(grid=False)
        plt.xlabel(input.var())
        plt.ylabel("count")

with ui.nav_panel("Page 2"):
    "Page 2 content"


    # 강사님 코드 다시 확인해보기