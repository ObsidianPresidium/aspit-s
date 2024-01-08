import getopt
import math
import os
import tkinter.messagebox as messagebox
import tkinter as tk
import tkintermapview
from PIL import Image, ImageTk
import datetime
import dmi_rest as dr

api_key = None
filename = ""
window_name = "DMI Kola"  # Kort over lynnedslag app

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


def do_kola(mapview : tkintermapview.TkinterMapView, year):
    try:
        year = int(year)
    except ValueError:
        messagebox.showerror(window_name, "Årstal er ikke et heltal.")
        return 1

    if year < 2000 or year > datetime.date.today().year:  # 2000 is the earliest data for DMI registered lightning strikes
        messagebox.showerror(window_name, "Årstal er ugyldigt.\nPrøver du at tilgå data fra fremtiden eller før år 2000?")
        return 1

    bolt = Image.open("bolt.png")
    bolt = bolt.resize((20, 24))
    bolt = ImageTk.PhotoImage(bolt)
    lon_strikes, lat_strikes = dr.get_lightning(year, api_key, filename)

    for lon, lat in zip(lon_strikes, lat_strikes):
        print(f"Lightning strike at {lon}, {lat}")
        current_marker = mapview.set_marker(lon, lat, icon=bolt)

