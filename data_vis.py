import polars as pl
from icecream import ic
import streamlit as st
import altair as alt
import json

data = pl.read_csv("earnings-clean.csv", null_values=["NA", ""])
print(data.columns)

print(data["earnings"].is_null().sum())

data14 = (
    data.filter(pl.col("year") == 2014)
        .filter(~pl.col("geo").is_in(["EA17", "EA18", "EA19", "EU27_2007", "EU27_2020", "EU28"]))
        .filter(~pl.col("earnings").is_null())
)

st.dataframe(data14)
data14_grouped = data14.group_by("geo").agg(pl.col("earnings").mean().alias("earnings_mean"))
print(data14_grouped)

#https://raw.githubusercontent.com/leakyMirror/map-of-europe/27a335110674ae5b01a84d3501b227e661beea2b/TopoJSON/europe.topojson

chart = (alt.Chart(alt.topo_feature("https://raw.githubusercontent.com/leakyMirror/map-of-europe/27a335110674ae5b01a84d3501b227e661beea2b/TopoJSON/europe.topojson", 'europe'))
         .mark_geoshape(stroke = "black").encode(
    color=alt.Color('earnings_mean:Q', scale=alt.Scale(scheme='reds')),  # Colore basato su 'earnings'
    tooltip=['geo:N', 'earnings_mean:Q']  # Tooltip per visualizzare informazioni
    ).transform_lookup(
    lookup='id',  # Chiave comune per unire (nel TopoJSON)
    from_=alt.LookupData(data14_grouped, 'geo', ['earnings_mean'])  # Fonte dei dati
    ).project(
    type='mercator'  # Proiezione geografica
    ).properties(
    width=800,
    height=600,
    title="Distribuzione dei guadagni in Europa nel 2014"
    )
)

st.altair_chart(
    chart, 
    use_container_width=True)

