import flet as ft

import requests
import datetime

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
        icon=ft.Icons.ERROR,
        actions=[ft.TextButton("Okay", on_click=close)]
    )

    def changeDialog(title, content):
        error_dialog.title = ft.Text(title)
        error_dialog.content = ft.Text(content)

        page.show_dialog(error_dialog)
        error_dialog.open = True
        page.update()

    def getWeather(e):
        def unit_conversion(kelvin):
            celsius = kelvin - 273.15
            fahrenheit = (kelvin - 273.15) * 1.8 + 32
            return celsius, fahrenheit
        
        if city_input.value.strip() == "":
            changeDialog("No town/city entered", "You must type in a town/city.")
            return
        
        url = f"{base_url}appid={api_key}&q={city_input.value}"
        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                changeDialog("Invalid town/city", f"{city_input.value}, is not a valid town/city.")
                return
        
        except requests.exceptions.RequestException:
            changeDialog("Connection error", "Check you internet connection.")

        else:
            temp_celsius, temp_fahrenheit = unit_conversion(response["main"]["temp"])
            feels_like_celsius, feels_like_fahrenheit = unit_conversion(response["main"]["feels_like"])
            humidity = response["main"]["humidity"]
            wind_speed = response["wind"]["speed"]
            description = response["weather"][0]["description"]
            sunrise_time = datetime.datetime.fromtimestamp(response["sys"]["sunrise"] + response["timezone"])
            sunset_time = datetime.datetime.fromtimestamp(response["sys"]["sunset"] + response["timezone"])

            temperature = ft.Text(value="")

            # weather_icon = ft.Icon()

            feels_like_temp = ft.Text(value="")

            if unit_dropdown.value == "degrees":
                temperature.value = temp_celsius
                feels_like_temp.value = feels_like_celsius
            else:
                temperature.value = temp_fahrenheit
                feels_like_temp.value = feels_like_fahrenheit

            page.add(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[ft.Text(value=city_input.value)]
                        ),
                        ft.Row(
                            controls=[
                                temperature,
                                feels_like_temp
                            ]
                        )
                    ]
                )
            )


    city_input = ft.TextField(
        value="",
        hint_text="Enter a town/city..."
    )

    unit_dropdown = ft.Dropdown(
        value="degrees",
        width=100,
        options=[
            ft.DropdownOption(key="degrees", text="°C"),
            ft.DropdownOption(key="fahrenheit", text="°F")
        ]
    )

    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[city_input]
                ),
                ft.Row(
                    controls=[
                        unit_dropdown,
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