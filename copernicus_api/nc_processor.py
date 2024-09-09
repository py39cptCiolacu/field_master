import netCDF4
import numpy as np


def process_nc(file_path : str) -> None:

    nc_file = netCDF4.Dataset(file_path, mode = 'r')

    