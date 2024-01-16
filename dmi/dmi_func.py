import getopt
import math
import os
import tkinter.messagebox
import tkinter.messagebox as messagebox
import tkinter as tk
import tkinter.filedialog as filedialog
from tkinter import ttk
import datetime
import requests
import json
import time
from PIL import Image, ImageTk
import threading

new_image_tk = None
api_key = None
progress_bar: ttk.Progressbar
progress_info: tk.Text
progress_label: tk.Label
progress_eta_label: tk.Label
map_label: tk.Label
request_button: tk.Button
main_window: tk.Tk
progress: int = 0
progressf: float = 0
progress_var: tk.IntVar
tree: ttk.Treeview
filename = ""
window_name = "DMI Kola"  # Kort over lynnedslag app
map_w = 793
map_h = 637
lightning_strikes_outside_borders = 0
lightning_strikes_per_municipality = None
do_write_lightning_strikes = False

initial_image = Image.open("denmark_osm_small.png")
latest_image: Image = None

def parseargs(argobject):
    global api_key, filename, do_write_lightning_strikes, lightning_strikes_per_municipality
    try:
        opts, args = getopt.getopt(argobject, "hk:f:o:i:", ["help", "key=", "filename=", "json=", "output-lightning-strikes=", "input-lightning-strikes="])
    except getopt.GetoptError:
        print("An option was not recognized or you forgot to supply an argument with your parameter.")
        exit(1)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("usage: dmi_gui.py [OPTION]")
            print("Options:")
            print("-h                                      v")
            print("  --help                                : Show this help message and exit.")
            print("-k <key>                                v")
            print("  --key <key>                           : DMI Lightning Data API Key")
            print("-f <filename>                           v")
            print("  --filename <filename>                 v")
            print("  --json <filename>                     : Path to locally stored JSON response from DMI.")
            print("-o <filename>                           v")
            print("  --output-lightning-strikes <filename> : Write calculated lightning strikes per municipality to this file")
            print("-i <filename>                           v")
            print("  --input-lightning-strikes <filename>  : Use lightning strikes per municipality from this file instead of manually calculating")
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
        elif opt in ("-o", "--output-lightning-strikes"):
            if arg is None or arg == "":
                raise Exception("Supply a path to the file.")
            else:
                do_write_lightning_strikes = arg
        elif opt in ("-i", "--input-lightning-strikes"):
            if arg is None or arg == "":
                raise Exception("A filename is needed for the input lightning strikes option.")
            else:
                with open(arg, "r", encoding="utf-8") as file:
                    lightning_strikes_per_municipality = json.load(file)


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


def load_into_func(mw : tk.Tk, pl : tk.Label, pi : tk.Text, pb : ttk.Progressbar, pv : tk.IntVar, pe: tk.Label, ml : tk.Label, rb: tk.Button, tr: ttk.Treeview):
    global main_window
    global progress_label
    global progress_info
    global progress_bar
    global progress_var
    global progress_eta_label
    global map_label
    global request_button
    global tree

    main_window = mw
    progress_label = pl
    progress_info = pi
    progress_bar = pb
    progress_eta_label = pe
    map_label = ml
    request_button = rb
    progress_var = pv
    tree = tr


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

    step_coord_to_pixel((lon_strikes, lat_strikes))


def format_municipalities():
    with open("municipalities_unformatted.json", "r") as f:
        municipalities = json.load(f)

    municipalities = municipalities["geometries"]["features"]
    output = []

    for polygon in municipalities:
        name = polygon["properties"]["id"]
        name = name.replace("Ae", "Æ")
        name = name.replace("ae", "æ")
        name = name.replace("Oe", "Ø")
        name = name.replace("oe", "ø")
        if polygon["geometry"]["type"] == "MultiPolygon":
            # do something completely different
            for sub_polygon in polygon["geometry"]["coordinates"]:
                out_polygon = []
                for point in sub_polygon[0]:
                    out_polygon.append((point[1], point[0],))
                output.append({"name": name, "polygon": out_polygon, "num_lightning_strikes": 0})
        elif polygon["geometry"]["type"] == "Polygon":
            polygon = polygon["geometry"]["coordinates"][0]
            out_polygon = []
            for point in polygon:
                out_polygon.append((point[1], point[0],))
            output.append({"name": name, "polygon": out_polygon, "num_lightning_strikes": 0})

    return output


def log(info : str | None, step : float | None =-1, bar_info : str | None=None):
    global progress_info
    global progress_bar
    global progress
    global progressf
    global progress_var
    if info is not None:
        progress_info.configure(state="normal")
        progress_info.insert("1.0", info + "\n")
        progress_info.configure(state="disabled")
    if info is not None or bar_info is not None:
        progress_label.configure(text=info if bar_info is None else bar_info)

    if step is not None:
        if step != -1:
            progress = step
            progressf = step
            progress_var.set(int(progress))
        elif step >= 100:
            progress_var.set(99)
            progress_bar.step(0.9)  # this is necessary because there is no float var in Tkinter


def coord_to_pixel(lat_list, lon_list):
    global progress_bar
    global progress
    global progressf
    x_list = []
    y_list = []
    step_delta: float = (3 - progress) / len(lat_list)
    progress_bar.stop()
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
        progressf += step_delta
        progress = int(progressf)
        progress_var.set(int(progressf))

    return x_list, y_list


