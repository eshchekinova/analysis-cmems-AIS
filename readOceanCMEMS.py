"""Read Copernicus ocean and wave data model

"""
import pandas as pd
import argparse
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os

def create_df(dir_in, variables):
    # declare empty dataframe structure
    df = pd.DataFrame()
    # read model data from netcdf daily files
    for variable_name in variables:
        # select files containing variable {variable_name}
        input_files = sorted(dir_in.glob(f"*{variable_name}*.nc"))

        # convert files in nc directory to dataset using xarray
        nc_ds = xr.open_mfdataset(
            input_files,
            parallel=True,
            concat_dim="time",
            data_vars="minimal",
            combine="nested",
        )
        df = df.append(nc_ds.to_dataframe(),sort=True)
        #print(df['uo'].index, "True")
        #print(df.iloc[:, df['uo'].index.get_level_values(0)=='depth'])
        #var_def = df[variable_name].values[0:-1]
        #depth=df[variable_name].index.get_level_values(0)[0:-1].values
        #latitude=df[variable_name].index.get_level_values(1)[0:-1].values
        #longitude=df[variable_name].loc[df[variable_name].index.get_level_values(2)<18]
        #print(longitude)
        #time_ocean_mdl=df[variable_name].index.get_level_values(3)[0:-1].values
        #depth=df.loc(df.cell == 'depth')
        #df_depth=depth.to_dataframe()
        #print(len(depth))
    return df

def readOcean(base_dir, ocean_dir_in, wave_dir_in,vars_ocean,vars_wave):

    # Create dataframe structure for ocean and wave data
    # get directories for ocean dataset
    dir_in = base_dir / ocean_dir_in / "nc"

    dir_in.mkdir(parents=True, exist_ok=True)

    df_ocean = create_df(dir_in, vars_ocean)
    #print(df_ocean['uo'].index[0][1])
    #print(df_ocean['uo'].loc[['longitude'],:]<18)

    # get directories for wave dataset
    dir_in = base_dir / wave_dir_in / "nc"
    dir_in.mkdir(parents=True, exist_ok=True)

    df_wave = create_df(dir_in, vars_wave)
    return df_ocean, df_wave
