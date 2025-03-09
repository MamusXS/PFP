import pandas as pd
import joblib
import numpy as np

model_file = "rf_model.joblib"
input_file = "prediction_data.csv"
encoders = joblib.load("label_encoders.joblib")

# Load the trained model
pipeline = joblib.load(model_file)

# Load the data for predictions (matches to predict)
df = pd.read_csv(input_file)

# Assuming you have a historical match data file, e.g., for Elo ratings, etc.
file_path = "/storage/emulated/0/Python/Football_Data/new_data/football_dataset.csv"
data = pd.read_csv(file_path)

# Initialize a list to store results
all_predictions = []

# Loop through each match in the prediction input file (df)
for index, row in df.iterrows():
    team1 = row["Home"]
    team2 = row["Away"]
    div = row["Div"]
    wk = row["Wk"]
    time = row["Time"]

    # Filter matches where the team is either Home or Away
    teamA_matches = data[
        (data["Home"] == team1) | (data["Away"] == team1)
    ].copy()
    teamB_matches = data[
        (data["Home"] == team2) | (data["Away"] == team2)
    ].copy()
    teamAA_matches = data[(data["Home"] == team1)].copy()
    teamBB_matches = data[(data["Away"] == team2)].copy()
    div_matches = data[(data["Div"] == div)].copy()

    # Check if historical data exists for both teams
    if teamA_matches.empty:
        print(f"No historical data for {team1}. Skipping match.")
        continue
    if teamB_matches.empty:
        print(f"No historical data for {team2}. Skipping match.")
        continue
    if div_matches.empty:
        print(f"No historical data for division {div}. Skipping match.")
        continue

    # Check the shapes of the DataFrames
#    print(f"teamA_matches shape: {teamA_matches.shape}")
#    print(f"teamB_matches shape: {teamB_matches.shape}")
#    print(f"div_matches shape: {div_matches.shape}")

    # Calculate EloRating and EloCh for Team 1 and Team 2
    teamA_matches["Elo"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["EloH"], teamA_matches["EloA"]
    )
    teamB_matches["Elo"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["EloH"], teamB_matches["EloA"]
    )

    teamA_matches["EloCh"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["EloChH"], teamA_matches["EloChA"]
    )
    teamB_matches["EloCh"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["EloChH"], teamB_matches["EloChA"]
    )
    
    teamA_matches["TGS"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["HG"], teamA_matches["AG"]
    )
    teamB_matches["TGS"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["HG"], teamB_matches["AG"]
    )
    
    teamA_matches["TGC"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["AG"], teamA_matches["HG"]
    )
    teamB_matches["TGC"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["AG"], teamB_matches["HG"]
    )
    
    teamA_matches["PPG"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["PH"], teamA_matches["PA"]
    )
    teamB_matches["PPG"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["PH"], teamB_matches["PA"]
    )
    
    teamA_matches["xG"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["xG_H"], teamA_matches["xG_A"]
    )
    teamB_matches["xG"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["xG_H"], teamB_matches["xG_A"]
    )
    
    teamA_matches["xGA"] = np.where(
        teamA_matches["Home"] == team1, teamA_matches["xG_A"], teamA_matches["xG_H"]
    )
    teamB_matches["xGA"] = np.where(
        teamB_matches["Home"] == team2, teamB_matches["xG_A"], teamB_matches["xG_H"]
    )    

    teamAA_matches["GS"] = teamAA_matches["HG"]
    teamBB_matches["GS"] = teamBB_matches["AG"]

    teamAA_matches["GC"] = teamAA_matches["AG"]
    teamBB_matches["GC"] = teamBB_matches["HG"]

    div_matches["GD1"] = div_matches["HG"]
    div_matches["GD2"] = div_matches["AG"]
    
    teamAA_matches["PPG"] = teamAA_matches["PH"]
    teamBB_matches["PPG"] = teamBB_matches["PA"]
    
    teamAA_matches["xG"] = teamAA_matches["xG_H"]
    teamBB_matches["xG"] = teamBB_matches["xG_A"]
    
    teamAA_matches["xGA"] = teamAA_matches["xG_A"]
    teamBB_matches["xGA"] = teamBB_matches["xG_H"]

    # Check that there is enough data to calculate Elo ratings
    if teamA_matches["Elo"].empty or teamA_matches["EloCh"].empty:
        print(f"Insufficient Elo data for {team1}. Skipping match.")
        continue
    if teamB_matches["Elo"].empty or teamB_matches["EloCh"].empty:
        print(f"Insufficient Elo data for {team2}. Skipping match.")
        continue

    # Elo Rating for both teams
    eloH = (
        teamA_matches["Elo"].iloc[-1]
        + teamA_matches["EloCh"].iloc[-1]
    )
    eloA = (
        teamB_matches["Elo"].iloc[-1]
        + teamB_matches["EloCh"].iloc[-1]
    )

    # Calculate goal statistics
