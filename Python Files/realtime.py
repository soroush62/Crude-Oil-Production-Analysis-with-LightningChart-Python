import pandas as pd
import lightningchart as lc
from lightningchart import Color, Themes
import numpy as np
import time

# Set the license
lc.set_license(open('../license-key').read())

# Load the dataset
file_path = 'Dataset/DP_LIVE.xlsx'
oil_data = pd.read_excel(file_path)

# Remove rows where 'Value' is blank or zero
filtered_data = oil_data.dropna(subset=['Value'])
filtered_data = filtered_data[filtered_data['Value'] > 0]

# Convert TIME to datetime
filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y')

# Pivot the data to get production values for each country by year
pivot_data = filtered_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum', fill_value=0)
# pivot_data.ffill(inplace=True)  # Use ffill instead of method parameter for newer versions

# Get list of countries and years
countries = pivot_data.columns
time_values = pivot_data.index
time_values_ms = [int(t.timestamp()) * 1000 for t in time_values]  # Convert to milliseconds for use in chart

# Initialize the Dashboard with 2 rows
dashboard = lc.Dashboard(theme=Themes.CyberSpace, rows=2, columns=1)

# First row: Create BarChart for Crude Oil Production by Country
bar_chart = dashboard.BarChart(row_index=0, column_index=0)
bar_chart.set_title("Crude Oil Production by Country Over Time")
# bar_chart.set_axis_x_title('Country')
# bar_chart.set_axis_y_title('Production (KTOE)')

# Bar Chart Data Setup for first row
def update_bar_chart(year_index):
    year = time_values[year_index].year
    production_values = pivot_data.iloc[year_index].values.tolist()

    # Create a list of dictionaries for categories and values
    bar_data = [{'category': country, 'value': production_values[i]} for i, country in enumerate(countries)]
    
    # Set the bar chart data
    bar_chart.set_data(bar_data)
    
    # Update the title for the bar chart
    bar_chart.set_title(f"Crude Oil Production by Country - Year {year}")

# Second row: Create MapChart for Real-Time Crude Oil Production by Country
map_chart = dashboard.MapChart(row_index=1, column_index=0)
map_chart.set_title("Real-Time Crude Oil Production by Country")

# Function to update the MapChart
def update_map_chart(year_index):
    year = time_values[year_index].year
    production_values = pivot_data.iloc[year_index].values.tolist()

    data_year = pd.DataFrame({
        'ISO_A3': countries,
        'value': production_values
    })

    map_chart.invalidate_region_values(data_year.to_dict(orient='records'))
    map_chart.set_title(f"Real-Time Crude Oil Production - Year {year}")

    # Set color palette for production values
    map_chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': Color('#f7fbff')},  # Light color for low production
            {'value': 50000, 'color': Color('#FFD700')},  # Yellow for moderate production
            {'value': 100000, 'color': Color('#FF8C00')},  # Orange for higher production
            {'value': 500000, 'color': Color('#FF0000')},  # Red for high production
            {'value': 1000000, 'color': Color('#8B0000')}  # Dark Red for very high production
        ],
        look_up_property='value',
        percentage_values=False  # Use absolute values instead of percentages
    )

# Function to update the entire dashboard
def update_dashboard():
    for year_index in range(len(time_values)):
        # Update the BarChart and MapChart for the current year
        update_bar_chart(year_index)
        update_map_chart(year_index)

        # Simulate real-time updates by sleeping for 1 second between updates
        time.sleep(0.5)

# Open the dashboard and run the update loop
dashboard.open(live=True)
update_dashboard()






# import pandas as pd
# import lightningchart as lc
# import time

# lc.set_license(open('../license-key').read())

# file_path = 'Dataset/DP_LIVE.xlsx'
# oil_data = pd.read_excel(file_path)

# oil_data = oil_data[oil_data['Value'] > 0].dropna(subset=['Value'])

# oil_data = oil_data[(oil_data['TIME'] >= 1970) & (oil_data['TIME'] <= 2017)]

# oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')
# pivot_tide = oil_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum', fill_value=0)

# countries = pivot_tide.columns
# time_values = pivot_tide.index

# dashboard = lc.Dashboard(theme=lc.Themes.CyberSpace, rows=2, columns=1)

# bar_chart = dashboard.BarChart(row_index=0, column_index=0)

# map_chart = dashboard.MapChart(row_index=1, column_index=0)

# def update_charts_for_year(year):
#     year_data = oil_data[oil_data['TIME'].dt.year == year]
#     map_chart.set_title(f"Crude Oil Production - Year {year}")
#     bar_chart.set_title(f'Crude Oil Production by Country in Year {year}')
#     country_production = []
#     for country in countries:
#         if country == 'WLD':  
#             continue
#         production_value = year_data[year_data['LOCATION'] == country]['Value'].sum()
#         country_production.append({
#             "category": country,
#             "value": production_value
#         })

#     bar_chart.set_data(country_production)

#     map_data = []
#     for _, row in year_data.iterrows():
#         map_data.append({'ISO_A3': row['LOCATION'], 'value': row['Value']})
#     map_chart.invalidate_region_values(map_data)

#     map_chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': lc.Color(0, 0, 255)},  # Blue
#             {'value': 50000, 'color': lc.Color(255, 255, 0)},  # Yellow
#             {'value': 100000, 'color': lc.Color(255, 165, 0)},  #Orange
#             {'value': 500000, 'color': lc.Color(255, 0, 0)},  #Red
#         ],
#         look_up_property='value'
#     )

# def update_dashboard():
#     for year in range(1970, 2018):
#         print(f"Updating data for year: {year}")
#         update_charts_for_year(year)
#         time.sleep(2)

# dashboard.open(live=True)
# update_dashboard()




