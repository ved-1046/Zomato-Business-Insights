import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Zomato Business Dashboard",
    page_icon="🍽️",
    layout='wide'
)

st.title('Zomato Restaurant Business Dashboard')

st.markdown('' \
'Analyze restaurants using innteractive filters and business insights')

df = pd.read_csv("Zomato.csv")
filtered_df = df


st.sidebar.header('Dashboard filters')

areas = ["All Areas"] + sorted(df['area'].dropna().unique()) #we took unique areas and sorted them in alphabetical order
selected_area = st.sidebar.selectbox("Choose area ", areas)


if selected_area == "All Areas":
    filtered_df = df
else:
    filtered_df = df[df['area'] == selected_area]  


restaurants  = ["All Restaurants"] + sorted(df['restaurant type'].dropna().unique())
selected_restaurant = st.sidebar.selectbox("Choose Restaurant",restaurants)


if selected_restaurant != "All Restaurants":
    filtered_df = filtered_df[filtered_df['restaurant type'] == selected_restaurant]

minimum_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value = 0.0,
    max_value= 5.9,
    value = 0.9,
    step = 0.1
    ) 

# st.write(df['rate (out of 5)'].dtype)
filtered_df = filtered_df[
    filtered_df['rate (out of 5)'] >= minimum_rating
]


st.write(minimum_rating)
search = st.text_input("Search Restaurant")


if search:
    filtered_df = filtered_df[filtered_df['restaurant name'].str.contains(
        search ,
        case = False,
        na=False
    )]

if filtered_df.empty:
    st.warning('No restaurants found for selected filter')
    st.stop()


total_restaurants = len(filtered_df)
avg_rating = round(filtered_df['rate (out of 5)'].mean(),2)
total_areas = filtered_df['area'].nunique()
total_cuisines = filtered_df['cuisines type'].nunique() #unique cuisines instead of  number it returns


col1 , col2 , col3 , col4 = st.columns(4)
with col1:
    st.metric("Restaurants  " ,total_restaurants)

with col2:
    st.metric("Avg rating  " , avg_rating)


with col3:
    st.metric("Areas " ,total_areas)


with col4:
    st.metric("Cuisines" , total_cuisines)



st.subheader('Business Insights')
restaurant_counts = filtered_df['restaurant type'].value_counts()
restaurant_counts = restaurant_counts.reset_index()

fig = px.bar(restaurant_counts , 
             x = 'restaurant type',
             y = 'count',
             title='Restaurant Type Distribution',
             color='restaurant type',
             color_discrete_sequence=px.colors.qualitative.Set2)

fig.update_layout(
    xaxis_title = 'Restaurant Type',
    yaxis_title = "Number of Restaurants"
)

area_counts = filtered_df['area'].value_counts()
area_counts = area_counts.reset_index()

area_figure = px.bar(area_counts,
                 x = 'area',
                 y = 'count',
                 title = 'Area Distribution',
                 color_discrete_sequence=px.colors.qualitative.Bold)



chart1 , chart2 = st.columns(2)

with chart1:
    st.plotly_chart(fig)

with chart2:
    st.plotly_chart(area_figure)

#avg rating byt cuiisne
cuisine_counts = filtered_df.groupby('cuisines type')['rate (out of 5)'].mean().sort_values(ascending=False).head(10)
cuisine_counts = cuisine_counts.reset_index()

cuisine_figure = px.bar(cuisine_counts,
                        x = 'cuisines type',
                        y='rate (out of 5)',
                        title = 'Top 10 Cuisine',
                        color='rate (out of 5)',
                        color_continuous_scale='Viridis')



#what percentage of restaurants belong to each restaurant type
restaurant_pie = px.pie(restaurant_counts ,
                        names='restaurant type',
                        values='count',
                        title='Restaurant Type Distribution',
                        color_discrete_sequence=px.colors.qualitative.Pastel)

chart3 , chart4 = st.columns(2)
with chart3:
    st.plotly_chart(cuisine_figure)

with chart4:
    st.plotly_chart(restaurant_pie)


#distribution of ratings
rating_fig = px.histogram(
    filtered_df,
    x = 'rate (out of 5)',
    nbins= 10,
    title='Restaurant Rating Distribution',
    template='plotly_white'
)



#Rating vs Cost
scatter_fig = px.scatter(filtered_df,
                         x='avg cost (two people)',
                         y = 'rate (out of 5)',
                         hover_name='restaurant name',
                         color = 'restaurant type',
                         title='Rating vs Cost',
                         template='plotly_white')


chart5 , chart6 = st.columns(2)

with chart5:
    st.plotly_chart(rating_fig)

with chart6:
    st.plotly_chart(scatter_fig)

csv = filtered_df.to_csv(index = False).encode('utf-8')

st.download_button(
    'Download Filtered Data',
    data = csv,
    file_name='filtered_restaurants.csv',
    mime='text/csv'
)

st.subheader('Restaurant details')

st.dataframe(filtered_df[[
    'restaurant name',
    'restaurant type',
    'rate (out of 5)',
    'avg cost (two people)',
    'area'
]])

st.markdown('-----')
st.caption('Created by Vedika Tamshetti')