"""
Concatenates the annual grid load excel datasets into a single netCDF file for easy of use.

The original datasets are obtained from [ https://www.ercot.com/gridinfo/load/load_hist ].

All downloaded and extracted excel spreadsheets should be stored under [ {DATA_DIR}/load_timeseries ]
and renamed to [ {YEAR}_ercot_hourly_load_data ] where {} formats the string path.

The output netCDF is named [ load_timeseries.nc ] and stored under [ {DATA_DIR}/load_timeseries ].

"""

import pandas as pd
from os import listdir
import datetime
import xarray as xr

DATA_DIR = "../geo371t_data/"

datasets = []
for year in range(2003, 2023):
    ext = "xlsx"
    if year < 2016:
        ext = "xls"
    raw_dataset = pd.read_excel(f"{DATA_DIR}load_timeseries/{year}_ercot_hourly_load_data.{ext}")
    
    time = datetime.datetime(year, 1, 1)
    times = []
    for index in range(0, raw_dataset.shape[0]):
        time += datetime.timedelta(hours=1)
        times.append(time)
    ds_dict = {}
    if year < 2017:
        ds_dict = dict(
            coast=(["time"], raw_dataset["COAST"].values),
            east=(["time"], raw_dataset["EAST"].values),
            far_west=(["time"], raw_dataset["FAR_WEST"].values),
            north=(["time"], raw_dataset["NORTH"].values),
            north_c=(["time"], raw_dataset["NORTH_C"].values),
            southern=(["time"], raw_dataset["SOUTHERN"].values),
            south_c=(["time"], raw_dataset["SOUTH_C"].values),
            west=(["time"], raw_dataset["WEST"].values),
            ercot=(["time"], raw_dataset["ERCOT"].values),
        )
    else:
        ds_dict = dict(
            coast=(["time"], raw_dataset["COAST"].values),
            east=(["time"], raw_dataset["EAST"].values),
            far_west=(["time"], raw_dataset["FWEST"].values),
            north=(["time"], raw_dataset["NORTH"].values),
            north_c=(["time"], raw_dataset["NCENT"].values),
            southern=(["time"], raw_dataset["SOUTH"].values),
            south_c=(["time"], raw_dataset["SCENT"].values),
            west=(["time"], raw_dataset["WEST"].values),
            ercot=(["time"], raw_dataset["ERCOT"].values),
        )
        
    ds = xr.Dataset(
        data_vars=ds_dict,
        coords=dict(
            time=times,
        ),
        attrs=dict(description="ERCOT Electrical Grid load (gigawatts)"),
    )
    datasets.append(ds)
xr.concat(datasets, "time").to_netcdf(f"{DATA_DIR}load_timeseries/load_timeseries.nc")
