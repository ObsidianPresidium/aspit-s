import json
import requests

def get_municipality_name():
    json_file = "municipalities_by_id.json"
    with open(json_file, "r", encoding="utf-8") as f:
        my_dict = json.loads("".join(f.readlines()))

    ids = ""

    for municipality in my_dict["geometries"]["features"]:
        ids += municipality["properties"]["id"] + ","

    ids = ids[:-1]
    print(ids)

    url = f"https://boundaries-api.io/api/denmark/attributes/find/id/"
    params = {
        "id": ids
    }

    response = requests.get(url, params=params)

    print(response.status_code)
    print(response.reason)

    print("Writing data (municipalities_by_name)..")
    with open("municipalities_by_name.json", "w") as f:
        f.write(response.text)

    names = response.json()
    with open("municipalities_by_id.json", "r") as id_file:
        id_file_contents = id_file.read()
    for municipality in names["attributes"]:
        id_file_contents = id_file_contents.replace(municipality["id"], municipality["name"]["dan"])
    with open("municipalities_unformatted.json", "w") as f:
        f.write(id_file_contents)

if __name__ == "__main__":
    get_municipality_name()