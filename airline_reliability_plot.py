#Import Libraries
import pandas as pd

#Load Your Dataset
# Update the path once you have the real file
# Example: df = pd.read_csv('cleaned_flight_data.csv')
df = pd.read_csv("Resources/2018data.csv")

#Preprocess the Data
def preprocess_flight_data(df):
    # Convert FL_DATE column to datetime
    df["FL_DATE"] = pd.to_datetime(df["FL_DATE"])

    # Extract Month and Day of Week from the date
    df["MONTH"] = df["FL_DATE"].dt.month
    df["DAY_OF_WEEK"] = df["FL_DATE"].dt.day_name()

    # Fill missing DEP_DELAY values with 0 
    df["DEP_DELAY"] = df["DEP_DELAY"].fillna(0) 

    # Create a new column to flag if a flight was delayed (only if delay is > 0)
    df["IS_DELAYED"] = df["DEP_DELAY"] > 0

    # CANCELLED is already binary — no changes needed

    return df


#Reliability Calculation
def compute_reliability(df, group_col):
    summary = df.groupby(group_col).agg(
        Total_Flights=('FL_DATE', 'count'),
        Num_Delayed=('IS_DELAYED', 'sum'),
        Num_Cancelled=('CANCELLED', 'sum') 
    ).reset_index()

    summary["Delay_Percent"] = (summary["Num_Delayed"] / summary["Total_Flights"] * 100).round(2)
    summary["Cancellation_Percent"] = (summary["Num_Cancelled"] / summary["Total_Flights"] * 100).round(2)

    return summary.sort_values("Total_Flights", ascending=False)

#Run analysis only if the DataFrame isn't empty
if not df.empty:
    # Preprocess the data (adds month, weekday, delay flags)
    df = preprocess_flight_data(df)

    # Run reliability metrics
    by_carrier = compute_reliability(df, "OP_CARRIER")  
    by_month = compute_reliability(df, "MONTH")
    by_day = compute_reliability(df, "DAY_OF_WEEK")
    by_origin = compute_reliability(df, "ORIGIN")

    # Print samples for now
    print("Delay & Cancellation by Carrier:\n", by_carrier.head(), "\n")
    print("Delay & Cancellation by Month:\n", by_month.head(), "\n")
    print("Delay & Cancellation by Day of Week:\n", by_day.head(), "\n")
    print("Delay & Cancellation by Origin Airport:\n", by_origin.head(), "\n")
else:
    print("No data loaded yet. Please load your dataset in Step 1.")


# Drop rows with missing delay values
df_valid = df.dropna(subset=["DEP_DELAY", "ARR_DELAY"]).copy()

# Filter to flights that departed late
df_late = df_valid[df_valid["DEP_DELAY"] > 0].copy()

# Calculate time made up
df_late["TIME_MADE_UP"] = df_late["DEP_DELAY"] - df_late["ARR_DELAY"]

# remove extreme outliers
df_late = df_late[(df_late["TIME_MADE_UP"] >= 0) & (df_late["TIME_MADE_UP"] <= df_late["DEP_DELAY"])]

# Now group
by_carrier_makeup = df_late.groupby("OP_CARRIER").agg(
    Num_Late_Flights=('DEP_DELAY', 'count'),
    Avg_DEP_Delay=('DEP_DELAY', 'mean'),
    Avg_ARR_Delay=('ARR_DELAY', 'mean'),
    Avg_Minutes_Made_Up=('TIME_MADE_UP', 'mean')
).reset_index()

# Add group-level percentage column
by_carrier_makeup["Avg_Percent_Delay_Made_Up"] = (
    by_carrier_makeup["Avg_Minutes_Made_Up"] / by_carrier_makeup["Avg_DEP_Delay"]
)


# Visualizations
from sklearn.preprocessing import MinMaxScaler
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Select, LabelSet, NumeralTickFormatter
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.transform import factor_cmap  # still needed if you want to color points by airline later

# Normalize bubble size
scaler = MinMaxScaler(feature_range=(10, 40))
by_carrier["Size"] = scaler.fit_transform(by_carrier[["Total_Flights"]])

# Initial transparency column
by_carrier["alpha"] = 0.9  # Default for all points

# Data sources
source = ColumnDataSource(by_carrier)
filtered_source = ColumnDataSource(by_carrier.copy())

# Dropdown menu
dropdown = Select(title="Select Airline", value="All", options=["All"] + sorted(by_carrier["OP_CARRIER"].unique()))

# Plot setup
p = figure(
    title="Airline Reliability: Delay % vs Cancellation %",
    x_axis_label="Cancellation Percentage (%)",
    y_axis_label="Delay Percentage (%)",
    tools="pan,wheel_zoom,box_zoom,reset",
    height=700,
    width=1000,
    x_range=(0, 6),
    y_range=(20, 55)
)

# Style Title
p.title.align = "center"
p.title.text_font_size = "16pt"
p.title.text_font_style = "bold"

# Format ticks 
p.xaxis.formatter = NumeralTickFormatter(format="0.0")
p.yaxis.formatter = NumeralTickFormatter(format="0.0")

# Draw scatter plot 
scatter = p.scatter(
    x="Cancellation_Percent",
    y="Delay_Percent",
    size="Size",
    source=filtered_source,
    fill_alpha="alpha",  
    line_color="black",
    color="steelblue"
)

# Add labels
labels = LabelSet(
    x="Cancellation_Percent",
    y="Delay_Percent",
    text="OP_CARRIER",
    source=filtered_source,
    x_offset=5,
    y_offset=5,
    text_font_size="10pt",
    text_color="black"
)
p.add_layout(labels)

# Add hover tool 
hover = HoverTool(renderers=[scatter], tooltips=[
    ("Airline", "@OP_CARRIER"),
    ("Total Flights", "@Total_Flights{0,0}"),
    ("# Delayed", "@Num_Delayed{0,0}"),
    ("# Cancelled", "@Num_Cancelled{0,0}"),
    ("Delay %", "@Delay_Percent{0.0}"),
    ("Cancel %", "@Cancellation_Percent{0.0}")
])
p.add_tools(hover)

# Dropdown logic
def update_plot(attr, old, new):
    selected = dropdown.value
    data = by_carrier.copy()
    if selected != "All":
        data["alpha"] = data["OP_CARRIER"].apply(lambda x: 1.0 if x == selected else 0.1)
    else:
        data["alpha"] = 0.9
    filtered_source.data = dict(ColumnDataSource(data).data)

dropdown.on_change("value", update_plot)


# Poor performance (red zone)
p.quad(left=0, right=6, bottom=0, top=55, 
       fill_color="red", fill_alpha=0.15, line_alpha=0)

# Average performance (yellow zone)
p.quad(left=0, right=3.5, bottom=0, top=42, 
       fill_color="yellow", fill_alpha=0.15, line_alpha=0)

# Good performance (green zone)
p.quad(left=0, right=1.5, bottom=20, top=32, 
       fill_color="green", fill_alpha=0.15, line_alpha=0)


# Add to Bokeh app
curdoc().add_root(column(dropdown, p))
curdoc().title = "Airline Reliability"

# bokeh serve airline_reliability_plot.py --show
