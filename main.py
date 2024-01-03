import requests
from customtkinter import *
from tkinter import Label
from PIL import ImageTk, Image

root = CTk(fg_color="#f0f0ed")
set_appearance_mode("light")
root.title("Weather app")
WIDTH, HEIGHT = 320, 480
root.geometry(f"{WIDTH}x{HEIGHT}")

widgets = []


def draw(root):
    city = city_entry.get()
    url = f"https://the-weather-api.p.rapidapi.com/api/weather/{city}"
    headers = {
        "X-RapidAPI-Key": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X-RapidAPI-Host": "the-weather-api.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers).json()

    for widget in widgets:
        widget.destroy()

    try:
        weather_type = response['data']['current_weather']
        weather_type = weather_type.replace('/', '_')
        weather_type = weather_type.replace(' ', '_')

        weather_type_image = ImageTk.PhotoImage(Image.open(f"icons/{weather_type.lower()}.png"))
        weather_type_label = Label(root, image=weather_type_image)
        weather_type_label.image = weather_type_image
        weather_type_label.place(x=WIDTH/2, y=150, anchor="center")
        widgets.append(weather_type_label)

        name_label = Label(root, text=city.title(), font=("Arial", 30))
        name_label.place(x=WIDTH/2, y=56, anchor="center")
        widgets.append(name_label)

        images = ["icons/temperature.png", "icons/wind.png", "icons/humidity.png", "icons/visibility.png",
                  "icons/day.png", "icons/night.png"]
        images_positions = [(10, 240), (144, 240), (10, 320), (144, 320), (10, 400), (144, 400)]

        for i in range(6):
            image = ImageTk.PhotoImage(Image.open(images[i]))
            image_label = Label(root, image=image)
            image_label.image = image
            image_label.place(x=images_positions[i][0], y=images_positions[i][1])
            widgets.append(image_label)

        day_temp = response['data']['expected_temp']
        night_temp = response['data']['expected_temp']
        data = [f"{response['data']['temp']} °C", response['data']['wind'].lstrip(), response['data']['humidity'],
                response['data']['visibility'], f"{day_temp[4:day_temp.index('•')].rstrip()}C",
                f"{night_temp[15:].rstrip()}C"]
        data_positions = [(80, 250), (214, 250), (80, 330), (214, 330), (80, 414), (214, 414)]

        for i in range(6):
            data_label = Label(root, text=data[i], font=("Arial", 18))
            data_label.place(x=data_positions[i][0], y=data_positions[i][1])
            widgets.append(data_label)
    except:
        error_label = Label(root, text="Enter valid city or try again later.", font=("Arial", 14))
        error_label.place(x=10, y=40)
        widgets.append(error_label)


city_entry = CTkEntry(root, placeholder_text="Search for city...")
city_entry.place(x=0, y=0)

search_button = CTkButton(root, text="Search", command=lambda: draw(root))
search_button.place(x=180, y=0)

root.resizable(False, False)
root.mainloop()
