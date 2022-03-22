# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:43:16 2022

@author: elvir
"""
from  get_gwc_data import get_gwc
import numpy as np
from requests import get

url_str=f'https://globalwindatlas.info/api/gis/country/IRL/combined-Weibull-A/150'
test=get(url_str)
def _read_float_(f):
    return [np.float32(i) for i in f.strip().split()]

def _read_int_(f):
    return [np.int32(i) for i in f.strip().split()]

txt = test.split('\r\n')
print(txt[1])
# Read header information one line at a time
desc = txt[0].strip()  # File Description
# nrough, nhgt, nsec = _read_int_(txt[1])  # dimensions
roughnesses = _read_float_(txt[2])  # Roughness classes
heights = _read_float_(txt[3])  # heights

def _read_float_(f):
    return [np.float32(i) for i in f.strip().split()]

def _read_int_(f):
    return [np.int32(i) for i in f.strip().split()]