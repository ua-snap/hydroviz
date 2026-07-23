<template>
  <div class="container mb-6">
    <h1 class="title is-1 mt-6">Hydrologic Outlooks</h1>

    <article class="content is-size-5 clamp">
      <p>
        Complex datasets that incorporate climate futures often fail to meet the
        needs of land managers, decision-makers, and rightsholders. This can be
        due to a lack of trust, poor explanations of how best to use the data,
        or technological limitations to access.
      </p>

      <p>
        The goal of this site is to improve your ability to effectively and
        appropriately use hydrologic futures in natural resource management,
        ecological research, and more.
      </p>

      <p>This tool allows you to:</p>

      <ul>
        <li>
          Easily select, view and access interactive modeled data from gaged and
          ungaged streams and watersheds (HUC8).
        </li>
        <li>
          Quickly visualize range, uncertainty, means, and extremes for peak
          flow, low flow, seasonal averages, and other key variables.
        </li>
        <li>
          Access data downloads in flexible csv format or directly from the API
          to create customized outputs.
        </li>
      </ul>
    </article>

    <section class="block">
      <h2 class="title is-3">Who is this site for?</h2>
      <div class="content is-size-5 clamp">
        <p>
          This web tool was designed to meet the needs of land managers,
          hydrologists, ecologists, engineers, and anyone else in need of
          hydrologic information for use in long-term landscape-level planning.
          The visualizations offer a stepping-off point so you can quickly
          understand the most important aspects of the datasets, including
          projected change, range of projections, uncertainties, and key
          take-aways. If you need the full range of data for all models,
          emissions scenarios, and time periods, the site offers csv downloads
          that you can use to create your own graphics and perform your own
          analyses.
        </p>
      </div>
    </section>

    <section class="block">
      <h2 class="title is-3">Can modeled data be trusted?</h2>
      <div class="content is-size-5 clamp">
        <p>
          Modeled data is not perfect&mdash;and it&rsquo;s not a forecast. In
          some cases, the results may appear to be a poor representation of
          reality. Those who monitor streams and rivers and those who live and
          work on the land have personal and direct knowledge of the timing of
          stream flows. A stream gage offers more accurate and precise
          measurements than any model can. You may need to use local fine-scale
          ground-truthed models for some purposes, or you may need to rely only
          on gaged or measured flows. However, not all streams have gages. Even
          those that do may have intermittent data. And no stream gage can offer
          projections months, years, or decades into the future.
        </p>

        <p>
          Although there is a wide range of uncertainty in the model outputs
          shared on this site&mdash;<NuxtLink to="/models-uncertainty-trust"
            >discussed in more detail here</NuxtLink
          >&mdash;it can still be helpful to incorporate the signals of change
          that these models show. In other words, models will not show you
          exactly how a stream will behave on a single day, but they are a
          powerful tool for assessing trends across time.
        </p>
      </div>
    </section>

    <section class="block">
      <h2 class="title is-3">Why this approach?</h2>
      <div class="content is-size-5 clamp">
        <p>
          There are multiple ways to model stream networks, as well as specific
          models used to assess and predict storm water, surface flows, and
          groundwater. This site focuses on making it quick and easy for you to
          access and fully interpret datasets that are geographically broad,
          complete, and continuous.
        </p>

        <p>
          This site allows you to select locations, timeframes, and possible
          climate futures most pertinent to the decisions you need to make. By
          comparing multiple plausible futures, you can interpret and define
          uncertainty in a way that makes sense in the context of your own work.
        </p>
      </div>
    </section>

    <section class="block">
      <h2 class="title is-3">Where did the data come from?</h2>
      <div class="content is-size-5 clamp">
        <p>
          The Hydrologic Futures tool is primarily based on
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
          >. In order to incorporate data for Alaska and parts of western
          Canada, we have also included data from on
          <a href="https://nps.edu/web/rasm">RASM</a> (the Regional Arctic
          System Model), based on a dataset published by
          <a href="https://search.dataone.org/view/doi%3A10.18739%2FA25M62870"
            >Blaskey et. al, 2024</a
          >. Note that Alaska data is not only based on different hydrologic
          models than those used for the continental US, but also on different
          modeled climate futures (Earth System models).
        </p>
      </div>
    </section>
  </div>
</template>
