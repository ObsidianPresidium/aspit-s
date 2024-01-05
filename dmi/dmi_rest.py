import requests
import tkinter.messagebox as messagebox
import json

def get_lightning(year, key):
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
    features = response["features"]

    output = []
    for feature in features:
        output.append([feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]])

    return output

