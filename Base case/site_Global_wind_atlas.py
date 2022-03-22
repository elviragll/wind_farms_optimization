# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:45:39 2022

@author: elvir
"""


import numpy as np
from numpy import newaxis as na
import xarray as xr
from py_wake.site.xrsite import XRSite
import urllib.request
from py_wake.site._site import Site
import matplotlib as plt



#Code created to obtain quickly the wind parameters of the Weibull function using Global wind atlas

class GlobalWindAtlasSite(XRSite):
    """Site with Global Wind Climate (GWC) from the Global Wind Atlas based on
    lat and long which is interpolated at specific roughness and height.
    NOTE: This approach is only valid for sites with homogeneous roughness at the site and far around
    """

    def __init__(self, lat, long, height, roughness, ti=None, **kwargs):
        """
        Parameters
        ----------
        lat: float
            Latitude of the location
        long: float
            Longitude of the location
        height: float
            Height of the location
        roughness: float
            roughness length at the location
        """
        self.gwc_ds = self._read_gwc(lat, long)
        if ti is not None:
            self.gwc_ds['TI'] = ti
        XRSite.__init__(self, ds=self.gwc_ds.interp(height=height, roughness=roughness), **kwargs)

    def _read_gwc(self, lat, long):

        url_str = f'https://wps.globalwindatlas.info/?service=WPS&VERSION=1.0.0&REQUEST=Execute&IDENTIFIER=get_libfile&DataInputs=location={{"type":"Point","coordinates":[{long},{lat}]}}'
        s = urllib.request.urlopen(url_str).read().decode()  # response contains link to generated file
        url = s[s.index('http://wps.globalwindatlas.info'):].split('"')[0]
        lines = urllib.request.urlopen(url).read().decode().strip().split("\r\n")

        # Read header information one line at a time
        # desc = txt[0].strip()  # File Description
        nrough, nhgt, nsec = map(int, lines[1].split())  # dimensions
        roughnesses = np.array(lines[2].split(), dtype=float)  # Roughness classes
        heights = np.array(lines[3].split(), dtype=float)  # heights
        data = np.array([l.split() for l in lines[4:]], dtype=float).reshape((nrough, nhgt * 2 + 1, nsec))
        freq = data[:, 0] / data[:, 0].sum(1)[:, na]
        A = data[:, 1::2]
        k = data[:, 2::2]
        ds = xr.Dataset({'Weibull_A': (["roughness", "height", "wd"], A),
                          'Weibull_k': (["roughness", "height", "wd"], k),
                          "Sector_frequency": (["roughness", "wd"], freq)},
                        coords={"height": heights, "roughness": roughnesses,
                                "wd": np.linspace(0, 360, nsec, endpoint=False)})
        return ds



point= GlobalWindAtlasSite(51.316881, -8.01693, 150, 0.1)

A=np.array(point.ds.Weibull_A)
k=np.array(point.ds.Weibull_k)
f=np.array(point.ds.Sector_frequency)


