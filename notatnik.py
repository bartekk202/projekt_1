from tkinter import *
from tkinter import ttk
import tkintermapview

users: list = []
editorials: list = ["Redakcja A", "Redakcja B", "Redakcja C"]


class User:
    def __init__(self, name, surname, location, editorial, posts=""):
        self.name = name
        self.surname = surname
        self.location = location
        self.editorial = editorial
        self.posts = posts
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url)
        response_html = BeautifulSoup(response.text, "html.parser")
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


def add_user():
    zmienna_imie = entry_name.get()
    zmienna_nazwisko = entry_surname.get()
    zmienna_miejscowosc = entry_location.get()
    zmienna_redakcja = combobox_redakcja.get()
    zmienna_posty = entry_posts.get()

    if zmienna_redakcja == "":
        return

    users.append(User(zmienna_imie, zmienna_nazwisko, zmienna_miejscowosc, zmienna_redakcja, zmienna_posty))
    clear_form()
    show_users()


def clear_form():
    entry_name.delete(0, END)
    entry_surname.delete(0, END)
    entry_location.delete(0, END)
    entry_posts.delete(0, END)
    combobox_redakcja.set("")
    entry_name.focus()


def show_users():
    listboox_lista_obiektow.delete(0, END)
    selected_editorial = combobox_filtruj_redakcja.get()
    for idx, user in enumerate(users):
        if selected_editorial == "" or user.editorial == selected_editorial:
            listboox_lista_obiektow.insert(END, f"{user.name} {user.surname} ({user.editorial})")


def remove_user():
    i = listboox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()


def show_user_details():
    i = listboox_lista_obiektow.index(ACTIVE)
    user = users[i]
    label_name_szczegoly_obiektow_wartosc.config(text=user.name)
    label_surname_szczegoly_obiektow_wartosc.config(text=user.surname)
    label_location_szczegoly_obiektow_wartosc.config(text=user.location)
    label_posts_szczegoly_obiektow_wartosc.config(text=user.posts)
    map_widget.set_position(user.coordinates[0], user.coordinates[1])
    map_widget.set_zoom(12)


def edit_user():
    i = listboox_lista_obiektow.index(ACTIVE)
    user = users[i]
    entry_name.insert(0, user.name)
    entry_surname.insert(0, user.surname)
    entry_location.insert(0, user.location)
    entry_posts.insert(0, user.posts)
    combobox_redakcja.set(user.editorial)
    button_dodaj_obiekt.config(text="zapisz", command=lambda: update_user(i))


def update_user(i):
    user = users[i]
    user.name = entry_name.get()
    user.surname = entry_surname.get()
    user.location = entry_location.get()
    user.posts = entry_posts.get()
    user.editorial = combobox_redakcja.get()
    user.marker.delete()
    user.coordinates = user.get_coordinates()
    user.marker = map_widget.set_marker(user.coordinates[0], user.coordinates[1])
    show_users()
    clear_form()
    button_dodaj_obiekt.config(text="dodaj użytkownika", command=add_user)


# --- GUI ---
root = Tk()
root.geometry("1200x800")
root.title("Redakcje")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# ramka_lista_obiektow
Label(ramka_lista_obiektow, text="Redakcje").grid(row=0, column=0, columnspan=3)
combobox_filtruj_redakcja = ttk.Combobox(ramka_lista_obiektow, values=[""] + editorials)
combobox_filtruj_redakcja.grid(row=1, column=0, columnspan=3)
combobox_filtruj_redakcja.set("")
combobox_filtruj_redakcja.bind("<<ComboboxSelected>>", lambda e: show_users())

listboox_lista_obiektow = Listbox(ramka_lista_obiektow, width=60, height=15)
listboox_lista_obiektow.grid(row=2, column=0, columnspan=3)

Button(ramka_lista_obiektow, text="pokaż szczegóły", command=show_user_details).grid(row=3, column=0)
Button(ramka_lista_obiektow, text="usuń obiekt", command=remove_user).grid(row=3, column=1)
Button(ramka_lista_obiektow, text="edytuj obiekt", command=edit_user).grid(row=3, column=2)

# ramka_formularz
Label(ramka_formularz, text="FORMULARZ").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Imię").grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text="Nazwisko").grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text="Miejscowość").grid(row=3, column=0, sticky=W)
Label(ramka_formularz, text="Posty").grid(row=4, column=0, sticky=W)
Label(ramka_formularz, text="Redakcja").grid(row=5, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=3, column=1)
entry_posts = Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)
combobox_redakcja = ttk.Combobox(ramka_formularz, values=editorials)
combobox_redakcja.grid(row=5, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text="dodaj użytkownika", command=add_user)
button_dodaj_obiekt.grid(row=6, column=0, columnspan=2)

# ramka_szczegoly_obiektow
Label(ramka_szczegoly_obiektow, text="szczegóły obiektu:").grid(row=0, column=0)
Label(ramka_szczegoly_obiektow, text="Imię:").grid(row=1, column=0)
label_name_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="......")
label_name_szczegoly_obiektow_wartosc.grid(row=1, column=1)
Label(ramka_szczegoly_obiektow, text="Nazwisko:").grid(row=1, column=2)
label_surname_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="......")
label_surname_szczegoly_obiektow_wartosc.grid(row=1, column=3)
Label(ramka_szczegoly_obiektow, text="Miejscowość:").grid(row=1, column=4)
label_location_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="......")
label_location_szczegoly_obiektow_wartosc.grid(row=1, column=5)
Label(ramka_szczegoly_obiektow, text="Posty:").grid(row=1, column=6)
label_posts_szczegoly_obiektow_wartosc = Label(ramka_szczegoly_obiektow, text="......")
label_posts_szczegoly_obiektow_wartosc.grid(row=1, column=7)

# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=800, corner_radius=5)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)
map_widget.grid(row=0, column=0, columnspan=3)

root.mainloop()
