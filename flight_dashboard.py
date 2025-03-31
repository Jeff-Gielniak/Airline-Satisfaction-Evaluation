from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Select, FactorRange, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import column, row
import pandas as pd

# Load dataset
file_path = r"C:\Users\19144\OneDrive\Documents\Analysis Project\Crown funding Analysis\Project 3\project3\Resources\Analysis_complete.csv"
df = pd.read_csv(file_path)
df_filtered = df[["Month", "TravelType", "CabinType", "Avg_OverallScore", "AirlineName"]]

# Map numeric month to 3-character month abbreviations
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
df_filtered.loc[:, 'Month'] = df_filtered['Month'].astype(int)  # Ensure 'Month' is integer

# Aggregate data by Month
monthly_avg = df_filtered.groupby("Month")["Avg_OverallScore"].mean().reset_index()

# Map the Month numbers to month names
monthly_avg['MonthName'] = monthly_avg['Month'].apply(lambda x: month_names[x-1])

# Create a ColumnDataSource with the month names
source = ColumnDataSource(monthly_avg)

# Create figure with factorized x_range for month abbreviations
p = figure(x_range=FactorRange(*month_names), title="Average Ratings by Month",
           x_axis_label="Month", y_axis_label="Avg Overall Score", height=400, width=700)

# Add a HoverTool to display values on hover
hover = HoverTool()
hover.tooltips = [("Month", "@MonthName"), ("Avg Overall Score", "@Avg_OverallScore")]
p.add_tools(hover)

# Update the bars to match the factorized x-axis (using month names)
p.vbar(x='MonthName', top='Avg_OverallScore', width=0.5, source=source)

# Dropdown filters
traveler_select = Select(title="Traveler Type", value="All", options=["All"] + df_filtered["TravelType"].unique().tolist())
cabin_select = Select(title="Cabin Type", value="All", options=["All"] + df_filtered["CabinType"].unique().tolist())
airline_select = Select(title="Airline", value="All", options=["All"] + df_filtered["AirlineName"].unique().tolist())

# Update function
def update():
    filtered_df = df_filtered.copy()
    
    if traveler_select.value != "All":
        filtered_df = filtered_df[filtered_df["TravelType"] == traveler_select.value]
    if cabin_select.value != "All":
        filtered_df = filtered_df[filtered_df["CabinType"] == cabin_select.value]
    if airline_select.value != "All":
        filtered_df = filtered_df[filtered_df["AirlineName"] == airline_select.value]
    
    updated_avg = filtered_df.groupby("Month")["Avg_OverallScore"].mean().reset_index()
    updated_avg['MonthName'] = updated_avg['Month'].apply(lambda x: month_names[x-1])  # Map months again
    source.data = ColumnDataSource.from_df(updated_avg)

# Callbacks
traveler_select.on_change('value', lambda attr, old, new: update())
cabin_select.on_change('value', lambda attr, old, new: update())
airline_select.on_change('value', lambda attr, old, new: update())

# Layout
layout = column(row(traveler_select, cabin_select, airline_select), p)
curdoc().add_root(layout)


##bokeh serve --show flight_dashboard.py

