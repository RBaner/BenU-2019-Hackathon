import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import functions

latitudes = functions.parse(19,15000)
longitudes = functions.parse(20,15000)
df = pd.DataFrame({
    'x':longitudes,
    'y':latitudes
})

np.random.seed(200)
k = 15
centroids = {
    i+1: [-87.95+np.random.randint(0,4500)*(1/10000), 41.63+np.random.randint(0,4000)*(1/10000)]
    for i in range(k)
}
colmap = functions.write(k)

def assignment(df, centroids):
    for i in centroids.keys():
        # sqrt((x1 - x2)^2 - (y1 - y2)^2)
        df['distance_from_{}'.format(i)] = (
            np.sqrt(
                (df['x'] - centroids[i][0]) ** 2
                + (df['y'] - centroids[i][1]) ** 2
            )
        )
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
#    df['color'] = df['closest'].map(lambda x: colmap[x])
    return df

df = assignment(df, centroids)

old_centroids = copy.deepcopy(centroids)

def update(k):
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return k

centroids = update(centroids)
df = assignment(df, centroids)

while True:
    closest_centroids = df['closest'].copy(deep=True)
    centroids = update(centroids)
    df = assignment(df, centroids)
    if closest_centroids.equals(df['closest']):
        break

fig = plt.figure(figsize=(7, 7))
#plt.scatter(df['x'], df['y'], color=df['color'], alpha=0.5, edgecolor='k')
plt.scatter(df['x'], df['y'], alpha=0.5, edgecolor='k')
for i in centroids.keys():
#    plt.scatter(*centroids[i], color=colmap[i])
    plt.scatter(*centroids[i], color="r")
plt.xlim(-87.95, -87.5)
plt.ylim(41.63, 42.03)
plt.show()
print(centroids)
