import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim
import tkinter as tk
import math
from PIL import Image, ImageTk


def get_timezone(city):
    geolocator = Nominatim(user_agent="timezone_app")
    location = geolocator.geocode(city)
    if location:
        lat, lon = location.latitude, location.longitude
        tz_finder = TimezoneFinder()
        tz = tz_finder.timezone_at(lng=lon, lat=lat)
        if tz:
            return pytz.timezone(tz)
    return None


def draw_clock(canvas, city, city_time):
    canvas.create_oval(10, 10, 210, 210, outline="black", width=2)

    for i in range(1, 13):
        angle = math.radians(i * 30)
        x = 110 + 80 * math.sin(angle)
        y = 110 - 80 * math.cos(angle)
        canvas.create_text(x, y, text=str(i), font=("Arial", 14))

    hour = city_time.hour % 12 + city_time.minute / 60
    minute = city_time.minute
    second = city_time.second

    hour_angle = math.radians(hour * 30)
    canvas.create_line(110, 110, 110 + 50 * math.sin(hour_angle), 110 - 50 * math.cos(hour_angle), width=6, fill="black")

    minute_angle = math.radians(minute * 6)
    canvas.create_line(110, 110, 110 + 70 * math.sin(minute_angle), 110 - 70 * math.cos(minute_angle), width=4, fill="blue")

    second_angle = math.radians(second * 6)
    canvas.create_line(110, 110, 110 + 70 * math.sin(second_angle), 110 - 70 * math.cos(second_angle), width=2, fill="red")

    canvas.create_text(110, 220, text=city, font=("Arial", 10))


def update_clock(canvas, city, timezone):
    now = datetime.now(timezone)
    canvas.delete("all")
    draw_clock(canvas, city, now)
    canvas.after(1000, update_clock, canvas, city, timezone)


def create_window():
    window = tk.Tk()
    window.title("Orologi del Mondo")
    window.attributes("-fullscreen", True)  # Impostare la finestra a schermo intero
    window.configure(bg='black')  # Impostare il colore di sfondo a nero

    # Carica l'immagine di sfondo
    try:
        bg_image = Image.open("ora_mondo.jpg")  # Assicurati che il nome del file sia corretto
        bg_image = bg_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)  # Cambiato ANTIALIAS in LANCZOS
        bg_image_tk = ImageTk.PhotoImage(bg_image)

        # Etichetta per l'immagine di sfondo
        background_label = tk.Label(window, image=bg_image_tk)
        background_label.place(relwidth=1, relheight=1)  # Rendi l'immagine di sfondo a tutta la finestra
    except Exception as e:
        print(f"Errore nel caricamento dell'immagine di sfondo: {e}")

    cities = ["Roma", "Tokyo", "Pechino", "San Pietroburgo", "Camberra", "New York", "Seoul"]
    for i, city in enumerate(cities):
        tz = get_timezone(city)
        if tz:
            frame = tk.Frame(window)
            frame.grid(row=i // 5, column=i % 5, padx=10, pady=10)

            canvas = tk.Canvas(frame, width=220, height=240)
            canvas.pack()

            now = datetime.now(tz)
            draw_clock(canvas, city, now)
            update_clock(canvas, city, tz)

    # Aggiungi il pulsante per chiudere il programma usando grid
    close_button = tk.Button(window, text="Chiudi", font=("Arial", 16), command=window.quit, bg="red", fg="white")
    close_button.grid(row=len(cities) // 3 + 1, column=1, pady=20)  # Usa grid per il pulsante

    # Gestisci l'evento di chiusura della finestra
    window.protocol("WM_DELETE_WINDOW", window.quit)  # Chiudi la finestra quando si clicca sulla "X" in alto a destra

    window.mainloop()


create_window()
