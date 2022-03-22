# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:56:55 2022

@author: elvir
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine
wt_14 = GenericWindTurbine('G14MW', 236, 150, power_norm=14000, turbulence_intensity=.1)
wt_15 = GenericWindTurbine('G15MW', 236, 150, power_norm=15000, turbulence_intensity=.1)
wt_18 = GenericWindTurbine('G18MW', 258, 160, power_norm=18000, turbulence_intensity=.1)
wt_20 = GenericWindTurbine('G20MW', 273, 175, power_norm=20000, turbulence_intensity=.1)
wt_22 = GenericWindTurbine('G22MW', 286, 185, power_norm=22000, turbulence_intensity=.1)

#assuming that the swept area is proportional to the nominal power, Pnom has a cuadratic relationship with the diameter


ws = np.arange(3,25)
plt.xlabel('Wind speed [m/s]')
plt.ylabel('Power [kW]')


plt.plot(ws, wt_14.power(ws)*1e-3,'.-', label=wt_14.name())
plt.plot(ws, wt_15.power(ws)*1e-3,'.-', label=wt_15.name())
plt.plot(ws, wt_18.power(ws)*1e-3,'.-', label=wt_18.name())
plt.plot(ws, wt_20.power(ws)*1e-3,'.-', label=wt_20.name())
plt.plot(ws, wt_22.power(ws)*1e-3,'.-', label=wt_22.name())
plt.legend(loc=1)

wt= np.transpose(np.array([wt_14.power(ws)*1e-3,wt_15.power(ws)*1e-3,wt_18.power(ws)*1e-3,wt_20.power(ws)*1e-3,wt_22.power(ws)*1e-3]))

df = pd.DataFrame({'Wind speed[m/s]': ws[:], 'Power[kW]  WT14MW': wt[:, 0], 'Power [kW]  WT15MW': wt[:, 1], 'Power[kW]  WT18MW': wt[:, 2], 'Power[kW]  WT20MW': wt[:, 3], 'Power[kW]  WT22MW': wt[:, 4]})
df.to_excel('WTpowercurve.xlsx')


plt.plot(ws, wt_14.thrust(ws)*1e-3,'.-', label=wt_14.name())