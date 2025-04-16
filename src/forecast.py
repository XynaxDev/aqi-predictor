import pandas as pd
from prophet import Prophet
import pickle

df = pd.read_csv("data/processed/cleaned_aqi_sohna_hourly_processed.csv")

if 'y' not in df.columns:
    raise ValueError("Column 'y' not found in the input data. Check preprocessing.")
if 'AQI' in df.columns:
    df = df.rename(columns={'AQI': 'y'})
df['y'] = df['y'].clip(lower=0) 

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=True,
    seasonality_mode='additive'
)

model.fit(df)
with open('models/trained_model.pkl', 'wb') as f:
    pickle.dump(model, f)

last_date = pd.to_datetime(df['ds'].iloc[-1])
future = pd.DataFrame({'ds': pd.date_range(start=last_date + pd.Timedelta(hours=1), periods=17520, freq='h')})

forecast = model.predict(future)
forecast.to_csv("outputs/forecasts/aqi_forecast_sohna_next_year_long.csv", index=False)

forecast_pivot = forecast[['ds', 'yhat']].copy()
forecast_pivot['Date'] = forecast_pivot['ds'].dt.date
forecast_pivot['Hour'] = forecast_pivot['ds'].dt.strftime('%H:%M:%S')
pivot_table = forecast_pivot.pivot(index='Date', columns='Hour', values='yhat').reset_index()
pivot_table.columns.name = None
pivot_table.index.name = None

pivot_table.to_csv("outputs/forecasts/aqi_forecast_sohna_next_year.csv", index=False)

print("Forecast shape:", pivot_table.shape)
print("Min forecasted AQI:", pivot_table.iloc[:, 1:].min().min())
print("Max forecasted AQI:", pivot_table.iloc[:, 1:].max().max())