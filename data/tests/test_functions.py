import requests
import scores
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np


api_base_url = "localhost:5000/"


def run_test_suite(test_streams):
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

    Returns:
        None (prints output to console and generates plots).
    """
    # load CONUS shapefile for mapping
    conus_shp = "data/tests/shp/ne_50m_admin_1_states_provinces_lakes/ne_50m_admin_1_states_provinces_lakes.shp"
    conus_gdf = gpd.read_file(conus_shp)

    stats_list = []

    for stream_dict in reformat_test_stream_dict(test_streams):
        modeled_data = fetch_modeled_climatology_data(stream_dict["hydroviz_stream_id"])
        observed_data, gauge_metadata = fetch_observed_climatology_data(
            stream_dict["hydroviz_stream_id"]
        )

        stats = calculate_comparative_statistics(modeled_data, observed_data)
        stats_info = {
            "stats_lc_dict": stats,
            "model": "Maurer",
            "scenario": "historical",
            "era": "1976-2005",
        }
        stats_list.append((stream_dict, stats_info))

        plot_hydrograph(modeled_data, observed_data, gauge_metadata, stream_dict, stats)
        plot_stream_map(stream_dict, gauge_metadata, conus_gdf)

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


def fetch_modeled_climatology_data(hydroviz_stream_id):
    """Fetch modeled historical daily climatology data from the API.

    Args:
        hydroviz_stream_id (str): The Hydroviz stream ID.

    Returns:
        dict: Modeled climatology data, limited to the Maurer model. Results include both
        landcover types.
    """
    modeled_data = {
        "dynamic": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
        "static": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
    }

    url = api_base_url + f"conus_hydrology/modeled_climatology/{hydroviz_stream_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter for Maurer model only
        for landcover in ["dynamic", "static"]:
            for doy_dict in data["data"][landcover]["Maurer"]["historical"][
                "1976-2005"
            ]:
                modeled_data[landcover]["doy"].append(doy_dict["doy"])
                modeled_data[landcover]["min_values"].append(doy_dict["min"])
                modeled_data[landcover]["mean_values"].append(doy_dict["mean"])
                modeled_data[landcover]["max_values"].append(doy_dict["max"])

    return modeled_data


def fetch_observed_climatology_data(hydroviz_stream_id):
    """Fetch observed daily climatology data from the API.

    Args:
        hydroviz_stream_id (str): The Hydroviz stream ID.

    Returns:
        dict: Observed climatology data.
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
            observed_data["actual"]["min_values"].append(doy_dict["min"])
            observed_data["actual"]["mean_values"].append(doy_dict["mean"])
            observed_data["actual"]["max_values"].append(doy_dict["max"])

        gauge_metadata = {
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "name": data["name"],
            "percent_complete": data["metadata"]["percent_complete"],
        }

    return observed_data, gauge_metadata


def plot_hydrograph(modeled_data, observed_data, gauge_metadata, stream_dict, stats):
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

    # Create figure
    plt.figure(figsize=(12, 6))

    # Plot with properly ordered water year data
    plt.plot(
        water_year_doy,
        modeled_dynamic_mean_ordered,
        label="Modeled Dynamic Mean",
        color="blue",
    )
    plt.fill_between(
        water_year_doy,
        modeled_dynamic_min_ordered,
        modeled_dynamic_max_ordered,
        color="blue",
        alpha=0.2,
        label="Modeled Dynamic Min-Max Range",
    )
    plt.plot(
        water_year_doy,
        modeled_static_mean_ordered,
        label="Modeled Static Mean",
        color="green",
    )
    plt.fill_between(
        water_year_doy,
        modeled_static_min_ordered,
        modeled_static_max_ordered,
        color="green",
        alpha=0.2,
        label="Modeled Static Min-Max Range",
    )
    plt.plot(
        water_year_doy,
        observed_mean_ordered,
        label="Observed Mean",
        color="red",
    )
    plt.fill_between(
        water_year_doy,
        observed_min_ordered,
        observed_max_ordered,
        color="red",
        alpha=0.2,
        label="Observed Min-Max Range",
    )
    # Get info for title
    stream_id = stream_dict["hydroviz_stream_id"]
    model = "Maurer"
    scenario = "historical"
    era = "1976-2005"
    gauge_name = gauge_metadata["name"]
    percent_complete = gauge_metadata["percent_complete"]
    latitude = gauge_metadata["latitude"]
    longitude = gauge_metadata["longitude"]

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
    plt.title(
        f"Modeled and Observed Daily Streamflow Climatology for Stream ID: {stream_id}"
    )

    plt.suptitle(
        f"Gauge: {gauge_name} (Lat: {latitude:.2f}, Lon: {longitude:.2f}) | Data Completeness: {percent_complete:.1f}%\nModel: {model} | Scenario: {scenario} | Era: {era}",
        fontsize=10,
        y=0.93,
    )

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    return None


def plot_stream_map(stream_dict, gauge_metadata, conus_gdf):
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
    fig, ax = plt.subplots(figsize=(8, 8))
    conus_gdf.boundary.plot(ax=ax, color="black", linewidth=0.5)
    gauge_gdf.plot(ax=ax, color="red", markersize=100, label="Stream Gauge")
    plt.title(
        f"Stream Gauge Location: {gauge_metadata['name']} (Lat: {gauge_metadata['latitude']:.2f}, Lon: {gauge_metadata['longitude']:.2f})"
    )
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return None


def print_stats_summary(stats_list):
    """Print summary statistics comparing modeled and observed data.
    Args:
        stats_list (list): A list where each item is a tuple; first element is stream_dict, second element is corresponding stats_info dict.

    Returns:
        None: Prints statistics to console.
    """
    for stream_dict, stats_info in stats_list:
        stream_id = stream_dict["hydroviz_stream_id"]
        region = stream_dict["region"]
        subregion = stream_dict["subregion"]
        model = stats_info["model"]
        scenario = stats_info["scenario"]
        era = stats_info["era"]
        stats = stats_info["stats_lc_dict"]

        print(f"Stream ID: {stream_id} | Region: {region} | Subregion: {subregion}")
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
        "dynamic": {"NNSE": None, "NMAE": None, "NRMSE": None},
        "static": {"NNSE": None, "NMAE": None, "NRMSE": None},
    }

    # Convert lists to numpy arrays
    modeled_mean_dynamic = np.array(modeled_data["dynamic"]["mean_values"])
    modeled_mean_static = np.array(modeled_data["static"]["mean_values"])
    observed_mean = np.array(observed_data["actual"]["mean_values"])

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
        mae = scores.continuous.mean_absolute_error(obs, mod)
        nmae = mae / np.mean(obs)

        # NRMSE = RMSE / range of observations
        rmse = scores.continuous.root_mean_squared_error(obs, mod)
        nrmse = rmse / (np.max(obs) - np.min(obs))

        stats[group_name]["NNSE"] = nnse
        stats[group_name]["NMAE"] = nmae
        stats[group_name]["NRMSE"] = nrmse

    return stats
