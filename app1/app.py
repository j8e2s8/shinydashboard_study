# shift + enter로는 안되고, 상단에 재생버튼을 눌러야됨.

from shiny.express import input, render, ui

ui.input_slider("n", "N", 0, 100, 20)
                        # 0: 최소값, 100 : 최대값, 20 : 처음 띄울 때 시작값
                        # "N" : 제목
                        # "n" : 내가 설정하면 바뀔 값



@render.code  # 코드 청크로 출력해줌
def txt():
    return f"n*2 is {input.n() * 2}"











# f 활용하는 법 (참고)
name = "Alice"
greeting = f"Hello, {name}!"
print(greeting)

width =10
height =20
area = width * height
print( f"여기 지역의 넓이는 {area}입니다")