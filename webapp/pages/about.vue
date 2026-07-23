<template>
  <div class="container mb-6">
    <h1 class="title is-1 mt-6">Hydrologic Outlooks</h1>

    <article class="content is-size-5 clamp">
      <p class="clamp is-size-4">
        <strong>
          The goal of this site is to improve your ability to effectively and
          appropriately use hydrologic futures in natural resource management,
          ecological research, and more.
        </strong>
      </p>
      <p>
        Complex datasets that incorporate climate futures often fail to meet the
        needs of land managers, decision-makers, and rightsholders. This can be
        due to a lack of trust, poor explanations of how best to use the data,
        or technological limitations to access.
      </p>

      <p>This tool allows you to:</p>

      <ul>
        <li>
          Easily <strong>select, view and access</strong> modeled data from
          gaged and ungaged streams.
        </li>
        <li>
          Quickly
          <strong>visualize range, uncertainty, means, and extremes</strong> for
          <strong> peak flow, low flow, seasonal averages </strong>, and other
          key variables.
        </li>
        <li>
          Access <strong>data downloads in flexible CSV format</strong> or
          directly from the API to create customized outputs.
        </li>
      </ul>
    </article>

    <section class="block">
      <h2 class="title is-3">Who is this site for?</h2>
      <div class="content is-size-5 clamp">
        <p>
          This web tool was designed to meet the needs of
          <strong> land managers, hydrologists, ecologists, engineers </strong>,
          and anyone else in need of hydrologic information for use in
          <strong>long-term landscape-level planning</strong>. The
          visualizations offer a stepping-off point so you can quickly
          understand the most important aspects of the datasets, including
          <strong>
            projected change, range of projections, uncertainties, and key
            take-aways </strong
          >. If you need the full range of data for all models, emissions
          scenarios, and time periods, the site offers CSV (spreadsheet)
          downloads that you can use to create your own graphics and perform
          your own analyses. Best practices, examples and case studies are
          outlined in the <NuxtLink to="/how-to">How-To Guide</NuxtLink>.
        </p>
      </div>
    </section>

    <section class="block">
      <h2 class="title is-3">Can modeled data be trusted?</h2>
      <div class="content is-size-5 clamp">
        <p>
          <strong
            >Modeled data is not perfect&mdash;and it&rsquo;s not a
            forecast</strong
          >. In some cases, the results may appear to be a poor representation
          of reality. Those who monitor streams and rivers and those who live
          and work on the land have personal and direct knowledge of the timing
          of stream flows. A stream gage offers more accurate and precise
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
          that these models show. In other words,
          <strong>
            models will not show you exactly how a stream will behave on a
            single day, but they are a powerful tool for assessing trends across
            time </strong
          >.
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
          You can select locations, timeframes, and possible climate futures
          most pertinent to the decisions you need to make.
          <strong>
            By comparing multiple plausible futures, you can interpret and
            define uncertainty in a way that makes sense in the context of your
            own work.</strong
          >
        </p>
      </div>
    </section>

    <section class="block">
      <h2 class="title is-3">Where did the data come from?</h2>
      <div class="content is-size-5 clamp">
        <p>
          The Hydrologic Futures tool is built primarily on PRMS (the
          Precipitation Runoff Modeling System), a USGS model used to simulate
          streamflow and water budgets under a range of climate and land use
          scenarios. For Alaska and parts of western Canada, the tool instead
          relies on a separate regional model, RASM, since both the hydrologic
          modeling and the climate projections differ from those used for the
          continental US. For details on the specific models, data, and methods
          behind the tool, see our
          <NuxtLink to="/data-and-methodology">data and methodology</NuxtLink>
          page.
        </p>
      </div>
    </section>
  </div>
</template>
