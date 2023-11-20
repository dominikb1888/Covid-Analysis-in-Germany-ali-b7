import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster

# Load your GeoJSON data
geojson_path = 'bundeslande.geojson'
gdf = gpd.read_file(geojson_path)

del gdf['BEGINN']
del gdf['WSK']

csv_path = 'covid_de.csv'
data = pd.read_csv(csv_path)



# Merge GeoJSON data with CSV data on the common column
merged_data = gdf.merge(data, left_on='GEN', right_on='Bundesland')


# Create a folium map centered around the mean latitude and longitude of the GeoJSON data
map_center = [merged_data.geometry.centroid.y.mean(), merged_data.geometry.centroid.x.mean()]
m = folium.Map(location=map_center, zoom_start=6)

# Create MarkerClusters for better performance
marker_cluster = MarkerCluster().add_to(m)

# Add GeoJSON layer with covid data and tooltips
folium.GeoJson(merged_data,
               name='Covid Data',
               tooltip=folium.GeoJsonTooltip(fields=['Bundesland', 'Covid Cases'],
                                             aliases=['Region', 'Covid Cases'],
                                             localize=True),
               ).add_to(marker_cluster)

# Add additional data as markers
for idx, row in merged_data.iterrows():
    folium.Marker(location=[row.geometry.centroid.y, row.geometry.centroid.x],
                  popup=f"<strong>{row['GEN']}</strong><br>Population: {row['Population']}<br>Vaccination Rate: {row['Vaccination Rate']}<br>Covid Cases: {row['Covid Cases']}<br>Total Deaths: {row['Total Deaths']}",
                  icon=folium.Icon(color='blue'),
                  ).add_to(marker_cluster)

# Create a HeatMap layer using the location coordinates and intensity (e.g., COVID cases)
heat_data = [[point.xy[1][0], point.xy[0][0], row['Covid Cases']] for idx, row in merged_data.iterrows() for point in [row.geometry.centroid]]
HeatMap(heat_data, name='Heatmap', radius=25, blur=20, gradient={0.4: '#FFD700', 0.65: '#FF4500', 1: '#8B0000'}).add_to(m)

# Add Layer Control to toggle layers
folium.LayerControl().add_to(m)

# Save the map as an HTML file
m.save('de_covidmapfinal.html')
