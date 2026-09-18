<template>
  <Intro />
  <div class="section">
    <div class="container" id="conus-map">
      <h2 class="title is-3">Continental United States</h2>
      <p class="block is-size-4 clamp">
        This dataset is based on the Precipitation Runoff Modeling System
        (PRMS), USGS, and uses the NHD stream network.
        <NuxtLink to="/data-and-methodology"
          >Read more about this data.</NuxtLink
        >
      </p>
      <Map region="conus" />
    </div>
  </div>
  <div class="section">
    <div class="container" id="alaska-map">
      <h2 class="title is-3">Alaska &amp; Northwest Canada</h2>
      <div class="block is-size-4 clamp">
        <p>
          These streamflow and river-temperature projections come from the
          NSF-funded
          <a
            href="https://www.colorado.edu/research/arctic-rivers/"
            rel="external"
            >Arctic Rivers Project</a
          >, developed collaboratively for use by communities and decision
          makers.
          <NuxtLink to="/data-and-methodology"
            >Read more about this data.</NuxtLink
          >
          The hydrologic model is the Regional Arctic System Model (RASM), and
          uses the MERIT Hydro stream network.
        </p>
      </div>
      <Map region="alaska" />
    </div>
  </div>
</template>
