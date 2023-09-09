from flask import Flask, render_template
import plotly.express as px
import pandas as pd
import json
import plotly
import plotly.express as px

app = Flask(__name__)

#server = app.server

@app.route('/')
def index():

     # Scatter mapbox plot code
    df = pd.read_csv("G:\\Choropleth and Chart Data\\Waterway Data\\data.csv", encoding='latin1')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Date'] = df['Date'] + pd.offsets.DateOffset(years=3)
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
    df = df.sort_values('Date')
    
    start_date = '2019-07-01'
    end_date = '2020-03-31'
    
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    
    def add_minus_sign(x):
        return -x
    
    df['Latitude '] = df['Latitude '].apply(add_minus_sign)
    
    fig = px.scatter_mapbox(
        df,
        lat='Latitude ',
        lon='Longitude',
        color='Temp °C',
        opacity=0.7,
        hover_data=['Estuary_name'],
        animation_frame='Date',
        range_color=(df['Temp °C'].min(), df['Temp °C'].max()),
        title='Changing Water Conditions',
        labels={'Temp °C': 'Temperature (°C)'},
        mapbox_style="carto-positron",
        zoom=4,
        center={"lat": df["Latitude "].mean(), "lon": df["Longitude"].mean()},
        height=500,
        color_continuous_scale='BuPu'
    )
    
    fig.update_traces(marker=dict(size=20))
    fig.update_layout(coloraxis_colorbar=dict(title='Temperature (°C)'))
    
    graphJSON_scatter = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Read the CSV data for the first plot
    df_fire = pd.read_csv("G:\\NASA\\fire_nrt_V1_101674.csv")
    df_fire.rename(columns={"acq_date": "date"}, inplace=True)
    nsw_bounds = [141, -37.5, 153.5, -28.1]
    start_date = "2019-09-01"
    end_date = "2020-01-31"
    df_nsw = df_fire[(df_fire["longitude"] >= nsw_bounds[0]) &
                     (df_fire["longitude"] <= nsw_bounds[2]) &
                     (df_fire["latitude"] >= nsw_bounds[1]) &
                     (df_fire["latitude"] <= nsw_bounds[3]) &
                     (df_fire["date"] >= start_date) &
                     (df_fire["date"] <= end_date)]
    fig_fire = px.density_mapbox(
        df_nsw,
        lat="latitude",
        lon="longitude",
        z="bright_ti4",
        color_continuous_scale="YlOrRd",
        radius=10,
        zoom=5,
        center={"lat": -32.5, "lon": 147},
        animation_frame="date",
        title="Fires/Heat Signatures Timeline: Sep 2019 to Jan 2020"
    )
    fig_fire.update_traces(zauto=False, zmin=0, zmax=4000)
    fig_fire.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar=dict(title="Fire Intensity")
    )
    graphJSON_fire = json.dumps(fig_fire, cls=plotly.utils.PlotlyJSONEncoder)

    # Read the CSV data for the second plot
    df_temp = pd.read_csv("G:\\Choropleth and Chart Data\\Waterway Data\\data.csv", encoding='latin1')
    df_temp = df_temp.sort_values('Date')
    df_temp['Date'] = pd.to_datetime(df_temp['Date'], format='%d/%m/%Y')
    df_avg_temp = df_temp.groupby('Date')['Temp °C'].mean().reset_index()
    fig_temp = px.line(
        data_frame=df_avg_temp,
        x='Date',
        y='Temp °C',
        title='Average Temperature Change in NSW Estuaries over time'
        
    )
    fig_temp.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            range=['2007-10-01', '2008-01-01']
        ),
        xaxis_title='Date',
        yaxis_title='Average Temperature (°C)'
    )
    graphJSON_temp = json.dumps(fig_temp, cls=plotly.utils.PlotlyJSONEncoder)

    # Read the CSV data for the third plot
    df_estuaries = pd.read_csv("G:\\Choropleth and Chart Data\\Waterway Data\\data.csv", encoding='latin1')
    df_estuaries = df_estuaries.sort_values('Date')
    df_estuaries['Date'] = pd.to_datetime(df_estuaries['Date'], format='%d/%m/%Y')
    lakes_of_interest = ['Lake','Lagoon','Creek']
    filtered_df = df_estuaries[df_estuaries['Estuary_type'].isin(lakes_of_interest)]
    avg_estuary_df = filtered_df.groupby(['Date', 'Estuary_type'])['Temp °C'].mean().reset_index()
    fig_estuaries = px.line(
        data_frame=avg_estuary_df,
        x='Date',
        y='Temp °C',
        color='Estuary_type',
        title='Average Temperature Change for NSW Estuaries Over Time',
        line_shape='linear'
    )
    fig_estuaries.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            range=['2007-12-01', '2008-06-01']
        ),
        xaxis_title='Date',
        yaxis_title='Average Temperature (°C)'
    )
    graphJSON_estuaries = json.dumps(fig_estuaries, cls=plotly.utils.PlotlyJSONEncoder)

    # Read the CSV data for the fourth plot
    df_lakes = pd.read_csv("G:\\Choropleth and Chart Data\\Waterway Data\\data.csv", encoding='latin1')
    lakes_of_interest = ['Conjola Lake', 'Meroo Lake', 'Tuross River', 'Termeil Lake']
    filtered_df_lakes = df_lakes[df_lakes['Estuary_name'].isin(lakes_of_interest)]
    filtered_df_lakes = filtered_df_lakes.sort_values('Date')
    filtered_df_lakes['Date'] = pd.to_datetime(filtered_df_lakes['Date'], format='%d/%m/%Y')
    avg_temp_df_lakes = filtered_df_lakes.groupby(['Date', 'Estuary_name'])['Temp °C'].mean().reset_index()
    fig_lakes = px.line(
        data_frame=avg_temp_df_lakes,
        x='Date',
        y='Temp °C',
        color='Estuary_name',
        title='Average Temperature Change for NSW Lakes Over Time'
    )
    fig_lakes.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date",
            range=['2008-12-01', '2009-12-01']
        ),
        xaxis_title='Date',
        yaxis_title='Average Temperature (°C)'
    )
    graphJSON_lakes = json.dumps(fig_lakes, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graphJSON_scatter=graphJSON_scatter, graphJSON_fire=graphJSON_fire, graphJSON_temp=graphJSON_temp, graphJSON_estuaries=graphJSON_estuaries, graphJSON_lakes=graphJSON_lakes)

if __name__ == '__main__':
    app.run()
