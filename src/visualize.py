import pandas as pd
import pickle
from prophet.plot import plot_plotly, plot_components_plotly

forecast = pd.read_csv("outputs/forecasts/aqi_forecast_sohna_next_year_long.csv")

forecast['ds'] = pd.to_datetime(forecast['ds'])

with open("models/trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Create and save the interactive forecast plot
fig = plot_plotly(model, forecast)
fig_components = plot_components_plotly(model, forecast)
fig.write_html("outputs/forecasts/aqi_forecast_plot.html")
fig_components.write_html("outputs/forecasts/aqi_forecast_plot_components.html")