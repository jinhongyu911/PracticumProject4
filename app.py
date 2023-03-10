import pandas as pd
import streamlit as st
import plotly_express as px

st.header("""
US Vehicle Ad Data Analysis
**Correlations** between different vehicle **attributes**.

***
""")

vehicles = pd.read_csv('vehicles_us.csv')
vehicles['manufacturer'] = vehicles['model'].str.split().str[0]

model_median_year = vehicles.groupby('model')['model_year'].median()
type_median_odometer = vehicles.groupby('type')['odometer'].median()
model_mode_cylinders = vehicles.groupby(['model'])['cylinders'].agg(lambda x: x.mode())
model_mode_paint = vehicles.groupby(['model'])['paint_color'].agg(lambda x: x.mode())
model_median_price = vehicles.groupby('model')['price'].median()

mask1 = vehicles['model_year'].isnull()
mask2 = vehicles['odometer'].isnull()
mask3 = vehicles['cylinders'].isnull()
mask4 = vehicles['paint_color'].isnull()
mask5 = vehicles['price'] == 1

vehicles.loc[mask1, 'model_year'] = vehicles.loc[mask1, 'model'].map(model_median_year)
vehicles.loc[mask2, 'odometer'] = vehicles.loc[mask2, 'type'].map(type_median_odometer)
vehicles.loc[mask3, 'cylinders'] = vehicles.loc[mask3, 'model'].map(model_mode_cylinders)
vehicles.loc[mask4, 'paint_color'] = vehicles.loc[mask4, 'model'].map(model_mode_paint)
vehicles.loc[mask5, 'price'] = vehicles.loc[mask5, 'model'].map(model_median_price)
vehicles['is_4wd'].fillna(0, inplace=True)

vehicles['model_year'] = vehicles['model_year'].astype(int)
def model_period(year):
    if 1900 <= year <= 1920:
        return '1900-1920'
    if 1920 < year <= 1940:
        return '1921-1940'
    if 1940 < year <= 1960:
        return '1941-1960'
    if 1960 < year <= 1980:
        return '1961-1980'
    if 1980 < year <= 2000:
        return '1981-2000'
    if 2000 < year <= 2020:
        return '2001-2020'

vehicles['model_period'] = vehicles['model_year'].apply(model_period)


conditions = ['new', 'like new', 'excellent', 'good',  'fair', 'salvage']

st.subheader("""Car Type Distribution by Brand""")
sorted_unique_manufacturer = sorted(vehicles['manufacturer'].unique())
multi_select1 = st.multiselect('Select Manufacturer', sorted_unique_manufacturer, sorted_unique_manufacturer)
df1 = vehicles[vehicles['manufacturer'].isin(multi_select1)]
#brand_by_type = pd.pivot_table(df1, index='manufacturer', columns='type', values='price', aggfunc='count')
#brand_by_type.plot(kind='bar', stacked=True, title='Car Type Distribution by Brand', figsize=[10, 5])
fig = px.bar(df1, x="manufacturer", color="type", barmode="stack")
st.plotly_chart(fig)



st.subheader("""Car Condition Distribution By Model Year""")
sorted_model_period = sorted(vehicles['model_period'].unique())
multi_select2 = st.multiselect('Select Model Period (up to)', sorted_model_period, sorted_model_period)
df2 = vehicles[vehicles['model_period'].isin(multi_select2)]
mdyr_by_condition = pd.pivot_table(df2, index='model_year', columns='condition', values='price', aggfunc='count')
#mdyr_by_condition.plot(kind='bar', stacked=True, title='Car Condition Distribution By Model Year', figsize=[10, 5])
fig = px.bar(mdyr_by_condition, x=mdyr_by_condition.index,  y=mdyr_by_condition.columns, color='condition',
             category_orders={'condition': conditions}, barmode="stack")
st.plotly_chart(fig)



st.subheader("""Price Distribution By Brand""")
brand1 = st.selectbox('1st Brand', sorted_unique_manufacturer)
brand2 = st.selectbox('2st Brand', sorted_unique_manufacturer)
brand1_vehicles = vehicles[vehicles['manufacturer'] == brand1]
brand2_vehicles = vehicles[vehicles['manufacturer'] == brand2]

colors = ['#1f77b4', '#c23e3e']
normalize = st.checkbox('Normalize histogram', value=True)
if normalize:
    histnorm = 'percent'
else:
    histnorm = None

fig1 = px.histogram(brand1_vehicles, x='price', color_discrete_sequence=[colors[0]], opacity=0.8, nbins=20, histnorm=histnorm)
fig2 = px.histogram(brand2_vehicles, x='price', color_discrete_sequence=[colors[1]], opacity=0.5, nbins=20, histnorm=histnorm)

fig_combined = fig1.add_trace(fig2.data[0])
fig_combined.update_layout(barmode='overlay', xaxis_title='Price')
st.plotly_chart(fig_combined)



st.subheader("""Car Price by Model Year""")
multi_select2 = st.multiselect('Select Model Years (up to)', sorted_model_period, sorted_model_period)
df3 = vehicles[vehicles['model_period'].isin(multi_select2)]
#vehicles.plot(kind='scatter', y='price', x='model_year', title='Car Price vs Model Year', figsize=[10, 5])
fig = px.scatter(df3, x="model_year", y="price", color='condition', category_orders={'condition': conditions})
st.plotly_chart(fig)



st.subheader("""Odometer Reading Distribution by Model Year""")
multi_select2 = st.multiselect('Select Model Years', sorted_model_period, sorted_model_period)
df4 = vehicles[vehicles['model_period'].isin(multi_select2)]
fig = px.scatter(df4, x="model_year", y="odometer", color='condition', category_orders={'condition': conditions})
st.plotly_chart(fig)



st.subheader("""Price Distribution by Odometer Reading""")
fig = px.scatter(vehicles, x="odometer", y="price", color='condition', category_orders={'condition': conditions})
st.plotly_chart(fig)