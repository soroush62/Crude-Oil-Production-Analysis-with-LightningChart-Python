# import pandas as pd
# import lightningchart as lc
# from datetime import datetime
# import numpy as np

# lc.set_license(open('../license-key').read())

# file_path = 'Dataset/DP_LIVE.xlsx'
# data = pd.read_excel(file_path)

# country_list = ['AUS', 'CAN', 'USA', 'NOR', 'IRQ', 'RUS', 'IRN', 'MEX']
# filtered_data = data[data['LOCATION'].isin(country_list)]

# filtered_data = filtered_data.dropna(subset=['Value'])

# filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y').dt.strftime('%Y')

# x_values = filtered_data['TIME'].unique().tolist()

# chart = lc.BarChart(
#     vertical=True,
#     theme=lc.Themes.White,
#     title='Crude Oil Production Over Time (Stacked Bar Chart)'
# )

# stacked_data = []
# for country in country_list:
#     stacked_data.append({'subCategory': country,
#                          'values': filtered_data[filtered_data['LOCATION'] == country]['Value'].values.tolist()}
#                         )
# chart.set_data_stacked(x_values, stacked_data)
# chart.set_value_label_display_mode('hidden')

# # chart.set_palette_colors(
# #         steps=[
# #             {'value': min(filtered_data['Value']), 'color': lc.Color('blue')}, 
# #             {'value': (min(filtered_data['Value']) + max(filtered_data['Value'])/2), 'color': lc.Color('yellow')}, 
# #             {'value': max(filtered_data['Value']), 'color': lc.Color('red')}  
# #         ],
# #         percentage_values=True 
# #     )

# chart.add_legend().add(chart)
# chart.open()



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

filtered_data['TIME'] = pd.to_datetime(filtered_data['TIME'], format='%Y').dt.strftime('%Y')
x_values = filtered_data['TIME'].unique().tolist()

chart = lc.BarChart(
    vertical=True,
    theme=lc.Themes.White,
    title='Crude Oil Production Over Time (Stacked Bar Chart)'
)

chart.set_sorting('alphabetical') 

color_map = {
    'AUS': '#FF0000',    # Red
    'CAN': '#00FF00',    # Green
    'USA': '#0000FF',    # Blue
    'NOR': '#FFFF00',    # Yellow
    'IRQ': '#FF00FF',    # Magenta
    'RUS': '#00FFFF',    # Cyan
    'IRN': '#800080',    # Purple
    'MEX': '#FFA500'     # Orange
}
stacked_data = []
for country in country_list:
    country_values = filtered_data[filtered_data['LOCATION'] == country]['Value'].values.tolist()
    stacked_data.append({
        'subCategory': country,
        'values': country_values,
        'color': color_map[country]  
    })

chart.set_data_stacked(x_values, stacked_data)

chart.set_value_label_display_mode('hidden')
chart.add_legend().add(chart)
chart.set_label_rotation(45)
chart.open()
