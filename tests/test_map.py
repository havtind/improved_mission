"""test_map.py"""

import folium
import pandas as pd
from folium.plugins import FastMarkerCluster
 

def test_folium_map():
    """ ensure that the Folium plugin is able to create a map."""

    file_path = "data/45784.csv"
    df = pd.read_csv(file_path)
    tmp_lat, tmp_lng = 41.9028, 12.4964
    my_map = folium.Map(location=[tmp_lat, tmp_lng], zoom_start=5)

    # using FastMarkerCluster because faster when about 100k markers.
    my_map.add_child(FastMarkerCluster(df[['latitude', 'longitude']].values.tolist()))

    assert isinstance(my_map, folium.folium.Map), "Map creation failed"

 