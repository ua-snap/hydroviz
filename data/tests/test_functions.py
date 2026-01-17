import requests
import scores
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import xarray as xr


api_base_url = "http://localhost:5000/"


def run_test_suite(test_streams, type):
    """For each stream in the test_streams dict, run the test suite.
    This function fetches modeled historical daily climatology data and
    observed daily climatology data from the API, and plots them together.
    A general map of the stream location is generated for context.
    Comparative statistics are also calculated:
      - Normalized Nash–Sutcliffe model efficiency coefficient (NNSE)
      - Normalized Mean Absolute Error (NMAE)
      - Normalized Root Mean Squared Error (NRMSE)

    Args:
        test_streams (dict): A dictionary where the first level is region,
        second level is subregion, and the third level is a list of dictionaries
        with stream information.
        type (str): Type of test suite being run ('baseline' or 'ensemble').

    Returns:
        None (prints output to console and generates plots).
    """
    # load CONUS shapefile for mapping
    conus_shp = "shp/ne_50m_admin_1_states_provinces_lakes/ne_50m_admin_1_states_provinces_lakes.shp"
    conus_gdf = gpd.read_file(conus_shp)

    stats_list = []

    for stream_dict in reformat_test_stream_dict(test_streams):
        modeled_data = fetch_modeled_climatology_data(
            stream_dict["hydroviz_stream_id"], type
        )

        if modeled_data is None:
            print(
                f"Problem getting modeled data for stream ID: {stream_dict['hydroviz_stream_id']}. Skipping."
            )
            continue

        observed_data, gauge_metadata = fetch_observed_climatology_data(
            stream_dict["hydroviz_stream_id"]
        )

        if observed_data is None:
            print(
                f"Problem getting observed data for stream ID: {stream_dict['hydroviz_stream_id']}. Skipping."
            )
            continue
        if gauge_metadata is None:
            print(
                f"Problem getting gauge metadata for stream ID: {stream_dict['hydroviz_stream_id']}. Skipping."
            )
            continue

        stats = calculate_comparative_statistics(modeled_data, observed_data)
        stats_info = {
            "stats_lc_dict": stats,
            "model": None,
            "scenario": "historical",
            "era": "1976-2005",
        }
        if type == "baseline":
            stats_info["model"] = "Maurer"
        elif type == "ensemble":
            stats_info["model"] = "Ensemble Mean"

        stats_list.append((stream_dict, stats_info, gauge_metadata))

        plot_hydrograph(
            modeled_data, observed_data, gauge_metadata, stream_dict, stats, type
        )
        plot_stream_map(gauge_metadata, conus_gdf)

        print("\n\n\n")
        print(
            "-----------------------------------------------------------------------------------------------------------------"
        )
        print("\n\n\n")

        # break

    print("\n\n\n")
    print_stats_summary(stats_list)

    return None


def reformat_test_stream_dict(test_streams):
    """Reformat the test_streams dictionary into a flat list of stream info dicts.

    Args:
        test_streams (dict): A nested dictionary with regions, subregions, and
        stream information.

    Returns:
        list: A flat list of dictionaries containing stream information.
    """
    reformatted_stream_dicts = []
    for region, subregions in test_streams.items():
        for subregion, streams in subregions.items():
            for stream_info in streams["streams"]:
                stream_dict = {"region": region, "subregion": subregion, **stream_info}
                reformatted_stream_dicts.append(stream_dict)
    return reformatted_stream_dicts


