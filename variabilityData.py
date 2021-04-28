"""Conversion from netcdf to zarr_store using xarray and zarr.

"""

import argparse
import pandas as pd
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import os


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


# run test
test_xr_time_coord_to_day_string()


if __name__ == "__main__":
    # get base directory
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--basedir",
        default=".",
        help=(
            "Base directory where the data dirs will be found." "\nDefaults to $PWD."
        ),
    )
    parser.add_argument(
        "--product_id",
        default="global-reanalysis-phy-001-030-daily",
        help=(
            "Product ID."
            "\nDefaults to global-reanalysis-phy-001-030-daily."
        ),
    )
    parser.add_argument(
        "--var", action="append", help="<Required> Add variable", required=False
    )

    args = parser.parse_args()
    base_dir = Path(args.basedir)

    # set data analysis directory
    dir_analysis = base_dir/"analysis"

    if args.var is not None:
        variables = args.var
    else:
        variables = []
    product_id = args.product_id

    # set input and output paths
    path_in_dir = base_dir / product_id / "nc"
    path_out_dir_nc = dir_analysis / product_id /"nc"
    path_out_dir_figures = dir_analysis / product_id /"figures"

    # make sure the output dir exists
    path_out_dir_nc.mkdir(parents=True, exist_ok=True)
    path_out_dir_figures.mkdir(parents=True, exist_ok=True)

    # make analysis of mean and std statistics for every variable
    for variable_name in variables:
        # select files containing variable {variable_name}
        input_files = sorted(path_in_dir.glob(f"*{variable_name}*.nc"))

        # convert files in nc directory to dataset using xarray
        ds = xr.open_mfdataset(
            input_files,
            parallel=True,
            concat_dim="time",
            data_vars="minimal",
            combine="nested",
        )

        # calculate mean var_mean and std var_std of every variable for the entire time interval
        var_mean = ds.mean(dim='time',skipna=None)
        #var_mean[f"{variable_name}"]=var_mean[variable_name]
        #var_mean[f"{variable_name}_mean"].attrs = var_mean[f"{variable_name}"].attrs
        #var_mean = var_mean.drop([variable_name])

        var_std = ds.std(dim='time',skipna=None)
        #var_std[f"{variable_name}_std"]=var_std[variable_name]
        #var_std[f"{variable_name}_std"].attrs = var_std[f"{variable_name}"].attrs
        #var_std = var_std.drop([variable_name])

    #    var_std = ds.std(dim='time',skipna=None)
    #    ds_std_mean = var_mean.merge(var_std)

        start_day = xr_time_coord_to_day_string(ds.time.min())
        end_day = xr_time_coord_to_day_string(ds.time.max())

        # save mean and std in .nc file

        #f"{product_id}_{variable_name}_{start_day}_{end_day}.nc"
        file_name_out = f"{variable_name}_mean_{start_day}_{end_day}.nc"
        var_mean.to_netcdf(path=f"{path_out_dir_nc}/{file_name_out}", mode='w')

        file_name_out = f"{variable_name}_std_{start_day}_{end_day}.nc"
        var_std.to_netcdf(path=f"{path_out_dir_nc}/{file_name_out}", mode='w')
        # plot mean and std of .nc for given time period

        fig, (ax1, ax2) = plt.subplots(ncols=2)
        #plt.figure(figsize=(7,7));

        ax1=plt.axes(projection=ccrs.PlateCarree());
        #var_mean.to_array().plot.pcolormesh(cmap='RdBu_r')
        var_mean[variable_name].isel(depth=0).plot(ax=ax1, x='longitude', y='latitude')

        ax1=plt.title(f"Mean of {variable_name},\n {start_day}-{end_day}")
        ax1=plt.xlabel("Longitude[degrees_east]")
        ax1=plt.ylabel("Latitute[degrees_north]")
        ax1.coastlines();

        var_std[variable_name].isel(depth=0).plot(ax=ax2, x='longitude', y='latitude')

        ax2 = plt.axes(projection=ccrs.PlateCarree());
        ax2=plt.title(f"Std of {variable_name},\n {start_day}-{end_day}")
        ax2=plt.xlabel("Longitude[degrees_east]")
        ax2=plt.ylabel("Latitute[degrees_north]")
        ax2.coastlines();

        os.chdir(path_out_dir_figures)
        plt.draw()
        # save figures to separate directory in .png file
        # mean_std_{product_id}_{variable_name}_{start_day}_{end_day}.png
        plt.savefig(f"mean_std_{product_id}_{variable_name}_{start_day}_{end_day}.png")
