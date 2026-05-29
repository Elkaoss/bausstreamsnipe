import pandas as pd
from collections import Counter

# Charger le fichier Excel
df = pd.read_excel("league_match_history.xlsx")

counter = Counter()

total_games = len(df)

# Parcours des games
for players in df["players_in_game"]:

    if pd.isna(players):
        continue

    # Séparer les joueurs
    player_list = [p.strip() for p in str(players).split("|")]

    # Evite doublons dans une même game
    unique_players = set(player_list)

    counter.update(unique_players)

# Top 5
top5 = counter.most_common(10)

print("Top 5 joueurs rencontrés :\n")

for player, count in top5:

    percentage = (count / total_games) * 100

    print(f"{player} - {count} games - {percentage:.2f}%")