def fetch_modeled_climatology_data(hydroviz_stream_id, type):
    """Fetch modeled historical daily climatology data from the API.

    Args:
        hydroviz_stream_id (str): The Hydroviz stream ID.
        type (str): Type of modeled data to fetch ('baseline' or 'ensemble').

    Returns:
        dict: Modeled climatology data.
        Results include both landcover types.
    """
    modeled_data = {
        "dynamic": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
        "static": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
    }

    url = api_base_url + f"conus_hydrology/modeled_climatology/{hydroviz_stream_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if type == "baseline":
            for landcover in ["dynamic", "static"]:
                for doy_dict in data["data"][landcover]["Maurer"]["historical"][
                    "1976-2005"
                ]:
                    modeled_data[landcover]["doy"].append(doy_dict["doy"])
                    modeled_data[landcover]["min_values"].append(doy_dict["doy_min"])
                    modeled_data[landcover]["mean_values"].append(doy_dict["doy_mean"])
                    modeled_data[landcover]["max_values"].append(doy_dict["doy_max"])
        elif type == "ensemble":
            all_models = [
                "ACCESS1-0",
                "BCC-CSM1-1",
                "BNU-ESM",
                "CCSM4",
                "GFDL-ESM2G",
                "GFDL-ESM2M",
                "IPSL-CM5A-LR",
                "IPSL-CM5A-MR",
                "MIROC-ESM",
                "MIROC-ESM-CHEM",
                "MIROC5",
                "MRI-CGCM3",
                "NorESM1-M",
            ]

            # collect the min, mean, max across all models for each day of year
            # get the max of max, min of min, and mean of mean
            # and populate the modeled_data dict

            for landcover in ["dynamic", "static"]:
                for doy_dict in data["data"][landcover][all_models[0]]["historical"][
                    "1976-2005"
                ]:
                    doy = doy_dict["doy"]
                    min_values = []
                    mean_values = []
                    max_values = []
                    for ensemble_member in all_models:
                        for doy_dict in data["data"][landcover][ensemble_member][
                            "historical"
                        ]["1976-2005"]:
                            if doy_dict["doy"] == doy:
                                min_values.append(doy_dict["doy_min"])
                                mean_values.append(doy_dict["doy_mean"])
                                max_values.append(doy_dict["doy_max"])
                                break
                    modeled_data[landcover]["doy"].append(doy)
                    modeled_data[landcover]["min_values"].append(min(min_values))
                    modeled_data[landcover]["mean_values"].append(np.mean(mean_values))
                    modeled_data[landcover]["max_values"].append(max(max_values))

    else:
        return None

    return modeled_data


def fetch_observed_climatology_data(hydroviz_stream_id):
    """Fetch observed daily climatology data from the API.

    Args:
        hydroviz_stream_id (str): The Hydroviz stream ID.

    Returns:
        A tuple containing: a dict of observed climatology data and a dict of gauge metadata.
    """
    observed_data = {
        "actual": {"doy": [], "min_values": [], "mean_values": [], "max_values": []}
    }
    url = api_base_url + f"conus_hydrology/observed_climatology/{hydroviz_stream_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for doy_dict in data["data"]["actual"]["usgs"]["observed"]["1976-2005"]:
            observed_data["actual"]["doy"].append(doy_dict["doy"])
            observed_data["actual"]["min_values"].append(doy_dict["doy_min"])
            observed_data["actual"]["mean_values"].append(doy_dict["doy_mean"])
            observed_data["actual"]["max_values"].append(doy_dict["doy_max"])

        gauge_metadata = {
            "latitude": data.get("latitude", "NA"),
            "longitude": data.get("longitude", "NA"),
            "name": data.get("name", "NA"),
            "percent_complete": data.get("metadata", "NA").get(
                "percent_complete", "NA"
            ),
        }
    else:
        return None, None

    return observed_data, gauge_metadata


