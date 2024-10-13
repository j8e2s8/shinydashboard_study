from shiny.express import ui, input, render

ui.page_opts(fillable=True)  # fillable=True : 박스가 페이지 사이즈에 맞게 채워짐

with ui.layout_columns():  
    with ui.card():     # 카드 1개
        ui.card_header("Card 1 header")
        ui.p("Card 1 body")
        ui.input_slider("slider", "Slider", 0, 10, 5)

    with ui.card():     # 카드 2개
        ui.card_header("Card 2 header")
        ui.p("Card 2 body")
        ui.input_text("text", "Add text", "")


@render.text
def text_out():
    return f"Input text: {input.text()}"