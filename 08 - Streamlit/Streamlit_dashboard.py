import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Plotly
import plotly.offline as py
from plotly import tools
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from streamlit_folium import folium_static
import folium
from PIL import Image


#### loading data files
paris = pd.read_csv(r"./data/Paris_for_EDA.csv")
lyon = pd.read_csv(r"./data/Lyon_for_EDA.csv")
lyon_2 = pd.read_csv(r"./data/sec2_Lyon.csv")
paris_2 = pd.read_csv(r"./data/sec2_Paris.csv")


#### Setting the layout of the page
st.set_page_config(layout="wide")


################# SIDEBAR

st.sidebar.markdown("## Paris vs. Lyon")
st.sidebar.markdown("#### Analysis of hystorical data and forecast for 2022")

# Selection of year
year_pie = st.sidebar.selectbox(
    "Please select a year:", (2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021)
)

# Selection of month
month_sel = st.sidebar.selectbox(
    "Please select a month:",
    (
        "January",
        "Febuary",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ),
)
month_name = {
    "January": 1,
    "Febuary": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12,
}
month_chart = month_name[month_sel]

# Selection of pollutant
poll = st.sidebar.radio(
    "Please select a pollutant:", ("PM2.5", "PM10", "Ozone", "Nitorgen dioxide")
)
poll_name = {"PM2.5": "pm25", "PM10": "pm10", "Ozone": "o3", "Nitorgen dioxide": "no2"}
pollutant = poll_name[poll]


################# DATA MANIPULATION
cols_to_drop = ["tempmax", "tempmin", "precipcover"]
lyon.drop(columns=cols_to_drop, inplace=True)
paris.drop(columns=cols_to_drop, inplace=True)

paris.datetime = pd.to_datetime(paris.datetime)
lyon.datetime = pd.to_datetime(lyon.datetime)

paris["year"] = paris.datetime.dt.year
lyon["year"] = lyon.datetime.dt.year

lyon["target"] = pd.cut(lyon.pm25, bins=[0, 50, 100, 200], labels=[0, 1, 2])
paris["target"] = pd.cut(paris.pm25, bins=[0, 50, 100, 200], labels=[0, 1, 2])

##### For pie chart
years_target_paris = pd.crosstab(paris.target, paris.year)
years_target_paris = years_target_paris.reset_index(drop=True)

years_target_lyon = pd.crosstab(lyon.target, lyon.year)
years_target_lyon = years_target_lyon.reset_index(drop=True)

##### For line chart
line_paris = paris[["datetime", pollutant]].loc[(paris.year == year_pie)]
line_lyon = lyon[["datetime", pollutant]].loc[(lyon.year == year_pie)]

#### Tabel
paris["city"] = "Paris"
lyon["city"] = "Lyon"
data = pd.concat([paris, lyon])
columns = [
    "temp",
    "humidity",
    "precip",
    "windspeed",
    "pressure",
    "cloudcover",
    "visibility",
    "uvindex",
    "year",
    "month",
    "pm25",
    "pm10",
    "o3",
    "no2",
    "city",
]
table = (
    data[columns][
        (data[columns]["year"] == year_pie) & (data[columns]["month"] == month_chart)
    ]
    .groupby(["city"])
    .agg("mean")
    .round()
)
table_weather = table[
    [
        "temp",
        "humidity",
        "precip",
        "windspeed",
        "pressure",
        "cloudcover",
        "visibility",
        "uvindex",
    ]
]


### Bar chart
table_pollutant = table[["pm25", "pm10", "o3", "no2"]]
table_pollutant = table_pollutant.T

#################SECTION2
# Models fit
fit_pol = lyon_2.loc[lyon_2.poll == pollutant][
    ["ds", "yhat_lower", "yhat_upper", "yhat", "y", "month", "day_of_week"]
]
name_poll = {"pm25": "PM2.5", "pm10": "PM10", "o3": "ozone", "no2": "nitrogen dioxide"}
fit_por = paris_2.loc[paris_2.poll == pollutant][
    ["ds", "yhat_lower", "yhat_upper", "yhat", "y"]
]

