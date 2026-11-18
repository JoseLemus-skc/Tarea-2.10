import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# MODIFICACION ESTETICA
st.set_page_config(
    page_title="Crime Dashboard | San Francisco Police Department", 
    page_icon="Screenshot 2025-02-27 at 23-02-54 Can someone Jak this image of a cat pointing. r_WojakDrawings.png", 
    layout="wide"
)
st.title("Crimes in San Francisco")
st.markdown("Know the crimes in each area.")

df = pd.read_csv("Police.csv")

col1, col2 = st.columns([0.2, 0.8], vertical_alignment="top")
exp = st.expander("See DataFrames")

# MODIFICACION ESTETICA
st.sidebar.image("Screenshot 2026-11-17 234133.jpg", width="stretch")
st.sidebar.header("Setting:")

day_group = df.groupby(['Incident Day of Week'])['Incident Number'].count()

st.markdown("## Most insecure area.")

year = df['Incident Year'].unique()
year_selected = st.sidebar.selectbox('Year', year)

dist = df['Police District'].unique()

dist_selected = st.sidebar.selectbox('Area', dist)

# MODIFICACION DE DATOS

col1.multiselect("Districts", options = dist, default = 'Out of SF', select_all = True, key = "multi_dist")

dist_multiselected = st.session_state["multi_dist"]

dists_crime_count = pd.DataFrame()

for district in dist_multiselected:
    dists_crime_count[district] = df[df['Police District'] == district].groupby('Incident Category')['Incident ID'].nunique()

col2.line_chart(dists_crime_count)
exp.dataframe(dists_crime_count, width="stretch")

mapa = pd.DataFrame()

mapa['lat'] = df[((df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected))]['Latitude']
mapa['lon'] = df[((df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected))]['Longitude']

mapa = mapa.dropna()
st.map(mapa)

st.markdown("## The most insecure day.")

val = df[((df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected))]

vals = pd.DataFrame(val)

val_count = vals['Incident Day of Week'].value_counts()

val_count = val_count.reindex(index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], fill_value=0)

st.bar_chart(val_count)

fig = px.pie(values=val_count.values, names=val_count.index)
st.plotly_chart(fig, use_container_width=True)

cat = df[((df['Incident Year'] == year_selected) & (df['Police District'] == dist_selected))]['Incident Category']

x2 = cat.value_counts()
y2 = x2.index

st.markdown("## The most frequent crimes.")

fig2 = go.Figure(go.Bar(x=x2.values, y=y2, orientation='h'))
st.plotly_chart(fig2, use_container_width=True)

category=df['Incident Category']
genre = st.radio("Have you been a victim of any of these crimes?", ('Yes', 'No'))

if genre == 'Yes':
    st.write('Help us put the following.')
    year = st.slider('In what year did it happen?', 1930, 2020, 2023)
    distrito = st.selectbox('In which area was it?', dist)
    dia = st.selectbox('What day was i?', val_count.index)
    crimen = st.selectbox('What happened', category.unique())
    
    st.write("The crime was", crimen, "in", distrito, "it was a", dia, "in", year)
    st.write("Thank you!")
else:

# MODIFICACION ESTETICA

    st.error("Please report a crime, ANY crime", icon=None, width="stretch", title=None)