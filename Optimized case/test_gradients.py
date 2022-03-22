# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 16:42:54 2022

@author: elvir
"""

## Optimized grid: gradient based

from emeraldsite import SG14, EmeraldSite, wt_x, wt_y
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
from py_wake.site.xrsite import GlobalWindAtlasSite


# Defining wind turbine object
windTurbines = SG14()


# Define the boundaries

boundary = np.array([(-417010.23, 5708588.888),(-455073.235, 5692304.918),(-451895.787,5683361.623),
                    (-441037.275,5681680.286),(-439036.758,5670883.073),(-416471.458,5671303.56)])


# Define the site object
site = EmeraldSite



wtx= -1*np.array(wt_x)
wty= np.array(wt_y)
wtx= np.array(wtx)[[0, 1, 2, 8, 9, 10, 16, 17, 18]]
wty= np.array(wty)[[0, 1, 2, 8, 9, 10, 16, 17, 18]]

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
            driver=EasyScipyOptimizeDriver(optimizer='SLSQP', maxiter=5000, tol=1E-08),
           constraints=[XYBoundaryConstraint(boundary, 'polygon'), SpacingConstraint(min_spacing=236*7)],
            plot_comp=XYPlotComp())

cost, state, recorder = tf.optimize(disp=True)

rec_file_name = f'{"Optimizedcase"}_{n_wt}'  
recorder.save(rec_file_name)
            
plt.savefig(f'{"Optimizedcase"}_{n_wt}_tfc.png')
