import getopt
import math
import os
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk
import datetime
import requests
import json
from PIL import Image, ImageTk
import threading

new_image_tk = None
api_key = None
progress_bar: ttk.Progressbar
progress_info: tk.Text
progress_label: tk.Label
map_label: tk.Label
request_button: tk.Button
progress = 0
filename = ""
window_name = "DMI Kola"  # Kort over lynnedslag app
map_w = 793
map_h = 637

initial_image = Image.open("denmark_osm_small.png")
latest_image = None

def parseargs(argobject):
    global api_key, filename
    try:
        opts, args = getopt.getopt(argobject, "hk:f:", ["help", "key=", "filename=", "json="])
    except getopt.GetoptError:
        print("An option was not recognized or you forgot to supply an argument with your parameter.")
        exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("usage: dmi_gui.py [OPTION]")
            print("Options:")
            print("-h                      v")
            print("  --help                : Show this help message and exit.")
            print("-k <key>                v")
            print("  --key <key>           : DMI Lightning Data API Key")
            print("-f <filename>           v")
            print("  --filename <filename> v")
            print("  --json <filename>     : Path to locally stored JSON response. Must be in DMI's format.")
            exit(0)
        elif opt in ("-k", "--key"):
            if arg is None:
                raise Exception("Key is required")
            else:
                api_key = arg
        elif opt in ("-f", "--filename", "--json"):
            if arg is None or arg == "":
                raise Exception("Supply a path to the file.")
            else:
                filename = arg


def get_key():
    global api_key
    if api_key is not None:
        return api_key
    else:
        root_folder = os.path.dirname(os.path.abspath(__file__))
        folder_contents = os.listdir(root_folder)
        for item in folder_contents:
            if os.path.basename(item) == "key.txt":
                with open(os.path.join(root_folder, "key.txt"), "r") as key_file:
                    api_key = key_file.readline()
                    return api_key
        return False


def load_into_func(pl : tk.Label, pi : tk.Text, pb : ttk.Progressbar, ml : tk.Label, rb: tk.Button):
    global progress_label
    global progress_info
    global progress_bar
    global map_label
    global request_button

    progress_label = pl
    progress_info = pi
    progress_bar = pb
    map_label = ml
    request_button = rb


class BaseThread(threading.Thread):
    def __init__(self, callback=None, callback_args=None, *args, **kwargs):
        target = kwargs.pop('target')
        super(BaseThread, self).__init__(target=self.target_with_callback, *args, **kwargs)
        self.callback = callback
        self.method = target
        self.callback_args = callback_args

    def target_with_callback(self):
        self.method()
        if self.callback is not None:
            self.callback(*self.callback_args)


def get_lightning(year, key, json_file=None):
    if json_file is None or json_file == "":
        url = f"https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items"
        headers = { "X-Gravitee-Api-Key": key }
        params = {
            "datetime": f"{year}-01-01T00:00:00+01:00/{year + 1}-01-01T00:00:00+01:00",
            "limit": 299999,
            "bbox": "7.6722,54.4127,15.6043,57.9733"
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            messagebox.showerror("Error!")
            raise SystemExit("Error!")

        response = response.json()
        print(response)
    else:
        json_file = os.path.abspath(json_file)
        with open(json_file, "r", encoding="utf-8") as file:
            response = json.loads("".join(file.readlines()))
    features = response["features"]

    lon_strikes = []
    lat_strikes = []
    for feature in features:
        lon_strikes.append(feature["geometry"]["coordinates"][1])
        lat_strikes.append(feature["geometry"]["coordinates"][0])

    step_calculate((lon_strikes, lat_strikes))



def log(info : str, step : float=-1):
    global progress_info
    global progress_bar
    global progress
    step = 99.9 if step > 99.9 else step
    progress_info.configure(state="normal")
    progress_info.insert("1.0", info + "\n")
    progress_info.configure(state="disabled")
    progress_label.configure(text=info)

    if step != -1:
        progress = step
        progress_bar.step(step)



def coord_to_pixel(lat_list, lon_list):
    global progress_bar
    global progress
    x_list = []
    y_list = []
    step_delta = (50 - progress) / len(lat_list)
    #             W      E       N       S
    map_coords = (7.625, 15.601, 57.979, 54.419)
    map_lat_bottom_rad = map_coords[3] * math.pi / 180
    map_lon_delta = (map_coords[1] - map_coords[0])
    world_map_width = ((map_w / map_lon_delta) * 360) / (2 * math.pi)
    map_offset_y = (world_map_width / 2 * math.log((1 + math.sin(map_lat_bottom_rad)) / (1 - math.sin(map_lat_bottom_rad))))

    for lat, lon in zip(lat_list, lon_list):
        lat_rad = lat * math.pi / 180
        x = (lon - map_coords[0]) * (map_w / map_lon_delta)
        y = map_h - ((world_map_width / 2 * math.log((1 + math.sin(lat_rad)) / (1 - math.sin(lat_rad)))) - map_offset_y)
        x_list.append(x)
        y_list.append(y)
        progress += step_delta
        progress_bar.step(progress)

    return x_list, y_list


def step_calculate(lightning_strikes):
    progress_bar.configure(mode="determinate")
    log(f"Omregner koordinaterne fra {len(lightning_strikes[0])} lynnedslag til danmarkskortet...", 25)
    x_list, y_list = coord_to_pixel(*lightning_strikes)
    step_create_image(x_list, y_list)



def step_create_image(x_list, y_list):
    global latest_image
    global new_image_tk
    global progress
    log(f"Sætter lyn-ikoner på danmarkskortet...")
    new_image = initial_image.copy()
    bolt = Image.open("bolt.png")
    bolt_resized = bolt.resize((20, 24))
    step_delta = (99.9 - progress) / len(x_list)
    for x, y in zip(x_list, y_list):
        position = (int(x) - 10, int(y) - 12)  # 41 and 48 are half of the bolt images width and height
        new_image.paste(bolt_resized, position, bolt_resized)
        progress += step_delta
        progress_bar.step(progress)

    latest_image = new_image
    new_image.save("lightning_map.png")
    new_image_tk = ImageTk.PhotoImage(new_image)
    map_label.configure(image=new_image_tk)
    log("Færdig.", 99.9)
    request_button.configure(state="active")


def do_kola(year):
    try:
        year = int(year)
    except ValueError:
        messagebox.showerror(window_name, "Årstal er ikke et heltal.")
        return 1

    if year < 2000 or year > datetime.date.today().year:  # 2000 is the earliest data for DMI registered lightning strikes
        messagebox.showerror(window_name, "Årstal er ugyldigt.\nPrøver du at tilgå data fra fremtiden eller før år 2000?")
        return 1

    download_thread = threading.Thread(target=get_lightning, args=(year, api_key, filename,))
    progress_bar.configure(mode="indeterminate")
    request_button.configure(state="disabled")
    log(f"Downloader data fra år {year} fra DMI...")
    download_thread.start()







