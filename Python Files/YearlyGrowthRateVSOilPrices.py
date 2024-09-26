import pandas as pd
import numpy as np
import lightningchart as lc
from datetime import datetime

lc.set_license(open('../license-key').read())

production_file_path = 'Dataset/DP_LIVE.xlsx'
prices_file_path = 'Dataset/Oil Prices by Year.xlsx'

oil_data = pd.read_excel(production_file_path)
oil_data = oil_data[(oil_data['Value'] > 0) & (~oil_data['LOCATION'].isin(['WLD','EU28 ','G20 ','OECD']))].dropna(subset=['Value'])

oil_data['TIME'] = pd.to_datetime(oil_data['TIME'], format='%Y')
pivot_production = oil_data.pivot_table(index=oil_data['TIME'].dt.year, values='Value', aggfunc='sum').reset_index()
pivot_production.columns = ['Year', 'Total_Production']

oil_prices = pd.read_excel(prices_file_path)

merged_data = pd.merge(pivot_production, oil_prices, on='Year', how='inner')

merged_data['YoY_Production'] = merged_data['Total_Production'].pct_change() * 100

merged_data.fillna(0, inplace=True)

chart = lc.ChartXY(theme=lc.Themes.Dark, title="Yearly Growth Rate of Oil Production and Oil Prices")
y_axis_production = chart.get_default_y_axis()
y_axis_production.set_title("Yearly Production (YoY %)")

y_axis_prices = chart.add_y_axis(opposite=True)
y_axis_prices.set_title("Oil Prices (USD/bbl)")

series_production = chart.add_area_series()
series_production.set_name('YoY Production (YoY %)')

series_prices = chart.add_point_line_series(y_axis=y_axis_prices)
series_prices.set_name('Oil Prices (USD/bbl)')
series_prices.set_point_shape('triangle').set_point_size(6).set_line_thickness(2).set_line_color(lc.Color(255, 255, 0))  # Yellow

x_values = [int(datetime(year, 1, 1).timestamp()) * 1000 for year in merged_data['Year']]
y_values_production = merged_data['YoY_Production'].tolist()

series_production.add(x=x_values, y=y_values_production)
series_production.set_fill_color(lc.Color(255,153,153))  # light red
series_production.set_line_color(lc.Color(255,153,153))  

y_values_prices = merged_data['Price'].tolist()
series_prices.add(x=x_values, y=y_values_prices)

x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

y_axis_production.add_constant_line().set_value(0).set_stroke(2, lc.Color(255, 0, 0))  # Red 

legend = chart.add_legend()
legend.set_margin(70)
legend.add(series_production)
legend.add(series_prices)

chart.open()
