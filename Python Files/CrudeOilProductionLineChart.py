import pandas as pd
import lightningchart as lc
from datetime import datetime
import numpy as np

lc.set_license(open('../license-key').read())

file_path = 'Dataset/DP_LIVE.xlsx'
data = pd.read_excel(file_path)

country_list = ['AUS', 'CAN', 'USA', 'NOR', 'IRQ', 'RUS', 'IRN', 'MEX']
filtered_data = data[data['LOCATION'].isin(country_list)]

filtered_data = filtered_data.dropna(subset=['Value'])

filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y')

chart = lc.ChartXY(
    theme=lc.Themes.Light,
    title='Crude Oil Production Over Time (Multiple Countries)'
)

color_map = {key: lc.Color(np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)) for key in country_list}

point_shapes = [
    'circle',
    'triangle',
    'square',
    'star',
    'arrow',
    'plus',
    'cross',
    'diamond',
]
legend = chart.add_legend()
for i, country in enumerate(country_list):
    country_data = filtered_data[filtered_data['LOCATION'] == country]
    x_values = [int(datetime(d.year, 1, 1).timestamp()) * 1000 for d in country_data['TIME']]
    y_values = country_data['Value'].values.tolist()

    series = chart.add_point_line_series()
    series.set_point_shape(point_shapes[i % len(point_shapes)])  
    series.set_point_size(6)          
    series.set_line_thickness(2)     
    series.set_line_color(color_map[country]) 
    series.set_name(country)  
    series.add(x=x_values, y=y_values)
    legend.add(series)
    

x_axis = chart.get_default_x_axis()
x_axis.set_title('Year')
x_axis.set_tick_strategy('DateTime', utc=True)

y_axis = chart.get_default_y_axis()
y_axis.set_title('Crude Oil Production (KTOE)')



chart.open()
