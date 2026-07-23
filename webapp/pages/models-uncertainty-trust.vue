<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">Models, Uncertainty, and Trust</h1>
      <p class="content is-size-4 clamp">
        This page outlines the different types of models used to produce the
        datasets that this tool offers, and gives important
        <NuxtLink to="#uncertainty"
          >guidance on how to frame uncertainty</NuxtLink
        >
        when interpreting the data and
        <NuxtLink to="#trust">
          thinking about the trustworthiness of modeled data.</NuxtLink
        >
      </p>
      <div class="content clamp is-size-5">
        <div class="block pt-5">
          <h2 class="title is-4">What models are used in this tool?</h2>
          <p>
            These hydrologic futures were created using three kinds of models:
            streamflow network models, climate models, and the hydrologic models
            themselves. The PRMS dataset also incorporates an additional model
            for future land use.
          </p>
          <p>
            PRMS uses climate projections from thirteen bias-corrected models
            from the Coupled Model Intercomparison Project Phase 5 (<a
              href="https://wcrp-cmip.org/cmip-phases/cmip5/"
              >CMIP5</a
            >) from the World Climate Research Programme (<a
              href="https://www.wcrp-climate.org/"
              >WCRP</a
            >). Alaska data is based on
            <a href="https://wcrp-cmip.org/cmip-phases/cmip6/">CMIP6</a>.
            <NuxtLink to="/data-and-methodology">Read more details</NuxtLink>
            about the datasets used in this tool.
          </p>
        </div>

        <div class="block pt-5" id="uncertainty">
          <h2 class="title is-4">
            What are the major sources of data uncertainty?
          </h2>

          <p>Data uncertainty stems from several key factors:</p>
          <ul>
            <li>
              <strong>Spatial uncertainty</strong>
              <ul>
                <li>
                  The stream network is an estimation and may not match local
                  topography perfectly.
                </li>
                <li>
                  The spatial resolution of climate data, even after
                  downscaling, is coarser than that of stream networks, and may
                  not perfectly represent fine-scale topographic and localized
                  effects.
                </li>
              </ul>
            </li>
            <li>
              <strong>Short-term uncertainty in streamflow modeling</strong>
              <ul>
                <li>
                  Hydrologic input data is limited, particularly regarding the
                  temporal and spatial resolution of precipitation.
                </li>
                <li>
                  A limited quantity of data is available from stream gages for
                  use in model calibration.
                </li>
              </ul>
            </li>
            <li>
              <strong>Long-term uncertainty</strong>
              <ul>
                <li>
                  Future human behavior is intrinsically uncertain, as described
                  by
                  <a
                    href="https://www.climatehubs.usda.gov/hubs/northwest/topic/what-are-climate-model-phases-and-scenarios"
                    >RCP</a
                  >s and
                  <a
                    href="https://www.sciencedirect.com/science/article/pii/S0959378016300681"
                    >SSPs</a
                  >.
                </li>
                <li>
                  Simplifications and assumptions in earth system model
                  structure and errors or limitations in meteorological and
                  hydrologic measurements lead to earth system model differences
                  and biases. Considering multiple climate models can offset
                  these biases, as detailed in the How-to Guide.
                </li>
              </ul>
            </li>
          </ul>
        </div>

        <div class="block pt-6" id="trust">
          <h2 class="title is-4">How can we trust these datasets?</h2>
          <p>
            <strong>
              Data used in decision-making needs to be interpreted in a way that
              is meaningful and trustworthy </strong
            >. Understanding how to minimize and categorize uncertainty can help
            you make informed choices about how to apply the dataset and frame
            its outputs. The following techniques can help. For additional
            advice and expertise, see our
            <NuxtLink to="/how-to">How-To Guide</NuxtLink> and this excellent
            external resource:
            <NuxtLink to="https://pubs.usgs.gov/publication/70260921">
              &ldquo;Best practices for incorporating climate change science
              into Department of the Interior analyses, consultations, and
              decision making.&rdquo;</NuxtLink
            >
          </p>
          <ul>
            <li>
              <strong>
                Compare model outputs and actual gage data for areas you are
                familiar with
              </strong>
              to get an understanding of where the models agree with
              observational data, where they differ, and in what ways they
              differ.
            </li>
            <li>
              <strong>
                Look at the difference between time periods for a given variable </strong
              >&mdash;the change signal&mdash;rather than the absolute values
              for that variable.
              <strong>
                Framing possible future changes by relative magnitude </strong
              >, e.g. a 50% increase in maximum daily flow, can incorporate the
              realities of model uncertainty while still offering useful
              insight.
            </li>
            <li>
              <strong>Site-specific bias correction</strong> is an approach that
              can address numerical misalignment while preserving change
              signals. This is a mathematical approach in which a statistical
              relationship or scaling factor is calculated to adjust model
              predictions for a specific site, based on known measurements.
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
#uncertainty {
  ul ul {
    margin-top: 0;
    margin-bottom: 1rem;
  }
}
</style>