# Forecast for 2022
fit_2022l = lyon_2.loc[(lyon_2.poll == pollutant) & (lyon_2.year == 2022)][
    ["ds", "yhat_lower", "yhat_upper", "yhat", "y"]
]
fit_2022p = paris_2.loc[(paris_2.poll == pollutant) & (paris_2.year == 2022)][
    ["ds", "yhat_lower", "yhat_upper", "yhat", "y"]
]

# Trend line
fit_tredl = lyon_2.loc[lyon_2.poll == pollutant][
    ["ds", "trend_lower", "trend_upper", "trend"]
]
fit_tredp = paris_2.loc[paris_2.poll == pollutant][
    ["ds", "trend_lower", "trend_upper", "trend"]
]

# Yearly seasonality
fit_yearlyl = lyon_2.loc[(lyon_2.poll == pollutant) & (lyon_2.year == 2016)][
    ["ds", "yearly", "month"]
]
fit_yearlyp = paris_2.loc[(paris_2.poll == pollutant) & (paris_2.year == 2016)][
    ["ds", "yearly", "month"]
]

fit_yearlyl.ds = pd.to_datetime(fit_yearlyl.ds)
fit_yearlyp.ds = pd.to_datetime(fit_yearlyp.ds)

fit_yearlyl["month_day"] = fit_yearlyl["ds"].dt.dayofyear
fit_yearlyp["month_day"] = fit_yearlyp["ds"].dt.dayofyear

averge_for_daysl = fit_yearlyl.groupby("month_day").agg("mean")
averge_for_daysp = fit_yearlyp.groupby("month_day").agg("mean")

# Weekly seasonality
fit_weeklyl = lyon_2.loc[(lyon_2.poll == pollutant) & (lyon_2.year == 2016)][
    ["ds", "weekly", "day_of_week"]
]
fit_weeklyp = paris_2.loc[(paris_2.poll == pollutant) & (paris_2.year == 2016)][
    ["ds", "weekly", "day_of_week"]
]

averge_daysl = fit_weeklyl.groupby("day_of_week").agg("mean")
averge_daysp = fit_weeklyp.groupby("day_of_week").agg("mean")
averge_daysp = averge_daysp.reindex(
    index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)
averge_daysl = averge_daysl.reindex(
    index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

#################### Charts #############################


# ########## PIE CHARTS

fig_pie = make_subplots(
    rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
)
labels = ["Good", "Moderate", "Bad"]

colors = ["rgb(79, 129, 102)", "#FFC300 ", "rgb(175, 49, 35)"]
fig_pie.add_trace(
    go.Pie(
        labels=labels,
        values=years_target_paris[year_pie],
        name="Paris",
        marker_colors=colors,
    ),
    1,
    1,
)
fig_pie.add_trace(
    go.Pie(
        labels=labels,
        values=years_target_lyon[year_pie],
        name="Lyon",
        marker_colors=colors,
    ),
    1,
    2,
)


# Use `hole` to create a donut-like pie chart
fig_pie.update_traces(hole=0.35, hoverinfo="label+percent+name")

fig_pie.update_layout(
    title_text=f"Percentage of days with various Air quality in Paris and Lyon in {year_pie}",
    # Add annotations in the center of the donut pies.
    annotations=[
        dict(text="PARIS", x=0.17, y=0.5, font_size=20, showarrow=False),
        dict(text="LYON", x=0.82, y=0.5, font_size=20, showarrow=False),
    ],
)


#### Line chart
fig_pollutant_year = go.Figure()
fig_pollutant_year.add_trace(
    go.Line(
        x=line_paris["datetime"],
        y=line_paris[pollutant],
        name="Paris",
        line_color="#2A6C6C",
    )
)
fig_pollutant_year.add_trace(
    go.Line(
        x=line_lyon["datetime"],
        y=line_lyon[pollutant],
        name="Lyon",
        line_color="#C70039",
    )
)

name_poll = {"pm25": "PM2.5", "pm10": "PM10", "o3": "ozone", "no2": "nitrogen dioxide"}
# Layout
fig_pollutant_year.update_layout(
    barmode="group",
    xaxis_tickangle=-45,
    title=f"Yearly concentration of {name_poll[pollutant]} in {year_pie}",
    xaxis_title="Date",
    yaxis_title="Concentartion",
)


################# METRICS ###########

### Metrics_Paris
fig_metrics_paris = go.Figure()

# Temperature
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "temp"],
        title={"text": "Temperture, ºC"},
        domain={"row": 0, "column": 0},
    )
)
# Humidity
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "humidity"],
        title={"text": "Humidity, %"},
        domain={"row": 1, "column": 0},
    )
)
# Precipitation
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "precip"],
        title={"text": "Precipitation, mm"},
        domain={"row": 1, "column": 1},
    )
)
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "pressure"],
        title={"text": "Pressure, hPa"},
        domain={"row": 0, "column": 1},
    )
)
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "cloudcover"],
        title={"text": "Cloud cover, %"},
        domain={"row": 0, "column": 2},
    )
)
fig_metrics_paris.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Paris", "uvindex"],
        title={"text": "UV index"},
        domain={"row": 1, "column": 2},
    )
)


