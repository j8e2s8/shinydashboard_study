from shiny.express import ui

with ui.layout_column_wrap(gap="2rem"):  # 왼쪽 slider과 오른쪽 slider 사이의 gap을 지정해줌
    ui.input_slider("slider1", "Slider 1", min=0, max=100, value=50)
    ui.input_slider("slider2", "Slider 2", min=0, max=100, value=50)

# 근데 보여지는 창이 작아지면 왼쪽 slider이 위로가고, 오른쪽 slider이 아래로 감. 이렇게 창 크기에 따라 달라지는걸 반응형이라고 함.