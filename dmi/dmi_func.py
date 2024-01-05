from getopt import getopt
import os
import tkinter.messagebox as messagebox
import tkinter as tk
import datetime
import dmi_rest as dr
import math
from PIL import Image, ImageTk

new_image_tk = None
api_key = None
window_name = "DMI Kola"  # Kort over lynnedslag app
map_w = 2533
map_h = 2160

initial_image = Image.open("map.png")
latest_image = None

def parseargs(argobject):
    global api_key
    opts, args = getopt(argobject, "hk", ["--help", "--key"])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print("usage: dmi_gui.py [OPTION]")
            print("Options:")
            print("-h            :")
            print("  --help      : Show this help message and exit.")
            print("-k <key>      : DMI Lightning Data API Key")
            print("  --key <key> : DMI Lightning Data API Key")
            exit(0)
        elif opt in ("-k", "--key"):
            if arg is None:
                raise Exception("Key is required")
            else:
                api_key = arg


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


def coord_to_pixel(lat, lon):
    map_lon_left = 7.8
    map_lon_right = 15.4
    map_lon_delta = map_lon_right - map_lon_left
    map_lat_bottom = 54.3

    map_lat_bottom_degree = map_lat_bottom * math.pi / 180

    x = (lon - map_lon_left) * (map_w / map_lon_delta)
    lat = lat * math.pi / 180
    world_map_width = ((map_w / map_lon_delta) * 360) / (2 * math.pi)
    map_offset_y = (world_map_width / 2 * math.log((1 + math.sin(map_lat_bottom_degree)) / (1 - math.sin(map_lat_bottom_degree))))
    y = map_h - ((world_map_width / 2 * math.log((1 + math.sin(lat)) / (1 - math.sin(lat)))) - map_offset_y)

    print(f"Lightning strike at {x}, {y}")
    return [int(x), int(y)]


def do_kola(label : tk.Label, year):
    global latest_image
    global new_image_tk
    try:
        year = int(year)
    except ValueError:
        messagebox.showerror(window_name, "Årstal er ikke et heltal.")
        return 1

    if year < 2000 or year > datetime.date.today().year:  # 2000 is the earliest data for DMI registered lightning strikes
        messagebox.showerror(window_name, "Årstal er ugyldigt.\nPrøver du at tilgå data fra fremtiden eller før år 2000?")
        return 1

    lightning_strikes = dr.get_lightning(year, api_key)
    new_image = initial_image.copy()
    bolt = Image.open("bolt.png")
    for strike in lightning_strikes:
        x, y = coord_to_pixel(strike[0], strike[1])
        position = (x - 41, y - 48)  # 41 and 48 are half of the bolt images width and height
        new_image.paste(bolt, position)

    latest_image = new_image
    new_image_tk = new_image.resize((500, 426))
    new_image_tk.save("new_map.png")
    new_image_tk = ImageTk.PhotoImage(new_image_tk)
    label.configure(image=new_image_tk)
