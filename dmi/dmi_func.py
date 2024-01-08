import getopt
import math
import os
import tkinter.messagebox as messagebox
import tkinter as tk
import datetime
import dmi_rest as dr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

new_image_tk = None
api_key = None
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

def coord_to_pixel(lat_list, lon_list):
    x_list = []
    y_list = []
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

    return x_list, y_list


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

    lightning_strikes = dr.get_lightning(year, api_key, filename)
    new_image = initial_image.copy()
    bolt = Image.open("bolt.png")
    bolt_resized = bolt.resize((20, 24))
    x_list, y_list = coord_to_pixel(*lightning_strikes)
    for x, y in zip(x_list, y_list):
        position = (int(x) - 10, int(y) - 12)  # 41 and 48 are half of the bolt images width and height
        new_image.paste(bolt_resized, position, bolt_resized)

    latest_image = new_image
    new_image.save("lightning_map.png")
    new_image_tk = ImageTk.PhotoImage(new_image)
    label.configure(image=new_image_tk)

