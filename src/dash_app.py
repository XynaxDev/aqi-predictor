from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px

data = pd.read_csv("outputs/forecasts/aqi_forecast_sohna_next_year.csv")

data['Date'] = data['Date'].astype(str)


app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sohna AQI Prediction Tool", style={'textAlign': 'center'}),
    
    html.Div([
        html.Label("Pick one day:"),
        dcc.DatePickerSingle(
            id='single-date-picker',
            date=None, 
            display_format='YYYY-MM-DD',
            placeholder='Choose a date'
        ),
        html.Button('Show Day', id='submit-date', n_clicks=0),
        dcc.Graph(id='single-date-graph')
    ], style={'margin': '20px'}),
    
    html.Div([
        html.Label("Pick a date range:"),
        dcc.DatePickerRange(
            id='date-range-picker',
            start_date=None,
            end_date=None,
            display_format='YYYY-MM-DD',
            start_date_placeholder_text='Start Day',
            end_date_placeholder_text='End Day'
        ),
        html.Button('Show Range', id='submit-range', n_clicks=0),
        dcc.Graph(id='range-graph')
    ], style={'margin': '20px'})
])

@callback(
    Output('single-date-graph', 'figure'),
    Input('submit-date', 'n_clicks'),
    Input('single-date-picker', 'date')
)
def show_single_day(n_clicks, picked_date):
    if n_clicks > 0 and picked_date:
        try:
            day_chosen = pd.to_datetime(picked_date).strftime('%Y-%m-%d')
            day_data = data[data['Date'] == day_chosen]
            if not day_data.empty:
                simple_data = day_data.melt(id_vars=['Date'], value_vars=day_data.columns[1:], 
                                         var_name='Hour', value_name='AQI')
                daily_avg = simple_data['AQI'].mean()
                chart = px.bar(simple_data, x='Hour', y='AQI', title=f'AQI for {day_chosen} (Average: {daily_avg:.1f})', 
                               color_discrete_sequence=['#FF4500']) 
                return chart
            else:
                return px.bar(title=f'No data for {day_chosen}')
        except ValueError as e:
            return px.bar(title=f"Oops, date issue: {str(e)}")
    return px.bar(title="Pick a day and click Show Day")

@callback(
    Output('range-graph', 'figure'),
    Input('submit-range', 'n_clicks'),
    Input('date-range-picker', 'start_date'),
    Input('date-range-picker', 'end_date')
)
def show_range(n_clicks, start_day, end_day):
    if n_clicks > 0 and start_day and end_day:
        try:
            start = pd.to_datetime(start_day).strftime('%Y-%m-%d')
            end = pd.to_datetime(end_day).strftime('%Y-%m-%d')
            days_to_show = (data['Date'] >= start) & (data['Date'] <= end)
            range_data = data[days_to_show]
            if not range_data.empty:
                daily_avg = range_data.iloc[:, 1:].mean(axis=1)
                range_data['Daily_AQI'] = daily_avg
                chart = px.bar(range_data, x='Date', y='Daily_AQI', title=f'AQI Average from {start} to {end}', 
                               color_discrete_sequence=['#FF4500']) 
                return chart
            else:
                return px.bar(title=f'No data for {start} to {end}')
        except ValueError as e:
            return px.bar(title=f"Oops, range issue: {str(e)}")
    return px.bar(title="Pick a range and click Show Range")

if __name__ == '__main__':
    app.run(debug=True)