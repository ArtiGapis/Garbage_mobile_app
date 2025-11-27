import json
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

def reader(filename):
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def get_garbage(trash):
    data = reader('trash_db.json')
    return data[trash]


def load_events():
    events = {}

    trash_wrap = {
        "mixed": {"title": "Mišrios atliekos", "color": "#02cf1a"},  # raudonai
        "paper": {"title": "Popieriaus atliekos", "color": "#032896"},  # žaliai
        "glass": {"title": "Stiklo atliekos", "color": "#383831"}  # mėlynai
    }

    for trash_type in trash_wrap.keys():
        misrios = get_garbage(trash_type)

        for m in misrios:
            y, m, d = m.replace(" ", "-").split("-")
            date_str = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
            events[date_str] = {
                "title": trash_wrap[trash_type]['title'],
                "color": trash_wrap[trash_type]['color']
            }
    return events


