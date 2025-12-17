import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
import calendar
from datetime import date

LT_MONTHS = [
    "", "Sausis", "Vasaris", "Kovas", "Balandis", "Gegužė", "Birželis",
    "Liepa", "Rugpjūtis", "Rugsėjis", "Spalis", "Lapkritis", "Gruodis"
]


class EventCalendar(toga.Box):
    def __init__(self, year, month, events=None, on_date_selected=None, on_month_change=None):
        super().__init__(style=Pack(direction=COLUMN, padding=10))

        self.year = year
        self.month = month
        self.events = events or {}
        self.on_date_selected = on_date_selected
        self.on_month_change = on_month_change

        # **********************
        #      HEADER
        # **********************
        header = toga.Box(style=Pack(direction=ROW, alignment=CENTER, padding_bottom=10))

        # ◀ Previous month
        prev_btn = toga.Button("◀", on_press=self.prev_month, style=Pack(width=30))

        # Month label
        self.month_label = toga.Label(
            f"{LT_MONTHS[self.month]} {self.year}",
            style=Pack(font_size=16, alignment=CENTER, padding_left=10, padding_right=10)
        )

        # ▶ Next month
        next_btn = toga.Button("▶", on_press=self.next_month, style=Pack(width=30))

        header.add(prev_btn)
        header.add(self.month_label)
        header.add(next_btn)

        self.add(header)

        # Container for calendar grid so we can rebuild it
        self.grid_box = toga.Box(style=Pack(direction=COLUMN))
        self.add(self.grid_box)

        self.build_calendar()

    # -------------------------
    # BUILD CALENDAR GRID
    # -------------------------
    def build_calendar(self):
        self.grid_box.clear()

        weekdays = ["Pr", "An", "Tr", "Kt", "Pn", "Št", "Sk"]
        row = toga.Box(style=Pack(direction=ROW))
        for day in weekdays:
            row.add(toga.Label(day, style=Pack(width=40, alignment=CENTER, padding=3)))

        self.grid_box.add(row)

        cal = calendar.Calendar(firstweekday=0)
        today_str = date.today().strftime("%Y-%m-%d")

        for week in cal.monthdayscalendar(self.year, self.month):
            week_row = toga.Box(style=Pack(direction=ROW))

            for day in week:
                if day == 0:
                    btn = toga.Label("", style=Pack(width=44, height=30))
                else:
                    date_str = f"{self.year}-{self.month:02d}-{day:02d}"
                    event = self.events.get(date_str)

                    if event:
                        bg = event.get("color", "#FFDD88")
                    else:
                        bg = "#EEEEEE"

                    if date_str == today_str:
                        bg = "#66CCFF"  # highlight today

                    btn = toga.Button(
                        str(day),
                        style=Pack(width=40, height=50, padding=2,
                                   background_color=bg, alignment=CENTER),
                        on_press=self._make_on_press(date_str)
                    )

                week_row.add(btn)

            self.grid_box.add(week_row)

    # -------------------------
    # NAVIGATION
    # -------------------------
    def prev_month(self, widget):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1

        self.month_label.text = f"{LT_MONTHS[self.month]} {self.year}"
        self.build_calendar()

        if self.on_month_change:
            self.on_month_change(self.year, self.month)

    def next_month(self, widget):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1

        self.month_label.text = f"{LT_MONTHS[self.month]} {self.year}"
        self.build_calendar()

        if self.on_month_change:
            self.on_month_change(self.year, self.month)

    def _make_on_press(self, date_str):
        def handler(widget):
            event = self.events.get(date_str)
            if self.on_date_selected:
                self.on_date_selected(date_str, event)
        return handler