def plot_hydrograph(
    modeled_data, observed_data, gauge_metadata, stream_dict, stats, type
):
    """Plot the modeled and observed hydrograph data.

    Args:
        modeled_data (dict): Modeled climatology data.
        observed_data (dict): Observed climatology data.
        stream_dict (dict): Stream information dictionary.
        stats (dict): Comparative statistics.

    Returns:
        None: Generates a plot.
    """
    # index values to align with water year
    doy_values = np.arange(1, 367)
    water_year_order = np.concatenate(
        [
            np.arange(276, 367),  # Oct 1 (275) to Dec 31 (366)
            np.arange(1, 276),  # Jan 1 (1) to Sep 30 (273)
        ]
    )

    # Find the indices to reorder the data
    reorder_indices = np.searchsorted(doy_values, water_year_order)

    # Create water year DOY axis (1 to 366)
    water_year_doy = np.arange(1, len(water_year_order) + 1)

    # Convert lists to numpy arrays and reorder
    modeled_dynamic_min_ordered = np.array(modeled_data["dynamic"]["min_values"])[
        reorder_indices
    ]
    modeled_dynamic_mean_ordered = np.array(modeled_data["dynamic"]["mean_values"])[
        reorder_indices
    ]
    modeled_dynamic_max_ordered = np.array(modeled_data["dynamic"]["max_values"])[
        reorder_indices
    ]

    modeled_static_min_ordered = np.array(modeled_data["static"]["min_values"])[
        reorder_indices
    ]
    modeled_static_mean_ordered = np.array(modeled_data["static"]["mean_values"])[
        reorder_indices
    ]
    modeled_static_max_ordered = np.array(modeled_data["static"]["max_values"])[
        reorder_indices
    ]

    observed_min_ordered = np.array(observed_data["actual"]["min_values"])[
        reorder_indices
    ]
    observed_mean_ordered = np.array(observed_data["actual"]["mean_values"])[
        reorder_indices
    ]
    observed_max_ordered = np.array(observed_data["actual"]["max_values"])[
        reorder_indices
    ]

    # if there are any values < 0 in the "min" arrays, set them to 0 for plotting and print a warning
    # this should not happen, but we want to know if it does!
    for arr, label in [
        (modeled_dynamic_min_ordered, "Modeled Dynamic Min"),
        (modeled_static_min_ordered, "Modeled Static Min"),
        (observed_min_ordered, "Observed Min"),
    ]:
        if np.any(arr < 0):
            print(
                f"Warning: Values < 1 found in {label} data. Setting values to 1 for log-scale plotting."
            )
            arr[arr < 0] = 0.0

    # Create figure
    plt.figure(figsize=(10, 6))

    # Plot with properly ordered water year data
    plt.plot(
        water_year_doy,
        modeled_dynamic_mean_ordered,
        label="Modeled Dynamic Mean",
        color="lightcoral",
    )
    plt.fill_between(
        water_year_doy,
        modeled_dynamic_min_ordered,
        modeled_dynamic_max_ordered,
        color="lightcoral",
        alpha=0.2,
        label="Modeled Dynamic Min-Max Range",
    )
    plt.plot(
        water_year_doy,
        modeled_static_mean_ordered,
        label="Modeled Static Mean",
        color="cornflowerblue",
    )
    plt.fill_between(
        water_year_doy,
        modeled_static_min_ordered,
        modeled_static_max_ordered,
        color="cornflowerblue",
        alpha=0.2,
        label="Modeled Static Min-Max Range",
    )
    plt.plot(
        water_year_doy,
        observed_mean_ordered,
        label="Observed Mean",
        color="black",
    )
    plt.fill_between(
        water_year_doy,
        observed_min_ordered,
        observed_max_ordered,
        color="gray",
        alpha=0.2,
        label="Observed Min-Max Range",
    )
    # Get info for title
    stream_id = stream_dict["hydroviz_stream_id"]
    if type == "baseline":
        model = "Maurer"
    elif type == "ensemble":
        model = "Ensemble Mean"
    scenario = "historical"
    era = "1976-2005"
    gauge_name = gauge_metadata["name"]
    gauge_id = stream_dict["usgs_gauge_id"]
    percent_complete = gauge_metadata["percent_complete"]
    latitude = gauge_metadata["latitude"]
    longitude = gauge_metadata["longitude"]

    # Format stats values for title

    if stats["dynamic"]["NNSE"] != "NA":
        nnse_dyanmic = f"{stats['dynamic']['NNSE']:.3f}"
    else:
        nnse_dyanmic = "NA"

    if stats["static"]["NNSE"] != "NA":
        nnse_static = f"{stats['static']['NNSE']:.3f}"
    else:
        nnse_static = "NA"

    if stats["dynamic"]["NMAE"] != "NA":
        nmae_dynamic = f"{stats['dynamic']['NMAE']:.3f}"
    else:
        nmae_dynamic = "NA"

    if stats["static"]["NMAE"] != "NA":
        nmae_static = f"{stats['static']['NMAE']:.3f}"
    else:
        nmae_static = "NA"

    if stats["dynamic"]["NRMSE"] != "NA":
        nrmse_dynamic = f"{stats['dynamic']['NRMSE']:.3f}"
    else:
        nrmse_dynamic = "NA"

    if stats["static"]["NRMSE"] != "NA":
        nrmse_static = f"{stats['static']['NRMSE']:.3f}"
    else:
        nrmse_static = "NA"

    # Set x-axis limits and labels for water year
    plt.xlim(0, 365)
    # plt.xlabel('Days from Start of Water Year (Oct 1 = 0)')
    plt.ylabel("Streamflow (cfs)")

    # Add month labels for reference
    month_labels = [
        "Oct",
        "Nov",
        "Dec",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
    ]
    # Approximate day of year for start of each month in water year
    month_starts = [0, 31, 62, 92, 123, 151, 182, 212, 243, 273, 304, 335]
    plt.xticks(month_starts, month_labels, rotation=45)

    # add title
    plt.suptitle(
        f"Modeled and Observed Daily Streamflow Climatology for Stream ID: {stream_id}\n Ecoregion: {stream_dict['region']}, Subregion: {stream_dict['subregion']}",
        fontsize=13,
    )

    plt.title(
        f"Gauge: {gauge_id} - {gauge_name} ({latitude:.2f}, {longitude:.2f}) | Data Completeness: {percent_complete:.1f}%\nModel: {model} | Scenario: {scenario} | Era: {era} \n\n NNSE: Dynamic = {nnse_dyanmic}, Static = {nnse_static} | NMAE: Dynamic = {nmae_dynamic}, Static = {nmae_static} | NRMSE: Dynamic = {nrmse_dynamic}, Static = {nrmse_static}",
        fontsize=10,
    )

    # use symlog scale on y-axis
    # uses a linear scale for values between -linthresh and linthresh, and a logarithmic scale for values outside that range
    plt.yscale("symlog", linthresh=1, linscale=1)
    # get absolute min and max of all y values for setting y-limits
    y = np.concatenate(
        [
            modeled_dynamic_min_ordered,
            modeled_dynamic_max_ordered,
            modeled_static_min_ordered,
            modeled_static_max_ordered,
            observed_min_ordered,
            observed_max_ordered,
        ]
    )
    plt.ylim(y[y > 0].min(), y.max())

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return None


