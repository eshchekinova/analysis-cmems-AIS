"""Select Copernicus data according to AIS tracking data

"""
import pandas as pd
import argparse
from pathlib import Path
import xarray as xr
import numpy as np
import os
import readOceanCMEMS as rdo_cmems
import extractTrajAIS as exr_traj_ais


def create_dataframe_BufferAIS(file_name,base_dir,size_buff,size_margin, ocean_dir_in, wave_dir_in, \
    variables_ocean_model, variables_wave_model):

    # Read from AIS data for Baltic Sea

    # extract AIS data into dataframe
    df_trajs = exr_traj_ais.readAIS2df(file_name)
    # get mean latitude and longitude for every vessel trajectories
    lat_mean_AIS = df_trajs["LATITUDE"]
    lon_mean_AIS = df_trajs["LONGITUDE"]
    
    # read ocean and wave model data into dateframe structures
    df_ocean, df_wave  = rdo_cmems.readOcean(base_dir, ocean_dir_in, wave_dir_in, \
                                            variables_ocean_model,variables_wave_model)


    # set margin around region of interest in degrees

    inc_lat = 5
    inc_lon = 5

    lat_ocean = np.unique(df_ocean[variables_ocean_model[0]].index.get_level_values(1)[0:-1].values)
    lon_ocean = np.unique(df_ocean[variables_ocean_model[0]].index.get_level_values(2)[0:-1].values)
    lat_wave = np.unique(df_wave[variables_wave_model[0]].index.get_level_values(1)[0:-1].values)
    lon_wave = np.unique(df_wave[variables_wave_model[0]].index.get_level_values(2)[0:-1].values)

    # set boundaries for convex region that includes AIS trajectory
    lat_view_min = lat_mean_AIS.min() - inc_lat
    lat_view_max = lat_mean_AIS.max() + inc_lat
    lon_view_min = lon_mean_AIS.min() - inc_lon
    lon_view_max = lon_mean_AIS.max() + inc_lon

    # get size of ocean, wave latitute, longitude grid
    delta_lat_wave = abs(lat_wave[1]-lat_wave[0])
    delta_lat_ocean = abs(lat_ocean[1]-lat_ocean[0])
    delta_lon_wave = abs(lon_wave[1]-lon_wave[0])
    delta_lon_ocean = abs(lon_ocean[1]-lon_ocean[0])

    # get ocean, wave data for local convex area including AIS tracks
    #print(df_ocean.loc[lambda df_ocean: abs(df_ocean[variables_ocean_model[0]].index.get_level_values(2))<10])

    #print(df_wave.loc[lambda df_wave: (df_wave[variables_wave_model[0]].index.get_level_values(1)<lat_view_max) & \
    #                   (df_wave[variables_wave_model[0]].index.get_level_values(1)>lat_view_min)])
    df_ocean_slct=df_ocean.loc[lambda df_ocean: (df_ocean[variables_ocean_model[0]].index.get_level_values(1)<lat_view_max) & \
                       (df_ocean[variables_ocean_model[0]].index.get_level_values(1)>lat_view_min) & \
                       (df_ocean[variables_ocean_model[0]].index.get_level_values(2)<lon_view_max) & \
                       (df_ocean[variables_ocean_model[0]].index.get_level_values(2)>lon_view_min)]

    df_wave_slct=df_wave.loc[lambda df_wave: (df_wave[variables_wave_model[0]].index.get_level_values(0)<lat_view_max) & \
                       (df_wave[variables_wave_model[0]].index.get_level_values(0)>lat_view_min) & \
                       (df_wave[variables_wave_model[0]].index.get_level_values(1)<lon_view_max) & \
                       (df_wave[variables_wave_model[0]].index.get_level_values(1)>lon_view_min)]
    del df_ocean, df_wave

    print(df_ocean_slct)
    # select ocean, wave data for a given AIS trajectory
    df_ocean_traj_slct=df_ocean_slct.loc[lambda df_ocean_slct: [(abs(df_ocean_slct[variables_ocean_model[0]].index.get_level_values(1)-\
                       lat_mean_AIS[i])<delta_lat_ocean for i in range(len(lat_mean_AIS)))]]
    df_ocean_traj_slct=df_ocean_traj_slct.loc[lambda df_ocean_traj_slct: [(abs(df_ocean_traj_slct[variables_ocean_model[0]].index.get_level_values(2)-\
                       lon_mean_AIS[i])<delta_lon_ocean for i in range(len(lon_mean_AIS)))]]
    df_wave_traj_slct=df_wave_slct.loc[lambda df_wave_slct: [(abs(df_wave_slct[variables_wave_model[0]].index.get_level_values(1)-\
                       lat_mean_AIS[i])<delta_lat_wave for i in range(len(lat_mean_AIS)))]]
    df_wave_traj_slct=df_wave_traj_slct.loc[lambda df_wave_traj_slct: [(abs(df_wave_traj_slct[variables_wave_model[0]].index.get_level_values(2)-\
                       lon_mean_AIS[i])<delta_lon_ocean for i in range(len(lon_mean_AIS)))]]

    return df_wave_traj_slct,df_ocean_traj_slct,df_ocean_slct, df_wave_slct
