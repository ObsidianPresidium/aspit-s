import requests

url = f"https://boundaries-api.io/api/denmark/geometry/find/level/"
params = {
    "level": 2
}
response = requests.get(url, params=params)

print(response.status_code)
print(response.reason)
print("Writing data..")
with open("municipalities_by_id.json", "w") as f:
    f.write(response.text)