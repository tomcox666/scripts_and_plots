import pandas as pd
import plotly.express as px
import numpy as np

# Example DataFrame with expanded data including European airports
df_airport_delays = pd.DataFrame({
    'LOCATION': ['US', 'US', 'US', 'US', 'US', 'US', 'US', 'EU', 'EU', 'EU', 'EU', 'EU', 'EU'],
    'OR_STATE': ['OREGON', 'OREGON', 'OREGON', 'CALIFORNIA', 'CALIFORNIA', 'WASHINGTON', 'WASHINGTON',
                 'FRANCE', 'FRANCE', 'GERMANY', 'GERMANY', 'UK', 'UK'],
    'AIRPORT': ['PDX - Portland', 'PDX - Portland', 'EUG - Eugene', 'SFO - San Francisco', 'LAX - Los Angeles',
                'SEA - Seattle', 'GEG - Spokane', 'CDG - Paris', 'ORY - Paris', 'FRA - Frankfurt', 'MUC - Munich',
                'LHR - London', 'LGW - London'],
    'AIRLINE': ['ALASKA AIRLINES', 'DELTA', 'UNITED AIRLINES', 'AMERICAN AIRLINES', 'SOUTHWEST AIRLINES', 'JETBLUE', 'SPIRIT AIRLINES',
                'AIR FRANCE', 'EASYJET', 'LUFTHANSA', 'LUFTHANSA', 'BRITISH AIRWAYS', 'EASYJET'],
    'NUM_OF_FLIGHTS_BY_AIRLINE_AIRPORT': [100, 50, 25, 75, 125, 80, 40, 120, 90, 70, 50, 110, 60],
    'AVG_DELAY_BY_AIRLINE': [10, 5, -5, 15, 20, 8, 12, 10, 8, 5, 10, 15, 12]
})

# Create treemap chart figure
fig = px.treemap(df_airport_delays, 
                  path=['LOCATION', 'OR_STATE', 'AIRPORT', 'AIRLINE'], 
                  values='NUM_OF_FLIGHTS_BY_AIRLINE_AIRPORT',
                  color='AVG_DELAY_BY_AIRLINE',
                  color_continuous_scale='balance',
                  color_continuous_midpoint=np.average(df_airport_delays['AVG_DELAY_BY_AIRLINE']))

# Create suburst chart figure
fig_2 = px.sunburst(df_airport_delays, 
                  path=['LOCATION', 'OR_STATE', 'AIRPORT', 'AIRLINE'], 
                  values='NUM_OF_FLIGHTS_BY_AIRLINE_AIRPORT',
                  color='AVG_DELAY_BY_AIRLINE',
                  color_continuous_scale='balance',
                  color_continuous_midpoint=np.average(df_airport_delays['AVG_DELAY_BY_AIRLINE']))

# Update layout
fig.update_layout(
    title="Flight Delays and Traffic by Airport",
    margin=dict(t=50, l=25, r=25, b=25)
)

fig_2.update_layout(
    title="Flight Delays and Traffic by Airport",
    margin=dict(t=50, l=25, r=25, b=25)
)

# Add hover information
fig.update_traces(
    hovertemplate='<b>%{label}</b><br>' +
                  'Flights: %{value}<br>' +
                  'Avg Delay: %{color}<extra></extra>'
)

# Add hover information
fig.update_traces(
    hovertemplate='<b>%{label}</b><br>' +
                  'Flights: %{value}<br>' +
                  'Avg Delay: %{color}<extra></extra>'
)

# Show the plot
fig.show()
fig_2.show()