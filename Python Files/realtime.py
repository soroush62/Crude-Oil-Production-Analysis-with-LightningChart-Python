# import pandas as pd
# import lightningchart as lc
# from lightningchart import Color, Themes
# import numpy as np
# import time

# # Set the license
# lc.set_license(open('../license-key').read())

# # Load the dataset
# file_path = 'Dataset/DP_LIVE.xlsx'
# oil_data = pd.read_excel(file_path)

# # Remove rows where 'Value' is blank or zero
# filtered_data = oil_data.dropna(subset=['Value'])
# filtered_data = filtered_data[filtered_data['Value'] > 0]

# # Convert TIME to datetime
# filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y')

# # Pivot the data to get production values for each country by year
# pivot_data = filtered_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum')
# pivot_data.ffill(inplace=True)  # Use ffill instead of method parameter for newer versions

# # Get list of countries and years
# countries = pivot_data.columns
# time_values = pivot_data.index
# time_values_ms = [int(t.timestamp()) * 1000 for t in time_values]  # Convert to milliseconds for use in chart

# # Initialize the Dashboard with 2 rows
# dashboard = lc.Dashboard(theme=Themes.Dark, rows=2, columns=1)

# # First row: Create BarChart for Crude Oil Production by Country
# bar_chart = dashboard.BarChart(row_index=0, column_index=0)
# bar_chart.set_title("Crude Oil Production by Country Over Time")
# # bar_chart.set_axis_x_title('Country')
# # bar_chart.set_axis_y_title('Production (KTOE)')

# # Bar Chart Data Setup for first row
# def update_bar_chart(year_index):
#     year = time_values[year_index].year
#     production_values = pivot_data.iloc[year_index].values.tolist()

#     # Create a list of dictionaries for categories and values
#     bar_data = [{'category': country, 'value': production_values[i]} for i, country in enumerate(countries)]
    
#     # Set the bar chart data
#     bar_chart.set_data(bar_data)
    
#     # Update the title for the bar chart
#     bar_chart.set_title(f"Crude Oil Production by Country - Year {year}")

# # Second row: Create MapChart for Real-Time Crude Oil Production by Country
# map_chart = dashboard.MapChart(row_index=1, column_index=0)
# map_chart.set_title("Real-Time Crude Oil Production by Country")

# # Function to update the MapChart
# def update_map_chart(year_index):
#     year = time_values[year_index].year
#     production_values = pivot_data.iloc[year_index].values.tolist()

#     data_year = pd.DataFrame({
#         'ISO_A3': countries,
#         'value': production_values
#     })

#     map_chart.invalidate_region_values(data_year.to_dict(orient='records'))
#     map_chart.set_title(f"Real-Time Crude Oil Production - Year {year}")

#     # Set color palette for production values
#     map_chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': Color('#f7fbff')},  # Light color for low production
#             {'value': 50000, 'color': Color('#FFD700')},  # Yellow for moderate production
#             {'value': 100000, 'color': Color('#FF8C00')},  # Orange for higher production
#             {'value': 500000, 'color': Color('#FF0000')},  # Red for high production
#             {'value': 1000000, 'color': Color('#8B0000')}  # Dark Red for very high production
#         ],
#         look_up_property='value',
#         percentage_values=False  # Use absolute values instead of percentages
#     )

# # Function to update the entire dashboard
# def update_dashboard():
#     for year_index in range(len(time_values)):
#         # Update the BarChart and MapChart for the current year
#         update_bar_chart(year_index)
#         update_map_chart(year_index)

#         # Simulate real-time updates by sleeping for 1 second between updates
#         time.sleep(1)

# # Open the dashboard and run the update loop
# dashboard.open(live=True)
# update_dashboard()






# import pandas as pd
# import lightningchart as lc
# from lightningchart import Color, Themes
# import numpy as np
# import time

# # Set the license
# lc.set_license(open('../license-key').read())

# # Load the dataset
# file_path = 'Dataset/DP_LIVE.xlsx'
# oil_data = pd.read_excel(file_path)

# # Remove rows where 'Value' is blank or zero
# filtered_data = oil_data.dropna(subset=['Value'])
# filtered_data = filtered_data[filtered_data['Value'] > 0]

# # Convert TIME to datetime
# filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y')

# # Pivot the data to get production values for each country by year
# pivot_data = filtered_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum')
# pivot_data.ffill(inplace=True)  # Use ffill instead of method parameter for newer versions

