import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import calendar
from datetime import date
from Trash import app_base


print("importuotas modulis:", app_base.__file__)

LT_MONTHS = [
    "",  # indeksui sulyginti (1–12)
    "Sausis", "Vasaris", "Kovas", "Balandis", "Gegužė", "Birželis",
    "Liepa", "Rugpjūtis", "Rugsėjis", "Spalis", "Lapkritis", "Gruodis"
]
today = date.today().strftime("%Y-%m-%d")


class EventCalendar(toga.Box):
    def __init__(self, year, month, events=None, on_date_selected=None):
        super().__init__(style=Pack(direction=COLUMN, padding=10))

        self.year = year
        self.month = month
        self.events = events or {}
        self.on_date_selected = on_date_selected

        # Header with month name

        # Month control row (← month →)
        controls = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_bottom=5))

        prev_btn = toga.Button("◀", on_press=self.prev_month, style=Pack(padding=5))
        next_btn = toga.Button("▶", on_press=self.next_month, style=Pack(padding=5))

        controls.add(prev_btn)
        controls.add(
            toga.Label(
                LT_MONTHS[self.month],
                style=Pack(font_size=16, alignment=CENTER, padding=5, flex=1)
            )
        )
        controls.add(next_btn)

        self.month_label = controls.children[1]  # išsaugom, kad galėtume atnaujinti pavadinimą

        self.add(controls)

        month_name = LT_MONTHS[self.month].capitalize()
        self.title = toga.Label(
            f"{month_name}",
            style=Pack(font_size=16, alignment=CENTER, padding_bottom=10, flex=1),
        )
        self.add(self.title)

        # Weekday headers
        weekdays = ["Pr", "An", "Tr", "Kt", "Pn", "Št", "Sk"]
        row = toga.Box(style=Pack(direction=ROW))
        for day in weekdays:
            row.add(
                toga.Label(day, style=Pack(width=40, alignment=CENTER, padding=3))
            )
        self.add(row)

        # Calendar grid
        cal = calendar.Calendar(firstweekday=0)
        for week in cal.monthdayscalendar(self.year, self.month):
            week_row = toga.Box(style=Pack(direction=ROW))
            for day in week:
                if day == 0:
                    # Empty space
                    btn = toga.Label("", style=Pack(width=44, height=30))
                else:
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"

                    event = self.events.get(date_str)
                    if event:
                        bg = event.get("color", "#FFDD88")  # fallback spalva
                    else:
                        bg = "#EEEEEE"

                    # Pažymėti šiandienos datą specialia spalva
                    if date_str == today:
                        bg = "#66CCFF"  # mėlynas langelis šiandienai

                    btn = toga.Button(
                        str(day),
                        style=Pack(
                            width=40,
                            height=50,
                            padding=2,
                            background_color=bg,
                            alignment=CENTER
                        ),
                        on_press=self._make_on_press(date_str)
                    )

                week_row.add(btn)
            self.add(week_row)

    def _make_on_press(self, date_str):
        def handler(widget):
            event = self.events.get(date_str)
            if self.on_date_selected:
                self.on_date_selected(date_str, event)
        return handler


class CalendarApp(toga.App):
    def startup(self):
        # Kiekvienam įvykiui suteikiame spalvą
        events = app_base.load_events()

        def date_selected(date_str, event):
            if event:
                self.main_window.info_dialog("Įvykis", f"{date_str} — {event['title']}")
            else:
                self.main_window.info_dialog("Data", f"Pasirinkta: {date_str}")

        calendar_widget = EventCalendar(
            year=2025,
            month=int(date.today().strftime("%m")),
            events=events,
            on_date_selected=date_selected
        )

        self.main_window = toga.MainWindow(title="Kauno miesto individualių namų šiukšlių vežimo grafikas")
        self.main_window.content = calendar_widget
        self.main_window.show()

        # ---- nauja dalis ----
        today_str = date.today().strftime("%Y-%m-%d")
        if today_str in events:
            date_selected(today_str, events[today_str])
        else:
            date_selected(today_str, None)

def main():
    return CalendarApp()
