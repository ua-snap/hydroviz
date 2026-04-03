<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">About</h1>
      <div class="content is-size-4">
        <h3 class="title is-3">Hydrologic Outlooks</h3>
        <ul>
          <li>
            View and access interactive modeled data from gaged and ungaged
            streams and watersheds (HUC8)
          </li>
          <li>
            Quickly visualize range, uncertainty, means, and extremes for peak
            flow, low flow, seasonal averages, and other key variables.
          </li>
          <li>
            Access data downloads in flexible CSV format or directly from the
            API to create customized outputs.
          </li>
        </ul>

        <h3 class="title is-3">Who is this site for?</h3>
        <p>
          This web tool was designed to meet the needs of land managers,
          hydrologists, ecologists, engineers, and others in need of hydrologic
          information for use in long-term landscape-level planning. The
          visualizations in this tool offer a stepping-off point that is
          intended to allow the user to quickly understand the most important
          aspects of the dataset, including projected change, range of
          projections, uncertainties, and key take-aways. For those who require
          the full range of data for all specific models, emissions scenarios,
          and time periods in order to create their own graphics and perform
          their own analyses, the site offers CSV downloads.
        </p>

        <h3 class="title is-3">Where did the data come from?</h3>
        <p>
          The Hydrologic Futures tool is based on
          <a
            href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
            >PRMS</a
          >
          (the Precipitation Runoff Modeling System), which was developed by
          modelers at USGS (United States Geological Survey). PRMS was developed
          to simulate and evaluate streamflow, hydrologic processes, and water
          budgets under various climate and land use scenarios. PRMS uses the
          underlying geospatial fabric (hydrologic response units and stream
          segments) provided by the National Hydrologic Model Infrastructure (<a
            href="https://www.usgs.gov/mission-areas/water-resources/science/national-hydrologic-model-infrastructure"
            >NHMI</a
          >) and
          <a
            href="https://www.usgs.gov/data/application-national-hydrologic-model-infrastructure-precipitation-runoff-modeling-system-nhmi"
            >associated calibrations</a
          >.
        </p>

        <h3 class="title is-3">
          What are the most effective ways to use this tool?
        </h3>
        <p>
          Given the sources of uncertainty associated with this dataset, tool
          outputs are most appropriate for broadly assessing hydrologic change
          over time, at the level of hydrologic units or landscapes, rather than
          for generating short-term forecasts for specific stream segments.
          Visuals within the tool have been designed to depict summaries of
          change, including range and uncertainty.
        </p>
        <p>
          For those who choose to download data for tailored uses, care should
          be taken to consider the pros and cons of viewing specific models,
          scenarios (RCPs) and time periods. Users should also consider whether
          the most extreme values or more middle-of-the-road models and
          scenarios are most pertinent to their work, as well as whether they
          are most interested in average (typical) future hydrologic conditions,
          or extreme conditions (e.g. high or low flows). Based on these needs,
          they can select variables, models, scenarios, and output formats
          accordingly.
        </p>

        <h3 class="title is-3">How can I access and download data?</h3>
        <p>
          Downloads are available for a range of purposes and user groups,
          including those who want simple images and spreadsheet data (CSVs) and
          those who want full API access. From the tool, images can be
          downloaded via the camera icon, data can be copied and pasted from any
          table, and complete CSVs can be downloaded for single stream segments.
          From the API, endpoints will allow for accessing hydrographs (flow
          climatology) or all statistics for a single stream segment.
        </p>

        <h3 class="title is-3">How should these data and products be cited?</h3>
        <p>
          PRMS data are freely distributed, and require no licenses or
          permissions from USGS, but should be
          <a
            href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
            >appropriately cited</a
          >.
        </p>

        <h3 class="title is-3">
          What is the full range of data available via this site, and
          represented in this tool?
        </h3>
        <p>
          A total of 52 hydrologic statistics are available via this tool
          calculated from modeled daily streamflow data. The full list of
          variables can be <NuxtLink to="/data">viewed here</NuxtLink>. Global
          Climate Models are available; some offer data for all four scenarios
          (RCP 2.6, 4.5, 6.0, and 8.5) and others only for a subset of these
          scenarios. The full list of model/RCP combinations can be
          <NuxtLink to="/data">viewed here</NuxtLink>. All outputs are
          summarized by era: 1976&ndash;2005 (historical), 2016&ndash;2045,
          2046&ndash;2075 and 2071&ndash;2100. Visualizations within the tool
          focus on a subset of the full dataset in order to provide the more
          relevant summaries. All data is provided in CSV downloads.
        </p>
      </div>
    </div>
  </section>
</template>