def plot_stream_map(gauge_metadata, conus_gdf):
    """Generate a map of the stream location.

    Args:
        stream_dict (dict): Stream information dictionary.

    Returns:
        None: Generates a map plot.
    """
    # Create a GeoDataFrame for the gauge lat/lon
    gauge_gdf = gpd.GeoDataFrame(
        {
            "name": [gauge_metadata["name"]],
            "geometry": gpd.points_from_xy(
                [gauge_metadata["longitude"]], [gauge_metadata["latitude"]]
            ),
        },
        crs="EPSG:4326",
    )
    # Plot the map
    fig, ax = plt.subplots(figsize=(5, 3))
    conus_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    gauge_gdf.plot(ax=ax, color="red", markersize=100, label="Stream Gauge")
    plt.title(
        f"Stream Gauge Location: {gauge_metadata['name']} \n (Lat: {gauge_metadata['latitude']:.2f}, Lon: {gauge_metadata['longitude']:.2f})",
        fontsize=10,
    )

    # limit the map extent to the CONUS
    ax.set_xlim(-128, -65)
    ax.set_ylim(24, 50)

    # plt.legend()
    plt.grid(True, alpha=0.3)
    # plt.tight_layout()
    plt.show()

    return None


def print_stats_summary(stats_list):
    """Print summary statistics comparing modeled and observed data.
    Args:
        stats_list (list): A list where each item is a 3-tuple;
        first element is stream_dict, second element is corresponding stats_info dict,
        third element is gauge metadata.

    Returns:
        None: Prints statistics to console.
    """
    for stream_dict, stats_info, gauge_metadata in stats_list:
        stream_id = stream_dict["hydroviz_stream_id"]
        region = stream_dict["region"]
        subregion = stream_dict["subregion"]
        model = stats_info["model"]
        scenario = stats_info["scenario"]
        era = stats_info["era"]
        stats = stats_info["stats_lc_dict"]
        gauge_id = stream_dict["usgs_gauge_id"]
        gauge_name = gauge_metadata["name"]
        pct_complete = gauge_metadata["percent_complete"]

        print(f"Stream ID: {stream_id} | Region: {region} | Subregion: {subregion}")
        print(
            f"Gauge ID: {gauge_id} | Gauge Name: {gauge_name} | Data Completeness: {pct_complete:.1f}%"
        )
        print(f"Model: {model} | Scenario: {scenario} | Era: {era}")
        for landcover in ["dynamic", "static"]:
            print(f"  Landcover Type: {landcover.capitalize()}")
            print(
                f"    NNSE: {stats[landcover]['NNSE']:.4f}, NMAE: {stats[landcover]['NMAE']:.4f}, NRMSE: {stats[landcover]['NRMSE']:.4f}"
            )
        print("-" * 80)

    return None


