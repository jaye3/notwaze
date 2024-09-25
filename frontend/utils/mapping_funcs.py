from streamlit_folium import st_folium as folium
from folium.plugins import PolyLineTextPath
import pandas as pd
from shapely.geometry import Point

def add_markers(gdf):
  # Add POIs to the map

  # Dictionary for Icons, by type of structures
  icon_dict = {
      'Museum': 'university',
      'Historic Site': 'landmark',
      'Monument': 'monument',
      'Park': 'tree',
      'Toilet': 'toilet',
      'Drinking Water': 'tint'
  }

  # Dictionary for Colours, by type of structures
  color_dict = {
      'Museum': 'red',
      'Historic Site': 'orange',
      'Monument': 'purple',
      'Park': 'green',
      'Toilet': 'cadetblue',
      'Drinking Water': 'blue'
  }

  # For each poi, generate a marker and add to map
  for idx, row in gdf.iterrows():
      popup_content = f"<div style='text-align: center;'><strong>{row['NAME']}</strong><br>"

      if 'PHOTOURL' in gdf.columns and pd.notna(row['PHOTOURL']):
          popup_content += f"<img src='{row['PHOTOURL']}' style='width: 100px; height: 100px; display: block; margin: 0 auto;'><br>"

      if 'DESCRIPTION' in gdf.columns and pd.notna(row['DESCRIPTION']):
          popup_content += f"{row['DESCRIPTION']}<br>"

      popup_content += "</div>"

      folium.Marker(
          [row.geometry.y, row.geometry.x],
          popup=folium.Popup(popup_content, max_width=250),
          icon=folium.Icon(icon=icon_dict[row['TYPE']], prefix='fa', color=color_dict[row['TYPE']])
      ).add_to(m)

def add_route_lines(route_geometries):
  # add route lines to the map

  # colours for routes
  colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

  # for each route, generate a line + arrows and add to map
  for i, route_geometry in enumerate(route_geometries):
      # Convert LineString to list of coordinate pairs
      locations = [(lat, lon) for lon, lat in route_geometry.coords]

      # Use a different color for each route
      color = colors[i % len(colors)]
      polyline = folium.PolyLine(locations=locations, color='blue', weight=2, opacity=1, tooltip=f'Route {i+1}')
      polyline.add_to(m)

      # Add arrows to the polyline
      arrows = PolyLineTextPath(
          polyline,
          '➤',  # Arrow symbol
          repeat=True,
          offset=12,
          attributes={'fill': color, 'font-weight': 'bold', 'font-size': '12'}
      )
      m.add_child(arrows)