def is_point_in_polygon(point, polygon):
    x, y = point
    inside = False
    n = len(polygon)
    p1x, p1y = polygon[0]

    for i in range(1, n+1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xints:
                            inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def step_coord_to_pixel(lightning_strikes):
    progress_bar.configure(mode="determinate")
    log(f"Omregner koordinaterne fra {len(lightning_strikes[0])} lynnedslag til danmarkskortet...", 3, "Omregner koordinater...")
    x_list, y_list = coord_to_pixel(*lightning_strikes)
    municipalities = step_detect_municipality(*lightning_strikes)
    step_create_image(x_list, y_list, municipalities)


def step_detect_municipality(lon_list, lat_list):
    global progressf
    global progress
    global progress_var
    global progress_eta_label
    global lightning_strikes_outside_borders
    if not lightning_strikes_per_municipality:
        lightning_strikes_outside_borders = 0
        step_delta: float = (97 - progress) / len(lon_list)
        log("Dette kommer til at tage laaang tid. Anbefaling: hent en kop kaffe.\nUdregner hvor lynnedslag falder i kommunerne", 3, "Udregner lynnedslag for kommunerne")
        m = format_municipalities()
        for x, y in zip(lon_list, lat_list):
            municipality_found = False
            current_municipality = 0
            while not municipality_found:
                if current_municipality >= len(m):
                    lightning_strikes_outside_borders += 1
                    municipality_found = True
                    current_municipality -= 1
                elif is_point_in_polygon((x, y), m[current_municipality]["polygon"]):
                    m[current_municipality]["num_lightning_strikes"] += 1
                    municipality_found = True
                    current_municipality -= 1
                current_municipality += 1
            progressf += step_delta
            progress = int(progressf)
            progress_var.set(int(progressf))

        # consolidate islands of municipalities into the same municipality in a differently structured dict
        # from: { "name": string, "polygon": list, "num_lightning_strikes": int }
        # to: { "<name>": <sum_num_lightning_strikes> }
        municipalities_strikes = {}

        for municipality in m:
            if municipality["name"] not in municipalities_strikes.keys():
                municipalities_strikes[municipality["name"]] = municipality["num_lightning_strikes"]
            else:
                municipalities_strikes[municipality["name"]] += municipality["num_lightning_strikes"]

        if do_write_lightning_strikes:
            with open(do_write_lightning_strikes, "w", encoding="utf-8") as file:
                json.dump(municipalities_strikes, file)
    else:
        municipalities_strikes = lightning_strikes_per_municipality

    progress_eta_label.configure(text="")
    step_insert_into_treeview(municipalities_strikes)
    return municipalities_strikes

def step_insert_into_treeview(municipalities):
    global tree
    tree.delete(*tree.get_children())
    municipalities = {key: value for key, value in sorted(municipalities.items(), key=lambda item: item[1], reverse=True)}
    for index, (municipality, lightning_strikes) in enumerate(municipalities.items()):
        if index % 2 == 0:
            tree.insert(parent="", index="end", iid=str(index), text="", values=(municipality, lightning_strikes),
                        tags=("evenrow",))
        else:
            tree.insert(parent="", index="end", iid=str(index), text="", values=(municipality, lightning_strikes),
                        tags=("oddrow",))


def step_create_image(x_list, y_list, municipalities):
    global latest_image
    global new_image_tk
    global progress
    global progressf
    global progress_var
    log(f"Sætter lyn-ikoner på danmarkskortet...")
    new_image = initial_image.copy()
    bolt = Image.open("bolt.png")
    bolt_resized = bolt.resize((5, 6))
    step_delta : float = (99.9 - progress) / len(x_list)
    for x, y in zip(x_list, y_list):
        position = (int(x) - 2, int(y) - 3)  # 41 and 48 are half of the bolt images width and height
        new_image.paste(bolt_resized, position, bolt_resized)
        progressf += step_delta
        progress = int(progressf)
        progress_var.set(progress)

    latest_image = new_image
    new_image.save("lightning_map.png")
    new_image_tk = ImageTk.PhotoImage(new_image)
    map_label.configure(image=new_image_tk)
    log(f"Lynnedslag i Ringkøbing-Skjern Kommune: {municipalities['Ringkøbing-Skjern']}", 100, "")
    log(f"Lynnedslag udenfor Danmarks grænser: {lightning_strikes_outside_borders}", 100, "")
    log("---FÆRDIG---", 100, "")
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
    progress_bar.start()
    request_button.configure(state="disabled")
    log("---START---", bar_info="Klar")
    log(f"Downloader data fra år {year} fra DMI...")
    download_thread.start()


def clear():
    global new_image_tk
    global latest_image
    global tree
    log("Sletter lynnedslag", 0, "")
    tree.delete(*tree.get_children())
    latest_image = initial_image
    new_image_tk = ImageTk.PhotoImage(initial_image)
    map_label.configure(image=new_image_tk)


def save_as():
    if latest_image is not None:
        new_filename = filedialog.asksaveasfilename(initialdir="~", title="Gem billede",
                                                    filetypes=(
                                                        ("PNG-billede", "*.png"),
                                                        ("Alle filer", "*.*")
                                                    ))
        latest_image.save(new_filename, "PNG")
    else:
        tkinter.messagebox.showerror(window_name, message="Intet billede er tegnet endnu", parent=main_window)
