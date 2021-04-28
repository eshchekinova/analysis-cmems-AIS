"""Plot ocean data and trajectories

"""

import argparse
import pandas as pd
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import os
import geoviews as gv
import holoviews as hv
import hvplot.pandas
from IPython.display import display
from IPython.core.display import Image
import cartopy
import datashader
import cartopy.crs as ccrs
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

def xr_time_coord_to_day_string(time):
    dt = pd.to_datetime(time.data)
    dt = dt.to_pydatetime()
    return dt.strftime("%Y-%m-%d")


# a quick test: Ensure that the above function returns the correct
# day string for a known time stamp
def test_xr_time_coord_to_day_string():
    """Test functionality of xr_time_coord_to_day_string.

    Ensure that the above function returns the correct
    day string for a known time stamp."""
    assert "2001-01-23" == xr_time_coord_to_day_string(
        xr.DataArray(pd.Timestamp("2001-01-23T01:23:45Z"))
    )
def fun_vel_dir()

    x =
    return

def reg_plot(dir_figures, lat_AIS, lon_AIS, draught,vsl_type, df_ocean_lense):

    # calculate ocean currents magnitude and direction
    mer_curr = df_ocean_lense['uo']
    zon_curr = df_ocean_lense['vo']
    vel_curr = np.sqrt(mer_curr**2 + zon_curr**2)
    dir_curr = np.arcsin(zon_curr/mer_curr)

    # make sure the output dir exists
    dir_figures.mkdir(parents=True, exist_ok=True)

    fig, (ax1, ax2) = plt.subplots(ncols=2)
    # plt.figure(figsize=(7,7));

    ax1 = plt.axes(projection=ccrs.PlateCarree())

    #    ax1=plt.title(f"Mean of {variable_name},\n {start_day}-{end_day}")
    ax1 = plt.xlabel("Longitude[degrees_east]")
    ax1 = plt.ylabel("Latitute[degrees_north]")

    dfr_traj = pd.DataFrame({'LONGITUDE' : lon_AIS, 'LATITUDE': lat_AIS})


    # dfr_traj.plot(ax=ax2, x='longitude', y='latitude')
    # ax2 = plt.axes(projection=ccrs.PlateCarree());
    # ax2=plt.title(f"Std of {variable_name},\n {start_day}-{end_day}")
    # ax2=plt.xlabel("Longitude[degrees_east]")
    # ax2=plt.ylabel("Latitute[degrees_north]")
    # ax2.coastlines();
    data_plot = (
          dfr_traj.hvplot.points(
              x="LONGITUDE", y="LATITUDE", geo=True, datashade=True,
              hover=False,
              frame_height=350, frame_width=350,
          )
          * gv.feature.coastline(scale='50m')
    )
    display(data_plot)
    df_ocean_lense.hvplot.contourf(z = 'uo',x='LONGITUDE', y='LATITUDE'
        levels=20, geo=True,
        coastline=True,
        widget_location='left_top'
    )

    display(data_ocean)
    os.chdir(dir_figures)
    # save figures to separate directory in .png file
    # mean_std_{product_id}_{variable_name}_{start_day}_{end_day}.png
    hvplot.save(data_plot, 'Traj.png')
