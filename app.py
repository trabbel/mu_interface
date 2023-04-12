import dash
from dash import dcc
from dash import html
from dash import ctx
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Output, Input, State
from datetime import datetime, timedelta
import pathlib

import os

# Global variables
MEASUREMENT_PATH = pathlib.Path.home() / "measurements" #/ "measuerments" / "lrpi1"
ENERGY_PATH = pathlib.Path.home() / "measurements" / "power_monitor"
DISPLAY_LAST_HOURS = 2
BOX_ID = 0
PORT = "ACM0"
SUBDIRECTORY = f"rockwp{BOX_ID}_tty{PORT}"

print(SUBDIRECTORY)

# Set up the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])


# Define the layout
app.layout = dbc.Container(
    [
        html.Div(id="intermediate-value", style={"display": "none"}),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("WatchPlant Dashboard"),
                    ],
                    width=11,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Settings",
                            id="settings-button",
                            color="primary",
                            className="ml-auto",
                        ),
                    ],
                    width=1,
                    className="ml-auto",
                ),
            ],
            style={"margin-top": "20px"},
        ),
        html.Hr(),
        dbc.Collapse(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Measurment File Path"),
                                dbc.Input(
                                    type="text",
                                    id="measurement-path",
                                    value=str(MEASUREMENT_PATH),
                                    debounce=True,
                                    className="mb-3",
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                html.Label("Energy Consumption File Path"),
                                dbc.Input(
                                    type="text",
                                    id="energy-path",
                                    value=str(ENERGY_PATH),
                                    debounce=True,
                                    className="mb-3",
                                ),
                            ],
                            width=6,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [html.Label("What sensor node should be displayed?")],
                            width=3,
                        ),
                        dbc.Col(
                            [
                                dcc.RadioItems(
                                    ["ACM0", "ACM1", "ACM2"],
                                    "ACM0",
                                    id="sensor-select",
                                    inline=True,
                                    inputStyle={
                                        "margin-left": "20px",
                                        "margin-right": "10px",
                                    },
                                )
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            [html.Label("Orange/Grey Box ID")],
                            width=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    value=BOX_ID,
                                    min=0,
                                    id="box_id-select",
                                ),
                            ],
                            width=1,
                        ),
                        dbc.Col(
                            [html.Label("How many hours to display?")],
                            width=2,
                        ),
                        dbc.Col(
                            [
                                dbc.Input(
                                    type="number",
                                    value=DISPLAY_LAST_HOURS,
                                    min=1,
                                    max=12,
                                    id="time-select",
                                ),
                            ],
                            width=1,
                        ),
                    ]
                ),
                html.Hr(),
            ],
            id="settings-collapse",
            is_open=False,
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="plot1",
                            config={
                                "displaylogo": False,
                                "edits": {"legendPosition": True},
                                "modeBarButtonsToRemove": ["autoScale2d"],
                                "scrollZoom": True,
                            },
                        )
                    ],
                    width=12,
                )
            ],
            style={"margin-top": "20px", "title": "Measurement Data"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id="plot2",
                            config={
                                "displaylogo": False,
                                "edits": {"legendPosition": True},
                                "modeBarButtonsToRemove": ["autoScale2d"],
                                "scrollZoom": True,
                            },
                        )
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id="plot3",
                            config={
                                "displaylogo": False,
                                "edits": {"legendPosition": True},
                                "modeBarButtonsToRemove": ["autoScale2d"],
                                "scrollZoom": True,
                            },
                        )
                    ],
                    width=6,
                ),
            ],
            style={"margin-top": "20px"},
        ),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,
            n_intervals=0,
        ),
    ],
    fluid=True,
)


# Callback to toggle settings collaps
@app.callback(
    Output("settings-collapse", "is_open"),
    [Input("settings-button", "n_clicks")],
    [State("settings-collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    return not is_open if n else is_open


# Callback to change settings
@app.callback(
    Output("intermediate-value", "children"),
    [
        Input("measurement-path", "value"),
        Input("energy-path", "value"),
        Input("sensor-select", "value"),
        Input("box_id-select", "value"),
        Input("time-select", "value"),
    ],
)
def change_plot_settings(value1, value2, value3, value4, value5):
    trigger = ctx.triggered_id
    global BOX_ID, PORT, SUBDIRECTORY, MEASUREMENT_PATH, ENERGY_PATH, DISPLAY_LAST_HOURS
    if trigger == "measurement-path":
        new_path = pathlib.Path(value1)
        MEASUREMENT_PATH = new_path
    elif trigger == "energy-path":
        new_path = pathlib.Path(value2)
        ENERGY_PATH = new_path
    elif trigger == "sensor-select":
        PORT = value3
        SUBDIRECTORY = f"rockwp{BOX_ID}_tty{PORT}"
    elif trigger == "box_id-select":
        BOX_ID = value4
        SUBDIRECTORY = f"rockwp{BOX_ID}_tty{PORT}"
    elif trigger == "time-select":
        DISPLAY_LAST_HOURS = value5
    print(SUBDIRECTORY)
    return None


# Callback to update live plots
@app.callback(
    [Output("plot1", "figure"), Output("plot2", "figure"), Output("plot3", "figure")],
    [Input("interval-component", "n_intervals")],
)
def update_plots(n):
    # Load the updated data from the CSV file
    file_names = os.listdir(MEASUREMENT_PATH / SUBDIRECTORY)
    file_names.sort()
    df = pd.read_csv(MEASUREMENT_PATH / SUBDIRECTORY / file_names[-1])
    df["timestamp"] = pd.to_datetime(df["timestamp"])  # convert to datetime object

    # Filter the data for the sliding window
    # df_window = df.loc[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(hours=2)]
    df_window = df.loc[
        df["timestamp"]
        > pd.Timestamp(year=2021, month=5, day=31, hour=14, minute=30)
        - pd.Timedelta(hours=DISPLAY_LAST_HOURS)
    ]
    # Create the first plot
    fig1 = px.line(
        df_window,
        x="timestamp",
        y=[
            "temp_external",
            "light_external",
            "humidity_external",
            "differential_potential_ch1",
            "differential_potential_ch2",
        ],
        title="Measurement Data",
        template="plotly",
    )
    fig1["layout"]["uirevision"] = "1"

    # Create the second plot
    fig2 = px.line(
        df, x="timestamp", y="temp-external", title="Placeholder for MU/Pi input"
    )
    fig2["layout"]["uirevision"] = "2"

    # Create the third plot
    df = pd.read_csv(ENERGY_PATH / "data.csv")
    df["time"] = pd.to_datetime(df["time"])  # convert to datetime object
    # df_window = df.loc[df['timestamp'] > pd.Timestamp.now() - pd.Timedelta(hours=2)]
    df_window = df.loc[
        df["time"]
        > pd.Timestamp(year=2023, month=4, day=6, hour=2)
        - pd.Timedelta(hours=DISPLAY_LAST_HOURS)
    ]

    fig3 = px.line(
        df_window, x="time", y=["value1", "value2"], title="Energy Consumption"
    )
    fig3["layout"]["uirevision"] = "3"
    # Return the updated figures
    return fig1, fig2, fig3


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
