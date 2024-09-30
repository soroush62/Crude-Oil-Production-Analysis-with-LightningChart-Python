import pandas as pd
import lightningchart as lc
from random import randint

lc.set_license(open('../license-key').read())

file_path = 'Dataset/DP_LIVE.xlsx'
oil_data = pd.read_excel(file_path)

filtered_data = oil_data[(oil_data['TIME'] == 2011) & (oil_data['Value']>100000)]

year_data = filtered_data.dropna(subset=['Value'])

countries = year_data['LOCATION'].values.tolist()
production_values = year_data['Value'].values.tolist()

chart = lc.PieChart(title='Crude Oil Production Breakdown by Country in 2011',theme=lc.Themes.Light)
chart.set_slice_stroke(color=lc.Color('white'),thickness=1)

for i, country in enumerate(countries):
    random_color = lc.Color(randint(0, 255), randint(0, 255), randint(0, 255))
    
    chart.add_slice(
        name=country,            
        value=production_values[i],      
        )

chart.open()
