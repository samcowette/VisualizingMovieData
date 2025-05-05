import pandas as pd;
import matplotlib.pyplot as plt;
import seaborn as sns;
import ast;

#read csv files and merge them on ID
credits_df = pd.read_csv('tmdb_5000_credits.csv')
movies_df = pd.read_csv('tmdb_5000_movies.csv')
df = movies_df.merge(credits_df, left_on='id', right_on='movie_id')

df['genres'] = df['genres'].apply(ast.literal_eval)
df['cast'] = df['cast'].apply(ast.literal_eval)
df['crew'] = df['crew'].apply(ast.literal_eval)

#Extracting relevant inforamtiojn from genres (only main genre), cast (top 3 cast memebers) and crew (director)
df['main_genre'] = df['genres'].apply(lambda x: x[0]['name'] if x else None)
df['top_cast'] = df['cast'].apply(lambda x: [i['name'] for i in x[:3]] if x else [])
df['director'] = df['crew'].apply(lambda x: next((i['name'] for i in x if i['job'] == 'Director'), None))

#Cleaning budget and revenue
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

#Removing data with no budget or revenue
df = df[(df['budget'] > 0) & (df['revenue'] > 0)]
df['profit'] = df['revenue'] - df['budget']

#Removing movies with vote count below 1000
df = df[df['vote_count'] > 1000]

#Visualizing the data
print("Top 10 movies by profit: ")
print(df[['original_title', 'profit']].sort_values(by='profit', ascending=False).head(5))
print("Top 10 movies by budget: ")
print(df[['original_title', 'budget']].sort_values(by='budget', ascending=False).head(5))
print("Most frequent actors inside the top 50 movies by profit: ")
print(df[['original_title', 'top_cast', 'profit']].sort_values(by='profit', ascending=False).head(50)['top_cast'].explode().value_counts().head(15))

#plotting a scatterplot of the correlation matrix between budget, and profit
sns.scatterplot(x='budget', y='profit', data=df)
plt.title('Budget vs Profit')
plt.xlabel('Budget')
plt.ylabel('Profit')
plt.show()

#Revenue by genre barplot
sns.barplot(x='main_genre', y='revenue', data=df)
plt.title('Revenue by Genre')
plt.xlabel("Genre")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()

#Plotting a heatmap of the correlation between budget. revenue, and profit
sns.heatmap(df[['budget', 'revenue', 'profit']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()