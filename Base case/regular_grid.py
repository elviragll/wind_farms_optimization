# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 13:51:59 2022

@author: elvir
"""

import numpy as np
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
import pandas as pd


#UTM coordinates:
    #https://coordinates-converter.com/en/decimal/51.536000,-10.062008?karte=OpenStreetMap&zoom=8

pointA = (417010.23, 5708588.888)
pointB= (455073.235, 5692304.918)
pointC = (451895.787,5683361.623)
pointD = (441037.275,5681680.286)
pointE= (439036.758,5670883.073)
pointF = (416471.458,5671303.56)


polygon =np.array([pointA, pointB, pointC, pointD, pointE, pointF])

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
points=np.array((xx.ravel(), yy.ravel())).T




path = mpltPath.Path(polygon)
inside = path.contains_points(points)


for i in range(len(inside)):
    if inside[i]==False:
      points[i,:]=None

outside = inside[:]==False
inside2= np.logical_not(outside)

# Finally we will remove these from the data set
points_clean = points[inside2,:]

n_WT = len(points_clean)
production = n_WT*14

plt.scatter(polygon[:,0],polygon[:,1])
plt.scatter(points[:,0],points[:,1])
plt.gca().invert_xaxis()
plt.show()


print(points_clean)

df = pd.DataFrame(points_clean)
df.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw.xlsx", header=False, index=False)
