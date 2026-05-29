# import requests
# import pandas as pd
# import time

API_KEY = "YOUR PERSONAL KEY"

GAME_NAME = "Thebausffs"
TAG_LINE = "COOL"

# Region routing
REGION = "europe"
PLATFORM = "euw"

headers = {
    "X-Riot-Token": API_KEY
}

account_url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{GAME_NAME}/{TAG_LINE}"

account_response = requests.get(account_url, headers=headers)
account_data = account_response.json()

puuid = account_data["puuid"]

print("PUUID:", puuid)

all_matches = []
start = 0
count = 100

while True:
    matches_url = (
        f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/"
        f"{puuid}/ids?start={start}&count={count}"
    )

    response = requests.get(matches_url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.text)
        break

    match_ids = response.json()

    if not match_ids:
        break

    all_matches.extend(match_ids)

    print(f"Downloaded {len(all_matches)} matches")

    start += count

    time.sleep(1.2)

print("Total matches:", len(all_matches))

rows = []

for i, match_id in enumerate(all_matches):

    match_url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"

    response = requests.get(match_url, headers=headers)

    if response.status_code != 200:
        print("Failed:", match_id)
        continue

    data = response.json()

    participants = data["info"]["participants"]

    target_player = next(p for p in participants if p["puuid"] == puuid)

    other_players = []

    for p in participants:
        if p["puuid"] != puuid:
            riot_id = f"{p.get('riotIdGameName', 'Unknown')}#{p.get('riotIdTagline', '')}"
            other_players.append(riot_id)

    rows.append({
        "match_id": match_id,
        "champion": target_player["championName"],
        "kills": target_player["kills"],
        "deaths": target_player["deaths"],
        "assists": target_player["assists"],
        "win": target_player["win"],

        "players_in_game": " | ".join(other_players)
    })

    print(f"{i+1}/{len(all_matches)} processed")

    time.sleep(1.2)

df = pd.DataFrame(rows)

df.to_excel("league_match_history.xlsx", index=False)

print("Excel file created")
