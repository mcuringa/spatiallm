import json
import re
import requests

PLACES = [
    "Mama's Too",
    "Lucali",
    "Luigi's",
    "L'Industrie Pizza",
    "F&F Pizzeria",
    "Stretch Pizza",
    "Ops",
    "Joe's Pizza",
    "Grand Street Pizza",
    "Una Pizza Napoletana",
    "Patsy's Pizzeria",
]

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def build_query(names):
    # NYC admin boundary (Overpass area from relation)
    # We match exact names via regex anchors: ^...$
    blocks = "\n".join(
        f'  nwr["name"~"^{re.escape(n)}$"](area.nyc);'
        for n in names
    )
    return f"""
[out:json][timeout:60];
area["name"="New York City"]["boundary"="administrative"]->.nyc;
(
{blocks}
);
out tags center;
""".strip()


def main():
    query = build_query(PLACES)
    r = requests.post(OVERPASS_URL, data=query.encode("utf-8"), timeout=90)
    r.raise_for_status()
    data = r.json()

    # pretty print json
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()