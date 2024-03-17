#first clean the dataset
import pandas as pd
import numpy as np

df = pd.read_csv('dataset/vgchartz-2024.csv')

df = df.dropna(subset=['publisher', 'genre', 'critic_score', 'total_sales'])
df = df[(df['publisher'] != 'Unknown') & (df['genre'] != 'Misc')]

df['genre'] = np.where(df['genre'].isin(['Action', 'Action-Adventure', 'Adventure']), 'Action-Adventure', df['genre'])

df['total_count'] = df.groupby(['genre', 'publisher'])['title'].transform('count')
df['total_sales'] = df.groupby(['genre', 'publisher'])['total_sales'].transform('sum')
df['critic_score'] = df.groupby(['genre', 'publisher'])['critic_score'].transform('mean')

df['count_zscore'] = (df['total_count'] - df.groupby('genre')['total_count'].transform('mean')) / df.groupby('genre')['total_count'].transform('std')
df['sales_zscore'] = (df['total_sales'] - df.groupby('genre')['total_sales'].transform('mean')) / df.groupby('genre')['total_sales'].transform('std')

df['count_zscore'] = df['count_zscore'].round(1)
df['sales_zscore'] = df['sales_zscore'].round(1)
df['total_sales'] = df['total_sales'].round(1)
df['total_count'] = df['total_count'].round(1)
df['critic_score'] = df['critic_score'].round(1)

df = df[['genre', 'publisher', 'critic_score', 'count_zscore', 'sales_zscore']]
df.drop_duplicates(subset=['genre', 'publisher'], inplace=True)
df.sort_values(by='genre', inplace=True)

df = df.dropna(subset=['publisher', 'genre', 'count_zscore', 'sales_zscore'])

df.to_csv('dataset/genre_publisher_zscores.csv', index=False)




#create the 3d scatter plot using plotly and save as a html file
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('dataset/genre_publisher_zscores.csv')

def get_color_category(score):
    if score > 8:
        return 'yellow'
    elif 6 <= score <= 8:
        return '#c7d5e0'
    elif 4 <= score <= 6:
        return '#66c0f4'  
    elif 2 <= score < 4:
        return '#2a475e' 
    else:
        return '#1b2838'  

genres = df['genre'].unique()

buttons = []
for genre in genres:
    visible = [g == genre for g in df['genre']]
    button = dict(label=genre,
                  method='update',
                  args=[{'visible': visible},
                     ])
    buttons.append(button)

fig = go.Figure()

for genre in genres:
    for publisher in df['publisher'].unique():
        publisher_data = df[(df['publisher'] == publisher) & (df['genre'] == genre)].dropna()
        if not publisher_data.empty:
            
            fig.add_trace(go.Scatter3d(
                x=publisher_data['critic_score'],
                y=publisher_data['count_zscore'],
                z=publisher_data['sales_zscore'],
                mode='markers',
                marker=dict(
                    size=publisher_data['count_zscore']*8 + 30,
                    color=publisher_data['critic_score'].apply(get_color_category),  
                    opacity=1
                ),
                name=publisher,
                text=[
                    f'<br><b style="font-size: 20px;">{pub}</b><br>'
                    f'<b>Critic Score:</b> {critic}<br>'
                    f'<b>Total Games:</b> {count}<br>'
                    f'<b>Total Sales:</b> {percentage}'
                    for pub, critic, count, percentage in zip(
                        publisher_data['publisher'], 
                        publisher_data['critic_score'], 
                        publisher_data['count_zscore'],
                        publisher_data['sales_zscore'])
                ], 
                hoverinfo='text',
                visible=True if genre == df['genre'].iloc[0] else False  
            ))
for genre in genres:
  for publisher in df['publisher'].unique():
        publisher_data = df[(df['publisher'] == publisher) & (df['genre'] == genre)].dropna()
        if not publisher_data.empty:
          fig.add_trace(go.Scatter3d(
    x=[1, 10], y=[0, 0], z=[0, 0],
    mode='lines',
    line=dict(color='#fff', width=3),
    name='Total Count Z-Score = 0', hoverinfo='none',
    visible=True
))

fig.update_layout(
    scene=dict(
      xaxis=dict(title='Critic Score', range=[1, 10], color='#fff'),
yaxis=dict(title='Total Games', range=[-2, 2.2], color='#fff'),
zaxis=dict(title='Total Sales', range=[-2, 3.8], color='#fff'),

        aspectmode='manual',
        aspectratio=dict(x=0.8, y=1, z=0.8),
    ),
    font=dict(
        family="Kanit, sans-serif"
    ),
    hoverlabel=dict(
        font=dict(family="Kanit, sans-serif"), 
    ),
    updatemenus=[dict(buttons=buttons)],
    showlegend=False
)

fig.show()

#save to html
#fig.write_html('scatter_plot.html')
