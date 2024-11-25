import json
import os
import urllib.request
import zipfile
from tqdm import tqdm

json_file = "external_files.json"

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

with open(json_file, "r", encoding="utf-8") as f:
    external_files_json = json.load(f)

external_files = external_files_json["externalFiles"]



if __name__ == "__main__":
    print("Get External Files")
    print("====================")
    print(" -> Sorting by retrieval method...")
    kaggle_files = []
    normal_files = []
    for file in external_files:
        if file["method"] == "kaggle":
            kaggle_files.append(file)
        else:
            normal_files.append(file)
    print(" -> Creating directories...")
    for file in external_files:
        os.makedirs(os.path.dirname(file["filename"]), exist_ok=True)

    if len(kaggle_files) > 0:
        print(" -> Retrieving Kaggle files...")
        if not os.path.exists(os.path.join(os.path.expanduser("~"), ".config", "kaggle", "kaggle.json")):
            print("Kaggle API not configured. Please enter your Kaggle username and API token")
            os.makedirs(os.path.join(os.path.expanduser("~"), ".config", "kaggle"), exist_ok=True)
            kaggle_username = input("Kaggle username: ")
            kaggle_token = input("Kaggle API token: ")

            with open(os.path.join(os.path.expanduser("~"), ".config", "kaggle", "kaggle.json"), "w", encoding="utf-8") as f:
                json.dump({"username": kaggle_username, "key": kaggle_token}, f)
            os.chmod(os.path.join(os.path.expanduser("~"), ".config", "kaggle", "kaggle.json"), 0o600)
        import kaggle
        kaggle.api.authenticate()
        for file in kaggle_files:
            print(file["filename"])
            kaggle.api.dataset_download_files(file["name"], path=os.path.dirname(file["filename"]), unzip=True)
            print()

    if len(normal_files) > 0:
        print(" -> Downloading other external files...")
        for file in external_files:
            print(os.path.basename(file["filename"]))
            download_url(file["url"], file["filename"])
            print()

        print(" -> Extracting...", end="")
        for file in external_files:
            if file["decompress"]:
                with zipfile.ZipFile(file["filename"], 'r') as zip_ref:
                    zip_ref.extractall(os.path.dirname(file["filename"]))
                os.remove(file["filename"])

    print("Done")