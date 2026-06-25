<template>
  <Intro />
  <div class="section">
    <div class="container">
      <h2 class="title is-3">Continental United States</h2>
      <p class="block is-size-4 clamp">
        This dataset is based on
        <a
          href="https://www.usgs.gov/software/precipitation-runoff-modeling-system-prms"
          >PRMS</a
        >
        (the Precipitation Runoff Modeling System), USGS, and uses the NHD
        stream network.
      </p>
      <Map region="conus" />
    </div>
  </div>
  <div class="section">
    <div class="container">
      <h2 class="title is-3">Alaska</h2>
      <p class="block is-size-4 clamp">
        Data for Alaska and parts of Western Canada is based on
        <a href="https://nps.edu/web/rasm">RASM</a> (the Regional Arctic System
        Model), Naval Postgraduate School, and uses the
        <a
          href="https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2019WR024873"
          >MERIT Hydro</a
        >
        stream network.
      </p>
      <Map region="alaska" />
    </div>
  </div>
  <a id="search-watersheds" />
  <div class="section">
    <div class="container">
      <h2 class="title is-3">Search watersheds</h2>
      <p class="block is-size-4 clamp">
        Search for a HUC8 ID in the Continental United States or Alaska using
        its name or ID number.
      </p>
      <Search />
    </div>
  </div>
</template>
