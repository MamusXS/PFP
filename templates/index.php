<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Prime Football Prediction </title>

    <!-- Global stylesheets -->
    <link href="{{ url_for('static', filename='fonts/inter/inter.css') }}" rel="stylesheet" type="text/css">
    <link href="{{ url_for('static', filename='icons/phosphor/styles.min.css') }}" rel="stylesheet" type="text/css">
    <link href="{{ url_for('static', filename='css/ltr/all.min.css') }}" id="stylesheet" rel="stylesheet" type="text/css">
    <!-- /global stylesheets -->

    <!-- Core JS files -->
    <script src="{{ url_for('static', filename='demo/demo_configurator.js') }}"></script>
    <script src="{{ url_for('static', filename='js/bootstrap/bootstrap.bundle.min.js') }}"></script>
    <!-- /core JS files -->

    <!-- Theme JS files -->
    <script src="{{ url_for('static', filename='js/app.js') }}"></script>

    <script src="https://themes.kopyov.com/limitless/demo/template/assets/js/jquery/jquery.min.js"></script>
    <script src="https://themes.kopyov.com/limitless/demo/template/assets/js/vendor/forms/selects/select2.min.js"></script>

    <script src="https://themes.kopyov.com/limitless/demo/template/assets/demo/pages/form_select2.js"></script>
    <!-- /theme JS files -->

    <script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>

</head>

