"""
LOADS THE DATA AND PLOTS MESSI'S Shots ON A FIELD.

"""

import warnings

import matplotlib.pyplot as plt
from mplsoccer import Pitch
from statsbombpy import sb

# skip the statsbombpy warning because we dont need to be logged in for free data
warnings.filterwarnings("ignore")

LA_LIGA = 11
SEASON_2014_15 = 26  # the Messi-Suárez-Neymar treble season

# --- 1. Get every Barça match in that season ---------------------------------
# sb.matches() returns a pandas DataFrame: think of it as a spreadsheet,
# one row per match, one column per piece of info (date, teams, score...).
matches = sb.matches(competition_id=LA_LIGA, season_id=SEASON_2014_15)
print(f"Matches in the dataset this season: {len(matches)}")

# Find the away Clásico (Barcelona vs Real Madrid at the Santiago Bernabeu).
clasico = matches[
    (matches["home_team"] == "Real Madrid") & (matches["away_team"] == "Barcelona")
].iloc[0]  # .iloc[0] = "give me the first row"
print(f"Picked: {clasico['home_team']} {clasico['home_score']}-"
      f"{clasico['away_score']} {clasico['away_team']} ({clasico['match_date']})")

# --- 2. Get every event in that match -----------------------------------------
# An "event" is anything that happens on the ball: a pass, a dribble, a shot...
events = sb.events(match_id=clasico["match_id"])
print(f"Events in this match: {len(events)}")

# --- 3. Keep only Messi's shots ------------------------------------------------
shots = events[events["type"] == "Shot"]
messi_shots = shots[shots["player"].str.contains("Messi", na=False)]

print(f"\nMessi took {len(messi_shots)} shots:")
print(messi_shots[["minute", "shot_outcome", "shot_body_part", "shot_statsbomb_xg"]]
      .to_string(index=False))

# --- 4. Draw them on a pitch ---------------------------------------------------
# StatsBomb's pitch is 120 x 80. Coordinates are flipped so every team
# attacks left -> right, meaning the goal being shot at is always at x = 120
# Each shot's "location" is an [x, y] list.
pitch = Pitch(pitch_type="statsbomb", pitch_color="#1a1a2e", line_color="#c7d5cc")
fig, ax = pitch.draw(figsize=(10, 7))

for _, shot in messi_shots.iterrows():
    x, y = shot["location"]
    is_goal = shot["shot_outcome"] == "Goal"
    pitch.scatter(
        x, y, ax=ax,
        s=shot["shot_statsbomb_xg"] * 1500 + 50,  # bigger dot = better chance
        color="#edbb00" if is_goal else "#a50044",  # Barça gold / Barça red
        edgecolors="white", zorder=2,
    )

ax.set_title("Messi's shots vs Real Madrid, away 2014/15  (gold = goal, size = xG)",
             color="white", fontsize=13)
fig.set_facecolor("#1a1a2e")
fig.savefig("figures/01_messi_clasico_away_shots.png", dpi=150, bbox_inches="tight")
print("\nSaved figures/01_messi_clasico_away_shots.png")