#    if len(teamAA_matches["GS"].tail(10)) == 0 or len(div_matches["GD1"].tail(200)) == 0:
#        print(f"Insufficient goal data for {team1}. Skipping match.")
#        continue
#    if len(teamBB_matches["GS"].tail(10)) == 0 or len(div_matches["GD2"].tail(200)) == 0:
#        print(f"Insufficient goal data for {team2}. Skipping match.")
#        continue

    # Create simulated input data for prediction
    input_data = {
        "Wk": [wk],
        "Div": [div],
        "Day": ["Sat"],
        "Month": [3],
        "Season": [2024-2025],
        "Time": [time],
        "Home": [team1],
        "Away": [team2],
        "ES_5_H": [teamA_matches["EloCh"].tail(5).sum()],
        "ES_5_A": [teamB_matches["EloCh"].tail(5).sum()],
        "PPG_5_H": [teamA_matches["PPG"].tail(5).mean().round(2)],
        "PPG_5_A": [teamB_matches["PPG"].tail(5).mean().round(2)],
        "TGS_5_H": [teamA_matches["TGS"].tail(5).mean().round(2)],  
        "TGC_5_H": [teamA_matches["TGC"].tail(5).mean().round(2)],
        "TGS_5_A": [teamB_matches["TGS"].tail(5).mean().round(2)],
        "TGC_5_A": [teamB_matches["TGC"].tail(5).mean().round(2)],
        "TxG_5_H": [teamA_matches["xG"].tail(5).mean().round(2)],
        "TxGA_5_H": [teamA_matches["xGA"].tail(5).mean().round(2)],
        "TxG_5_A": [teamB_matches["xG"].tail(5).mean().round(2)],
        "TxGA_5_A": [teamBB_matches["xGA"].tail(5).mean().round(2)],
        "PPG5_HH": [teamAA_matches["PPG"].tail(5).mean().round(2)],
        "PPG5_AA": [teamBB_matches["PPG"].tail(5).mean().round(2)],
        "GS5_HH": [teamAA_matches["GS"].tail(5).mean().round(2)],
        "GS5_AA": [teamBB_matches["GS"].tail(5).mean().round(2)],
        "GC5_HH": [teamAA_matches["GC"].tail(5).mean().round(2)],
        "GC5_AA": [teamBB_matches["GC"].tail(5).mean().round(2)],
        "xG5_HH": [teamAA_matches["xG"].tail(5).mean().round(2)],
        "xG5_AA": [teamBB_matches["xG"].tail(5).mean().round(2)],
        "xGA5_HH": [teamAA_matches["xGA"].tail(5).mean().round(2)],
        "xGA5_AA": [teamBB_matches["xGA"].tail(5).mean().round(2)]
    }

    # Create a DataFrame for prediction
    df_input = pd.DataFrame(input_data)

    # Apply label encoding while handling unknown values
    for col in ["Div", "Day", "Time", "Home", "Away"]:
        if col in encoders:
            df_input[col] = df_input[col].apply(
                lambda x, col=col: encoders[col].transform([x])[0]
                if x in encoders[col].classes_
                else -1
            )
        else:
            print(f"Encoder for column '{col}' not found. Skipping match.")
            continue

    # Make predictions
    predictions = pipeline.predict(df_input)
    prediction_probabilities = pipeline.predict_proba(df_input)

    # Save predictions to the DataFrame
    df_input["Predicted_Res"] = predictions
    df_input["Prob_H"] = prediction_probabilities[:, 2]  # Probability for Home Win
    df_input["Prob_D"] = prediction_probabilities[:, 1]  # Probability for Draw
    df_input["Prob_A"] = prediction_probabilities[:, 0]  # Probability for Away Win

    # Append result to the list
    all_predictions.append(df_input)

# Combine all predictions into a single DataFrame
if all_predictions:
    final_predictions = pd.concat(all_predictions, ignore_index=True)

    # Display Results
    for index, row in final_predictions.iterrows():
        # Reverse label encoding for teams
        home_team = encoders["Home"].inverse_transform([int(row["Home"])])[0]
        away_team = encoders["Away"].inverse_transform([int(row["Away"])])[0]

        print(f"--- {home_team} vs {away_team} = [{row['Predicted_Res']}]")
        print(f"--- H: {round(row['Prob_H'] * 100)}%")
        print(f"--- D: {round(row['Prob_D'] * 100)}%")
        print(f"--- A: {round(row['Prob_A'] * 100)}%")
        print("______________________________")
else:
    print("No predictions were made due to insufficient data.")          