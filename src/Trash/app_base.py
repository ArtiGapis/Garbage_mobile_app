
import json
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
SECRET_CODE = "KAUNAS"  # 👈 pakeisk jei reikia

# -------------------------
# READ JSON FILE
# -------------------------
def reader(filename):
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

x= reader('street_db.json')
print(x['address'])

def get_garbage(trash):
    data = reader('V. Tuinylos g.23A.json')
    return data[trash]



# -------------------------
# LOAD JSON INFO TO DICT
# -------------------------
def load_events():
    events = {}

    trash_wrap = {
        "mixed": {"title": "Mišrios atliekos", "color": "#02cf1a"},
        "paper": {"title": "Popieriaus atliekos", "color": "#032896"},
        "glass": {"title": "Stiklo atliekos", "color": "#383831"}
    }

    for trash_type in trash_wrap.keys():
        types_wrap = get_garbage(trash_type)

        for m in types_wrap:
            y, m, d = m.replace(" ", "-").split("-")
            date_str = f"{int(y):04d}-{int(m):02d}-{int(d):02d}"
            events[date_str] = {
                "title": trash_wrap[trash_type]['title'],
                "color": trash_wrap[trash_type]['color']
            }
    return events
