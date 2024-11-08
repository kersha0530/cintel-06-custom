import requests
from shiny import reactive, render
from shiny.express import input
from shiny.express import ui
import pandas as pd
import os
import matplotlib.pyplot as plt

# Import external CSS for Font Awesome icons
ui.tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css")

# Load the CSV file
file_path = "https://github.com/kersha0530/cintel-06-custom/blob/main/exercise.csv"
if os.path.exists(file_path):
    exercise_data = pd.read_csv(file_path)
else:
    exercise_data = pd.DataFrame()

if exercise_data.empty:
    print("The exercise data is empty. Please check the file path or file contents.")
else:
    print("The exercise data has been successfully loaded.")

# Set page options
ui.page_opts(title="Kersha's Fitness App", fillable=True)

# Add CSS for styling
ui.tags.style("""
    body {
        background-color: lavender;
        font-family: 'Roboto', sans-serif;
        color: #4B0082;
    }
    h2, p {
        font-weight: bold;
        color: #4B0082;
    }
    .center-img {
        display: block;
        margin: auto;
        width: 150px;
    }
    .text-center {
        text-align: center;
    }
    .slider, select, .shiny-input {
        width: 100%;
        color: #4B0082;
        font-weight: bold;
    }
    .slider-label {
        color: #4B0082;
        font-weight: bold;
    }
    .links a {
        color: #4B0082;
        font-weight: bold;
        display: block;
        margin-bottom: 10px;
    }
    .plot-image {
        width: 100%;
        max-width: 800px;
        height: auto;
        display: block;
        margin: auto;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
""")

# Sidebar content
with ui.sidebar(open="open"):
    ui.h2("Kersha's Fitness App", class_="text-center")
    ui.div(
        ui.HTML("""
            <iframe src="https://d1csarkz8obe9u.cloudfront.net/index.php/posterbuilder/view/06717d7c5b2c186c75c84073b19caed0/1" 
                    style="height: 150px; width:100%; border:none;"></iframe>
        """),
        class_="center-img"
    )
    ui.div(ui.input_slider("time", "Select Time Interval", min=1, max=30, value=15, step=1, animate=True), class_="bold")
    ui.div(ui.input_select("diet", "Select Diet", choices=["Lowfat", "No Fat"]), class_="bold")
    ui.div(ui.input_select("kind", "Select Exercise Type", choices=["Rest", "Walking", "Running"]), class_="bold")
    ui.div(
        ui.h6("Links:", class_="bold"),
        ui.a(ui.tags.i(class_="fab fa-github", style="font-size: 1.5em; color: black;"), 
             "GitHub - The Exercise App", href="https://github.com/your-repository-link", target="_blank"),
        ui.a(ui.tags.i(class_="fas fa-shield-alt", style="font-size: 1.5em; color: darkblue;"), 
             "PyShiny Documentation", href="https://shiny.posit.co/py/", target="_blank"),
        class_="links"
    )
ui.h2("Personalize Your Fitness Metrics", class_="text-center")
# Icons for visual interest
ui.div(
    # Blue Dumbbell
    ui.tags.i(class_="fas fa-dumbbell text-center", style="font-size: 8em; color: blue;"),
    # Green Running Icon
    ui.tags.i(class_="fas fa-running text-center", style="font-size: 8em; color: green;"),
    # Red Heartbeat Icon
    ui.tags.i(class_="fas fa-heartbeat text-center", style="font-size: 8em; color: red;"),
    # Purple Dumbbell Icon (added here)
    ui.tags.i(class_="fas fa-dumbbell text-center", style="font-size: 8em; color: purple;"),
    # Additional icons if needed (you can add more icons similarly)
    ui.tags.i(class_="fas fa-bicycle text-center", style="font-size: 8em; color: orange;"),
    class_="d-flex justify-content-around"  # Using flexbox to ensure icons are spaced and aligned
)


# Instructions
ui.p("Select the desired options to view exercise data and trends.", class_="text-center")

# Function to plot exercise data
def plot_exercise_data(filtered_data, kind):
    plt.figure(figsize=(10, 5))
    if kind == "Running":
        plt.plot(filtered_data["time"], filtered_data["time"], marker='o', label="Exercise Time (Running)")
    else:
        plt.plot(filtered_data["time"], filtered_data["time"], marker='o', label=f"Exercise Time ({kind})")
    plt.title(f'{kind} Exercise Trends')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Time (minutes)')
    plt.grid()
    plt.tight_layout()
    plot_path = 'C:/Users/kbrou/OneDrive/Pictures/exercise_plot.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Reactive function to update data based on selections
@reactive.calc
def reactive_calc():
    time_range = input.slider("time")  # Directly access the slider value
    kind = input.select("kind")  # Directly access the select value
    filtered_data = exercise_data[exercise_data['time'] <= time_range]
    selected_data = filtered_data[filtered_data['kind'] == kind]
    return plot_exercise_data(selected_data, kind)


# New: Calculate calories burned (simplified)
@reactive.calc
def calories_burned():
    time_range = input.slider("time")  # Directly access the slider value
    kind = input.select("kind")  # Directly access the select value

    # Simplified formula: calories burned = time * calories per minute based on exercise type
    if kind == "Running":
        calories_per_minute = 10  # Example value for running
    elif kind == "Walking":
        calories_per_minute = 5  # Example value for walking
    else:
        calories_per_minute = 0  # No calories burned during rest
    
    total_calories = time_range * calories_per_minute
    return f"Calories Burned: {total_calories} kcal"

# New: Calculate heart rate (simplified)
@reactive.calc
def heart_rate():
    kind = input.select("kind")  # Directly access the select value
    
    # Example heart rate logic based on exercise type
    if kind == "Running":
        hr = 150  # Average heart rate for running
    elif kind == "Walking":
        hr = 120  # Average heart rate for walking
    else:
        hr = 80  # Average heart rate for resting
    
    return f"Heart Rate: {hr} bpm"


# Layout with two columns and cards for placeholders (using div and Bootstrap classes)
ui.div(
    ui.div(
        ui.div(
            ui.h3("Placeholder 1", class_="text-center"),
            ui.p("This is a placeholder for the first content card."),
            class_="card"
        ),
        class_="col-6"  # Bootstrap column for half-width
    ),
    ui.div(
        ui.div(
            ui.h3("Placeholder 2", class_="text-center"),
            ui.p("This is a placeholder for the second content card."),
            class_="card"
        ),
        class_="col-6"  # Bootstrap column for half-width
    ),
    class_="row"  # Bootstrap row class to align columns horizontally
)
