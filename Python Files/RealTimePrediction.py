# import pandas as pd
# import lightningchart as lc
# import time
# import statsmodels.api as sm
# import numpy as np

# # Load your LightningChart license
# lc.set_license(open('../license-key').read())

# # Load dataset
# file_path = 'Dataset/DP_LIVE.xlsx'
# oil_data = pd.read_excel(file_path)

# # Filter data for positive production values and years 1970 to 2017
# oil_data = oil_data[oil_data['Value'] > 0].dropna(subset=['Value'])
# oil_data = oil_data[(oil_data['TIME'] >= 1970) & (oil_data['TIME'] <= 2017)]

# # Convert the 'TIME' column to datetime
# oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')

# # Pivot table for oil production over time by country
# pivot_tide = oil_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum', fill_value=0)

# # Ensure the index is in the year format
# pivot_tide.index = pivot_tide.index.year

# # Fit ARIMA models and forecast for each country
# forecast_years = [2018, 2019, 2020]
# forecast_data = {}

# for country in pivot_tide.columns:
#     if country == 'WLD':  # Skip "WLD"
#         continue

#     try:
#         # Fit ARIMA(1,2,1) model for each country based on historical data
#         model = sm.tsa.ARIMA(pivot_tide[country], order=(1, 2, 1))
#         fitted_model = model.fit()
        
#         # Forecast crude oil production for 2018-2020
#         forecast = fitted_model.forecast(steps=len(forecast_years))
#         forecast_data[country] = forecast
#     except Exception as e:
#         print(f"ARIMA failed for {country}: {e}")
#         forecast_data[country] = [np.nan] * len(forecast_years)  # Handle failed forecasts

# # Initialize LightningChart dashboard with 2 rows (BarChart and MapChart)
# dashboard = lc.Dashboard(theme=lc.Themes.CyberSpace, rows=2, columns=1)

# # BarChart for crude oil production
# bar_chart = dashboard.BarChart(row_index=0, column_index=0)

# # MapChart for crude oil production
# map_chart = dashboard.MapChart(row_index=1, column_index=0)

# # Function to update charts for a specific year
# def update_charts_for_year(year, production_data):
#     year_data = oil_data[oil_data['TIME'].dt.year == year]
    
#     # Update bar chart
#     country_production = []
#     for country in pivot_tide.columns:
#         if country == 'WLD':  # Skip "WLD"
#             continue
        
#         production_value = production_data.get(country, 0)
#         country_production.append({
#             "category": country,
#             "value": production_value
#         })
    
#     bar_chart.set_data(country_production)
#     bar_chart.set_title(f'Crude Oil Production by Country in Year {year}')

#     # Update map chart
#     map_data = []
#     for _, row in year_data.iterrows():
#         map_data.append({'ISO_A3': row['LOCATION'], 'value': row['Value']})
#     map_chart.invalidate_region_values(map_data)
#     map_chart.set_title(f"Crude Oil Production - Year {year}")

#     # Set map chart palette
#     map_chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
#             {'value': 50000, 'color': lc.Color(255, 255, 0)},  # Yellow
#             {'value': 100000, 'color': lc.Color(255, 165, 0)},  # Orange
#             {'value': 500000, 'color': lc.Color(255, 0, 0)},  # Red
#         ],
#         look_up_property='value'
#     )

# # Function to update dashboard dynamically
# def update_dashboard():
#     # Display historical data first (1970-2017)
#     for year in range(1970, 2018):
#         print(f"Updating data for year: {year}")
#         if year in pivot_tide.index:
#             update_charts_for_year(year, pivot_tide.loc[year].to_dict())
#         else:
#             print(f"No data available for year: {year}")
#         time.sleep(2)

#     # Display forecast data for 2018-2020
#     for i, year in enumerate(forecast_years):
#         print(f"Updating forecast for year: {year}")
#         forecast_for_year = {country: forecast_data[country][i] for country in pivot_tide.columns if country != 'WLD'}
#         update_charts_for_year(year, forecast_for_year)
#         time.sleep(2)

# # Open the dashboard and start updating
# dashboard.open(live=True)
# update_dashboard()






import pandas as pd
import lightningchart as lc
import time
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

lc.set_license(open('../license-key').read())

file_path = 'Dataset/DP_LIVE.xlsx'
oil_data = pd.read_excel(file_path)

oil_data = oil_data[oil_data['Value'] > 0].dropna(subset=['Value'])
oil_data = oil_data[(oil_data['TIME'] >= 1970) & (oil_data['TIME'] <= 2017)]
oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')

pivot_tide = oil_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum', fill_value=0)
countries = pivot_tide.columns
time_values = pivot_tide.index

dashboard = lc.Dashboard(theme=lc.Themes.CyberSpace, rows=2, columns=1)
bar_chart = dashboard.BarChart(row_index=0, column_index=0)
map_chart = dashboard.MapChart(row_index=1, column_index=0)

def update_charts_for_year(year, data, is_predicted=False):
    if is_predicted:
        title_suffix = 'Predicted'
    else:
        title_suffix = 'Historical'

    bar_chart.set_title(f'{title_suffix} Crude Oil Production by Country in Year {year}')
    bar_chart.set_data(data)

    map_chart.invalidate_region_values([{"ISO_A3": item["category"], "value": item["value"]} for item in data])
    map_chart.set_title(f'{title_suffix} Crude Oil Production - Year {year}')

    map_chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
            {'value': 10000, 'color': lc.Color(0, 255, 0)},  # Green
            {'value': 50000, 'color': lc.Color(255, 255, 0)},  # Yellow
            {'value': 100000, 'color': lc.Color(255, 165, 0)},  # Orange
            {'value': 500000, 'color': lc.Color(255, 0, 0)},  # Red
        ],
        look_up_property='value',
    )

def predict_future_production(country):
    country_data = pivot_tide[country].values
    try:
        model = ARIMA(country_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10) 
        return forecast
    except Exception as e:
        print(f"ARIMA model failed for {country}: {e}")
        return [0] * 10  

def compute_all_predictions():
    predictions = {}
    for country in countries:
        if country != 'WLD':  
            predictions[country] = predict_future_production(country)
    return predictions

def prepare_predicted_data(year, predictions):
    predicted_data = []
    for country in predictions:
        predicted_value = predictions[country][year - 2018]
        predicted_data.append({"category": country, "value": predicted_value})
    return predicted_data

def update_dashboard(predictions):
    for year in range(1970, 2018):
        print(f"Updating historical data for year: {year}")
        year_data = oil_data[oil_data['TIME'].dt.year == year]
        data = [{"category": row['LOCATION'], "value": row['Value']} for _, row in year_data.iterrows() if row['LOCATION'] != 'WLD']
        update_charts_for_year(year, data)
        time.sleep(2)

    for year in range(2018, 2028): 
        print(f"Updating predicted data for year: {year}")
        predicted_data = prepare_predicted_data(year, predictions)
        update_charts_for_year(year, predicted_data, is_predicted=True)
        time.sleep(2)  

print("Computing predictions for 2018-2027...")
predictions = compute_all_predictions()
print("Predictions complete. Starting visualization...")

dashboard.open(live=True)
update_dashboard(predictions)
