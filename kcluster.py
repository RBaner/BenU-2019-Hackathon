#Rohit Banerjee, 2019

import pandas as pd #df
import numpy as np  #mean, sqrt, random
import matplotlib.pyplot as plt
from time import time #for random seed
import copy #deepcopy
import functions #parse, write

def assignment(df, centroids):
    """
    Assign each data point a closest centroid
    """
    for i in centroids.keys():
        df['distance_from_{}'.format(i)] = (
            np.sqrt((df['x'] - centroids[i][0]) ** 2 + (df['y'] - centroids[i][1]) ** 2))
    centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
    df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)            #finds minimum distance from any given data point to all centroids
    df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))#replaces "closest" column with identifier of closest centroid
    return(df)

def update(df,centroids):
    """
    Sets centroids to the mean location of their closest data points.
    Note that some centroids are set to NaN in this func as centroids with
    no "closest" data points are nullified and ignored from then on out.
    This is due to the dataset not being uniformly spread throughout the region
    like the centroids. This results in usually <15 of the original 15 centroids
    surviving.  
    """
    for i in centroids.keys():
        centroids[i][0] = np.mean(df[df['closest'] == i]['x'])
        centroids[i][1] = np.mean(df[df['closest'] == i]['y'])
    return(centroids)

def main():
    #initializing data frame and centroids
    latitudes = functions.parse(19,15000)
    longitudes = functions.parse(20,15000)
    df = pd.DataFrame({
        'x':longitudes,
        'y':latitudes
    })
    k = 15
    np.random.seed(int(time()))
    centroids = {
        #this range is specific to the chicago dataset
        i+1: [-87.95+np.random.randint(0,4500)*(1/10000), 41.63+np.random.randint(0,4000)*(1/10000)]
        for i in range(k)
    }
    #k-means clustering
    colmap = functions.write(k)
    df = assignment(df, centroids)
    while True:
        closest_centroids = df['closest'].copy(deep=True)
        centroids = update(df,centroids)
        df = assignment(df, centroids)
        if closest_centroids.equals(df['closest']):
            break
    #plotting
    fig = plt.figure(figsize=(7, 7))
    plt.scatter(df['x'], df['y'], alpha=0.5, edgecolor='k')
    for i in centroids.keys():
        plt.scatter(*centroids[i], color="r")
    plt.xlim(-87.95, -87.5)
    plt.ylim(41.63, 42.03)
    print({i:centroids[i] for i in centroids if pd.isnull(centroids[i][0]) != True}) #Prints all non-NaN centroids
    plt.show()
    return(1)

#driver code
if __name__ == '__main__':
    print(main())
