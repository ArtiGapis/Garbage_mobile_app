import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import calendar
from datetime import date
from Trash import app_base
from Trash import calendar_creator

LT_MONTHS = [
    "", "Sausis", "Vasaris", "Kovas", "Balandis", "Gegužė", "Birželis",
    "Liepa", "Rugpjūtis", "Rugsėjis", "Spalis", "Lapkritis", "Gruodis"
]

class CalendarApp(toga.App):

    SECRET_CODE = "KAUNAS"   # 👈 pakeisk jei reikia

    def startup(self):
        self.main_window = toga.MainWindow(
            title="Prisijungimas"
        )

        self.show_login()
        self.main_window.show()

    # -------------------------
    # CHECK INPUT
    # -------------------------
    def check_code(self, widget):
        if 'KAUNAS' == self.SECRET_CODE:
            self.show_calendar()
        else:
            self.main_window.error_dialog(
                "Klaida",
                "Neteisingas adresas"
            )

    # -------------------------
    # LOGIN SCREEN
    # -------------------------
    def show_login(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding=20, alignment=CENTER))

        label = toga.Label(
            "Naujas adresas:",
            style=Pack(padding_bottom=10, font_size=14)
        )

        self.input_field = toga.TextInput(
            placeholder="Įveskite adresą",
            style=Pack(width=200, padding_bottom=10)
        )

        new_button = toga.Button(
            "Patvirtinti",
            on_press=self.check_code,
            style=Pack(padding_top=10)
        )
        for address in app_base.reader('street_db.json')['address']:
            address_button = toga.Button(
                address,
                on_press=self.check_code,
                style=Pack(padding_top=10)
            )
            box.add(address_button)


        box.add(label)
        box.add(self.input_field)
        box.add(new_button)
        self.main_window.content = box



    # -------------------------
    # CALENDAR SCREEN
    # -------------------------
    def show_calendar(self):
        # from datetime import date
        # from Trash import app_base

        events = app_base.load_events()

        def date_selected(date_str, event):
            if event:
                self.main_window.info_dialog(
                    "Įvykis",
                    f"{date_str}\nŠiandien - {event['title']}"
                )
            else:
                self.main_window.info_dialog(
                    "Data",
                    f"{date_str}\nŠią dieną šiukšlių neveš"
                )

        year = date.today().year
        month = date.today().month

        calendar_widget = calendar_creator.EventCalendar(
            year=year,
            month=month,
            events=events,
            on_date_selected=date_selected
        )
        self.main_window.title = "Kauno miesto šiukšlių grafikas"
        self.main_window.content = calendar_widget

def main():
    return CalendarApp()
