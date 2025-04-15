import pandas as pd
import numpy as np

df = pd.read_csv('data/processed/cleaned_aqi_sohna_hourly.csv')


df_melted = pd.melt(df, id_vars=["Days"], var_name="Hour", value_name="y")
df_melted['Date'] = pd.to_datetime('2023-01-01') + pd.to_timedelta(df_melted['Days'] - 1, unit='D')
df_melted['ds'] = df_melted['Date'].astype(str) + ' ' + df_melted['Hour']
df_melted['ds'] = pd.to_datetime(df_melted['ds'])
df = df_melted[['ds', 'y']].dropna()


df.to_csv("data/processed/cleaned_aqi_sohna_hourly.csv", index=False)