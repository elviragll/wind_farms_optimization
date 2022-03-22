# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 13:43:25 2022

@author: elvir
"""

## Optimized grid: gradient based

from emeraldsite_clusters import EmeraldSite, SG14, wt_x1, wt_y1
from topfarm._topfarm import TopFarmProblem
from topfarm.plotting import XYPlotComp, NoPlot
from py_wake.deficit_models.gaussian import IEA37SimpleBastankhahGaussian
import topfarm
import numpy as np
import matplotlib.pylab as plt
from topfarm.constraint_components.spacing import SpacingConstraint
from topfarm.constraint_components.boundary import XYBoundaryConstraint
from topfarm.easy_drivers import EasyScipyOptimizeDriver, EasyRandomSearchDriver
# from pywakegrad1 import PyWakeGrad
from topfarm.cost_models.cost_model_wrappers import CostModelComponent

# Defining wind turbine object
windTurbines = SG14()


# Define the boundaries

pointA = (-417010.23, 5708588.888)
pointB= (-455073.235, 5692304.918)
pointC = (-451895.787,5683361.623)
pointD = (-441037.275,5681680.286)
pointE= (-439036.758,5670883.073)
pointF = (-416471.458,5671303.56)

pointAB=((pointA[0]+pointB[0])/2, (pointA[1]+pointB[1])/2)
pointL = ((pointAB[0]+pointD[0])/2, (pointAB[1]+pointD[1])/2)
pointM = ((pointA[0]+pointF[0]*2)/3, (pointA[1]+pointF[1]*2)/3)
pointN = ((pointF[0]+pointA[0]*2)/3, (pointF[1]+pointA[1]*2)/3)

#we create four different clusters

boundary1 = np.array([(pointA),(pointAB),(pointL),
                    (pointN)])
boundary2 = np.array([(pointN),(pointL),(pointD),
                    (pointM)])
boundary3 = np.array([(pointM),(pointD),(pointE),
                    (pointF)])

boundary4= np.array([(pointAB),(pointB),(pointC),
                    (pointD)])

boundary=[boundary1, boundary2, boundary3, boundary4]


# Define the site object
site = EmeraldSite


#Optimizing cluster 1
wtx= wt_x1
wty= wt_y1
wtx= np.array(wtx)[:15]
wty= np.array(wty)[:15]

n_wt=len(wtx)

def aep_func(x,y):
    wake_model = IEA37SimpleBastankhahGaussian(site, windTurbines)
    aep = wake_model(x,y).aep().sum()

    return aep


cost_comp = CostModelComponent(input_keys=['x','y'], 
                                n_wt=n_wt, 
                                cost_function=aep_func,
                                output_key="AEP", 
                                output_unit="GWh",
                                maximize=True)

# cost_comp=PyWakeGrad(n_wt=n_wt, method=method)

plot_comp = XYPlotComp()
    
tf = TopFarmProblem(
                design_vars={topfarm.x_key: wtx,
                            topfarm.y_key: wty,
                                    },            
                cost_comp=cost_comp,
                driver=EasyScipyOptimizeDriver(optimizer='SLSQP', maxiter=1000, tol=1E-08),
                constraints=[XYBoundaryConstraint(boundary1, 'polygon'), SpacingConstraint(min_spacing=236*7)],
                plot_comp=XYPlotComp())
    
cost, state, recorder = tf.optimize(disp=True)

# rec_file_name = f'{"Optimizedcase"}_{n_wt}'  
# recorder.save(rec_file_name)
            
# plt.savefig(f'{"Optimizedcase"}_{n_wt}_tfc.png')


