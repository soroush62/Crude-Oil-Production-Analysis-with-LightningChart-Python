import pandas as pd
import lightningchart as lc
from lightningchart import Color, Themes

lc.set_license(open('../license-key').read())

file_path = 'Dataset/DP_LIVE.xlsx'
oil_data = pd.read_excel(file_path)

def create_world_map_chart(data, year):
    data_year = data[data['TIME'] == year]
    data_year = data_year[['LOCATION', 'Value']].rename(columns={'LOCATION': 'ISO_A3', 'Value': 'value'})

    chart = lc.MapChart(map_type='World', theme=lc.Themes.White)

    chart.invalidate_region_values(data_year.to_dict(orient='records'))
    
    chart.set_title(f"Crude Oil Production - Year {year} - World")
    
    chart.set_palette_colors(
        steps=[
            {'value': 0, 'color': Color('#f7fbff')},  # Light color for low production
            {'value': 50000, 'color': Color('#FFD700')},  # Yellow for moderate production
            {'value': 100000, 'color': Color('#FF8C00')},  # Orange for higher production
            {'value': 500000, 'color': Color('#FF0000')},  # Red for high production
            {'value': 1000000, 'color': Color('#8B0000')}  # Dark Red for very high production
        ],
        look_up_property='value',
        percentage_values=False  # We use absolute values, not percentages
    )
    
    # Enable hover highlighting for interactivity
    chart.set_highlight_on_hover(enabled=True)
    
    # Add a legend for clarity
    legend = chart.add_legend(horizontal=True, title=f"Crude Oil Production - Year: {year}", data=chart)
    legend.set_font_size(10)

    # Open the chart in live mode
    chart.open(live=True)
    return chart

# Call the function for a specific year
create_world_map_chart(oil_data, 2010)
