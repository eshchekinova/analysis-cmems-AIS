"""Select Copernicus data according to AIS tracking data

"""
import pandas as pd
import argparse
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import os
from selenium import webdriver
import readOceanCMEMS as rdo_cmems
import extractTrajAIS as exr_traj_ais
import selectcmemsAIS2015 as slc_cmemsAIS
import plotDataAIS as plt_ais

#def distance_convert(dist_km):
#    one = 111
#    lat_size = dist_km
#    return lat_size, long_size


if __name__ == "__main__":
      # file name for AIS data
      file_name ="baltic-sea-ais-data-master/data/4vessels-30second-2015.csv.gz"

      # get base directory
      parser = argparse.ArgumentParser()
      parser.add_argument(
            "--basedir",
            default="./data2015",
            help=(
                   "Base directory where the data dirs will be found." "\nDefaults to $PWD."
            ),
      )
      parser.add_argument(
            "--ocean_product_id",
            default="global-reanalysis-phy-001-030-daily",
            help=(
                    "Product ID."
                    "\nDefaults to global-reanalysis-phy-001-030-daily."
            ),
      )
      parser.add_argument(
            "--wave_product_id",
            default="global-reanalysis-wav-001-032",
            help=(
                    "Product ID."
                    "\nDefaults to global-reanalysis-wav-001-032."
            ),
      )
      parser.add_argument(
            "--var", action="append", help="<Required> Add variable", required=False
      )
      parser.add_argument(
            "--buffer_size",
            default=10,
            help=(
                   "Buffering zone (in km) around AIS tracks in km."
            ),
      )
      parser.add_argument(
            "--margin_region",
            default=100,
            help=(
                   "Margin (in km) around convex region with AIS tracks."
            ),
      )

      args = parser.parse_args()
      base_dir = Path(args.basedir)
      size_buff = args.buffer_size
      size_margin = args.margin_region

      # set names of directories for ocean and wave models
      ocean_dir_in = Path(args.ocean_product_id)
      wave_dir_in = Path(args.wave_product_id)

      # set list of ocean and wave models variables
      variables_ocean_model = ['uo', 'vo'] # velocities in x direction, y direction
      variables_wave_model = ['VPED', 'VSDX', 'VSDY' ] #  VSDX, VSDY sea surface wave Stokes drift x direction, y direction

      # set data analysis directory
      dir_analysis = base_dir/"analysis"

      dir_analysis.mkdir(parents=True, exist_ok=True)

      # Check if directory with prepared ocean and wave fields extracted for local region and for a given AIS trajectory is non empty
      # if empty run function to extract and save local data into .csv format in dir_analysis folder
      if not os.listdir(dir_analysis):

          # Create dataframe structure for ocean and wave data
          df_wave_traj_slct,df_ocean_traj_slct,df_ocean_slct, df_wave_slct = \
              slc_cmemsAIS.create_dataframe_BufferAIS(file_name, base_dir,size_buff,size_margin, ocean_dir_in, wave_dir_in, \
              variables_ocean_model, variables_wave_model)

          df_wave_traj_slct.to_csv(dir_analysis/'wave_traj_slct.csv')
          df_ocean_traj_slct.to_csv(dir_analysis/'ocean_traj_slct.csv')
          df_ocean_slct.to_csv(dir_analysis/'wave_local.csv')
          df_wave_slct.to_csv(dir_analysis/'ocean_local.csv')
      else:
          df_wave_traj_slct = pd.read_csv(dir_analysis/'wave_traj_slct.csv')
          df_ocean_traj_slct = pd.read_csv(dir_analysis/'ocean_traj_slct.csv')
          df_ocean_slct = pd.read_csv(dir_analysis/'wave_local.csv')
          df_wave_slct = pd.read_csv(dir_analysis/'ocean_local.csv')

      # Plot Data
      # set directory for output figures
      path_out_dir_figures = base_dir /"figures"

      # Read from AIS data for Baltic Sea

      # extract AIS data into dataframe
      df_trajs = exr_traj_ais.readAIS2df(file_name)
      # get mean latitude and longitude for every vessel trajectories
      lat_mean_AIS = df_trajs["LATITUDE"]
      lon_mean_AIS = df_trajs["LONGITUDE"]

      # get vessel draught
      vessel_draught = df_trajs.groupby("IMO")["DRAUGHT"]
      vessel_type = df_trajs.groupby("IMO")["AISTYPE"]

      # Plot ocean data and AIS trajectories for a given region
      plt_ais.reg_plot(path_out_dir_figures,lat_mean_AIS,lon_mean_AIS,vessel_draught,vessel_type,df_ocean_traj_slct)
