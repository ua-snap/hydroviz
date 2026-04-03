<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">Models and Uncertainty</h1>
      <div class="content is-size-4">
        <div class="mb-5">
          <h2 class="title is-4">
            What climate models and scenarios are used in this tool?
          </h2>
          <p>
            PRMS and the Hydrologic Futures tool use climate projections from
            thirteen bias-corrected models from the Coupled Model
            Intercomparison Project Phase 5 (<a
              href="https://wcrp-cmip.org/cmip-phases/cmip5/"
              >CMIP5</a
            >) from the World Climate Research Programme (<a
              href="https://www.wcrp-climate.org/"
              >WCRP</a
            >). All models offer several future scenarios based on differing
            atmospheric Representative Concentration Pathways (<a
              href="https://www.ipcc-data.org/guidelines/pages/glossary/glossary_r.html"
              >RCPs</a
            >). These are based on different radiative forcing levels in Watts
            per square meter (W/m&sup2;).
          </p>
        </div>
        <div class="mb-5">
          <h2 class="title is-4">
            What are the major sources of data uncertainty?
          </h2>
          <p>
            Data uncertainty stems from several key factors. Spatial uncertainty
            and short-term temporal uncertainty can largely be attributed to
            uncertainty in hydrologic input data, particularly the temporal and
            spatial resolution of precipitation, and lack of stream gages for
            use in model calibration. Long-term uncertainty can be attributed to
            the intrinsic uncertainty of future human behavior, as described by
            <a
              href="https://www.climatehubs.usda.gov/hubs/northwest/topic/what-are-climate-model-phases-and-scenarios"
              >RCPs</a
            >. Additional uncertainty at all levels can arise from
            simplifications and assumptions in model structure and errors or
            limitations in meteorological and hydrologic measurements that lead
            to model differences.
          </p>
        </div>
        <div>
          <h2 class="title is-4">
            How are future changes in land use accounted for?
          </h2>
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
            downloads for more extensive analysis.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
