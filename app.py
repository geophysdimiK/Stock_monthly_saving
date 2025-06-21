import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import os
from datetime import datetime
from flask import request
from flask import Flask
from calculation import invest

app = dash.Dash(__name__)
server = app.server

CSV_FILE = "deposit.csv" #cols=[['datetime', 'invested amount', 'nr of shares', 'current value']]

if not os.path.exists(CSV_FILE):
    print("CSV not found - Load inital deposit value")
    date_and_time = datetime.strptime('Jun 2 2025  9:30AM', '%b %d %Y %I:%M%p')
    amount = 0
    shares_purchased = 0
    shares_total = 0
    value = 0
    df = pd.DataFrame([[date_and_time, amount, shares_purchased, shares_total, value]], columns=["datetime", "invested amount", "nr. of shares purchased", "nr. of shares total" ,"current value"])
    df.to_csv(CSV_FILE, index=False)
    

@server.route("/update", methods=["GET"])
def update():
    token = request.args.get("token")
    if token != "dein_geheimer_token":
        return "Unauthorized", 403

    result = invest(savings_rate=100)  # z. B. 100 USD
    return result, 200
    
    
df = pd.read_csv(CSV_FILE)

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["datetime"],
    y=df["current value"],
    mode="lines+markers",
    name="Portfoliowert"
))

app.layout = html.Div([
    html.H2("Portfolioentwicklung"),
    dcc.Graph(figure=fig)
])

