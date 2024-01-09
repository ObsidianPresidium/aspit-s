import requests
import os

def get_key():
    root_folder = os.path.dirname(os.path.abspath(__file__))
    folder_contents = os.listdir(root_folder)
    for item in folder_contents:
        if os.path.basename(item) == "key.txt":
            with open(os.path.join(root_folder, "key.txt"), "r") as key_file:
                api_key = key_file.readline()
                return api_key
    return False


def get_lightning(year, key):
    url = f"https://dmigw.govcloud.dk/v2/lightningdata/collections/observation/items"
    headers = { "X-Gravitee-Api-Key": key }
    params = {
        "datetime": f"{year}-01-01T00:00:00+01:00/{year + 1}-01-01T00:00:00+01:00",
        "limit": 299999,
        "bbox": "7.6722,54.4127,15.6043,57.9733"
    }
    print("Transferring data...")
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise SystemExit("Error!")

    print("Writing data to sample_data.json...")
    with open("sample_data.json", "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    get_lightning(2023, get_key())
