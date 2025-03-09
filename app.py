from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model and encoders
try:
    model_file = "rf_model.joblib"
    pipeline = joblib.load(model_file)
    encoders = joblib.load("label_encoders.joblib")
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    pipeline = None
    encoders = None

# Load the historical match data
try:
    file_path = "/storage/emulated/0/Python/Football_Data/new_data/football_dataset.csv"
    data = pd.read_csv(file_path)
except Exception as e:
    print(f"Error loading dataset: {e}")
    data = pd.DataFrame()  # Empty DataFrame if file not found

@app.route('/')
def home():
    return render_template('index.php')
    
@app.route('/predict', methods=['POST'])
def predict():
    if pipeline is None or encoders is None:
        return jsonify({"error": "Model or encoders not loaded. Check the server logs."})

    if data.empty:
        return jsonify({"error": "Dataset not loaded. Check the server logs."})

    # Get the input data (team names and division) from the request
    try:
        input_data = request.get_json(force=True)
        team1 = input_data["Home"]
        team2 = input_data["Away"]
        div = input_data["Div"]
        wk = input_data["Wk"]
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {e}"})

    # Filter matches where the team is either Home or Away
    teamA_matches = data[(data["Home"] == team1) | (data["Away"] == team1)].copy()
    teamB_matches = data[(data["Home"] == team2) | (data["Away"] == team2)].copy()
    teamAA_matches = data[(data["Home"] == team1)].copy()
    teamBB_matches = data[(data["Away"] == team2)].copy()
    div_matches = data[(data["Div"] == div)].copy()

    # Check if historical data exists for both teams
    if teamA_matches.empty:
        return jsonify({"error": f"No historical data for {team1}. Skipping match."})
    if teamB_matches.empty:
        return jsonify({"error": f"No historical data for {team2}. Skipping match."})
    if div_matches.empty:
        return jsonify({"error": f"No historical data for division {div}. Skipping match."})

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

    # Create simulated input data for prediction
    input_data = {
        "Wk": [wk],
        "Div": [div],
        "Day": ["Sat"],
        "Month": [3],
        "Season": [2024 - 2025],
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
        "xGA5_AA": [teamBB_matches["xGA"].tail(5).mean().round(2)],
    }

    # Create a DataFrame for prediction
    df_input = pd.DataFrame(input_data)

    # Apply label encoding while handling unknown values
    for col in ["Div", "Day", "Home", "Away"]:
        if col in encoders:
            df_input[col] = df_input[col].apply(
                lambda x, col=col: encoders[col].transform([x])[0]
                if x in encoders[col].classes_
                else -1
            )
        else:
            return jsonify({"error": f"Encoder for column '{col}' not found."})

    # Make predictions
    try:
        predictions = pipeline.predict(df_input)
        prediction_probabilities = pipeline.predict_proba(df_input)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {e}"})

    # Prepare the response
    response = {
        "Predicted_Res": predictions[0],
        "Prob_H": prediction_probabilities[0, 2],
        "Prob_D": prediction_probabilities[0, 1],
        "Prob_A": prediction_probabilities[0, 0],
    }

    return jsonify(response)

#if __name__ == '__main__':
#    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=False, threaded=True)