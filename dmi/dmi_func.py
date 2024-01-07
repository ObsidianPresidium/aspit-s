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
    print(lat_list)
    print(lon_list)
    #       W      E       N       S
    BBox = (7.625, 15.601, 57.979, 54.419)
    plt_image = plt.imread("denmark_osm_small.png")
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(lat_list, lon_list, zorder=1, c="b", s=10)
    ax.set_xlim(BBox[0], BBox[1])
    ax.set_ylim(BBox[2], BBox[3])

    fig.savefig("denmark_osm_small_mapped.png", transparent=True)

    # map_lon_left = 7.8
    # map_lon_right = 15.4
    # # mellem er der 2533 pixels
    # map_lat_bottom = 54.3
    # map_lat_top = 57.9
    # # mellem er der 2160 pixels
    # y_pixel_per_coord = map_h / abs( map_lon_right - map_lon_left )
    # x_pixel_per_coord = map_w / abs( map_lat_top - map_lat_bottom )
    #
    # x = x_pixel_per_coord * lon
    # y = y_pixel_per_coord * lat


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
    coord_to_pixel(*lightning_strikes)
