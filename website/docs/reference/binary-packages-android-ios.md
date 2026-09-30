import flet as ft
import random

def main(page: ft.Page):
    # Беттің баптаулары (Неон стилі, қараңғы фон)
    page.title = "DPI НАСТРОЙКА"
    page.bgcolor = "#0b0114"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Тариф таңдау функциясы
    selected_tariff = ft.Text(value="Таңдалды: SOFT — 300 тг", color="#ff00ea", size=14, weight=ft.FontWeight.BOLD)
    
    def change_tariff(e):
        selected_tariff.value = f"Таңдалды: {e.control.text}"
        page.update()

    # DPI генерациялау функциясы
    def generate_dpi(e):
        if not phone_input.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("Өтініш, телефон үлгісін жазыңыз!"))
            page.snack_bar.open = True
            page.update()
            return
        
        # Кездейсоқ DPI мәні
        random_dpi = random.randint(550, 720)
        
        result_tariff.value = f"💎 {selected_tariff.value.replace('Таңдалды: ', '')}"
        result_phone.value = f"📱 {phone_input.value.upper()}"
        result_dpi_val.value = str(random_dpi)
        result_box.visible = True
        page.update()

    # Жазулар мен Блоктар
    title = ft.Text("НАСТРОЙКА", color="#ff00ea", size=26, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    
    kaspi_box = ft.Container(
        content=ft.Column([
            ft.Text("🔹 KASPI ТӨЛЕМ", color="#00d2ff", size=12),
            ft.Text("+7 705 973 4112", size=16, weight=ft.FontWeight.BOLD),
            ft.Text("👤 Нұртас І.", size=14),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        border=ft.border.all(1, "#00d2ff"),
        border_radius=10,
        padding=10,
        width=320,
    )

    # Тариф батырмалары
    btn_style = ft.ButtonStyle(bgcolor="#18004c", color="white", border_side=ft.BorderSide(1, "#5a00ff"), shape=ft.RoundedRectangleBorder(radius=8))
    
    grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=160,
        child_aspect_ratio=1.8,
        spacing=10,
        run_spacing=10,
        controls=[
            ft.ElevatedButton("👑 VIP \n 400 тг", style=btn_style, on_click=change_tariff),
            ft.ElevatedButton("📍 SOFT \n 300 тг", style=btn_style, on_click=change_tariff),
            ft.ElevatedButton("🔥 ЧИТ \n 200 тг", style=btn_style, on_click=change_tariff),
            ft.ElevatedButton("⚡ ПОСЛЕ ОБНОВА \n 100 тг", style=btn_style, on_click=change_tariff),
        ]
    )
    
    grid_container = ft.Container(content=grid, width=320, height=140)
    
    counter_text = ft.Text("👥 Алды: 138 адам", color="#aaaaaa", size=12)
    phone_input = ft.TextField(label="Телефон үлгісі (мысалы: OPPO RENO 7)", border_color="#00d2ff", bgcolor="#110426", color="white", width=320)
    
    create_btn = ft.ElevatedButton(
        "Создать", 
        bgcolor="#ff0080", 
        color="white",
        width=150,
        height=45,
        on_click=generate_dpi
    )

    # Нәтиже шығаратын блок (бастапқыда көрінбейді)
    result_tariff = ft.Text("", color="#ff00ea", weight=ft.FontWeight.BOLD)
    result_phone = ft.Text("", color="white", weight=ft.FontWeight.BOLD)
    result_dpi_val = ft.Text("613", color="#00d2ff", size=36, weight=ft.FontWeight.BOLD)
    
    result_box = ft.Container(
        content=ft.Column([
            result_tariff,
            result_phone,
            ft.Text("🖥 DPI МӘНІ:", size=13),
            result_dpi_val,
            ft.Text("🤖 Android үшін тиімді DPI", color="#00d2ff", size=11)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        border=ft.border.all(1, "#ff00ea"),
        border_radius=10,
        padding=15,
        width=320,
        visible=False
    )

    # Экранға барлық элементтерді қосу
    page.add(
        ft.Container(
            content=ft.Column([
                title,
                kaspi_box,
                selected_tariff,
                grid_container,
                counter_text,
                phone_input,
                create_btn,
                ft.Divider(height=10, color="transparent"),
                result_box
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            border=ft.border.all(2, "#5a00ff"),
            border_radius=20,
            padding=20,
            width=360,
            bgcolor="#0d0522"
        )
    )

ft.app(target=main)
