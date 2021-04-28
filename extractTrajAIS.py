"""Extract AIS trajectories

"""
import pandas as pd
import argparse
from pathlib import Path
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import os

def readAIS2df(file_names):

    # Read from AIS data for Baltic Sea
    df = pd.read_csv(
        "baltic-sea-ais-data-master/data/4vessels-30second-2015.csv",
        parse_dates=[0, ]
    )
    # Prepare data inside dataframe
    # Drop ETA column
    df = df.drop(columns=["ETA", ])
    # Drop values with IMO equal to zero c
    df = df[df["IMO"] > 0]
    # Eliminate paddings NAME column
    df["NAME"] = df["NAME"].str.strip()
    df["DESTINATION"] = df["DESTINATION"].str.strip()
    df["CALLSIGN"] = df["CALLSIGN"].str.strip()
    return df
