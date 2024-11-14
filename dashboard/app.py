from ipyleaflet import Map, Marker, Polyline, TileLayer, basemaps
from faicons import icon_svg
from geopy.distance import geodesic, great_circle
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_widget

# Define sample city data (CITIES) and BASEMAPS
CITIES = {
    "Louisiana": {"latitude": 30.9843, "longitude": -91.9623, "altitude": 10},
    "Missouri": {"latitude": 38.5739, "longitude": -92.6038, "altitude": 214},
    "Ross Sea (Adélie Penguins)": {"latitude": -77.5, "longitude": 163.5, "altitude": 0},
    "Antarctic Peninsula (Adélie Penguins)": {"latitude": -64.0, "longitude": -60.0, "altitude": 0},
    "South Shetland Islands (Chinstrap Penguins)": {"latitude": -62.0, "longitude": -58.0, "altitude": 0},
    "Antarctic Peninsula (Chinstrap Penguins)": {"latitude": -63.0, "longitude": -57.0, "altitude": 0},
    "Falkland Islands (Gentoo Penguins)": {"latitude": -51.7, "longitude": -59.0, "altitude": 0},
    "South Georgia (Gentoo Penguins)": {"latitude": -54.5, "longitude": -36.0, "altitude": 0},
}

BASEMAPS = {
    "WorldImagery": basemaps.Esri.WorldImagery,
    "Mapnik": basemaps.OpenStreetMap.Mapnik,
}

# Define penguin colonies data
penguin_colonies = {
    "Adélie Penguins": [("Ross Sea", -77.5, 163.5), ("Antarctic Peninsula", -64.0, -60.0)],
    "Chinstrap Penguins": [("South Shetland Islands", -62.0, -58.0), ("Antarctic Peninsula", -63.0, -57.0)],
    "Gentoo Penguins": [("Falkland Islands", -51.7, -59.0), ("South Georgia", -54.5, -36.0)],
}

# Flatten colony names for user selection
colony_names = [f"{species} - {colony[0]}" for species, colonies in penguin_colonies.items() for colony in colonies]
city_names = sorted(list(CITIES.keys()))

ui.page_opts(title="Location and Penguin Colony Distance Calculator", fillable=True)

with ui.sidebar():
    ui.input_selectize("loc1", "Location 1", choices=city_names, selected="New York")
    ui.input_selectize("loc2", "Location 2", choices=city_names, selected="London")
    ui.input_selectize("penguin_colony", "Penguin Colony", choices=colony_names, selected=colony_names[0])
    ui.input_selectize("basemap", "Choose a basemap", choices=list(BASEMAPS.keys()), selected="WorldImagery")
    ui.input_dark_mode(mode="dark")

with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("globe"), theme="gradient-blue-indigo"):
        "Great Circle Distance"
        @render.text
        def great_circle_dist():
            circle = great_circle(loc1xy(), loc2xy())
            return f"{circle.kilometers.__round__(1)} km"

    with ui.value_box(showcase=icon_svg("ruler"), theme="gradient-blue-indigo"):
        "Geodesic Distance"
        @render.text
        def geo_dist():
            dist = geodesic(loc1xy(), loc2xy())
            return f"{dist.kilometers.__round__(1)} km"

    with ui.value_box(showcase=icon_svg("snowflake"), theme="gradient-blue-indigo"):
        "Distance to Penguin Colony"
        @render.text
        def penguin_dist():
            selected_colony = input.penguin_colony().split(" - ")
            species = selected_colony[0]
            colony_name = selected_colony[1]
            for colony in penguin_colonies[species]:
                if colony[0] == colony_name:
                    colony_location = (colony[1], colony[2])
                    break
            distance = geodesic(loc1xy(), colony_location).kilometers
            return f"{distance.__round__(1)} km to {colony_name} ({species})"

with ui.card():
    ui.card_header("Map (drag the markers to change locations)")
    @render_widget
    def map():
        return Map(zoom=4, center=(0, 0))

# Reactive values to store location information
loc1 = reactive.value()
loc2 = reactive.value()

@reactive.effect
def _():
    loc1.set(CITIES.get(input.loc1(), loc_str_to_coords(input.loc1())))
    loc2.set(CITIES.get(input.loc2(), loc_str_to_coords(input.loc2())))

# Helper function to convert location strings to coordinates
def loc_str_to_coords(x: str) -> dict:
    latlon = x.split(", ")
    if len(latlon) != 2:
        return {}
    lat, lon = map(float, latlon)
    return {"latitude": lat, "longitude": lon, "altitude": None}

@reactive.calc
def loc1xy():
    return loc1()["latitude"], loc1()["longitude"]

@reactive.calc
def loc2xy():
    return loc2()["latitude"], loc2()["longitude"]

@reactive.effect
def _():
    update_marker(map.widget, loc1xy(), on_move1, "loc1")

@reactive.effect
def _():
    update_marker(map.widget, loc2xy(), on_move2, "loc2")

@reactive.effect
def _():
    update_line(map.widget, loc1xy(), loc2xy())

@reactive.effect
def _():
    l1 = loc1xy()
    l2 = loc2xy()
    lat_rng = [min(l1[0], l2[0]), max(l1[0], l2[0])]
    lon_rng = [min(l1[1], l2[1]), max(l1[1], l2[1])]
    new_bounds = [[lat_rng[0], lon_rng[0]], [lat_rng[1], lon_rng[1]]]
    b = map.widget.bounds
    if len(b) == 0:
        map.widget.fit_bounds(new_bounds)
    elif (lat_rng[0] < b[0][0] or lat_rng[1] > b[1][0] or lon_rng[0] < b[0][1] or lon_rng[1] > b[1][1]):
        map.widget.fit_bounds(new_bounds)

@reactive.effect
def _():
    update_basemap(map.widget, input.basemap())

# Map helper functions
def update_marker(map: Map, loc: tuple, on_move: object, name: str):
    remove_layer(map, name)
    m = Marker(location=loc, draggable=True, name=name)
    m.on_move(on_move)
    map.add_layer(m)

def update_line(map: Map, loc1: tuple, loc2: tuple):
    remove_layer(map, "line")
    map.add_layer(Polyline(locations=[loc1, loc2], color="blue", weight=2, name="line"))

def update_basemap(map: Map, basemap: str):
    for layer in map.layers:
        if isinstance(layer, TileLayer):
            map.remove_layer(layer)
    map.add_layer((BASEMAPS[input.basemap()]))

def remove_layer(map: Map, name: str):
    for layer in map.layers:
        if layer.name == name:
            map.remove_layer(layer)

def on_move1(**kwargs):
    return on_move("loc1", **kwargs)

def on_move2(**kwargs):
    return on_move("loc2", **kwargs)

def on_move(id, **kwargs):
    loc = kwargs["location"]
    loc_str = f"{loc[0]}, {loc[1]}"
    choices = city_names + [loc_str]
    ui.update_selectize(id, selected=loc_str, choices=choices)
