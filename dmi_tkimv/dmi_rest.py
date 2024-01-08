import requests
import tkinter.messagebox as messagebox
import json
import os

def get_lightning(year, key, json_file=None):
    if json_file is None or json_file == "":
        url = f"https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items"
        headers = { "X-Gravitee-Api-Key": key }
        params = {
            "datetime": f"{year}-01-01T00:00:00+01:00/{year + 1}-01-01T00:00:00+01:00"
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

    return lon_strikes, lat_strikes
