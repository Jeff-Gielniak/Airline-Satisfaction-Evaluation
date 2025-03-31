# Import Libraries
import pandas as pd
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, LabelSet, Select, BoxAnnotation
from bokeh.layouts import column, row

# Load and clean dataset
df = pd.read_csv("Resources/2018data.csv")
df.columns = df.columns.str.strip().str.upper()
df = df.dropna(subset=['ORIGIN', 'DEP_DELAY', 'CANCELLED'])

# Add helper columns
df['NUM_FLIGHT'] = 1

# Group and calculate metrics
airport_stats = df.groupby('ORIGIN').agg({
    'DEP_DELAY': [
        lambda x: (x > 15).sum() / len(x) * 100,  # Delay %
        lambda x: x[x > 0].mean()                 # Avg delay (mins)
    ],
    'NUM_FLIGHT': 'sum'
}).reset_index()

# Flatten MultiIndex columns
airport_stats.columns = ['ORIGIN', 'Delay_Percentage', 'Avg_Delay', 'Num_Flights']

# ✅ Restore original dot size logic based on traffic volume
airport_stats['Size'] = (airport_stats['Num_Flights'] / airport_stats['Num_Flights'].max()) * 40 + 5

# Create ColumnDataSource
full_source = ColumnDataSource(airport_stats)
source = ColumnDataSource(airport_stats)

# Create figure
p = figure(
    title="Airport Reliability: Avg Delay vs Delay %",
    x_axis_label="Average Delay (Minutes)",
    y_axis_label="Delay Percentage (%)",
    height=700,
    width=1000,
    tools="pan,wheel_zoom,box_zoom,reset"
)

# Style title
p.title.text_font_size = '16pt'
p.title.align = 'center'

# Add quadrant overlays
x_mid = 40
y_mid = 20
p.add_layout(BoxAnnotation(right=x_mid, top=y_mid, fill_alpha=0.1, fill_color='green'))    # Bottom Left
p.add_layout(BoxAnnotation(left=x_mid, top=y_mid, fill_alpha=0.1, fill_color='yellow'))   # Bottom Right
p.add_layout(BoxAnnotation(right=x_mid, bottom=y_mid, fill_alpha=0.1, fill_color='orange'))  # Top Left
p.add_layout(BoxAnnotation(left=x_mid, bottom=y_mid, fill_alpha=0.1, fill_color='red'))   # Top Right

# Plot bubbles
p.scatter(x='Avg_Delay', y='Delay_Percentage', size='Size', source=source,
          fill_alpha=0.6, line_color='black', fill_color='steelblue')

# Add airport labels
labels = LabelSet(x='Avg_Delay', y='Delay_Percentage', text='ORIGIN',
                  source=source, x_offset=5, y_offset=0,
                  text_align='left', text_baseline='middle',
                  text_font_size='9pt')
p.add_layout(labels)

# Hover tooltip
hover = HoverTool(tooltips=[
    ("Airport", "@ORIGIN"),
    ("Avg Delay (min)", "@Avg_Delay{0.0}"),
    ("% Delayed", "@Delay_Percentage{0.0}%"),
    ("Flights", "@Num_Flights")
])
p.add_tools(hover)

# Dropdowns
airport_options = ['All'] + sorted(airport_stats['ORIGIN'].unique().tolist())
airport_dropdown = Select(title="Select Airport", value='All', options=airport_options)

top_n_options = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', 'All']
top_n_dropdown = Select(title="Show Top N Airports by Traffic", value='30', options=top_n_options)

# Update function
def update_source(attr, old, new):
    top_n = top_n_dropdown.value
    selected_airport = airport_dropdown.value

    if top_n == 'All':
        filtered_df = airport_stats.copy()
    else:
        filtered_df = airport_stats.sort_values(by='Num_Flights', ascending=False).head(int(top_n))

    if selected_airport != 'All':
        filtered_df['Alpha'] = filtered_df['ORIGIN'].apply(lambda x: 1.0 if x == selected_airport else 0.2)
        fill_color = ['steelblue' if a == 1.0 else 'lightgray' for a in filtered_df['Alpha']]
    else:
        filtered_df['Alpha'] = 0.9
        fill_color = ['steelblue'] * len(filtered_df)

    new_data = ColumnDataSource.from_df(filtered_df)
    new_data['fill_color'] = fill_color
    source.data = new_data

# Attach dropdown listeners
airport_dropdown.on_change('value', update_source)
top_n_dropdown.on_change('value', update_source)

# Initial load
update_source(None, None, None)

# Layout
curdoc().add_root(column(row(top_n_dropdown, airport_dropdown), p))



# bokeh serve --show airport_reliability_plot.py
