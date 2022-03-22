from requests import get
import numpy as np
import xarray as xr

def get_gwc(lat, long):
    """Download the gwc file from globalwindatalas
    
    Parameters
    ----------
    lat: float
        Latitude of the location

    long: float
        Longitude of the location

    
    Returns
    -------
    txt: string
        gwc text file in a python string
    """
    url_str=f'https://globalwindatlas.info/api/gwa/custom/Lib/?lat={lat}&long={long}'
    resp = get(url_str)
    return resp.text
    
def _read_float_(f):
    """Reads a line of space separated data and splits it into floats

    Parameters
    ----------
    f : file
        Object with method readline

    Returns
    -------
    list
        List of floats
    """
    return [np.float32(i) for i in f.strip().split()]

def _read_int_(f):
    """Reads a line of space-separated data and splits it into integers

    Parameters
    ----------
    f : file
        Object with method readline

    Returns
    -------
    list
        List of integers
    """
    return [np.int32(i) for i in f.strip().split()]
    
def read_gwc(txt_gwc):
    """Reads the A,k and wind direction frequency from the gwc text

    Parameters
    ----------
    txt_gwc : string
        Object with method readline

    Returns
    -------
    ds  xarray.dataset
        dataset containing the wind rose
    """
    txt = txt_gwc.split('\r\n')
    # Read header information one line at a time
    desc = txt[0].strip()  # File Description
    nrough, nhgt, nsec = _read_int_(txt[1])  # dimensions
    roughnesses = _read_float_(txt[2])  # Roughness classes
    heights = _read_float_(txt[3])  # heights

    # Initialize arrays
    freq = np.zeros([nrough, nsec], dtype="f4", order="F")
    k = np.zeros([nhgt, nrough, nsec], dtype="f4", order="F")
    A = np.zeros([nhgt, nrough, nsec], dtype="f4")

    ##################################################################
    # The remainder of the file is made up of rows with nsec columns.
    # For each height there is first a frequency row, then pairs of
    # A & k rows for each height.
    ##################################################################
    # Loop over roughness classes to read frequency line
    ni = 3
    for i, dummy in enumerate(roughnesses):
        freq[i, :] = _read_float_(txt[ni+1+i*3])
        # Loop over heights to read in all A & k values
        for j, dummy in enumerate(heights):
            A[j, i, :] = _read_float_(txt[ni+2+i*3])
            k[j, i, :] = _read_float_(txt[ni+3+i*3])
            
    
    ds = xr.Dataset({'Weibull_A':(["height", "roughness", "sector"], A),
                       'Weibull_k':(["height", "roughness", "sector"], k),
                       "Sector_frequency":(["roughness", "sector"], freq)
                      }, coords={"height":heights, "roughness":roughnesses, "sector":list(range(12))})        

    return ds

def get_gwc_ds(lat, long):
    txt = get_gwc(lat, long)
    ds = read_gwc(txt)
    return ds