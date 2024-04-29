# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
import configparser
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, BoxZoomTool, PanTool, ColumnDataSource

# Load configurations with error handling
config = configparser.ConfigParser()
config.read('econ_sim.config')

# Country setup
initial_pop_1 = int(config['COUNTRY_1']['initial_population'])
tech_level_1 = float(config['COUNTRY_1']['initial_technology'])
resources_1 = int(config['COUNTRY_1']['resources'])
pop_growth_rate_1 = float(config['COUNTRY_1']['population_growth_rate'])
tech_investment_1 = float(config['COUNTRY_1']['investment_in_technology'])

initial_pop_2 = int(config['COUNTRY_2']['initial_population'])
tech_level_2 = float(config['COUNTRY_2']['initial_technology'])
resources_2 = int(config['COUNTRY_2']['resources'])
pop_growth_rate_2 = float(config['COUNTRY_2']['population_growth_rate'])
tech_investment_2 = float(config['COUNTRY_2']['investment_in_technology'])

# Simulation loop
years = 30
gdp_history_1 = []
gdp_history_2 = []
year_list = list(range(30))  # Ensure proper serialization

for year in year_list:
    gdp_1 = initial_pop_1 * tech_level_1 * (resources_1 / 1000000)
    gdp_history_1.append(gdp_1)

    gdp_2 = initial_pop_2 * tech_level_2 * (resources_2 / 1000000)
    gdp_history_2.append(gdp_2)

    initial_pop_1 *= 1 + pop_growth_rate_1
    tech_level_1 += tech_investment_1
    resources_1 -= resources_1 * float(config['COUNTRY_1']['resource_depletion_rate'])

    initial_pop_2 *= 1 + pop_growth_rate_2
    tech_level_2 += tech_investment_2
    resources_2 -= resources_2 * float(config['COUNTRY_2']['resource_depletion_rate'])

# Matplotlib plot
plt.figure(figsize=(12, 7))
plt.plot(gdp_history_1, label='Country 1', color='royalblue', linewidth=2, linestyle='--')
plt.plot(gdp_history_2, label='Country 2', color='darkorange', linewidth=2, linestyle='-')

plt.xlabel('Year')
plt.ylabel('GDP (Millions)')
plt.title('Economic Growth Comparison')

# Add annotations and grid
plt.annotate('Tech Investment in Country 2', xy=(15, gdp_history_2[15] + 20000), xytext=(17, gdp_history_2[15] + 25000),
             arrowprops=dict(arrowstyle='->', color='lightgreen'))

plt.annotate('Economic Downturn in Country 1', xy=(10, gdp_history_1[10] - 30000), xytext=(8, gdp_history_1[10] - 35000),
             arrowprops=dict(arrowstyle='->', color='red'))

plt.legend()
plt.grid(True)
plt.show()

# Bokeh plot with explicit data source
data = {
    'years': year_list,
    'gdp_1': gdp_history_1,
    'gdp_2': gdp_history_2,
}

source = ColumnDataSource(data=data)  # Ensure explicit data source

bokeh_fig = figure(width=800, height=400, title='Interactive GDP Comparison')

bokeh_fig.line(x='years', y='gdp_1', source=source, line_width=2, color='royalblue', legend_label='Country 1')
bokeh_fig.line(x='years', y='gdp_2', source=source, line_width=2, color='darkorange', legend_label='Country 2')

hover = HoverTool(
    tooltips=[('Year', '@years'), ('GDP', '@y')],
    mode='vline'
)

bokeh_fig.add_tools(hover, BoxZoomTool(), PanTool())
bokeh_fig.xaxis.axis_label = 'Year'
bokeh_fig.yaxis.axis_label = 'GDP (Millions)'
bokeh_fig.legend.location = 'top_left'

show(bokeh_fig)  # Display the Bokeh interactive plot
