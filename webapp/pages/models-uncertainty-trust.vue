<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">Models, Uncertainty, and Trust</h1>
      <p class="content is-size-4 clamp">
        This page outlines the different models used to produce this dataset,
        and gives important
        <NuxtLink to="#uncertainty"
          >guidance on how to frame uncertainty</NuxtLink
        >
        with interpreting the data. We directly address the question,
        <NuxtLink to="#trust"> how can we trust these datasets?</NuxtLink>
      </p>
      <div class="content clamp is-size-5">
        <div class="block pt-5">
          <h2 class="title is-4">What models are used in this tool?</h2>
          <p>
            Both datasets share three common kinds of models: the
            <strong> streamflow network </strong>, an abstraction of stream
            location; <strong>climate models</strong>, which provide inputs to
            the hydrologic models; and the <strong>hydrologic models</strong>
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
              Spatial uncertainty
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
              Short-term uncertainty in streamflow modeling
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
              Long-term uncertainty
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
            One way to approach the question of trust with these datasets is to
            look at the limitations inherent in the uncertainty of modeling, and
            make informed choices about how to apply the dataset in practice or
            frame its outputs for decision making.
          </p>
          <ul>
            <li>
              Compare model outputs and actual gage data for areas you are
              familiar with to get an understanding of where the models agree
              with observational data, and where they differ.
            </li>
            <li>
              Look at the change signal above the absolute values. Framing
              possible future changes by relative magnitude can incorporate the
              realities of model uncertainty while still offering useful
              insight.
            </li>
            <li>
              Site-specific bias correction&mdash;the process of applying
              observational datasets to perform arithmetic corrections on
              specific stream segments to better align the model with
              records&mdash;is a rigorous approach that can address numerical
              alignment while preserving change signals.
            </li>
            <li>
              Read the literature to learn in depth about model performance and
              evaluation.
            </li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>