# # Get list of countries and years
# countries = pivot_data.columns
# time_values = pivot_data.index
# time_values_ms = [int(t.timestamp()) * 1000 for t in time_values]  # Convert to milliseconds for use in chart

# # Initialize the Dashboard with 2 rows
# dashboard = lc.Dashboard(theme=Themes.Dark, rows=2, columns=1)

# # First row: ChartXY for Crude Oil Production by Country
# chart_xy = dashboard.ChartXY(row_index=0, column_index=0)
# chart_xy.set_title("Crude Oil Production by Country Over Time")

# # Set up the X and Y axes
# x_axis = chart_xy.get_default_x_axis()
# x_axis.set_title('Time')
# x_axis.set_tick_strategy('DateTime')

# y_axis = chart_xy.get_default_y_axis()
# y_axis.set_title('Crude Oil Production')

# # Create a line series once and update it in each iteration
# legend=chart_xy.add_legend()
# line_series = {}
# for country in countries:
#     line_series[country] = chart_xy.add_line_series().set_name(country)
#     legend.add(line_series[country])

# # Second row: MapChart for Real-Time Crude Oil Production by Country
# map_chart = dashboard.MapChart(row_index=1, column_index=0)
# map_chart.set_title("Real-Time Crude Oil Production by Country")

# # Function to update the MapChart
# def update_map_chart(year_index):
#     year = time_values[year_index].year
#     production_values = pivot_data.iloc[year_index].values.tolist()

#     data_year = pd.DataFrame({
#         'ISO_A3': countries,
#         'value': production_values
#     })

#     map_chart.invalidate_region_values(data_year.to_dict(orient='records'))
#     map_chart.set_title(f"Real-Time Crude Oil Production - Year {year}")

#     # Set color palette for production values
#     map_chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': Color('#f7fbff')},  # Light color for low production
#             {'value': 50000, 'color': Color('#FFD700')},  # Yellow for moderate production
#             {'value': 100000, 'color': Color('#FF8C00')},  # Orange for higher production
#             {'value': 500000, 'color': Color('#FF0000')},  # Red for high production
#             {'value': 1000000, 'color': Color('#8B0000')}  # Dark Red for very high production
#         ],
#         look_up_property='value',
#         percentage_values=False  # Use absolute values instead of percentages
#     )

# # Function to update the ChartXY and dynamically adjust the Y-axis range
# def update_chart_xy(year_index):
#     year = time_values[year_index].year
#     production_values = pivot_data.iloc[year_index].values.tolist()

#     # Get the max value for the year to dynamically adjust the Y-axis range
#     max_value = max(production_values)

#     # Update data for each country's series
#     for i, country in enumerate(countries):
#         line_series[country].add([time_values_ms[year_index]], [production_values[i]])

#     # Dynamically adjust the Y-axis range based on the max value
#     if max_value > 0:
#         y_axis.set_interval(0, max_value * 1.1)  # Increase max range slightly

# # Function to update the entire dashboard
# def update_dashboard():
#     for year_index in range(len(time_values)):
#         # Update the ChartXY and MapChart for the current year
#         update_chart_xy(year_index)
#         update_map_chart(year_index)

#         # Simulate real-time updates by sleeping for 1 second between updates
#         time.sleep(1)

# # Open the dashboard and run the update loop
# dashboard.open(live=True)
# update_dashboard()






## BoxPLot
# import pandas as pd
# import lightningchart as lc
# import time

# # Load your LightningChart license
# lc.set_license(open('../license-key').read())

# # Load the dataset for oil production
# file_path = 'Dataset/DP_LIVE.xlsx'
# oil_data = pd.read_excel(file_path)

# # Remove rows with zero or missing 'Value'
# oil_data = oil_data[oil_data['Value'] > 0].dropna(subset=['Value'])

# # Filter the data for the years 1970 to 2017
# oil_data = oil_data[(oil_data['TIME'] >= 1970) & (oil_data['TIME'] <= 2017)]

# # Convert the 'TIME' column to datetime format
# oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')

# # Create a pivot table for oil production over time for each country
# pivot_tide = oil_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum')
# pivot_tide.ffill(inplace=True)  # Use .ffill() to fill missing values

# # Extract countries and time values
# countries = pivot_tide.columns
# time_values = pivot_tide.index

# # Setup the dashboard
# dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=1)

