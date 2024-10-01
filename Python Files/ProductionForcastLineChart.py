import pandas as pd
import lightningchart as lc
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
import warnings
from datetime import datetime

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

chart = lc.ChartXY(title="Crude Oil Production Forecast (2018-2027)", theme=lc.Themes.Dark)
chart.get_default_x_axis().set_title("Year")
chart.get_default_y_axis().set_title("Crude Oil Production (KTOE)")

legend = chart.add_legend()

historical_series = chart.add_point_line_series().set_name("Historical Data")
forecasted_series = chart.add_point_line_series().set_name("Forecasted Data")

historical_series.set_point_shape('circle').set_point_size(6).set_line_thickness(2).set_line_color(lc.Color(255, 255, 0))  # Blue
forecasted_series.set_point_shape('triangle').set_point_size(6).set_line_thickness(2).set_line_color(lc.Color(255, 0, 0))  # Red 

legend.add(historical_series)
legend.add(forecasted_series)

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
        if country=='WLD':  
            predictions[country] = predict_future_production(country)
    return predictions

print("Computing predictions for 2018-2027...")
predictions = compute_all_predictions()
print("Predictions complete.")

historical_total = []
predicted_total = []

for year in range(1970, 2018):
    year_data = oil_data[oil_data['TIME'].dt.year == year]
    data = [{"category": row['LOCATION'], "value": row['Value']} for _, row in year_data.iterrows() if row['LOCATION'] =='WLD']
    
    total_value = sum(item["value"] for item in data)
    historical_total.append((year, total_value))

x_historical_values = np.array([datetime(year, 1, 1).year for year, _ in historical_total])
y_historical_values = np.array([total for _, total in historical_total])
historical_series.add(x=x_historical_values, y=y_historical_values)

for year in range(2018, 2028):  
    predicted_data = []
    for country in predictions:
        predicted_value = predictions[country][year - 2018]
        predicted_data.append({"category": country, "value": predicted_value})

    predicted_total_value = sum(item["value"] for item in predicted_data)
    predicted_total.append((year, predicted_total_value))

x_forecast_values = np.array([datetime(year, 1, 1).year for year, _ in predicted_total])
y_forecast_values = np.array([total for _, total in predicted_total])
forecasted_series.add(x=x_forecast_values, y=y_forecast_values)

x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')

chart.open()


