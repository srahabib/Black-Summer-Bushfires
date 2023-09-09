import plotly.express as px
import pandas as pd

df = pd.read_csv("G:\\NASA\\fire_nrt_V1_101674.csv")

# Rename the "acq_date" column to "date"
df.rename(columns={"acq_date": "date"}, inplace=True)

# Set the latitude and longitude boundaries for New South Wales
nsw_bounds = [141, -37.5, 153.5, -28.1]  # [min_longitude, min_latitude, max_longitude, max_latitude]

# Filter the DataFrame to include only data within the New South Wales boundaries and the specified date range
start_date = "2019-09-01"
end_date = "2020-01-31"
df_nsw = df[(df["longitude"] >= nsw_bounds[0]) &
            (df["longitude"] <= nsw_bounds[2]) &
            (df["latitude"] >= nsw_bounds[1]) &
            (df["latitude"] <= nsw_bounds[3]) &
            (df["date"] >= start_date) &
            (df["date"] <= end_date)]

# Create the heatmap using Plotly Express with a slider component for the timeline
fig = px.density_mapbox(
    df_nsw,
    lat="latitude",
    lon="longitude",
    z="bright_ti4",
    color_continuous_scale="YlOrRd",  # Orange color scale
    radius=10,
    zoom=7,
    center={"lat": -32.5, "lon": 147},
    animation_frame="date",  # Use the "date" column for animation frames
    title="Fires/Heat Signatures Timeline: Sep 2019 to Jan 2020"
)

fig.update_traces(zauto=False, zmin=0, zmax=4000)  # Update the color scale range as needed
fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(title="Fire Intensity",tickvals=[])  # Update the color scale title
)

fig.show()