# # Row 1: Simulating Bar Chart using BoxSeries
# chart_bar = dashboard.ChartXY(row_index=0, column_index=0, title='Crude Oil Production by Country Over Time')
# chart_bar.get_default_x_axis().set_title('Country')
# chart_bar.get_default_y_axis().set_title('Production Volume (KTOE)')
# bar_series_dict = {}

# # Add a BoxSeries for each country
# for country in countries:
#     box_series = chart_bar.add_box_series()
#     box_series.set_name(country)
#     bar_series_dict[country] = box_series

# # Row 2: World Map for Crude Oil Production
# map_chart = dashboard.MapChart(row_index=1, column_index=0)
# map_chart.set_title("Crude Oil Production by Country")

# # Function to update the bar chart and map for the given year
# def update_charts_for_year(year):
#     # Filter data for the given year
#     year_data = oil_data[oil_data['TIME'].dt.year == year]

#     # Update BoxSeries for each country
#     for country in countries:
#         production_value = year_data[year_data['LOCATION'] == country]['Value'].sum()

#         if country in bar_series_dict:
#             # Add the box data to the BoxSeries (used as bar chart)
#             # BoxSeries requires a start and end along with quartiles, we simulate the start and end with the same value.
#             bar_series_dict[country].add(
#                 start=year,  # You can set any x-value like a year or country code
#                 end=year + 1,  # Simulating a small range for each bar
#                 median=production_value,  # Production value as median
#                 lower_quartile=production_value * 0.8,  # Simulated quartile for visualization
#                 upper_quartile=production_value * 1.2,  # Simulated quartile for visualization
#                 lower_extreme=production_value * 0.7,  # Simulated extreme for visualization
#                 upper_extreme=production_value * 1.3   # Simulated extreme for visualization
#             )

#     # Update Map Chart
#     map_data = []
#     for _, row in year_data.iterrows():
#         map_data.append({'ISO_A3': row['LOCATION'], 'value': row['Value']})
#     map_chart.invalidate_region_values(map_data)

#     # Set the palette colors for the map based on production levels
#     map_chart.set_palette_colors(
#         steps=[
#             {'value': 0, 'color': lc.Color(0, 0, 255)},  # Low production: Blue
#             {'value': 50000, 'color': lc.Color(255, 255, 0)},  # Medium production: Yellow
#             {'value': 100000, 'color': lc.Color(255, 165, 0)},  # High production: Orange
#             {'value': 500000, 'color': lc.Color(255, 0, 0)},  # Very High production: Red
#         ],
#         look_up_property='value'
#     )

# # Function to update the dashboard every 2 seconds for each year from 1970 to 2017
# def update_dashboard():
#     for year in range(1970, 2018):
#         print(f"Updating data for year: {year}")
#         update_charts_for_year(year)
#         time.sleep(2)

# # Open the dashboard and start real-time updates
# dashboard.open(live=True)
# update_dashboard()




import pandas as pd
import lightningchart as lc
import time

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

# Create a pivot table for oil production over time for each country
pivot_tide = oil_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='sum')
pivot_tide.ffill(inplace=True)  # Use .ffill() to fill missing values

# Extract countries and time values
countries = pivot_tide.columns
time_values = pivot_tide.index

# Setup the dashboard
dashboard = lc.Dashboard(theme=lc.Themes.Light, rows=2, columns=1)

# Row 1: BarChart for Oil Production by Country
bar_chart = dashboard.BarChart(row_index=0, column_index=0)
# bar_chart.set_title('Crude Oil Production by Country Over Time')
# dashboard.add_chart(bar_chart, row_index=0, column_index=0)

# Row 2: World Map for Crude Oil Production
map_chart = dashboard.MapChart(row_index=1, column_index=0)
# map_chart.set_title(f'Real-Time Crude Oil Production by Country {time_values[0].year}-{time_values[-1].year}')

# Function to update the bar chart and map for the given year
def update_charts_for_year(year):
    # Filter data for the given year
    year_data = oil_data[oil_data['TIME'].dt.year == year]
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

# Function to update the dashboard every 2 seconds for each year from 1970 to 2017
def update_dashboard():
    for year in range(1970, 2018):
        print(f"Updating data for year: {year}")
        update_charts_for_year(year)
        time.sleep(2)

# Open the dashboard and start real-time updates
dashboard.open(live=True)
update_dashboard()
