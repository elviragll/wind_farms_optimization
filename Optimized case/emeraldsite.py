# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 15:26:52 2022

@author: elvir
"""


#Emerald site
#data taken from regular_grid and WTpowerCurves

import numpy as np
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
from py_wake.site.xrsite import GlobalWindAtlasSite

wt_x = [419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 444044.1558571428,
 446801.42564285715,
 449558.69542857143,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 444044.1558571428,
 446801.42564285715,
 449558.69542857143,
 452315.9652142857,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 444044.1558571428,
 446801.42564285715,
 449558.69542857143,
 452315.9652142857,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 444044.1558571428,
 446801.42564285715,
 449558.69542857143,
 452315.9652142857,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 444044.1558571428,
 446801.42564285715,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 438529.61628571426,
 441286.88607142854,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 430257.80692857143,
 433015.0767142857,
 435772.3465,
 419228.72778571426,
 421985.99757142854,
 424743.2673571428,
 427500.53714285715,
 419228.72778571426,
 421985.99757142854]
wt_y = [5673576.3455,
 5673576.3455,
 5673576.3455,
 5673576.3455,
 5673576.3455,
 5673576.3455,
 5673576.3455,
 5673576.3455,
 5676269.618,
 5676269.618,
 5676269.618,
 5676269.618,
 5676269.618,
 5676269.618,
 5676269.618,
 5676269.618,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5678962.8905,
 5681656.163,
 5681656.163,
 5681656.163,
 5681656.163,
 5681656.163,
 5681656.163,
 5681656.163,
 5681656.163,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5684349.4355,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5687042.708,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5689735.9805,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5692429.2530000005,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5695122.5255,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5697815.798,
 5700509.0705,
 5700509.0705,
 5700509.0705,
 5700509.0705,
 5700509.0705,
 5700509.0705,
 5700509.0705,
 5703202.343,
 5703202.343,
 5703202.343,
 5703202.343,
 5705895.6155,
 5705895.6155]



power_curve = np.array([[3.0, 207056],
                        [4.0, 671160],
                        [5.0, 1.43641e+06],
                        [6.0, 2.57801e+06],
                        [7.0, 4.17124e+06],
                        [8.0, 6.29058e+06],
                        [9.0, 8.93878e+06],
                        [10.0, 1.15431e+07],
                        [11.0, 1.31506e+07],
                        [12.0, 1.37747e+07],
                        [13.0, 1.39492e+07],
                        [14.0, 1.39894e+07],
                        [15.0, 1.39978e+07],
                        [16.0, 1.39995e+07],
                        [17.0, 1.39999e+07],
                        [18.0, 1.4e+07],
                        [19.0, 1.4e+07],
                        [20.0, 1.4e+07],
                        [21.0, 1.4e+07],
                        [22.0, 1.4e+07],
                        [23.0, 1.4e+07],
                        [24.0, 1.4e+07],
                        [25.0, 1.4e+07]])



class SG14(WindTurbine):
    def __init__(self, method='linear'):
        """
        Parameters
        ----------
        method : {'linear', 'pchip'}
            linear(fast) or pchip(smooth and gradient friendly) interpolation
        """
        WindTurbine.__init__(self, name='SG14', diameter=236, hub_height=150,
                             powerCtFunction= GenericWindTurbine(name='SG14',
                                                        diameter = 236, 
                                                        hub_height = 150, 
                                                        power_norm = 1.4e+07).powerCtFunction  
                             )


#HornsrevV80 = V80
EmeraldWT = SG14

EmeraldSite= GlobalWindAtlasSite(lat=51.316881, long= -8.01693, height= 150,roughness= 0.1, ti=0.1)

def main():
    wt = SG14()
    print('Diameter', wt.diameter())
    print('Hub height', wt.hub_height())

    import matplotlib.pyplot as plt
    ws = np.linspace(3, 20, 100)
    plt.plot(ws, wt.power(ws) * 1e-3, label='Power')
    c = plt.plot([], [], label='Ct')[0].get_color()
    plt.ylabel('Power [kW]')
    ax = plt.gca().twinx()
    ax.plot(ws, wt.ct(ws), color=c)
    ax.set_ylabel('Ct')
    plt.xlabel('Wind speed [m/s]')
    plt.gcf().axes[0].legend(loc=1)
    plt.show()


if __name__ == '__main__':
    main()
