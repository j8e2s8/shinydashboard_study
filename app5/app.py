from shiny.express import ui

with ui.navset_pill(id="tab"):  
    with ui.nav_panel("A"):
        "Panel A content"

    with ui.nav_panel("B"):
        "Panel B content"

    with ui.nav_panel("C"):
        "Panel C content"

    with ui.nav_menu("Other links"):
        with ui.nav_panel("D"):
            "Page D content"

        "----"
        "Description:"
        with ui.nav_control():   # tap을 새 창으로 열라는 부분임. 위에껀 tap을 그냥 현재 창에 반영하는 거고.
            ui.a("Shiny", href="https://shiny.posit.co", target="_blank")