<body>
    <!-- Main navbar -->
    <div class="navbar navbar-dark navbar-expand-lg navbar-static border-bottom border-bottom-white border-opacity-10">
        <div class="container-fluid">
            <h3>Prime Football Prediction</h3>
        </div>
    </div>
    <!-- /main navbar -->


    <!-- Page content -->
    <div class="page-content">

        <!-- Main content -->
        <div class="content-wrapper">

            <!-- Inner content -->
            <div class="content-inner">

                <!-- Content area -->
                <div class="content">

                    <!-- Basic card -->
                    <div class="card">
                        <div class="card-body">
                            <!-- League Dropdown -->
                            <div class="mb-3 row">
                                <div class="col-12">
                                    <label for="divSelect" class="form-check-label">League</label>
                                    <select class="form-control select" data-minimum-results-for-search="Infinity" id="divSelect" name="div">
                                        <option value="Eng0">Premier League</option>
                                        <option value="Eng1">Championship</option>
                                        <option value="Spa">LaLiga</option>
                                        <option value="Ita">Serie A</option>
                                        <option value="Ger">Bundesliga</option>
                                        <option value="Fra">Ligue 1</option>
                                    </select>
                                </div>
                            </div>

                            <div class="mb-3 row">
                                <div class="col-6">
                                    <label class="form-check-label">Match Week</label>
                                    <input type="number" class="form-control" id="md" aria-label="md" aria-describedby="basic-addon1">
                                </div>

                                <div class="col-6">
                                    <label class="form-check-label">Day</label>
                                    <select class="form-control select" data-minimum-results-for-search="Infinity" id="day" name="day">
                                        <option value="Sat">Saturday</option>
                                        <option value="Sun">Sunday</option>
                                        <option value="Mon">Monday</option>
                                        <option value="Tue">Tuesday</option>
                                        <option value="Wed">Wednesday</option>
                                        <option value="Thu">Thursday</option>
                                        <option value="Fri">Friday</option>
                                    </select>
                                </div>
                            </div>


                            <div class="mb-3 row">
                                <div class="col-12">
                                    <label class="form-check-label">Home Team</label>
                                    <select class="form-control select" id="homeTeamSelect" onchange="disableSelectedHomeTeam()" name="team"></select>
                                </div>
                            </div>

                            <div class="mb-3 row">
                                <div class="col-12">
                                    <label class="form-check-label">Away Team</label>
                                    <select class="form-control select" id="awayTeamSelect" onchange="disableSelectedHomeTeam()" name="team"></select>
                                </div>
                            </div>

                            <center><button class="btn btn-primary" id="predictBtn">Predict</button></center>
                        </div>
                    </div>
                    <!-- /basic card -->

                    <!-- Basic card -->
                    <div class="card">
                        <div class="card-body">
                            <h4>Prediction Result:</h4>
                            <div id="result"></div>

                        </div>
                    </div>

                </div>
                <!-- /content area -->


                <!-- Footer -->
                <div class="navbar navbar-sm navbar-footer border-top">
                    <div class="container-fluid">
                        <span>&copy; 2025 <a href="javascript:void(0)">Prime Football Prediction</a></span>
                    </div>
                </div>
                <!-- /footer -->

            </div>
            <!-- /inner content -->

        </div>
        <!-- /main content -->

    </div>
    <!-- /page content -->

    <script>
        const footballData = {
            "Eng1": [
                "Blackburn",
                "Bristol City",
                "Burnley",
                "Cardiff City",
                "Coventry City",
                "Derby County",
                "Hull City",
                "Leeds United",
                "Luton Town",
                "Middlesbrough",
                "Millwall",
                "Norwich City",
                "Oxford United",
                "Plymouth Argyle",
                "Portsmouth",
                "Preston",
                "QPR",
                "Sheffield Utd",
                "Sheffield Weds",
                "Stoke City",
                "Sunderland",
                "Swansea City",
                "Watford",
                "West Brom"
            ],
            "Spa": [
                "Alavés",
                "Athletic Club",
                "Atlético Madrid",
                "Barcelona",
                "Betis",
                "Celta Vigo",
                "Espanyol",
                "Getafe",
                "Girona",
                "Las Palmas",
                "Leganés",
                "Mallorca",
                "Osasuna",
                "Rayo Vallecano",
                "Real Madrid",
                "Real Sociedad",
                "Sevilla",
                "Valencia",
                "Valladolid",
                "Villarreal"
            ],
            "Eng0": [
                "Arsenal",
                "Aston Villa",
                "Bournemouth",
                "Brentford",
                "Brighton",
                "Chelsea",
                "Crystal Palace",
                "Everton",
                "Fulham",
                "Ipswich Town",
                "Leicester City",
                "Liverpool",
                "Manchester City",
                "Manchester Utd",
                "Newcastle Utd",
                "Nott'ham Forest",
                "Southampton",
                "Tottenham",
                "West Ham",
                "Wolves"
            ],
            "Fra": [
                "Angers",
                "Auxerre",
                "Brest",
                "Le Havre",
                "Lens",
                "Lille",
                "Lyon",
                "Marseille",
                "Monaco",
                "Montpellier",
                "Nantes",
                "Nice",
                "Paris S-G",
                "Reims",
                "Rennes",
                "Saint-Étienne",
                "Strasbourg",
                "Toulouse"
            ],
            "Ita": [
                "Atalanta",
                "Bologna",
                "Cagliari",
                "Como",
                "Empoli",
                "Fiorentina",
                "Genoa",
                "Hellas Verona",
                "Inter",
                "Juventus",
                "Lazio",
                "Lecce",
                "Milan",
                "Monza",
                "Napoli",
                "Parma",
                "Roma",
                "Torino",
                "Udinese",
                "Venezia"
            ],
            "Ger": [
                "Augsburg",
                "Bayern Munich",
                "Bochum",
                "Dortmund",
                "Eint Frankfurt",
                "Freiburg",
                "Gladbach",
                "Heidenheim",
                "Hoffenheim",
                "Holstein Kiel",
                "Leverkusen",
                "Mainz 05",
                "RB Leipzig",
                "St. Pauli",
                "Stuttgart",
                "Union Berlin",
                "Werder Bremen",
                "Wolfsburg"
            ]
        };
    </script>

    <!-- JavaScript to Populate Dropdowns -->
    <script>
        $(document).ready(function () {
            // Event listener for League dropdown change
            $('#divSelect').change(function () {
                const selectedDiv = $(this).val();
                const teams = footballData[selectedDiv] || []; // Get teams for the selected Div

                // Clear existing options
                $('#homeTeamSelect').empty(); // No default option
                $('#awayTeamSelect').empty(); // No default option

                // Populate Home Team dropdown
                teams.forEach(team => {
                    $('#homeTeamSelect').append(`<option value="${team}">${team}</option>`);
                });

                // Populate Away Team dropdown
                teams.forEach(team => {
                    $('#awayTeamSelect').append(`<option value="${team}">${team}</option>`);
                });
                
                disableSelectedHomeTeam();
            });

            // Trigger change event to load initial data
            $('#divSelect').trigger('change');
        });
    </script>


    <script>
        function disableSelectedHomeTeam() {
            var homeTeamSelect = document.getElementById("homeTeamSelect");
            var awayTeamSelect = document.getElementById("awayTeamSelect");

            var selectedHomeTeam = homeTeamSelect.value;
            var selectedAwayTeam = awayTeamSelect.value;

            // Enable all options first
            for (var i = 0; i < awayTeamSelect.options.length; i++) {
                var option = awayTeamSelect.options[i];
                option.disabled = false;
            }

            // Disable the selected home team in the away team select
            for (var i = 0; i < awayTeamSelect.options.length; i++) {
                var option = awayTeamSelect.options[i];
                if (option.value === selectedHomeTeam) {
                    option.disabled = true;
                }
            }

            // If the selected home team is the same as the selected away team, change the selected away team
            if (selectedHomeTeam === selectedAwayTeam) {
                for (var i = 0; i < awayTeamSelect.options.length; i++) {
                    var option = awayTeamSelect.options[i];
                    if (!option.disabled && option.value !== selectedHomeTeam) {
                        $(awayTeamSelect).val(option.value).trigger('change'); // Update Select2
                        break;
                    }
                }
            }
        }

        // Call the function when the page loads
        window.onload = function() {
            disableSelectedHomeTeam();
        };

        // Attach event listeners to update the options dynamically
        document.getElementById("homeTeamSelect").addEventListener("change", disableSelectedHomeTeam);
        document.getElementById("awayTeamSelect").addEventListener("change", disableSelectedHomeTeam);

        document.addEventListener("DOMContentLoaded", function () {
            let mdInput = document.getElementById("md");
            let now = new Date();

            // Format hours and minutes with leading zero if needed
            let hours = now.getHours().toString().padStart(2, '0');
            let minutes = now.getMinutes().toString().padStart(2, '0');

            // Set the value in HH:MM format
            mdInput.value = `${hours}:${minutes}`;
        });


        document.getElementById("predictBtn").onclick = async function() {
            const homeTeam = document.getElementById("homeTeamSelect").value;
            const awayTeam = document.getElementById("awayTeamSelect").value;
            const division = document.getElementById("divSelect").value;
            const md = document.getElementById("md").value;
            const day = document.getElementById("day").value;

            if (!homeTeam || !awayTeam || !division) {
                document.getElementById("result").innerHTML = `<p style="color:red;">Please fill in all fields.</p>`;
                return;
            }

            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    Home: homeTeam, Away: awayTeam, Div: division, Wk: md, Day: day
                })
            });

            const data = await response.json();
            if (data.error) {
                document.getElementById("result").innerHTML = `<p style="color:red;">${data.error}</p>`;
            } else {
                document.getElementById("result").innerHTML = `
                <p><b>${homeTeam} vs ${awayTeam}</b></p>
                <p>Predicted Result: <b>${data.Predicted_Res}</b></p>
                <p>Probability:<br>Home: ${parseInt((data.Prob_H * 100).toFixed(0))}%<br>Draw: ${parseInt((data.Prob_D * 100).toFixed(0))}%<br>Away: ${parseInt((data.Prob_A * 100).toFixed(0))}%</p>
                `;
            }
        };

    </script>

</body>
</html>