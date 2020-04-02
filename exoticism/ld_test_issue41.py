import sys
import os
import numpy as np 
import limb_darkening as ld

# LIMB DARKENING
M_H = -4.0    # stellar metallicity - limited ranges available
Teff = 6100   # stellar temperature - for 1D models: steps of 250 starting at 3500 and ending at 6500
logg = 4.32  # log(g), stellar gravity - depends on whether 1D or 3D limb darkening models are used
grating = 'G141'
wsdata = np.loadtxt('../data/W17/W17_G141_wavelength_test_data.txt', skiprows=3)

print(wsdata.shape)

dirsen = '/Users/iz19726/Documents/ExoTiC/ExoTiC-ISM/Limb-darkening/'

result = ld.limb_dark_fit(grating, wsdata, M_H, Teff, logg, dirsen, ld_model='1D')
print(result)
