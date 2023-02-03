import streamlit as st
import pandas as pd
import numpy as np
# import plotly.graph_objects as go
# import plotly.figure_factory as figure_factory
import plotly.express as px


# from extract_data import extract_and_save

# df = extract_and_save()
df = pd.read_csv('./data/data_covid_2023-01-30', index_col=0)
df['Case_Fatality_Ratio'] = [df.loc[i, 'Deaths'] / df.loc[i, 'Confirmed']
                             if df.loc[i, 'Confirmed'] > 0 else 0 for i in df.index]
df['Case_Fatality_Ratio'] = np.round(df['Case_Fatality_Ratio'] * 100, 2)
df_map = px.data.gapminder().query("year==2007")
df = df.merge(df_map.loc[:, ['country', 'continent', 'iso_alpha', 'iso_num']],
              left_on='Country_Region', right_on='country', how='left')

cols_to_show = ['Combined_Key', 'Confirmed', 'Deaths', 'Incident_Rate', 'Case_Fatality_Ratio']
countries = df.Country_Region.unique()

st.set_page_config(page_title="Dashboard Covid", layout='wide')
st.set_option("deprecation.showPyplotGlobalUse", False)

st.subheader("Dashboard")
st.sidebar.subheader("Navegation")

name_pages = ["Plot by countries"]

page = st.sidebar.radio(
    "", name_pages
)

if page == name_pages[0]:
    st.subheader("Covid indicator by countries")

    metric = st.selectbox("Choice a metric", ['Confirmed', 'Deaths', 'Case_Fatality_Ratio'])

    df_group = df.dropna(subset='iso_alpha').groupby(['iso_alpha', 'continent',
                                                     'country']).agg({metric: 'mean'}).reset_index()
    fig = px.scatter_geo(df_group, locations="iso_alpha", color="continent",
                         hover_name="country", size=metric,
                         projection="natural earth")
    st.plotly_chart(fig)

    continent = st.selectbox("Choice a continent", df.continent.unique())

    df_countries = (
        df
        .loc[df['continent'] == continent]
        .groupby('country')
        .agg({'Confirmed': 'sum', 'Deaths': 'sum', 'Case_Fatality_Ratio': 'mean'})
    )
    st.dataframe(df_countries.sort_values('Case_Fatality_Ratio', ascending=False))
