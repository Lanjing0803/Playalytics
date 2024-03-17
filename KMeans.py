import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

#Find the optimal number of K
df = pd.read_csv('dataset/vgchartz-2024.csv')
X = df[['critic_score', 'total_sales','na_sales','jp_sales','pal_sales','other_sales']].dropna()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

k_values = range(1, 11)
wcss = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)
plt.plot(k_values, wcss, marker='o')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Within-Cluster Sum of Squares (WCSS)')
plt.title('Elbow Method for Optimal k')
plt.xticks(k_values)
plt.grid(True)
plt.show()

#Create the viz
df = pd.read_csv('dataset/vgchartz-2024.csv')

df = df.dropna(subset=['critic_score', 'total_sales','na_sales','jp_sales','pal_sales','other_sales'])
X = df[['critic_score', 'total_sales','na_sales','jp_sales','pal_sales','other_sales']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X_scaled)

plt.figure(figsize=(10, 6))

for cluster_id in sorted(df['cluster'].unique()):
    cluster_data = df[df['cluster'] == cluster_id]
    plt.scatter(cluster_data['critic_score'], cluster_data['total_sales'], label=f'Cluster {cluster_id}', alpha=0.7)

plt.title('K Means Clustering: Critic Scores vs. GlobalSales')
plt.xlabel('Critic Score')
plt.ylabel('Total Sales')
plt.legend()
plt.grid(True)
plt.show()