def calculate_comparative_statistics(modeled_data, observed_data):
    """Calculate some statistics using the scores package.

    Background for interpreting these stats: https://www.sciencedirect.com/science/article/pii/S1364815225003494

    https://scores.readthedocs.io/en/stable/tutorials/NSE.html
    https://scores.readthedocs.io/en/stable/tutorials/Mean_Absolute_Error.html
    https://scores.readthedocs.io/en/stable/tutorials/Root_Mean_Squared_Error.html

    These need to be normalized appropriately in order to compare across streams and regions.

    Args:
        modeled_data (dict): Modeled climatology data.
        observed_data (dict): Observed climatology data.

    Returns:
        dict: A dictionary containing comparative statistics.
    """
    stats = {
        "dynamic": {"NNSE": "NA", "NMAE": "NA", "NRMSE": "NA"},
        "static": {"NNSE": "NA", "NMAE": "NA", "NRMSE": "NA"},
    }

    # Convert lists to xarray DataArrays for scores calculations

    modeled_mean_dynamic = xr.DataArray(modeled_data["dynamic"]["mean_values"])
    modeled_mean_static = xr.DataArray(modeled_data["static"]["mean_values"])
    observed_mean = xr.DataArray(observed_data["actual"]["mean_values"])

    # test if all values are zero in any of the modeled arrays; if so, return NaN for all stats and print a warning
    # this catches a known missing data error
    for arr in [modeled_mean_dynamic, modeled_mean_static]:
        if np.all(arr.values == 0):
            print(
                "Warning: All modeled values are zero for one of the landcover types. Returning NaN for all statistics."
            )
            return stats

    # Group for stats calculations
    groups = {
        "dynamic": (observed_mean, modeled_mean_dynamic),
        "static": (observed_mean, modeled_mean_static),
    }

    # Calculate statistics for each group and populate stats dict
    for group_name, (obs, mod) in groups.items():
        # NNSE = 1 / (2 - NSE)
        nse = scores.continuous.nse(obs, mod)
        nnse = 1 / (2 - nse)

        # NMAE = MAE / mean of observations
        mae = scores.continuous.mae(obs, mod)
        nmae = mae / np.mean(obs)

        # NRMSE = RMSE / range of observations
        rmse = scores.continuous.rmse(obs, mod)
        nrmse = rmse / (np.max(obs) - np.min(obs))

        stats[group_name]["NNSE"] = nnse
        stats[group_name]["NMAE"] = nmae
        stats[group_name]["NRMSE"] = nrmse

    return stats
