
import sys
import os
import numpy as np
import pandas as pd
from scipy.io import readsav
from scipy.interpolate import interp1d, splev, splrep
from astropy.modeling.models import custom_model
from astropy.modeling.fitting import LevMarLSQFitter


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


dirsen = '/Users/iz19726/Documents/ExoTiC/ExoTiC-ISM/Limb-darkening/'

direc = os.path.join(dirsen, 'Kurucz')

print('Current Directories Entered:')
print('  ' + dirsen)
print('  ' + direc)
# Determine which model is to be used, the input metallicity M_H is later used to figure out the file name we need
direc = 'Kurucz'
file_list = 'kuruczlist.sav'
sav1 = readsav(os.path.join(dirsen, file_list))

# Select metallicity values above and below the input value. If input matches a value that is taken as the lower value in the interpolation grid.
M_H_Grid = np.array([-5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.5, 1.0])
M_H_Grid_load = np.array([14, 13, 12, 11, 10, 9, 8, 7, 5, 3, 2, 1, 0, 17, 20, 21, 22, 23, 24])

list_of_MH_Teff_logg = []

for metal in range(len(M_H_Grid)):

    model = bytes.decode(sav1['li'][M_H_Grid_load[metal]])  # Convert object of type "byte" to "string"

    # Work out how long the file is
    filename = os.path.join(dirsen, direc, model)
    total_len = file_len(filename)

    # data_index goes from 0 to end of file/length of each data chunk
    header_rows = 3    #  How many rows in each section we ignore for the data reading
    data_rows = 1221   # How  many rows of data we read

    len_file = int(total_len / (header_rows + data_rows))

    print(len_file)

    Teff_model_grid = np.empty(len_file, float)
    logg_model_grid = np.empty(len_file, float)
    for i in range(0, len_file):

        line_skip_header = (data_rows + header_rows) * i

        headerinfo = pd.read_csv(os.path.join(dirsen, direc, model), delim_whitespace=True, header=None,
                                 skiprows=line_skip_header, nrows=1)

        Teff_model_grid[i] = headerinfo[1].values[0]
        logg_model_grid[i] = headerinfo[3].values[0]

    Teff_logg_grid = np.array([Teff_model_grid,logg_model_grid])
    list_of_MH_Teff_logg.append(Teff_logg_grid)

savefilename = os.path.join(dirsen,direc,'ld_parameter_grids.npz')
print(savefilename)
np.savez(savefilename, *list_of_MH_Teff_logg)


