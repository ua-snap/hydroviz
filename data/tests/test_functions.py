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
    for stream_dict in reformat_test_stream_dict(test_streams):
        modeled_data = fetch_modeled_climatology_data(stream_dict["hydroviz_stream_id"])
        observed_data = fetch_observed_climatology_data(
            stream_dict["hydroviz_stream_id"]
        )

        stats = calculate_comparative_statistics(modeled_data, observed_data)
        plot_hydrograph(modeled_data, observed_data, stream_dict, stats)
        plot_stream_map(stream_dict)

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
    # Placeholder for API call to fetch modeled data
    modeled_data = {
        "dynamic": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
        "static": {"doy": [], "min_values": [], "mean_values": [], "max_values": []},
    }
    return modeled_data


def fetch_observed_climatology_data(hydroviz_stream_id):
    """Fetch observed daily climatology data from the API.

    Args:
        hydroviz_stream_id (str): The Hydroviz stream ID.

    Returns:
        dict: Observed climatology data.
    """
    # Placeholder for API call to fetch observed data
    observed_data = {"doy": [], "min_values": [], "mean_values": [], "max_values": []}
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


def print_summary_statistics():
    """Print summary statistics comparing modeled and observed data.

    Returns:
        None: Prints statistics to console.
    """
    # Placeholder for statistics calculation and printing
    pass
    return None


def calculate_comparative_statistics(modeled_data, observed_data):
    """Calculate the normalized Nash–Sutcliffe model efficiency coefficient (NNSE).

    Args:
        modeled_data (dict): Modeled climatology data.
        observed_data (dict): Observed climatology data.

    Returns:
        dict: A dictionary containing comparative statistics.
    """
    # Placeholder for stats calculation
    stats = {"NNSE": 0, "NMAE": 0, "NRMSE": 0}

    return stats
