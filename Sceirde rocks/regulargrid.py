# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:47:46 2022

@author: elvir
"""

import numpy as np
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt


#UTM coordinates:
    #https://coordinates-converter.com/en/decimal/51.536000,-10.062008?karte=OpenStreetMap&zoom=8

pointA = (-431718.995, 5902849.540)
pointB= (-436365.363, 5899028.270)
pointC = (-438457.961,5902633.499)
pointD = (-435441.476,5905479.446)

polygon =np.array([pointA, pointB, pointC, pointD])

# distance_D = 7
# diameter = 236
# distance = distance_D*diameter

n_WT = 16

xmin, xmax = (min(polygon[:,0]), max(polygon[:,0]))
# interval_x = round((xmax-xmin)/distance)
interval_x = 7
ymin, ymax = (min(polygon[:,1]), max(polygon[:,1]))
# interval_y = round((ymax-ymin)/distance)
interval_y = 7

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
# n_WT = len(points_clean)
production = n_WT*20

plt.scatter(polygon[:,0],polygon[:,1])
plt.scatter(points_clean[:,0],points_clean[:,1])
plt.gca().invert_xaxis()
plt.show()

# df = pd.DataFrame(points_clean)
# df.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw.xlsx", header=False, index=False)
