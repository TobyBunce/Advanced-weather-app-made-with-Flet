import flet as ft

import requests

base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = "f9d652545a526d2fc217f244b79d5433"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    
    def setTheme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE

        page.update()
    
    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        on_click=setTheme
    )
    
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.CLOUD),
        title=ft.Text("Weather App"),
        center_title=True,
        actions=[theme_button]
    )

    def close(e):
        error_dialog.open = False
        page.update()

    error_dialog = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Text(""),
        actions=[ft.TextButton("Okay", on_click=close)],
    )

    def changeDialog(title, content):
        error_dialog.title = ft.Text(title)
        error_dialog.content = ft.Text(content)

        page.show_dialog(error_dialog)
        error_dialog.open = True
        page.update()

    def getWeather(e):
        if city_input.value.strip() == "":
            changeDialog("No town/city entered", "You must type in a town/city.")
            return
        
        url = f"{base_url}appid={api_key}&q={city_input.value}&units=metric"
        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                changeDialog("Invalid town/city", f"{city_input.value}, is not a valid town/city.")
                return

            
        except requests.exceptions.RequestException:
            changeDialog("Connection error", "Check you internet connection.")
            page.update()

    city_input = ft.TextField(
        value="",
        icon=ft.Icons.MAP_ROUNDED,
        hint_text="Enter a town/city..."
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        city_input,
                        ft.FilledButton(
                            content="Go",
                            on_click=getWeather
                        )
                    ]
                )
            ]
        )
    )

if __name__ == "__main__":
    ft.run(main)