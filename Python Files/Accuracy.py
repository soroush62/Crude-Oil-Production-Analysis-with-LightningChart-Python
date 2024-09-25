import pandas as pd
import lightningchart as lc
import time
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder

# Load your LightningChart license
lc.set_license(open('../license-key').read())

# Load the dataset for oil production
file_path = 'Dataset/DP_LIVE.xlsx'
oil_data = pd.read_excel(file_path)

# Remove rows with zero or missing 'Value'
oil_data = oil_data[oil_data['Value'] > 0].dropna(subset=['Value'])

# Filter the data for the years 1970 to 2017
oil_data = oil_data[(oil_data['TIME'] >= 1970) & (oil_data['TIME'] <= 2017)]

# Convert the 'TIME' column to datetime format
oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')
oil_data['year'] = oil_data['TIME'].dt.year

# Label encode the country (LOCATION) for the model
label_encoder = LabelEncoder()
oil_data['LOCATION_ENCODED'] = label_encoder.fit_transform(oil_data['LOCATION'])

# Prepare data for the Random Forest model
X = oil_data[['year', 'LOCATION_ENCODED']]
y = oil_data['Value']

# Train a Random Forest model to predict crude oil production
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Predict crude oil production for each country from 2018 to 2025
predictions = []
predictions_years = list(range(2018, 2026))  # Predict for years 2018 to 2025

for year in predictions_years:
    for location_encoded in oil_data['LOCATION_ENCODED'].unique():
        predicted_value = rf_model.predict([[year, location_encoded]])
        predictions.append({
            'LOCATION': label_encoder.inverse_transform([location_encoded])[0],
            'TIME': pd.Timestamp(str(year)),
            'Value': predicted_value[0]
        })

# Convert predictions to DataFrame
predictions_df = pd.DataFrame(predictions)

# Concatenate actual data and predictions
oil_data_full = pd.concat([oil_data, predictions_df])

# Create a pivot table for oil production over time for each country
pivot_tide = oil_data_full.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum')
pivot_tide.ffill(inplace=True)  # Use .ffill() to fill missing values

# Extract countries and time values
countries = pivot_tide.columns
time_values = pivot_tide.index

# Setup the dashboard
dashboard = lc.Dashboard(theme=lc.Themes.CyberSpace, rows=2, columns=1)

# Row 1: BarChart for Oil Production by Country
bar_chart = dashboard.BarChart(row_index=0, column_index=0)

# Row 2: World Map for Crude Oil Production
map_chart = dashboard.MapChart(row_index=1, column_index=0)

# Function to update the bar chart and map for the given year
def update_charts_for_year(year):
    # Filter data for the given year
    year_data = oil_data_full[oil_data_full['TIME'].dt.year == year]
    map_chart.set_title(f"Crude Oil Production - Year {year}")
    bar_chart.set_title(f'Crude Oil Production by Country in Year {year}')
    
    # Update BarChart
    country_production = []
    for country in countries:
        production_value = year_data[year_data['LOCATION'] == country]['Value'].sum()
        country_production.append({
            "category": country,
            "value": production_value
        })

    # Update the BarChart
    bar_chart.set_data(country_production)

    # Update Map Chart
    map_data = []
    for _, row in year_data.iterrows():
        map_data.append({'ISO_A3': row['LOCATION'], 'value': row['Value']})
    map_chart.invalidate_region_values(map_data)

    # Set the palette colors for the map based on production levels
    map_chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': lc.Color(0, 0, 255)},  # Low production: Blue
            {'value': 50000, 'color': lc.Color(255, 255, 0)},  # Medium production: Yellow
            {'value': 100000, 'color': lc.Color(255, 165, 0)},  # High production: Orange
            {'value': 500000, 'color': lc.Color(255, 0, 0)},  # Very High production: Red
        ],
        look_up_property='value'
    )

# Function to update the dashboard every 2 seconds for each year from 1970 to 2025 (including predicted data)
def update_dashboard():
    for year in list(range(1970, 2018)) + predictions_years:
        print(f"Updating data for year: {year}")
        update_charts_for_year(year)
        time.sleep(2)

# Open the dashboard and start real-time updates
dashboard.open(live=True)
update_dashboard()

# Print the model's accuracy
y_pred = rf_model.predict(X)
mse = mean_squared_error(y, y_pred)
print(f"Mean Squared Error on training set: {mse:.2f}")
