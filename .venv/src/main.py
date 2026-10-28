import flet as ft

import math

import requests
import datetime

base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = "f9d652545a526d2fc217f244b79d5433"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    
    '''
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
    '''

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

    city_input = ft.TextField(
        value="",
        hint_text="Search for a town or city"
    )

    '''
    def clearInput(e):
        city_input.value = ""
    '''
    
    unit_dropdown = ft.Dropdown(
        value="degrees",
        width=100,
        options=[
            ft.DropdownOption(key="degrees", text="°C"),
            ft.DropdownOption(key="fahrenheit", text="°F")
        ]
    )

    temperature = ft.Text(
        value="",
        size=80,
        weight=ft.FontWeight.BOLD
    )
    feels_like_temp = ft.Text(
        value="",
        size=15
    )

    city_name_display = ft.Text(
        value="",
        size=20
    )

    wind_speed_display = ft.Text(
        value="",
        size=55
    )

    wind_direction_display = ft.Icon(
        icon=ft.Icons.ARROW_BACK_ROUNDED,
        size=70,
        rotate=ft.Rotate(
            angle=math.radians(90),
            alignment=ft.Alignment.CENTER
        )
    )

    def closeWeather(e):
        weather_display.visible = False
        input_display.visible = True

    weather_display = ft.Column(
        visible=False,
        controls=[
            ft.Row(
                controls=[
                    ft.TextButton(
                        content="Back",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=closeWeather
                    )
                ]
            ),
            ft.Row(
                controls=[city_name_display],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[temperature],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[feels_like_temp],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        icon=ft.Icons.AIR_ROUNDED,
                                        size=25
                                    ),
                                    ft.Text(
                                        value="Wind",
                                        size=25
                                    )
                                ],
                                alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[
                                    wind_speed_display,
                                    ft.Text(
                                        value="mph",
                                        size=25
                                    )
                                ],
                                alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(
                                        value="Direction"
                                    ),
                                    wind_direction_display
                                ],
                                alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ]
                    ),
                    bgcolor="#07070B",
                    border_radius=15,
                    expand=True,
                    margin=10,
                    padding=10
                ),
                alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Row(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        icon=ft.Icons.AIR_ROUNDED,
                                        size=25
                                    ),
                                    ft.Text(
                                        value="Sunset/Sunrise",
                                        size=25
                                    )
                                ]
                            )
                        ]
                    ),
                    bgcolor="#07070B",
                    border_radius=15,
                    expand=True,
                    margin=10,
                    padding=10,
                ),
                alignment=ft.CrossAxisAlignment.CENTER
            )
        ]
    )

    input_display = ft.Column(
        visible=True,
        controls=[
            ft.Row(
                controls=[
                    city_input
                ],
                margin=10
            ),
            ft.Row(
                controls=[
                    unit_dropdown,
                    ft.FilledButton(
                        content="Go",
                        on_click=lambda e: getWeather(e)
                    )
                ]
            )
        ]
    )

    def getWeather(e):
        def unit_conversion(kelvin):
            celsius = round(kelvin - 273.15)
            fahrenheit = round((kelvin - 273.15) * 1.8 + 32)
            return celsius, fahrenheit
        
        if city_input.value.strip() == "":
            changeDialog("No town/city entered", "You must type in a town/city.")
            return
        
        url = f"{base_url}appid={api_key}&q={city_input.value}"
        try:
            response = requests.get(url).json()

            if str(response.get("cod")) != "200":
                changeDialog("Invalid town/city", f"{city_input.value} is not a valid town/city.")
                return
        except requests.exceptions.RequestException:
            changeDialog("Connection error", "Check your internet connection.")
            return

        weather_display.visible = True
        input_display.visible = False
        
        city_name_display.value = response["name"]

        humidity = response["main"]["humidity"]
        humidity = f"{humidity}%"
        pressure = response["main"]["pressure"]
        pressure = f"{pressure} hPa"
        visibility = round((response["visibility"])/1609.344)
        visibility = f"{visibility} mi"

        wind_speed = response["wind"]["speed"]
        wind_speed = round(wind_speed * 2.23694)
        wind_direction = response["wind"]["deg"]
        wind_speed_display.value = wind_speed
        wind_direction_display.rotate.angle = math.radians(wind_direction + 90)

        sunrise = datetime.datetime.fromtimestamp(response["sys"]["sunrise"]).strftime(
            "%I:%M %p"
        )
        sunset = datetime.datetime.fromtimestamp(response["sys"]["sunset"]).strftime(
            "%I:%M %p"
        )
        
        temp_celsius, temp_fahrenheit = unit_conversion(response["main"]["temp"])
        feels_like_celsius, feels_like_fahrenheit = unit_conversion(response["main"]["feels_like"])

        if unit_dropdown.value == "degrees":
            temperature.value = f"{temp_celsius}°C"
            feels_like_temp.value = f"Feels like: {feels_like_celsius}°C"
        else:
            temperature.value = f"{temp_fahrenheit}°F"
            feels_like_temp.value = f"Feels like: {feels_like_fahrenheit}°F"

        page.update()

    page.add(input_display, weather_display)

if __name__ == "__main__":
    ft.run(main)