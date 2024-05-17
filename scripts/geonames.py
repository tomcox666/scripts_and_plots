import geopandas as gpd
import folium
import requests
from shapely.geometry import Point
import pandas as pd
from flask import Flask, request, render_template
import ujson
import os

app = Flask(__name__)

# Load GeoNames API credentials from environment variables
GEONAMES_USERNAME = os.environ['GEONAMES_USERNAME']


# Define a function to make API requests to GeoNames
def get_geonames_data(params):
    api_endpoint = 'http://api.geonames.org/searchJSON'
    params['username'] = GEONAMES_USERNAME
    response = requests.get(api_endpoint, params=params)
    data = ujson.loads(response.content)
    return data

# Define a function to process GeoNames data and create a Folium map
def create_map(data):
    df = pd.json_normalize(data['geonames'])
    df['geometry'] = df.apply(lambda row: Point(row.lng, row.lat), axis=1)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf = gdf.set_crs(epsg=4326)
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=12, title='GeoNames Data')

    population_threshold = 100000
    for idx, row in df.iterrows():
        if int(row['population']) > population_threshold:
            iframe = folium.IFrame(html=f'''
                <h1>{row['name']}</h1>
                <p>State: {row['adminName1']}</p>
                <p>Country Code: {row['countryCode']}</p>
                <p>Population: {row['population']}</p>
            ''', width=300, height=200)
            popup = folium.Popup(iframe, parse_html=True)
            marker = folium.Marker(location=[row['lat'], row['lng']], popup=popup)
            marker.add_to(m)
    return m

# Define a function to render the map as an HTML page
def render_map(map):
    return map._repr_html_()

# Define the main route
@app.route('/')
def index():
    country = request.args.get('country', default='US')
    params = {'country': country, 'maxRows': 1000}
    data = get_geonames_data(params)
    map = create_map(data)
    return render_map(map)

# Define the search route
@app.route('/search')
def search():
    query = request.args.get('query')
    params = {'q': query, 'maxRows': 1000}
    data = get_geonames_data(params)
    map = create_map(data)
    return render_map(map)

if __name__ == '__main__':
    app.run()