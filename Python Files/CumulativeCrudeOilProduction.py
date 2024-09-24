import pandas as pd
import numpy as np
import lightningchart as lc

lc.set_license(open('../license-key').read())

file_path = 'Dataset/DP_LIVE.xlsx'
data = pd.read_excel(file_path)

country_list = ['AUS', 'CAN', 'USA', 'NOR', 'IRQ', 'RUS', 'IRN', 'MEX']
filtered_data = data[data['LOCATION'].isin(country_list)]

filtered_data = filtered_data.dropna(subset=['Value'])

filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y')

pivot_tide = filtered_data.pivot_table(index='TIME', columns='LOCATION', values='Value', aggfunc='mean')
pivot_tide.fillna(method='ffill', inplace=True)

countries = pivot_tide.columns
time_values = pivot_tide.index
time_values_ms = [int(t.timestamp()) * 1000 for t in time_values]
chart = lc.ChartXY(theme=lc.Themes.White, title='Cumulative Crude Oil Production Over Time Across Countries')

base_area = np.zeros(len(time_values))

for country in countries:
    tide_heights = pivot_tide[country].fillna(0).values

    series = chart.add_area_series(
        data_pattern='ProgressiveX',
    )
    series.set_name(country)
    cumulative_heights = base_area + tide_heights
    series.add(time_values_ms, cumulative_heights.tolist())

    base_area = cumulative_heights

chart.get_default_x_axis().set_title('Time').set_tick_strategy('DateTime')
chart.get_default_y_axis().set_title('Crude Oil Production (KTOE)')


legend = chart.add_legend(data=chart)

chart.open()