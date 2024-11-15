# cintel-06-custom
## Map and Penguin Dataset Exploration

This interactive Shiny app offers a dual platform for exploring both a map-based location distance calculator and the Palmer Penguins dataset. Users can calculate distances between locations on a map, including penguin colonies, and filter penguin attributes for statistical analysis and visualizations.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Data Dictionary](#data-dictionary)
  - [Map Location Data](#map-location-data)
  - [Penguin Dataset Attributes](#penguin-dataset-attributes)
- [Usage Instructions](#usage-instructions)
  - [Map Application Details](#map-application-details)
  - [Penguin Dataset Exploration](#penguin-dataset-exploration)
- [Customization](#customization)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This application combines map-based distance calculations with interactive data exploration for the Palmer Penguins dataset. Ideal for visualizing geographical and statistical information in one app, it features a professional dark theme for accessibility and user experience.

## Features
- **Interactive Map**: Draggable markers for distance calculations between locations.
- **Penguin Dataset Exploration**: Multiple filters and visualizations for analyzing penguin species data.
- **Dark Theme**: A visually accessible and professional interface.
- **Visualization Options**:
  - Histogram
  - Scatterplot
  - Seaborn Histogram

## Getting Started

### Prerequisites
Ensure you have the following packages installed:

```bash
pip install plotly palmerpenguins pandas matplotlib seaborn shiny shinywidgets geopy ipyleaflet faicons

shiny run app.py


Access the Interface: Open the Shiny app in your browser to start exploring.

# Data Dictionary
* Map Location Data
* The map app includes predefined city locations as well as specific Antarctic penguin colony locations:

* Cities: Louisiana, Missouri, New York, Biscoe Island, Dream Island, Torgersen Island
* Penguin Colonies: Ross Sea (Adélie Penguins), Antarctic Peninsula (Chinstrap Penguins), Falkland Islands (Gentoo Penguins), and more.
  
# Penguin Dataset Attributes
The Palmer Penguins dataset includes:

* Species: Adelie, Chinstrap, Gentoo
* Island: Biscoe, Dream, Torgersen
* Flipper Length (mm): Filter range from 150 to 250 mm
* Bill Depth (mm): Filter range from 13 to 21 mm
* Bill Length (mm): Filter range from 30 to 60 mm
* Body Mass (g): Filter range from 2500 to 6500 g
* Sex: Male or Female
  
# Usage Instructions
* Map Application:
 -Select two locations to calculate distances, either by choosing cities or penguin colony sites. Choose a basemap option to customize the view.
* Penguin Exploration:
  -Set specific attributes in the sidebar to filter penguin data and explore via histograms, scatterplots, and seaborn histograms.
  
# Map Application Details
* City and Penguin Colony Locations
* The map includes a selection of cities and Antarctic penguin colonies for distance calculations.
* Distance Calculations
  
# Calculate and display:

* Great Circle Distance between two locations.
* Geodesic Distance as the shortest path between two points.
* Penguin Colony Distance to the nearest selected colony.
* Basemap Options
* Choose between WorldImagery and Mapnik for different map views.

# Penguin Dataset Exploration
# Explore the filtered Palmer Penguins dataset using the following visualization options:

# Penguin Attributes
Filter by:

* Species, Island, Flipper Length, Bill Depth, Bill Length, Body Mass, and Sex.
# Visualization Options
 The following panels provide insights into penguin data distributions:

* Filtered Table: Displays data based on the filtered criteria.
* Histogram: Plotly histogram of flipper lengths, color-coded by species.
* Scatterplot: Flipper length vs. bill length.
* Seaborn Histogram: Distribution of body mass by species.
# Customization
Modify the CITIES and BASEMAPS dictionaries within the script to update locations and basemap choices.
Adjust visualization and filtering options by changing parameters in the UI.
# Contributing
Contributions are welcome! Please follow standard coding conventions, document any changes, and submit a pull request.

# License
This project is licensed under the MIT License.

### Additional Notes
- **Clickable Links in README**: In Markdown, using `[]()` creates clickable links, as shown in the Table of Contents.
- **Underlining Text**: Markdown does not natively support underlining, so bold (`**text**`) or italic (`*text*`) styling is typically used instead.


