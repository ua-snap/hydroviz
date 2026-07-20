<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">Data and Methodology</h1>
      <div class="content is-size-4">
        <h2 class="title is-3">Overview</h2>
        <div class="mb-5">
          <h3 class="title is-4">About the data used in this tool</h3>
          <p>
            The data shown on this web tool are aggregated in two ways, showing
            "middle of the road" scenarios and extremes. This encourages
            exploration of the data at a high level without needing to first
            understand the complexities of global climate models, earth system
            models, or associated climate scenarios.
          </p>
        </div>
        <div class="mb-5">
          <h3 class="title is-4">How can I access and download data?</h3>
          <p>
            Downloads are available for a range of purposes and user groups,
            including those who want simple images and spreadsheet data (CSVs)
            and those who want full API access. From the tool, images can be
            downloaded via the camera icon, data can be copied and pasted from
            any table, and complete CSVs can be downloaded for single stream
            segments. From the API, endpoints will allow for accessing
            hydrographs (flow climatology) or all statistics for a single stream
            segment.
          </p>
        </div>
        <div class="mb-5">
          <h3 class="title is-4">
            How should these data and products be cited?
          </h3>
          <p>
            All data used in this tool, including
            <a
              href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
              >PRMS data</a
            >
            and <a href="https://nps.edu/web/rasm">RASM data</a>, are freely
            distributed, and require no licenses or permissions from USGS, but
            should be appropriately cited. All of SNAP's products are licensed
            under
            <a href="https://creativecommons.org/licenses/by/4.0/"
              >Creative Commons</a
            >. When citing our work, please include our logo and a link to our
            <a href="https://uaf-snap.org/">home page</a>.
          </p>
        </div>
        <div>
          <h3 class="title is-4">Choice of visualizations</h3>
          <p>
            Visualizations were selected to offer the user a quick overview of
            the characteristics of the magnitude and timing of flow for a
            selected river segment. The emphasis is on trends and change over
            future decades, rather than on absolute values. Calculations for all
            variables are outlined below in the full list of hydrologic
            variables. In some cases, the modeled nature of the data led to
            non-intuitive outputs or wide ranges of values. This is particularly
            true for low flow streams. These irregularities are flagged in text
            outputs, including cases where model outputs vary by more than 50%.
            In order to avoid visual clutter and false precision, online data is
            generally rounded to no more than two significant digits.
          </p>
        </div>
      </div>
      <div class="mb-5">
        <div class="content is-size-4">
          <h2 class="title is-3">Methodology</h2>
          <div class="mb-5">
            <h3 class="title is-4">Continental US</h3>
            <p>
              Climatologies and statistics were computed from data provided by
              the
              <a href="https://www.usgs.gov/node/279857"
                >USGS National Water Information System (NWIS)</a
              >
              and
              <a
                href="https://www.sciencebase.gov/catalog/item/5d826e4de4b0c4f70d059137"
                >LaFontaine et al. (2023)</a
              >. Stream segments were derived from the
              <a
                href="https://www.usgs.gov/data/geospatial-fabric-national-hydrologic-modeling-version-11"
                >National Hydrologic Model Geospatial Fabric</a
              >, and streamflow was modeled using the
              <a
                href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
                >Precipitation-Runoff Modeling System (PRMS)</a
              >
              with CMIP5 historical and projected climate data. The
              <a
                href="https://www.usgs.gov/data/application-national-hydrologic-model-infrastructure-precipitation-runoff-modeling-system-nhmi"
                >Maurer Calibration</a
              >
              is used as a baseline for the historical period. All projected
              climatologies and statistics shown in this tool were derived by
              calculating the change between the future and historical eras from
              each CMIP5 model, and applying this change to the Maurer
              Calibration historical baseline.
            </p>
          </div>
          <div class="mb-5">
            <h3 class="title is-4">Alaska</h3>
            <p>
              Climatologies and statistics were computed from data provided by
              <a
                href="https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023WR036217"
                >Blaskey et al.</a
              >
              Stream segments were derived from the
              <a
                href="https://water.usgs.gov/catalog/datasets/05199160-2947-404d-bac7-ba6aed53a96e/"
                >MERIT Hydro network</a
              >, and streamflow was modeled using the
              <a href="https://nps.edu/web/rasm"
                >Regional Arctic System Model (RASM)</a
              >
              with dynamically downscaled CMIP6 historical and projected climate
              data. A dynamically downscaled ERA5 baseline (Blaskey et al.) is
              used for the historical period. Hydrological statistics were
              calculated using the
              <a
                href="https://www.sciencedirect.com/science/article/pii/S1574954116300115"
                >MATLAB Hydrological Index Tool (MHIT)</a
              >. All projected climatologies and statistics shown in this tool
              were derived by calculating the change between the future and
              historical eras from the CMIP6 data, and applying this change to
              the dynamically downscaled
              <a
                href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview"
                >ERA5 baseline</a
              >.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
