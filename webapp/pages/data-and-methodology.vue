<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">Data, Methodology &amp; Bibliography</h1>
      <div class="block content is-size-4 clamp">
        <p>
          Read below for details on source data and the methodology used in this
          web tool, or jump down to ideas for
          <a href="#csv">using CSV downloads</a>, hints on how to
          <a href="#citation">cite this tool</a>, and a
          <a href="#bibliography">bibilography</a>.
        </p>
      </div>
      <div class="content clamp is-size-5">
        <div class="block">
          <h3 class="title is-3">Sources &amp; Methodology</h3>
          <h4 class="title is-4">Continental United States</h4>
          <p>
            Climatologies and statistics were computed from data provided by the
            <a href="https://www.usgs.gov/node/279857"
              >USGS National Water Information System (NWIS)</a
            >
            and
            <a
              href="https://www.sciencebase.gov/catalog/item/5d826e4de4b0c4f70d059137"
              >LaFontaine et al.(2023).</a
            >
            Stream segments were derived from the
            <a
              href="https://www.usgs.gov/data/geospatial-fabric-national-hydrologic-modeling-version-11"
              >National Hydrologic Model Geospatial Fabric</a
            >, and streamflow was modeled using the
            <a
              href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
              >Precipitation&ndash;Runoff Modeling System (PRMS)</a
            >
            with CMIP5 historical and projected climate data. The
            <a
              href="https://www.usgs.gov/data/application-national-hydrologic-model-infrastructure-precipitation-runoff-modeling-system-nhmi"
              >Maurer Calibration</a
            >
            is used as a baseline for the historical period. All projected
            climatologies and statistics shown in this tool were derived by
            calculating the change between the future and historical eras from
            each CMIP5 model, and applying this change to the Maurer Calibration
            historical baseline.
          </p>
          <p>
            <strong
              ><NuxtLink to="https://earthmaps.io/conus_hydrology"
                >Read complete details</NuxtLink
              >
              on climate models</strong
            >
            used in this dataset, and
            <strong> full definitions of all variables </strong>.
          </p>
          <h6>How are future changes in land use accounted for?</h6>
          <p>
            PRMS offers projections with and without additional model parameters
            that account for potential human land use changes, as assessed in a
            USGS Land Use and Land Cover (<a
              href="https://esajournals.onlinelibrary.wiley.com/doi/10.1890/13-1245.1"
              >LULC</a
            >) model. These projected changes are landscape-level rather than
            site-specific, and are based on projected shifts in logging,
            wildfire, agricultural land use, and other anthropogenic uses. The
            Hydrologic Futures tool offers this modified dataset via CSV data
            downloads for more extensive analysis. This online tool shows values
            with static, not dynamic, land cover.
          </p>
          <h4>Alaska &amp; Western Canada</h4>
          <p>
            Climatologies and statistics were computed from data provided by
            <a
              href="https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2023WR036217"
              >Blaskey et al.</a
            >. Stream segments were derived from the
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
            historical eras from the CMIP6 data, and applying this change to the
            dynamically downscaled
            <a
              href="https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview"
              >ERA5 baseline</a
            >.
          </p>
          <p>
            <strong
              ><NuxtLink to="https://earthmaps.io/arctic_hydrology"
                >Read complete details</NuxtLink
              >
              on climate models</strong
            >
            used in this dataset, and
            <strong> full definitions of all variables </strong>.
          </p>
        </div>
        <div class="block" id="csv">
          <h3 class="title is-3">What can I do with CSV downloads?</h3>
          <p>
            The web tool&rsquo;s built-in views show aggregated
            values&mdash;medians, minimums, etc, across many model runs&mdash;at
            multi-decadal timescales. The downloaded CSV data lets users go
            further:
          </p>
          <ul>
            <li>
              <strong>Build statistical analyses</strong>, complex graphics, or
              simple tables and charts tailored to a specific need.
            </li>
            <li>
              <strong>Extract output from a single model</strong> to compare
              against external data or other projects that relied on that model.
            </li>
            <li>
              <strong>Combine or compare across models</strong>&mdash;average a
              selected set, calculate deltas between two time periods, or find
              the range or standard deviation across models.
            </li>
            <li>
              <strong>Isolate specific days or custom time periods</strong> that
              monthly averages don&rsquo;t capture, such as an ecologically
              defined window like spawning season or spring thaw.
            </li>
          </ul>
        </div>
        <div class="block" id="citation">
          <h3 class="title is-3">
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
            should be appropriately cited. All of SNAP&rsquo;s products are
            licensed under
            <a href="https://creativecommons.org/licenses/by/4.0/"
              >Creative Commons</a
            >. When citing our work, please include our logo and a link to our
            <a href="https://uaf-snap.org/">home page</a>.
          </p>
        </div>
        <div class="block" id="bibliography">
          <section>
            <h3>Bibliography</h3>
            <h4>Key references</h4>
            <ul>
              <li>
                Blaskey, Dylan, Keith Musselman, Andrew Newman, &amp; Yifan
                Cheng. (2024).
                <cite class="resource-title"
                  >Alaskan river discharge, temperature, and climate data for a
                  climate reference (1990-2021) and at mid-century
                  (2034-2065).</cite
                >
                Arctic Data Center.
                <a href="https://doi.org/10.18739/a25m62870"
                  >https://doi.org/10.18739/a25m62870</a
                >
              </li>
              <li>
                Blaskey, D., Gooseff, M.N., Cheng, Y., Newman, A.J., Koch, J.C.,
                and Musselman, K.N. 2024.
                <cite class="resource-title"
                  >A high-resolution, daily hindcast (1990&ndash;2021) of
                  Alaskan River discharge and temperature from coupled and
                  optimized physical models.</cite
                >
                Water Resour. Res. 60(4): 1&ndash;19.
                <a href="https://doi.org/10.1029/2023WR036217"
                  >https://doi.org/10.1029/2023WR036217</a
                >
              </li>
              <li>
                Cheng, Y., A. Craig, K. Musselman, A. Bennett, M. Seefeldt, J.
                Hamman, and A. J. Newman. 2025.
                <cite class="resource-title"
                  >&ldquo;Coupled High-Resolution Land-Atmosphere Modeling for
                  Hydroclimate and Terrestrial Hydrology in Alaska and the Yukon
                  River Basin (1990-2021).&rdquo;</cite
                >
                Journal of Geophysical Research: Atmospheres 130(1):
                e2024JD041185
                <a href="https://doi.org/10.22541/essoar.171052504.47039219/v1"
                  >https://doi.org/10.22541/essoar.171052504.47039219/v1</a
                >
              </li>
              <li>
                Cheng, Y., A. P. Craig, K. N. Musselman, and A. J. Newman. 2024.
                <cite class="resource-title"
                  >&ldquo;Multi-Decadal Historical Regional Hydroclimate
                  Simulation with Two Mid 21st Century Pseudo-Global Warming
                  Futures over Alaska and the Yukon at 4 km
                  Resolution.&rdquo;</cite
                >
                Research Data Archive at the National Center for Atmospheric
                Research, Computational and Information Systems Laboratory.
                <a href="https://doi.org/10.5065/ZPSB-PS82"
                  >https://doi.org/10.5065/ZPSB-PS82</a
                >.
              </li>
              <li>
                LaFontaine, J.H., Hay, L.E., Viger, R.J., Markstrom, S.L.,
                Regan, R.S., Elliott, C.M., and Jones, J.W., 2013,
                <cite class="resource-title"
                  >Application of the Precipitation-Runoff Modeling System
                  (PRMS) in the Apalachicola-Chattahoochee-Flint River Basin in
                  the southeastern United States</cite
                >: U.S. Geological Survey Scientific Investigations Report
                2013-5162, 118 p.,
                <a href="http://pubs.usgs.gov/sir/2013/5162/"
                  >http://pubs.usgs.gov/sir/2013/5162/</a
                >.
              </li>
              <li>
                LaFontaine, J.H., Hay, L.E., and Riley, J.R., 2023,
                <cite class="resource-title"
                  >Application of the National Hydrologic Model Infrastructure
                  with the Precipitation-Runoff Modeling System (NHM-PRMS),
                  1950-2010, Maurer Calibration</cite
                >: U.S. Geological Survey data release,
                <a href="https://doi.org/10.5066/P9CVHLMB"
                  >https://doi.org/10.5066/P9CVHLMB</a
                >.
              </li>
              <li>
                Terando, A.J., Tucker, A.M., Runyon, A.N., Miller, J., Perkins,
                J.L., Kimbrel, S.W., Cross, A.S., and Boyles, R.P., 2024,
                <cite class="resource-title"
                  >Best practices for incorporating climate change science into
                  Department of the Interior analyses, consultations, and
                  decision making</cite
                >, iv, 72 p.,
                <a href="https://doi.org/10.21429/hjgj-j073"
                  >https://doi.org/10.21429/hjgj-j073</a
                >.
              </li>
              <li>
                Sohl, T.L., Sayler, K.L., Bouchard, M.A., Reker, R.R., Friesz,
                A.M., Bennett, S.L., Sleeter, B.M., Sleeter, R.R., Wilson, T.,
                Soulard, C., Knuppe, M. and Van Hofwegen, T. (2014),
                <cite class="resource-title"
                  >Spatially explicit modeling of 1992&ndash;2100 land cover and
                  forest stand age for the conterminous United States.</cite
                >
                Ecological Applications, 24: 1015-1036.
                <a href="https://doi.org/10.1890/13-1245.1"
                  >https://doi.org/10.1890/13-1245.1</a
                >
              </li>
              <li>
                Yamazaki, D., Ikeshima, D., Sosa, J., Bates, P. D., Allen, G.
                H., &amp; Pavelsky, T. (2019).
                <cite class="resource-title"
                  >MERIT Hydro: A high&hyphen;resolution global hydrography map
                  based on latest topography datasets.</cite
                >
                Water Resources Research, 55, 5053&ndash;5073.
                <a href="https://doi.org/10.1029/2019WR024873"
                  >https://doi.org/10.1029/2019WR024873</a
                >
              </li>
            </ul>
            <h4>Additional resources</h4>
            <ul>
              <li>
                <cite class="resource-title">3D Hydrography Program</cite>,
                USGS,
                <a href="https://www.usgs.gov/3d-hydrography-program"
                  >https://www.usgs.gov/3d-hydrography-program</a
                >
                (Accessed 7/16/2026)
              </li>
              <li>
                Abouali, Mohammad , Fariborz Daneshvar, A. Pouyan Nejadhashemi
                (2016).
                <cite class="resource-title"
                  >MATLAB Hydrological Index Tool (MHIT): A high performance
                  library to calculate 171 ecologically relevant hydrological
                  indices</cite
                >, Ecological Informatics, Volume 33, 2016, Pages 17-23,
                <a href="https://doi.org/10.1016/j.ecoinf.2016.03.004"
                  >https://doi.org/10.1016/j.ecoinf.2016.03.004</a
                >.
              </li>
              <li>
                <cite class="resource-title"
                  >Alaska Water Temperature Database (AKTEMP)</cite
                >. 2024. Water temperature data collected by 35 data providers,
                893 stations.
                <a href="https://aktemp.uaa.alaska.edu/#/"
                  >https://aktemp.uaa.alaska.edu/#/</a
                >
              </li>
              <li>
                Arp, C., and Cherry, J. 2022.
                <cite class="resource-title"
                  >River and lake ice phenology data for Alaska and Northwest
                  Canada from 1882 to 2021.</cite
                >
                National Science Foundation Arctic Data Center.
                <a href="https://doi.org/10.18739/A28W38388"
                  >doi:10.18739/A28W38388</a
                >
              </li>
              <li>
                Bieniek, P. A., U. S. Bhatt, R. L. Thoman, H. Angeloff, J.
                Partain, J. Papineau, F. Fritsch, et al. 2012.
                <cite class="resource-title"
                  >&ldquo;Climate Divisions for Alaska Based on Objective
                  Methods.&rdquo;</cite
                >
                Journal of Applied Meteorology and Climatology 51:
                1276&ndash;89.
                <a href="https://doi.org/10.1175/JAMC-D-11-0168.1"
                  >https://doi.org/10.1175/JAMC-D-11-0168.1</a
                >
              </li>
              <li>
                Blaskey, D., Cheng, Y., Newman, A.J., Koch, J.C., Gooseff, M.N.,
                and Musselman, K.N. 2025.
                <cite class="resource-title"
                  >Alaskan hydrology in transition: changing precipitation and
                  evapotranspiration patterns are projected to reshape seasonal
                  streamflow and water temperatures by midcentury
                  (2035&ndash;64).</cite
                >
                J. Hydrometeorology, 26: 613&ndash;626.
                <a href="https://doi.org/10.1175/JHM-D-24-0121.1"
                  >https://doi.org/10.1175/JHM-D-24-0121.1</a
                >
              </li>
              <li>
                Blaskey, D., J. C. Koch, M. N. Gooseff, A. J. Newman, Y. Cheng,
                J. A. O&rsquo;Donnell, and K. N. Musselman. 2023.
                <cite class="resource-title"
                  >&ldquo;Increasing Alaskan River Discharge during the Cold
                  Season Is Driven by Recent Warming.&rdquo;</cite
                >
                Environmental Research Letters 18: 024042
                <a href="https://doi.org/10.1088/1748-9326/acb661"
                  >https://doi.org/10.1088/1748-9326/acb661</a
                >
              </li>
              <li>
                Curran, J. H., and F. E. Biles. 2021.
                <cite class="resource-title"
                  >&ldquo;Identification of Seasonal Streamflow Regimes and
                  Streamflow Drivers for Daily and Peak Flows in
                  Alaska.&rdquo;</cite
                >
                Water Resources Research 57:e2020WR028425
                <a href="https://doi.org/10.1029/2020WR028425"
                  >https://doi.org/10.1029/2020WR028425</a
                >
              </li>
              <li>
                Datry T, Boulton AJ, Fritz K, Stubbington R, Cid N, Crabot J,
                Tockner K.
                <cite class="resource-title"
                  >Non-perennial segments in river networks.</cite
                >
                Nat Rev Earth Environ. 2023 Dec;4:815-830.
                <a href="https://doi.org/10.1038/s43017-023-00495-w"
                  >https://doi.org/10.1038/s43017-023-00495-w</a
                >.
              </li>
              <li>
                De Cicco, L. A., R. M. Hirsch, D. Lorenz, and W. D. Watkins.
                2022.
                <cite class="resource-title"
                  >&ldquo;dataRetrieval: R Packages for Discovering and
                  Retrieving Water Data Available from Federal Hydrologic Web
                  Services.&rdquo;</cite
                >
                <a href="https://doi.org/10.32614/CRAN.package.dataRetrieval"
                  >https://doi.org/10.32614/CRAN.package.dataRetrieval</a
                >
              </li>
              <li>
                Dudley, R.W., and Nielsen, M.G., 2011).
                <cite class="resource-title"
                  >Simulation of streamflow in the Pleasant, Narraguagus,
                  Sheepscot, and Royal Rivers, Maine, using watershed
                  models</cite
                >: U.S. Geological Survey Scientific Investigations Report
                2010&ndash;5221, 31 p., at
                <a href="http://pubs.usgs.gov/sir/2010/5221/"
                  >http://pubs.usgs.gov/sir/2010/5221/</a
                >.
              </li>
              <li>
                Elkins, Duncan, Sarah C. Sweat, Bernard R. Kuhajda, Anna L.
                George, Katie S. Hill, Seth J. Wenger,
                <cite class="resource-title"
                  >Illuminating hotspots of imperiled aquatic biodiversity in
                  the southeastern US</cite
                >, Global Ecology and Conservation, Volume 19, 2019,
                <a href="https://doi.org/10.1016/j.gecco.2019.e00654"
                  >https://doi.org/10.1016/j.gecco.2019.e00654</a
                >.
              </li>
              <li>
                Falke, J.A. and J.D. Paul, 2024,
                <cite class="resource-title"
                  >Spatial and Tabular Datasets Supporting the "Freshwater
                  Habitat Potential for Chinook Salmon in the Yukon and
                  Kuskokwim River Basins, Alaska" Project</cite
                >: U.S. Geological Survey data release,
                <a href="https://doi.org/10.5066/P95AV4JO"
                  >https://doi.org/10.5066/P95AV4JO</a
                >.
              </li>
              <li>
                Falke, J. A., B. M. Huntsman, and E. R. Schoen. 2019.
                <cite class="resource-title"
                  >&ldquo;Climatic Variation Drives Growth Potential of Juvenile
                  Chinook Salmon (Oncorhynchus tshawytscha) along a Sub-Arctic
                  Boreal Riverscape.&rdquo;</cite
                >
                In Advances in Understanding Landscape Influences on Freshwater
                Habitats and Biological Assemblages 57&ndash;82. Bethesda, MD:
                American Fisheries Society.
                <a href="https://doi.org/10.47886/9781934874561.ch4"
                  >https://doi.org/10.47886/9781934874561.ch4</a
                >
              </li>
              <li>
                Hay, L.E., Leavesley, G.H., Clark, M.P., Markstrom, S.L., Viger,
                R.J. and Umemoto, M. (2006),
                <cite class="resource-title"
                  >STEP WISE, MULTIPLE OBJECTIVE CALIBRATION OF A HYDROLOGIC
                  MODEL FOR A SNOWMELT DOMINATED BASIN1.</cite
                >
                JAWRA Journal of the American Water Resources Association, 42:
                877-890.
                <a href="https://doi.org/10.1111/j.1752-1688.2006.tb04501.x"
                  >https://doi.org/10.1111/j.1752-1688.2006.tb04501.x</a
                >
              </li>
              <li>
                Holmes, K., A. I. Shiklomanov, A. Suslova, M. Tretiakov, J. W.
                McClelland, L. Scott, R. G. M. Spencer, and S. E. Tank. 2021.
                <cite class="resource-title"
                  >&ldquo;River Discharge. NOAA Technical Report OAR ARC
                  21&ndash;11.&rdquo;</cite
                >
                <a href="https://repository.library.noaa.gov/view/noaa/34199"
                  >https://repository.library.noaa.gov/view/noaa/34199</a
                >
              </li>
              <li>
                Jaeger KL, Olden JD, Pelland NA.
                <cite class="resource-title"
                  >Climate change poised to threaten hydrologic connectivity and
                  endemic fishes in dryland streams.</cite
                >
                Proc Natl Acad Sci U S A. 2014 Sep 23;111(38):13894-9.
                <a href="https://doi.org/10.1073/pnas.13208901"
                  >https://doi.org/10.1073/pnas.13208901</a
                >
              </li>
              <li>
                Koch, J. C., Y. Sj&ouml;berg, J. A. O&rsquo;Donnell, M. P.
                Carey, P. F. Sullivan, and A. Terskaia. 2022.
                <cite class="resource-title"
                  >&ldquo;Sensitivity of Headwater Streamflow to Thawing
                  Permafrost and Vegetation Change in a Warming
                  Arctic.&rdquo;</cite
                >
                Environmental Research Letters 17: 044074
                <a href="https://doi.org/10.1088/1748-9326/ac5f2d"
                  >https://doi.org/10.1088/1748-9326/ac5f2d</a
                >
              </li>
              <li>
                Krabbenhoft CA, Rogosch JS, Rowland FE.
                <cite class="resource-title"
                  >Long-Term Regime Shifts in Xeric Ecoregion Freshwater Fish
                  Assemblages due to Anthropogenic and Climate Stressors.</cite
                >
                Ecol Evol. 2025 Sep 1;15(9):e72067.
                <a href="https://doi.org/10.1002/ece3.72067"
                  >https://doi.org/10.1002/ece3.72067</a
                >.
              </li>
              <li>
                Markstrom, S.L., Regan, R.S., Hay, L.E., Viger, R.J., Webb,
                R.M.T., Payn, R.A., and LaFontaine, J.H., 2015,
                <cite class="resource-title"
                  >PRMS-IV, the precipitation-runoff modeling system, version
                  4</cite
                >: U.S. Geological Survey Techniques and Methods, book 6, chap.
                B7, 158 p.,
                <a href="https://doi.org/10.3133/tm6B7"
                  >https://doi.org/10.3133/tm6B7</a
                >
              </li>
              <li>
                Mauger, S., Shaftel, R., Leppi, J.C., and Rinella, D.J. 2017.
                <cite class="resource-title"
                  >Summer temperature regimes in southcentral Alaska streams:
                  watershed drivers of variation and potential implications for
                  Pacific salmon.</cite
                >
                Can. J. Fish. Aquat. Sci. 74: 702&ndash;715.
                <a href="https://doi.org/10.1139/cjfas-2016-0076"
                  >https://doi.org/10.1139/cjfas-2016-0076</a
                >.
              </li>
              <li>
                <cite class="resource-title">New NHDPlus HR Map Service</cite>
                By National Hydrography September 15, 2020
                <a href="https://www.usgs.gov/news/new-nhdplus-hr-map-service"
                  >https://www.usgs.gov/news/new-nhdplus-hr-map-service</a
                >
                (Accessed 7/16/2026).
              </li>
              <li>
                Regan, R.S., and LaFontaine, J.H., 2017,
                <cite class="resource-title"
                  >Documentation of the dynamic parameter, water-use, stream and
                  lake flow routing, and two summary output modules and updates
                  to surface-depression storage simulation and initial
                  conditions specification options with the Precipitation-Runoff
                  Modeling System (PRMS)</cite
                >: U.S. Geological Survey Techniques and Methods, book 6, chap.
                B8, 60 p.,
                <a href="https://doi.org/10.3133/tm6B8"
                  >https://doi.org/10.3133/tm6B8</a
                >.
              </li>
              <li>
                Regan, R.S., Markstrom, S.L., Hay, L.E., Viger, R.J., Norton,
                P.A., Driscoll, J.M., LaFontaine, J.H., 2018,
                <cite class="resource-title"
                  >Description of the National Hydrologic Model for use with the
                  Precipitation-Runoff Modeling System (PRMS)</cite
                >: U.S. Geological Survey Techniques and Methods, book 6, chap
                B9, 38 p.,
                <a href="https://doi.org/10.3133/tm6B9"
                  >https://doi.org/10.3133/tm6B9</a
                >.
              </li>
              <li>
                Schoen, E. R., K. G. Howard, J. M. Murphy, D. E. Schindler, P.
                A. H. Westley, and V. R. von Biela. 2023.
                <cite class="resource-title"
                  >&ldquo;Divergent Responses of Western Alaska Salmon to a
                  Changing Climate.&rdquo;</cite
                >
                NOAA Arctic Report Card.
                <a href="https://doi.org/10.25923/f2hv-5581"
                  >https://doi.org/10.25923/f2hv-5581</a
                >
              </li>
              <li>
                Sergeant, C. J., J. A. Falke, R. A. Bellmore, J. R. Bellmore,
                and R. L. Crumley. 2020.
                <cite class="resource-title"
                  >&ldquo;A Classification of Streamflow Patterns across the
                  Coastal Gulf of Alaska.&rdquo;</cite
                >
                Water Resources Research 56: e2019WR026127.
                <a href="https://doi.org/10.1029/2019WR026127"
                  >https://doi.org/10.1029/2019WR026127</a
                >
              </li>
              <li>
                Shaftel, R. 2024.
                <cite class="resource-title"
                  >&ldquo;Data From: Integrating Climate Data and River Modeling
                  to Reveal Influences on Declining Chinook Salmon in Sub-Arctic
                  River Basins.&rdquo;</cite
                >
                Data set. Zenodo.
                <a href="https://doi.org/10.5281/zenodo.14029373"
                  >https://doi.org/10.5281/zenodo.14029373</a
                >.
              </li>
              <li>
                Shaftel, R., S. Mauger, J. Falke, D. Rinella, J. Davis, and L.
                Jones. 2020.
                <cite class="resource-title"
                  >&ldquo;Thermal Diversity of Salmon Streams in the
                  Matanuska-Susitna Basin, Alaska.&rdquo;</cite
                >
                Journal of the American Water Resources Association 56:
                630&ndash;646
                <a href="https://doi.org/10.1111/1752-1688.12839"
                  >https://doi.org/10.1111/1752-1688.12839</a
                >.
              </li>
              <li>
                Shaftel, R., Feddern, M.L., McAfee, S.A., Schoen, E.R.,
                Cunningham, C., von Biela, V.R., et al. 2026.
                <cite class="resource-title"
                  >Integrating climate data and river modeling to reveal Chinook
                  salmon habitat conditions in sub-Arctic river basins.</cite
                >
                Ecosphere.
                <a href="https://doi.org/10.1002/ecs2.70399"
                  >https://doi.org/10.1002/ecs2.70399</a
                >
              </li>
              <li>
                Sun, Ge; Caldwell, Peter V.; McNulty, Steven G.; Georgakakos,
                Aris P.; Arumugam, Sankar; Cruise, James; McNider, Richard T.;
                Terando, Adam; Conrads, Paul A.; Feldt, John; Misra, Vasu;
                Romolo, Luigi; Rasmussen, Todd C.; Marion, Daniel A. 2013.
                <cite class="resource-title"
                  >Impacts of Climate Change and Variability on Water Resources
                  in the Southeast USA.</cite
                >
                NCA Southeast Technical Report 204-234.
                <a href="https://doi.org/10.5822/978-1-61091-509-0_10"
                  >https://doi.org/10.5822/978-1-61091-509-0_10</a
                >
              </li>
              <li>
                Tarek, M., F. P. Brissette, and R. Arsenault. 2020.
                <cite class="resource-title"
                  >&ldquo;Evaluation of the ERA5 Reanalysis as a Potential
                  Reference Dataset for Hydrological Modelling over North
                  America.&rdquo;</cite
                >
                Hydrology and Earth System Sciences 24: 2527&ndash;44.
                <a href="https://doi.org/10.5194/hess-24-2527-2020"
                  >https://doi.org/10.5194/hess-24-2527-2020</a
                >.
              </li>
              <li>
                U.S. Geological Survey. 2022.
                <cite class="resource-title"
                  >&ldquo;USGS Water Data for the Nation: U.S. Geological Survey
                  National Water Information System Database.&rdquo;</cite
                >
                <a href="https://doi.org/10.5066/F7P55KJN"
                  >https://doi.org/10.5066/F7P55KJN</a
                >
              </li>
              <li>
                <cite class="resource-title">Virtual Watershed Portal</cite>,
                Terrain Works,
                <a href="https://terrainworks.com/netmap-portal"
                  >https://terrainworks.com/netmap-portal</a
                >
                (Accessed 7/16/2026).
              </li>
              <li>
                von Biela, V. R., C. J. Sergeant, M. P. Carey, Z. Liller, C.
                Russell, S. Quinn-Davidson, P. S. Rand, P. A. H. Westley, and C.
                E. Zimmerman. 2022.
                <cite class="resource-title"
                  >&ldquo;Premature Mortality Observations among Alaska&rsquo;s
                  Pacific Salmon during Record Heat and Drought in
                  2019.&rdquo;</cite
                >
                Fisheries 47: 157&ndash;168.
                <a href="https://doi.org/10.1002/fsh.10705"
                  >https://doi.org/10.1002/fsh.10705</a
                >
              </li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.resource-title {
  font-weight: 500;
  font-style: normal;
}
</style>
