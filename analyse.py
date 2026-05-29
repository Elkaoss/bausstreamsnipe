import pandas as pd
from collections import Counter

df = pd.read_excel("league_match_history.xlsx")

counter = Counter()

total_games = len(df)

for players in df["players_in_game"]:

    if pd.isna(players):
        continue

    player_list = [p.strip() for p in str(players).split("|")]

    unique_players = set(player_list)

    counter.update(unique_players)

top5 = counter.most_common(10)

print("Top 10 joueurs rencontrés :\n")

for player, count in top5:

    percentage = (count / total_games) * 100

    print(f"{player} - {count} games - {percentage:.2f}%")