fig_metrics_paris.update_layout(
    title=f"Average values for Paris in {month_sel} {year_pie}",
    grid={"rows": 2, "columns": 3, "pattern": "independent"},
    template={"data": {"indicator": [{"mode": "number",}]}},
)


### Metrics Lyon

fig_metrics_lyon = go.Figure()

# Temperature
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "temp"],
        title={"text": "Temperture, ºC"},
        domain={"row": 0, "column": 0},
    )
)
# Humidity
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "humidity"],
        title={"text": "Humidity, %"},
        domain={"row": 1, "column": 0},
    )
)
# Precipitation
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "precip"],
        title={"text": "Precipitation, mm"},
        domain={"row": 1, "column": 1},
    )
)
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "pressure"],
        title={"text": "Pressure, hPa"},
        domain={"row": 0, "column": 1},
    )
)
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "cloudcover"],
        title={"text": "Cloud cover, %"},
        domain={"row": 0, "column": 2},
    )
)
fig_metrics_lyon.add_trace(
    go.Indicator(
        mode="number",
        value=table_weather.at["Lyon", "uvindex"],
        title={"text": "UV index"},
        domain={"row": 1, "column": 2},
    )
)


fig_metrics_lyon.update_layout(
    title=f"Average values for Lyon in {month_sel} {year_pie}",
    grid={"rows": 2, "columns": 3, "pattern": "independent"},
    template={"data": {"indicator": [{"mode": "number",}]}},
)


#### Bar chart
fig_bar_month = go.Figure()

fig_bar_month.add_trace(
    go.Bar(
        x=["PM2.5", "PM10", "Ozone", "Nitrogen dioxide"],
        y=table_pollutant["Lyon"],
        name="Lyon",
        marker_color="#C70039",
    ),
)
fig_bar_month.add_trace(
    go.Bar(
        x=["PM2.5", "PM10", "Ozone", "Nitrogen dioxide"],
        y=table_pollutant["Paris"],
        name="Paris",
        marker_color="#2A6C6C",
    ),
)


