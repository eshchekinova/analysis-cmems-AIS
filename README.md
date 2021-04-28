# Analysis of CMEMS data according to AIS paths

## Overview

The data analysis include estimation of mean/std of currents for netcdf data product using any given
domain. The ocean data are selected from initial domain to include only Automated Identification System ([AIS](https://en.wikipedia.org/wiki/Automatic_identification_system)) paths and surrounding
distance (AIS provided in a tabular format) for given period of time.

## Description

Here variability of currents is evauated for the [Copernicus product data]
(https://resources.marine.copernicus.eu/?option=com_csw&task=results) for year 2015, visualization
of mean/std values for the domain is given using Matplotlib and Cartopy libraries. In addition, according to
evaluated mean of AIS trajectories in the Baltic Sea the currents are extracted to `.nc` and visualazed for 
a buffering zone with user-defined distance around the AIS mean trajectories.  

## Files naming

The main directory contains two python scripts`variabilityData.py` and `selectcmemsAIS2015.py`
together with sub-directories `data` and `baltic-ais`. 

`Data` directory is subdivided into `<product_id_dir>` and `analysis`
that contain original `.nc` data with ocean products and their mean and std data evaluated over the same grid correspondingly. 

`baltic-ais` directory contains `4vessels30second-2015.csv.gz` file for the AIS data

## Usage

### Evaluate mean and std of global currents from ocean product

To obtain information about mean and std of both zonal and meridional current fields for global CMEMS data run in command line:
```shell
python3 variabilityData.py --basedir <your_data_directory> --var uo --var vo
```
or with option to select ocean product:
```shell
python3 variabilityData.py --basedir <your_data_directory> --var uo --var vo --product_id <existing_product_name>
```
Given arguments can be otherwise ommited and alternatively provided explicitly in the programm body as defaults

### Extract ocean product for mean AIS paths in Baltic Sea 

To extract ocean currenrs around AIS trajectories type in the command line:
```shell
python3 selectcmemsAIS2015.py --basedir <your_data_directory> --var uo --var vo --product_id <existing_product_name> --distance <distance_in_km>
```
### List of arguments

Given arguments can be otherwise omited and, alternatively, provided in explicit form in the programm body as default arguments.
`
- `product-id` being, e.g., `global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh`, or `global-analysis-forecast-wav-001-027`.
- `format` being `nc`, `zarr`, etc.
- `variable`, being `uo`, `vo`, etc.
- `start-time` being interpreted as left inclusive boundary of the time interval covered by the data file / data store, and `end-time` being interpreted as the right exclusive boundary of the time interval
- `extension` being `nc`, `zarr/`, etc.

