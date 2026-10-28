import flet

import requests
import datetime
base_url = "http://api.openweathermap.org/data/2.5/weather?"
api_key = "f9d652545a526d2fc217f244b79d5433"

def main(page: flet.Page):
  async def focus_input(e):
    await input_field.focus()
  
  page.appbar = flet.AppBar(
    leading=flet.Icon(flet.Icons.WB_SUNNY_ROUNDED),
    title=flet.Text("Flet Weather"),
    center_title=True,
    actions=[
      flet.IconButton(
        icon=flet.Icons.SEARCH,
        tooltip=flet.Tooltip(message="Search for a city/town"),
        mouse_cursor=flet.MouseCursor.CLICK,
        on_click=focus_input
      )
    ]
  )

  input_field = flet.TextField(
    prefix_icon=flet.Icons.SEARCH,
    hint_text="Search for a city/town",
    enable_ime_personalized_learning=True,
    expand=True,
    on_submit=lambda e: get_data(e)
  )

  page.add(
    flet.Column(
      controls=[
        flet.Row(
          controls=[input_field]
        )
      ]
    )
  )

  def get_data(e):
    
    def unit_conversion(kelvin):
      celsius = round(kelvin - 273.15)
      fahrenheit = round(celsius * 1.8 + 32)
      return celsius, fahrenheit

    

if __name__ == "__main__":
  flet.run(main)