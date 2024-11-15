import plotly.express as px
import palmerpenguins
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly, render_widget
from geopy.distance import geodesic, great_circle
from ipyleaflet import Map, basemaps, Marker, TileLayer, Polyline, basemap_to_tiles

# Sample city and BASEMAP data
CITIES = {
    "Louisiana": {"latitude": 30.9843, "longitude": -91.9623, "altitude": 10},
    "Missouri": {"latitude": 38.5739, "longitude": -92.6038, "altitude": 214},
    "New York": {"latitude": 40.7128, "longitude": -74.0060, "altitude": 33},
    "Biscoe Island": {"latitude": -66.5432, "longitude": -67.6667, "altitude": 0},
    "Dream Island": {"latitude": -64.7333, "longitude": -64.2333, "altitude": 0},
    "Torgersen Island": {"latitude": -64.7667, "longitude": -64.0833, "altitude": 0},
}

penguin_colonies = {
    "Adélie Penguins": [("Ross Sea", -77.5, 163.5), ("Antarctic Peninsula", -64.0, -60.0)],
    "Chinstrap Penguins": [("South Shetland Islands", -62.0, -58.0), ("Antarctic Peninsula", -63.0, -57.0)],
    "Gentoo Penguins": [("Falkland Islands", -51.7, -59.0), ("South Georgia", -54.5, -36.0)],
}

BASEMAPS = {
    "WorldImagery": basemaps.Esri.WorldImagery,
    "Mapnik": basemaps.OpenStreetMap.Mapnik,
}

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# UI Setup
ui.page_opts(title="Map and Penguin Dataset Exploration", fillable=True)

with ui.sidebar(bg="#333", style="color: #fff;"):
    # Centered header instructions
    ui.div("Select a penguin species from the list provided and choose destinations for locations 1 and 2 to customize The Interactive Map application.",
           style="text-align:center; padding:10px; font-weight:bold; color:#ffffff;"),
    ui.input_selectize("loc1", "Location 1", choices=list(CITIES.keys()), selected="Louisiana")
    ui.input_selectize("loc2", "Location 2", choices=list(CITIES.keys()), selected="Biscoe Island")
    ui.input_selectize("basemap", "Choose a basemap", choices=list(BASEMAPS.keys()), selected="WorldImagery")
    ui.div("For an interactive exploration of Antarctic penguins, choose the attributes of the penguin and consult the panel's plots and histograms to visualize how your selection is represented.",
           style="text-align:center; padding:10px; font-weight:bold; color:#ffffff;"),
    ui.input_selectize("selected_species_list", "Select Species", ["Adelie", "Gentoo", "Chinstrap"], multiple=True)
    ui.input_selectize("selected_island_list", "Select Island", ["Biscoe", "Dream", "Torgersen"], multiple=True)
    ui.input_slider("flipper_length_mm", "Flipper length (mm)", 150, 250, (150, 250))
    ui.input_slider("bill_depth_mm", "Bill depth (mm)", 13, 21, (13, 21))
    ui.input_slider("bill_length_mm", "Bill length (mm)", 30, 60, (30, 60))
    ui.input_slider("body_mass_g", "Body mass (g)", 2500, 6500, (2500, 6500))
    ui.input_selectize("sex", "Select Sex", ["Male", "Female"])

with ui.navset_card_underline():
    with ui.nav_panel("Map"):
        with ui.card(style="background-color: #222; color: #fff;"):
            ui.card_header("Map (drag the markers to change locations)")
            @render_widget
            def map_widget():
                return create_map()

    with ui.nav_panel("Filtered Table"):
        @render.table
        def filtered_table():
            return filtered_data()

    with ui.nav_panel("Histogram"):
        @render_plotly
        def plotly_histogram():
            filtered_df = filtered_data()
            return px.histogram(filtered_df, x="flipper_length_mm", color="species", title="Flipper Length Histogram")

    with ui.nav_panel("Scatterplot"):
        @render_plotly
        def plotly_scatterplot():
            filtered_df = filtered_data()
            return px.scatter(filtered_df, x="flipper_length_mm", y="bill_length_mm", color="species", title="Flipper Length vs. Bill Length")

    with ui.nav_panel("Seaborn Histogram"):
        @render.plot
        def seaborn_histogram():
            filtered_df = filtered_data()
            fig, ax = plt.subplots()
            sns.histplot(data=filtered_df, x="body_mass_g", hue="species", multiple="stack", ax=ax)
            ax.set_title("Body Mass Distribution (Seaborn)")
            ax.set_xlabel("Body Mass (g)")
            ax.set_ylabel("Count")
            return fig

@reactive.Calc
def filtered_data():
    data = penguins_df.copy()
    if input.selected_species_list():
        data = data[data['species'].isin(input.selected_species_list())]
    if input.selected_island_list():
        data = data[data['island'].isin(input.selected_island_list())]
    flipper_length = input.flipper_length_mm
    if isinstance(flipper_length, list) and len(flipper_length) == 2:
        data = data[(data['flipper_length_mm'] >= flipper_length[0]) & (data['flipper_length_mm'] <= flipper_length[1])]
    return data

def create_map():
    map_obj = Map(zoom=4, center=(0, 0))
    update_marker(map_obj, CITIES[input.loc1()], on_move1, "loc1")
    update_marker(map_obj, CITIES[input.loc2()], on_move2, "loc2")
    update_line(map_obj, CITIES[input.loc1()], CITIES[input.loc2()])
    map_obj.add_layer(basemap_to_tiles(BASEMAPS[input.basemap()]))
    return map_obj

def update_marker(map_obj, loc, on_move, name):
    marker = Marker(location=(loc["latitude"], loc["longitude"]), draggable=True, name=name)
    marker.on_move(on_move)
    map_obj.add_layer(marker)

def update_line(map_obj, loc1, loc2):
    line = Polyline(locations=[(loc1["latitude"], loc1["longitude"]), (loc2["latitude"], loc2["longitude"])], color="blue", weight=2, name="line")
    map_obj.add_layer(line)

def on_move1(event):
    new_loc = event["location"]
    CITIES["loc1"]["latitude"], CITIES["loc1"]["longitude"] = new_loc

def on_move2(event):
    new_loc = event["location"]
    CITIES["loc2"]["latitude"], CITIES["loc2"]["longitude"] = new_loc
