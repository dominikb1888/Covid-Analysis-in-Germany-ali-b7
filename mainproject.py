import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
import ipywidgets as widgets
from ipywidgets import interactive

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
               ).add_to(marker_cluster)


# Function to update GeoJSON layer based on the filter
# Function to update GeoJSON layer based on the filter
def update_map(cases_threshold):
    filtered_data = merged_data[merged_data['Covid Cases'] >= cases_threshold]
    
    # Remove previous Choropleth layer
    for layer in m._children.values():
        if isinstance(layer, folium.Choropleth):
            m.remove_layer(layer)
    
    # Add a new Choropleth layer with the filtered data
    folium.Choropleth(geo_data=filtered_data,
                      name='Filtered Covid Data',
                      data=filtered_data,
                      columns=['Bundesland', 'Total Deaths'],
                      key_on='feature.properties.Bundesland',
                      fill_color='YlOrRd',
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      legend_name='Deaths',
                      highlight=True,
                     ).add_to(m)

# Create an interactive slider for filtering COVID cases
cases_slider = widgets.FloatSlider(value=0, min=0, max=500000, step=10000, description='Min COVID Cases:')
widget = interactive(update_map, cases_threshold=cases_slider)
widget.children[-1].layout.height = 'auto'  # Adjusting the height for better visibility
display(widget)


# adding data as markers
for idx, row in merged_data.iterrows():
    # Choose marker color based on Covid Cases
    if row['Covid Cases'] < 200000:
        marker_color = 'green'  # Low cases
    elif 200000 <= row['Covid Cases'] < 900000:
        marker_color = 'blue'  # Moderate cases
    else:
        marker_color = 'red'  # High cases

    folium.Marker(location=[row.geometry.centroid.y, row.geometry.centroid.x],
                  popup=f"<strong>{row['GEN']}</strong><br>Population: {row['Population']}<br>Vaccination Rate: {row['Vaccination Rate']}<br>Covid Cases: {row['Covid Cases']}<br>Total Deaths: {row['Total Deaths']}",
                  icon=folium.Icon(color=marker_color),
                  ).add_to(marker_cluster)
    
    
  # Add Legend 
    legend_html = """
        <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 160px; height: 150px; 
                 border:2px solid grey; z-index:9999; font-size:12px;
                 background-color: white;
                 ">
     &nbsp; <strong>Legend</strong> <br>
     &nbsp; Low COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:blue"></i> (< 50,000)<br>
     &nbsp; Moderate COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:green"></i> (100,000 - 500,000)<br>
     &nbsp; High COVID Cases &nbsp; <i class="fa fa-map-marker fa-1x" style="color:red"></i> (> 500,000)
      </div>
     """

m.get_root().html.add_child(folium.Element(legend_html))

# Create a HeatMap layer using the location coordinates and intensity (e.g., COVID cases)
heat_data = [[point.xy[1][0], point.xy[0][0], row['Covid Cases']] for idx, row in merged_data.iterrows() for point in [row.geometry.centroid]]
HeatMap(heat_data, name='Heatmap', radius=25, blur=20, gradient={0.3: '#FFD700', 0.5: '#FF4500', 1: '#8B0000'}).add_to(m)

# Add Layer Control to toggle layers
folium.LayerControl().add_to(m)

# Save the map as an HTML file
m.save('de_covidmapfinal_filtered.html')
