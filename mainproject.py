import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap

# Load your GeoJSON data
geojson_path = 'bundeslande.geojson'
gdf = gpd.read_file(geojson_path)

del gdf['BEGINN']
del gdf['WSK']

csv_path = 'covid_de1.csv'
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
               control=False  # Set control to False to hide the layer by default
               ).add_to(marker_cluster)

# Create Choropleth layer
folium.Choropleth(geo_data=merged_data,
                  name='Deaths',
                  data=merged_data,
                  columns=['Bundesland', 'Total Deaths'],
                  key_on='feature.properties.Bundesland',
                  fill_color='YlOrRd',
                  fill_opacity=0.7,
                  line_opacity=0.2,
                  legend_name='Deaths',
                  highlight=True,
                  ).add_to(m)

# adding data as markers
for idx, row in merged_data.iterrows():
    # Choose marker color based on Covid Cases
    if row['Covid Cases'] < 200000:
        marker_color = 'green'  # Low cases
    elif 200000 <= row['Covid Cases'] < 900000:
        marker_color = 'blue'  # Moderate cases
    else:
        marker_color = 'red'  # High cases

    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(
            f"<strong>{row['GEN']}</strong><br>Population: {row['Population']}<br>Vaccination Rate: {row['Vaccination Rate']}<br>Covid Cases: {row['Covid Cases']}<br>Total Deaths: {row['Total Deaths']}",
            max_width=400  # Adjust the value according to your preference
        ),
        icon=folium.Icon(color=marker_color)
    ).add_to(marker_cluster)

# Add Legend
legend_html = """
    <div style="position: fixed; 
             bottom: 50px; left: 50px; width: 160px; height: 150px; 
             border:2px solid grey; z-index:9999; font-size:12px;
             background-color: white;
             ">
 &nbsp; <strong>no. of Cases</strong> <br>
 &nbsp; Low COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:green"></i> (< 200,000)<br>
 &nbsp; Moderate COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:blue"></i> (200,000 - 900,000)<br>
 &nbsp; High COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:red"></i> (> 900,000)
  </div>
 """

m.get_root().html.add_child(folium.Element(legend_html))

# Create a HeatMap layer using the location coordinates and intensity (e.g., COVID cases)
heat_data = [[point.xy[1][0], point.xy[0][0], row['Population']] for idx, row in merged_data.iterrows() for
             point in [row.geometry.centroid]]

gradient = {
    0.3: '#fdcc8a',  # Light orange
    0.5: '#fc8d59',  # Orange
    0.65: '#d7301f',  # Darker orange/red (for populations below 5 million)
    0.9: '#d7301f',  # Same dark shade (for populations between 5 million and 9 million)
    1.0: '#7f0000'  # Maximum dark shade (for populations above 10 million)
}

HeatMap(heat_data, name='Population Density', radius=35, blur=15, gradient=gradient).add_to(m)

# Create a FeatureGroup for the CircleMarker layer
vaccination_markers = folium.FeatureGroup(name='Vaccination Rate')

# Function to add CircleMarker layer for vaccination rates
def add_vaccination_markers(vaccination_rate_threshold):
    # Remove previous CircleMarker layer for vaccination rates
    for layer in vaccination_markers._children.values():
        vaccination_markers.get_root().remove(layer)

    # Convert 'Vaccination Rate' to numeric type
    merged_data['Vaccination Rate'] = pd.to_numeric(merged_data['Vaccination Rate'].str.rstrip('%'), errors='coerce')

    # Add new CircleMarker layer with the filtered vaccination rate data
    for idx, row in merged_data.iterrows():
        if pd.notna(row['Vaccination Rate']):
            if row['Vaccination Rate'] >= vaccination_rate_threshold:
                # Adjust circle size and color based on the vaccination rate
                radius = 10 + row['Vaccination Rate'] / 10
                color = 'red' if row['Vaccination Rate'] < 50 else 'orange' if row['Vaccination Rate'] < 80 else 'green'

                folium.CircleMarker(location=[row.geometry.centroid.y, row.geometry.centroid.x],
                                    radius=radius,
                                    color=color,
                                    fill=True,
                                    fill_color=color,
                                    fill_opacity=0.7,
                                    popup=f"<strong>{row['GEN']}</strong><br>Vaccination Rate: {row['Vaccination Rate']}%",
                                    ).add_to(vaccination_markers)

# Set a fixed threshold for vaccination rate (adjust as needed)
vaccination_rate_threshold = 10

# Call the function to add CircleMarker layer
add_vaccination_markers(vaccination_rate_threshold)

# Add the FeatureGroup to the map
vaccination_markers.add_to(m)

# Create a legend for CircleMarker
legend_html = """
    <div style="position: fixed; 
             top: 50px; left: 50px; width: 160px; height: 80px; 
             border:2px solid grey; z-index:9999; font-size:12px;
             background-color: white;
             ">
 &nbsp; <strong>Vaccination Rate</strong> <br>
 &nbsp; Less than 50% &nbsp; <i class="fa fa-circle" style="color:red"></i><br>
 &nbsp; 50% to 80% &nbsp; <i class="fa fa-circle" style="color:orange"></i><br>
 &nbsp; More than 80% &nbsp; <i class="fa fa-circle" style="color:green"></i><br>
  </div>
 """

m.get_root().html.add_child(folium.Element(legend_html))

folium.LayerControl().add_to(m)

# Choose the location where you want the popup to appear
popup_location = [52, 13]  # Replace with actual coordinates


# Save the map as an HTML file
m.save('de_covidmap.html')
