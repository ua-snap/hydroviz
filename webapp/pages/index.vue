<template>
  <Intro />
  <div class="section">
    <div class="container" id="conus-map">
      <h2 class="title is-3">Continental United States</h2>
      <p class="block is-size-4 clamp">
        This dataset is based on the Precipitation Runoff Modeling System
        (PRMS), USGS, and uses the NHD stream network.
        <NuxtLink to="data-and-methodology"
          >Read more about this data.</NuxtLink
        >
      </p>
      <Map region="conus" />
    </div>
  </div>
  <div class="section">
    <div class="container" id="alaska-map">
      <h2 class="title is-3">Alaska</h2>
      <div class="block is-size-4 clamp">
        <p>
          Data for Alaska and parts of Western Canada is based on the Regional
          Arctic System Model (RASM), Naval Postgraduate School, and uses the
          MERIT Hydro stream network.
          <NuxtLink to="/data-and-methodology"
            >Read more about this data.</NuxtLink
          >
        </p>
      </div>
      <Map region="alaska" />
    </div>
  </div>
</template>
