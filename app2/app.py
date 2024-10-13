# shift + enter로는 안되고, 상단에 재생버튼을 눌러야됨.

from shiny.express import input, render, ui

ui.input_slider("val", "N", 0, 100, 20)
                        # 0: 최소값, 100 : 최대값, 20 : 처음 띄울 때 시작값
                        # "N" : 제목
                        # "val" : 내가 설정하면 바뀔 값



@render.text   # 텍스트로 출력해줌
def slider_val():
    return f"Slider value: {input.val()}"


