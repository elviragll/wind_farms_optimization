# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:21:59 2022

@author: elvir
"""

#Sceirde rocks site
#data taken from regular_grid and WTpowerCurves

import numpy as np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
import numpy as np
import matplotlib.path as mpltPath
import matplotlib.pyplot as plt
from py_wake.site.xrsite import GlobalWindAtlasSite
from py_wake.deficit_models.gaussian import IEA37SimpleBastankhahGaussian
from topfarm.cost_models.cost_model_wrappers import CostModelComponent
from topfarm.easy_drivers import EasyScipyOptimizeDriver
from topfarm.constraint_components.spacing import SpacingConstraint
from topfarm.constraint_components.boundary import XYBoundaryConstraint
import topfarm
from topfarm.plotting import XYPlotComp
from topfarm._topfarm import TopFarmProblem
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

# plt.scatter(polygon[:,0],polygon[:,1])
# plt.scatter(points_clean[:,0],points_clean[:,1])
# plt.gca().invert_xaxis()
# plt.show()

# df = pd.DataFrame(points_clean)
# df.to_excel(excel_writer = r"C:\Users\elvir\OneDrive - Danmarks Tekniske Universitet\Master thesis\Base case\Coordinates_raw.xlsx", header=False, index=False)

wt_x = points_clean[:,0].tolist()
wt_x = np.array(wt_x)[:n_WT]
wt_y = points_clean[:,1].tolist()
wt_y = np.array(wt_y)[:n_WT]

height=175
diameter=273
wt_20 = GenericWindTurbine('WT20MW', diameter, height, power_norm=20000, turbulence_intensity=.1)
ws = np.arange(3,25)
power_curve = np.column_stack((ws,wt_20.power(ws)))



class WT20(WindTurbine):
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        WindTurbine.__init__(self, name='WT20MW', diameter=diameter, hub_height=height,
                             powerCtFunction= wt_20.powerCtFunction  
                             )

#here to put the coordinates of the place
site= GlobalWindAtlasSite(lat=53.236719, long= -9.953444, height= height ,roughness= 0.1, ti=0.1)


def aep_func(x,y):
    wake_model = IEA37SimpleBastankhahGaussian(site, WT20())
    aep = wake_model(x,y).aep().sum()

    return aep

cost_comp = CostModelComponent(input_keys=['x','y'], 
                                n_wt=n_WT, 
                                cost_function=aep_func,
                                output_key="AEP", 
                                output_unit="GWh",
                                maximize=True)

# cost_comp=PyWakeGrad(n_wt=n_wt, method=method)

plot_comp = XYPlotComp()
    
tf = TopFarmProblem(
                design_vars={topfarm.x_key: wt_x,
                            topfarm.y_key: wt_y,
                                    },            
                cost_comp=cost_comp,
                driver=EasyScipyOptimizeDriver(optimizer='SLSQP', maxiter=1000, tol=1E-07),
                constraints=[XYBoundaryConstraint(polygon, 'polygon'), SpacingConstraint(min_spacing=diameter*7)],
                plot_comp=XYPlotComp())
    
cost, state, recorder = tf.optimize(disp=True)

# rec_file_name = f'{"Optimizedcase"}_{n_wt}'  
# recorder.save(rec_file_name)
            
# plt.savefig(f'{"Optimizedcase"}_{n_wt}_tfc.png')