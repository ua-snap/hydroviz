import requests
import scores
import matplotlib.pyplot as plt
import geopandas as gpd


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

    stats_list = []

    for stream_dict in reformat_test_stream_dict(test_streams):
        modeled_data = fetch_modeled_climatology_data(stream_dict["hydroviz_stream_id"])
        observed_data = fetch_observed_climatology_data(
            stream_dict["hydroviz_stream_id"]
        )

        stats = calculate_comparative_statistics(modeled_data, observed_data)
        stats_list.append(stats)

        plot_hydrograph(modeled_data, observed_data, stream_dict, stats)
        plot_stream_map(stream_dict)

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

    return observed_data


def plot_hydrograph(modeled_data, observed_data, stream_dict, stats):
    """Plot the modeled and observed hydrograph data.

    Args:
        modeled_data (dict): Modeled climatology data.
        observed_data (dict): Observed climatology data.
        stream_dict (dict): Stream information dictionary.
        stats (dict): Comparative statistics.

    Returns:
        None: Generates a plot.
    """
    # Placeholder for plotting logic
    pass
    return None


def plot_stream_map(stream_dict):
    """Generate a map of the stream location.

    Args:
        stream_dict (dict): Stream information dictionary.

    Returns:
        None: Generates a map plot.
    """
    # Placeholder for map plotting logic
    pass
    return None


def print_stats_summary(stats_list):
    """Print summary statistics comparing modeled and observed data.

    Returns:
        None: Prints statistics to console.
    """
    # Placeholder for statistics calculation and printing
    pass
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
    # Placeholder for stats calculation
    stats = {"NNSE": 0, "NMAE": 0, "NRMSE": 0}

    return stats