month_dict = {
    1: "January",
    2: "Ferbuary",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
name_poll = {"pm25": "PM2.5", "pm10": "PM10", "o3": "ozone", "no2": "nitrogen dioxide"}
# Layout
fig_bar_month.update_layout(
    barmode="group",
    xaxis_tickangle=-45,
    title=f"Concentration of analysed pollutants in {month_dict[month_chart]} {year_pie}",
    title_x=0.5,
    xaxis_title="Pollutant",
    yaxis_title="Concentartion",
)


#### Lyon model
fig_lyon_model = go.Figure(
    [
        go.Scatter(
            name=name_poll[pollutant],
            x=fit_pol["ds"],
            y=fit_pol["yhat"],
            mode="lines",
            line=dict(color="#C70039"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_pol["ds"],
            y=fit_pol["yhat_upper"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_pol["ds"],
            y=fit_pol["yhat_lower"],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(199, 0, 57, 0.2)",
            fill="tonexty",
            showlegend=False,
        ),
        go.Scatter(
            name="Real data",
            x=fit_pol["ds"],
            y=fit_pol["y"],
            mode="markers",
            marker=dict(color="#100C58", size=2),
            showlegend=False,
        ),
    ]
)
fig_lyon_model.update_layout(
    yaxis_title="Concentration",
    title=f"Fitting of {name_poll[pollutant]} data to the forecast model - Lyon",
    hovermode="x",
)


###Model Paris
fig_paris_model = go.Figure(
    [
        go.Scatter(
            name=name_poll[pollutant],
            x=fit_por["ds"],
            y=fit_por["yhat"],
            mode="lines",
            line=dict(color="#2A6C6C"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_por["ds"],
            y=fit_por["yhat_upper"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_por["ds"],
            y=fit_por["yhat_lower"],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(97, 169, 136, 0.3)",
            fill="tonexty",
            showlegend=False,
        ),
        go.Scatter(
            name="Real data",
            x=fit_por["ds"],
            y=fit_por["y"],
            mode="markers",
            marker=dict(color="#100C58", size=2),
            showlegend=False,
        ),
    ]
)
fig_paris_model.update_layout(
    yaxis_title="Concentration",
    title=f"Fitting of {name_poll[pollutant]} data to the forecast model - Paris",
    hovermode="x",
)


### Forecast Lyon for 2022
fig_lyon_forecast = go.Figure(
    [
        go.Scatter(
            name=name_poll[pollutant],
            x=fit_2022l["ds"],
            y=fit_2022l["yhat"],
            mode="lines",
            line=dict(color="#C70039"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_2022l["ds"],
            y=fit_2022l["yhat_upper"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_2022l["ds"],
            y=fit_2022l["yhat_lower"],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(199, 0, 57, 0.2)",
            fill="tonexty",
            showlegend=False,
        ),
    ]
)
fig_lyon_forecast.update_layout(
    yaxis_title="Concentration",
    title=f"Forecatast of {name_poll[pollutant]} pollution in Lyon in 2022",
    hovermode="x",
)


### Forecast Paris
fig_paris_forecast = go.Figure(
    [
        go.Scatter(
            name=name_poll[pollutant],
            x=fit_2022p["ds"],
            y=fit_2022p["yhat"],
            mode="lines",
            line=dict(color="#2A6C6C"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_2022p["ds"],
            y=fit_2022p["yhat_upper"],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_2022p["ds"],
            y=fit_2022p["yhat_lower"],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(60, 175, 20, 0.3)",
            fill="tonexty",
            showlegend=False,
        ),
    ]
)
fig_paris_forecast.update_layout(
    yaxis_title="Concentration",
    title=f"Forecatast of {name_poll[pollutant]} pollution in Paris in 2022",
    hovermode="x",
)


## Trend lines
fig_trend = go.Figure(
    [
        # Lyon
        go.Scatter(
            name="Lyon",
            x=fit_tredl["ds"],
            y=fit_tredl["trend"],
            mode="lines",
            line=dict(color="#C70039"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_tredl["ds"][2920:],
            y=fit_tredl["trend_upper"][2920:],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_tredl["ds"][2920:],
            y=fit_tredl["trend_lower"][2920:],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(199, 0, 57, 0.2)",
            fill="tonexty",
            showlegend=False,
        ),
        # Paris
        go.Scatter(
            name="Paris",
            x=fit_tredp["ds"],
            y=fit_tredp["trend"],
            mode="lines",
            line=dict(color="#2A6C6C"),
        ),
        go.Scatter(
            name="Upper Bound",
            x=fit_tredp["ds"][2920:],
            y=fit_tredp["trend_upper"][2920:],
            mode="lines",
            marker=dict(color="#444"),
            line=dict(width=0),
            showlegend=False,
        ),
        go.Scatter(
            name="Lower Bound",
            x=fit_tredp["ds"][2920:],
            y=fit_tredp["trend_lower"][2920:],
            marker=dict(color="#444"),
            line=dict(width=0),
            mode="lines",
            fillcolor="rgba(68, 68, 68, 0.3)",
            fill="tonexty",
            showlegend=False,
        ),
    ]
)

fig_trend.update_layout(
    yaxis_title="Concentration",
    title=f"Trend of {name_poll[pollutant]} pollution in 2022",
    hovermode="x",
)


### Yearly seasonality
fig_season_yearly = go.Figure()
fig_season_yearly.add_trace(
    go.Line(
        x=averge_for_daysp.index,
        y=averge_for_daysp["yearly"],
        name="Paris",
        line_color="#2A6C6C",
    )
)
fig_season_yearly.add_trace(
    go.Line(
        x=averge_for_daysl.index,
        y=averge_for_daysl["yearly"],
        name="Lyon",
        line_color="#C70039",
    )
)

name_poll = {"pm25": "PM2.5", "pm10": "PM10", "o3": "ozone", "no2": "nitrogen dioxide"}
# Layout
fig_season_yearly.update_layout(
    barmode="group",
    xaxis_tickangle=-45,
    title=f"Yearly seasonality of {name_poll[pollutant]}",
    xaxis_title="Day of year",
    yaxis_title="Yearly",
)


### Weekly seasonality

fig_season_weekly = go.Figure()
fig_season_weekly.add_trace(
    go.Line(
        x=averge_daysp.index,
        y=averge_daysp["weekly"],
        name="Paris",
        line_color="#2A6C6C",
    )
)
fig_season_weekly.add_trace(
    go.Line(
        x=averge_daysl.index,
        y=averge_daysl["weekly"],
        name="Lyon",
        line_color="#C70039",
    )
)

name_poll = {"pm25": "PM2.5", "pm10": "PM10", "o3": "ozone", "no2": "nitrogen dioxide"}
# Layout
fig_season_weekly.update_layout(
    barmode="group",
    xaxis_tickangle=-45,
    title=f"Weekly seasonality of {name_poll[pollutant]}",
    xaxis_title="Day of week",
    yaxis_title="Weekly",
)


### Map

m = folium.Map(location=[46.2276, 2.2137], zoom_start=6, tiles="Stamen Toner")

# create markers
folium.CircleMarker(
    location=[48.8566, 2.3522],
    radius=5,
    popup="Paris",
    color="#2A6C6C",
    icon=folium.Icon(icon="cloud"),
).add_to(m)

folium.CircleMarker(
    location=[45.7640, 4.8357],
    popup="Lyon",
    radius=5,
    color="#C70039",
    icon=folium.Icon(color="#C70039"),
).add_to(m)


##############LAYOUT OF THE PAGE

###Image
image = Image.open("./Figures/Paris-Lyon.png")

st.image(image, caption="Paris-Lyon", use_column_width=True)

### Title of the page
st.markdown(
    "<h1 style='text-align: center; color: #071552;'>Air Quality<br/>Paris vs. Lyon</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "Welcome to this page. This is the final project I realized during the Ironhack Data Analytics Bootcamp."
)
st.markdown(
    "The goal of the project was to investigate and compare air pollution in Paris and Lyon and to forecast future air pollution using Time Series analysis and Supervised Machine Learning based on the weater data."
)
st.markdown(
    "The source code for this poroject can be found here: <https://github.com/radek-deb/Final_Project_Ironhack>"
)
st.markdown("Source of air quality data: <https://aqicn.org/data-platform/covid19/>")
st.markdown("Source of weather data: <https://www.visualcrossing.com/weather-api>")

st.markdown(f"## Historical air pollution and weather data 2014-2021")

container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        fig_pie
        fig_metrics_paris
        fig_bar_month
    with col2:
        fig_pollutant_year
        fig_metrics_lyon
        folium_static(m)


st.markdown(f"## Time Series - Forecast for 2022")
container2 = st.container()
col1, col2 = st.columns(2)

with container2:
    with col1:
        fig_paris_model
        fig_paris_forecast
        fig_season_weekly
    with col2:
        fig_lyon_model
        fig_lyon_forecast
        fig_season_yearly

container3 = st.container()
col3, col4, col5 = st.columns([1, 3, 1])
with container3:
    with col4:
        fig_trend
