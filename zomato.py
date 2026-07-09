import os
os.makedirs("images", exist_ok = True)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Zomato.csv')

print(df.columns)
print(df.info())
print(df.describe())
print(df.head(10))
print(df.isnull().sum()) #to check whether the null items are present or no
df = df.dropna(subset=['rate (out of 5)',
'cuisines type'])

print(df.duplicated().sum()) #if duplicated rows are present or no

def print_insight(text):
    print('\n' + "="*70)
    print("BUSINESS INSIGHT")
    print("=" * 70)
    print(text)
    print("=" * 70 + "\n")

print_insight(
"The dataset was first examined to understand its structure, " \
"data types, and overall quality. Missing values and duplicate" \
" records were checked before performing any analysis to ensure " \
"reliable results. Any issues identified during this stage were " \
"considered during the analysis to avoid misleading conclusions."
)

#cusisne that receive higher customer ratings
cuisine = df.groupby('cuisines type')['rate (out of 5)'].mean().sort_values(ascending=False).head(20)
print(cuisine)

#visualization
#it is Series - a single column
plt.figure(figsize=(10,6))
sns.barplot(x= cuisine.values , y = cuisine.index)
plt.title('Cusine with Higher ratings')
plt.xlabel('Average rating out of 5')
plt.ylabel('Cuisine Type')
plt.tight_layout()
plt.savefig("images/cuisine_ratings.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight("Certain cuisine types consistently " \
"receive higher average customer ratings than others. " \
"This suggests that customer preferences vary across cuisines and " \
"that some cuisines are more successful at delivering satisfying dining" \
"" \
" experiences. Restaurants offering these highly rated cuisines may have " \
"a competitive advantage in attracting customers.")



#relationship between the highest rated restaurants and highest food ordered restaurants
ratings_online = df.groupby('online_order')['rate (out of 5)'].mean().sort_values(ascending=False)
print(ratings_online)
plt.figure(figsize=(10,6))
sns.barplot(x = ratings_online.values , y = ratings_online.index , color='steelblue' )
plt.title('Realtion between online ordering and ratings')
plt.xlabel('Average rating')
plt.ylabel('online_order')
plt.savefig("images/online_order_vs_ratings.png",dpi=300,bbox_inches = "tight")
plt.show()


print_insight(
"Restaurants that offer online ordering have a slightly higher average" \
" customer rating " \
"than those that do not. This suggests that providing online ordering may " \
"improve customer convenience and satisfaction. However, the difference is" \
" modest, indicating that factors such as food quality "
"and service also play an important role in determining ratings."

)

#bookings for better dining experience
def analyze_rating(df,column):
    result = (
        df.groupby(column)['rate (out of 5)'].mean().sort_values(ascending = False)
    )

    return result

#is higher table booking is related to higher ratings?
book_table = analyze_rating(df, "table booking")
print(book_table)
plt.figure(figsize=(10,6))
sns.barplot(x = book_table.values , y = book_table.index , color='steelblue' )
plt.title('Booking relation with Ratings')
plt.xlabel('Average_rating')
plt.ylabel('Table booking')
plt.savefig("images/table_booking_vs_rating.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight(
"Restaurants that provide table booking generally receive higher average " \
"ratings than those without this facility. This may indicate that customers" \
" value convenience and a smoother dining experience. Offering table reservations" \
" could therefore contribute to improved customer satisfaction, particularly for dine-in restaurants.")

#does price of restaurant influence customer rating
print(df['avg cost (two people)'].describe())
bins = [0,600,1000,2000,6000]
labels = ['Budget','Mid-Range','Premium','Luxury']

df['cost_tier'] = pd.cut(   #numeric column to categorize
    df['avg cost (two people)'], 
    bins = bins, #the boundaries (where to split the values)
    labels=labels, #the categories, means name given to each interval
    include_lowest=True #lowest value is included in 1st interval

)

print(df[['avg cost (two people)', 'cost_tier']].head(10))

cost_rating = analyze_rating(df , 'cost_tier')
print(cost_rating)
plt.figure(figsize=(10,6))
sns.barplot(x = cost_rating.values , y = cost_rating.index , color='steelblue' )
plt.title('Average rating by cost_tier')
plt.xlabel('Average_rating')
plt.ylabel('Cost tier')
plt.savefig("images/cost_tier_vs_rating.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight("Business Insight"
"Premium and luxury restaurants achieved higher average ratings" \
" than budget restaurants. This suggests that customers may associate higher-priced" \
" restaurants with better food quality, service, or overall dining experience." \
" However, higher pricing alone does not guarantee better ratings, as customer expectations " \
"also increase with price.")

#does ratings and online ordering benefit each restuarant type?
pivot_table = pd.pivot_table(
    data = df,
    index='restaurant type',
    columns='online_order',
    values='rate (out of 5)',
    aggfunc='mean'

) #two categorial values using 1 numeric measure

print(pivot_table)

top_restos = df['restaurant type'].value_counts().head(10)
print(top_restos)

top_pivot = pivot_table.loc[top_restos.index]
print(top_pivot)

top_pivot.plot(kind='bar')

plt.title('Average rating by restaurant type and online ordering')
plt.xlabel('Restaurant type')
plt.ylabel('Average rating')
plt.xticks(rotation = 45)
plt.legend(title = 'online order')
plt.savefig("images/restaurant_type_vs_online_order.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight("The pivot table analysis showed that the impact of online ordering" \
" varies across restaurant types. While several restaurant categories" \
" receive higher ratings when online ordering is available, " \
"the improvement is not consistent across all categories. " \
"This indicates that the effectiveness of online " \
"ordering depends on the type of restaurant and its target customers.")

#can we trust ratings with few reviews?
plt.figure(figsize=(10,6))
sns.regplot(x='num of ratings' , y='rate (out of 5)',data=df,
            scatter_kws={'alpha' : 0.5},
            line_kws={'color' : 'steelblue'})

plt.title('Restaurant ratings vs Number of customer reviews')
plt.xlabel('No of customer reviews')
plt.ylabel('Average Rating')
plt.savefig("images/review_vs_ratings.png",dpi=300,bbox_inches = "tight")
plt.show()

correlation = df['num of ratings'].corr(df['rate (out of 5)'])
print(correlation)

print_insight("The scatter plot and correlation analysis revealed a weak positive" \
" relationship between the number of customer reviews and restaurant " \
"ratings. Restaurants with more reviews tend to have slightly higher " \
"ratings, but the relationship is not strong enough to conclude that more" \
" reviews directly lead to better ratings. Review count should therefore" \
" be considered alongside rating when evaluating restaurant performance.")

#which areas have high rated restos
area_analysis = (
    df.groupby('area').agg(
        {'rate (out of 5)' : 'mean',
         'restaurant name' : 'count'
         }
    ).sort_values(by='rate (out of 5)', ascending=False)
)

area_analysis = area_analysis[area_analysis['restaurant name'] >= 10]

top_areas = area_analysis.sort_values(
    by='rate (out of 5)',
    ascending=False

).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x='rate (out of 5)' , y = top_areas.index,
            data = top_areas,
            color='steelblue')

plt.title('Top 10 highest rated areas')
plt.xlabel('Average Rating')
plt.ylabel('Area')
plt.tight_layout()
plt.savefig("images/top_rated_areas.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight("After filtering out areas with very few restaurants, " \
"several locations consistently showed higher average ratings." \
" Focusing only on areas with a sufficient number of restaurants" \
" makes the analysis more reliable and avoids conclusions based on a very" \
" small sample size. These high-performing areas could " \
"be considered for marketing campaigns or future business expansion.")

correlation_matrix = df[['rate (out of 5)','num of ratings','avg cost (two people)']].corr()
print(correlation_matrix)

plt.figure(figsize=(6,5))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap='Blues',
    fmt = '.2f',
    
)


plt.title('Correlation Between Restaurant features')
plt.tight_layout()
plt.xticks(rotation = 45)
plt.yticks(rotation = 0)
plt.savefig("images/correlation_heatmap.png",dpi=300,bbox_inches = "tight")
plt.show()

print_insight("The correlation heatmap summarizes the relationships " \
"between the numerical features in the dataset. It shows that most " \
"variables have weak to moderate correlations, indicating that " \
"restaurant ratings are influenced by multiple factors rather than a " \
"single variable. This highlights the importance of considering several" \
" business aspects together when evaluating restaurant performance.")