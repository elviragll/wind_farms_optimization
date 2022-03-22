# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 12:50:36 2022

@author: elvir
"""


import numpy as np
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
import pandas as pd


#UTM coordinates:
    #https://coordinates-converter.com/en/decimal/51.536000,-10.062008?karte=OpenStreetMap&zoom=8

pointA = (-417010.23, 5708588.888)
pointB= (-455073.235, 5692304.918)
pointC = (-451895.787,5683361.623)
pointD = (-441037.275,5681680.286)
pointE= (-439036.758,5670883.073)
pointF = (-416471.458,5671303.56)

polygon=np.array([pointA, pointB, pointC, pointD, pointE, pointF])

pointAB=((pointA[0]+pointB[0])/2, (pointA[1]+pointB[1])/2)
pointL = ((pointAB[0]+pointD[0])/2, (pointAB[1]+pointD[1])/2)
pointM = ((pointA[0]+pointF[0]*2)/3, (pointA[1]+pointF[1]*2)/3)
pointN = ((pointF[0]+pointA[0]*2)/3, (pointF[1]+pointA[1]*2)/3)

polygon1 =np.array([pointA, pointAB, pointL, pointN])
polygon2 =np.array([pointN, pointL, pointD, pointM])
polygon3 =np.array([pointM, pointD, pointE, pointF])
polygon4 =np.array([pointAB, pointB, pointC, pointD])

distance_D = 11
diameter = 236
distance = distance_D*diameter

xmin, xmax = (min(polygon[:,0]), max(polygon[:,0]))
interval_x = round((xmax-xmin)/distance)
ymin, ymax = (min(polygon[:,1]), max(polygon[:,1]))
interval_y = round((ymax-ymin)/distance)

x = np.linspace(xmin,xmax,interval_x)
y = np.linspace(ymin,ymax,interval_y)
xx,yy=np.meshgrid(x,y)
points_raw=np.array((xx.ravel(), yy.ravel())).T




path1 = mpltPath.Path(polygon1)
inside1 = path1.contains_points(points_raw)

path2 = mpltPath.Path(polygon2)
inside2 = path2.contains_points(points_raw)

path3 = mpltPath.Path(polygon3)
inside3 = path3.contains_points(points_raw)

path4 = mpltPath.Path(polygon4)
inside4 = path4.contains_points(points_raw)

points1=points_raw.copy()
points2=points_raw.copy()
points3=points_raw.copy()
points4=points_raw.copy()

for i in range(len(inside1)):
    if inside1[i]==False:
      points1[i,:]=None


outside1 = inside1[:]==False
ins1= np.logical_not(outside1)

for i in range(len(inside2)):
    if inside2[i]==False:
      points2[i,:]=None

outside2 = inside2[:]==False
ins2= np.logical_not(outside2)

for i in range(len(inside3)):
    if inside3[i]==False:
      points3[i,:]=None

outside3 = inside3[:]==False
ins3= np.logical_not(outside3)

for i in range(len(inside4)):
    if inside4[i]==False:
      points4[i,:]=None

outside4 = inside4[:]==False
ins4= np.logical_not(outside4)

# Finally we will remove these from the data set
points_clean1 = points1[ins1,:]
points_clean2 = points2[ins2,:]
points_clean3 = points3[ins3,:]
points_clean4 = points4[ins4,:]

# n_WT = len(points1+points2+points3+points4)
# production = n_WT*14

plt.scatter(polygon[:,0],polygon[:,1])
plt.scatter(points_clean1[:,0],points_clean1[:,1])
plt.scatter(points_clean2[:,0],points_clean2[:,1])
plt.scatter(points_clean3[:,0],points_clean3[:,1])
plt.scatter(points_clean4[:,0],points_clean4[:,1])
#plt.gca().invert_xaxis()
plt.show()


# print(points_clean)

df1 = pd.DataFrame(points_clean1)
df1.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw_cluster1.xlsx", header="Cluster1", index=False)

df2 = pd.DataFrame(points_clean2)
df2.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw_cluster2.xlsx", header="Cluster2", index=False)

df3 = pd.DataFrame(points_clean3)
df3.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw_cluster3.xlsx", header="Cluster3", index=False)

df4 = pd.DataFrame(points_clean4)
df4.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw_cluster4.xlsx", header="Cluster4", index=False)
