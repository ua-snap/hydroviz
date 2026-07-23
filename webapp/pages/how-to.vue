<template>
  <section class="section">
    <div class="container">
      <h1 class="title is-1">How-To Guide</h1>
      <div class="block content is-size-4 clamp">
        <p>
          Read below for some tips on best practices when using data from this
          tool, ideas on
          <NuxtLink to="#csv">how to use the CSV downloads</NuxtLink>,
          <NuxtLink to="#practical-examples">example use cases</NuxtLink>, or
          <NuxtLink to="/models-uncertainty-trust"
            >learn more about models and uncertainty.</NuxtLink
          >
        </p>
      </div>
      <div class="content block is-size-5 pt-5 clamp">
        <h3 class="title is-4">
          What are the most effective ways to use this tool?
        </h3>

        <p>
          <a href="https://pubs.usgs.gov/publication/70260921"
            >This publication</a
          >
          is a great guide to incorporating climate change science into
          analysis, consultation, and decision-making. It offers technical
          guidance, practical application examples, and resource lists. Key
          points are summarized below.
        </p>

        <ul>
          <li>
            <strong>Focus on broad regions and timespans.</strong> Given the
            sources of uncertainty associated with this dataset, tool outputs
            are most appropriate for broadly assessing hydrologic change over
            time, at the level of hydrologic units or landscapes, rather than
            for specific stream segments. Visuals within the tool have been
            designed to depict summaries of change, including range and
            uncertainty.
          </li>
          <li>
            <strong>Compare multiple climate models.</strong> All Earth System
            Models and Global Climate Models include some uncertainty. Looking
            at several models allows you to see a wider range of plausible
            futures.
          </li>
          <li>
            <strong>Consider multiple scenarios.</strong> Each climate model is
            run using more than one scenario of future societal behavior and
            resulting greenhouse gas concentrations (RCPs, Representative
            Concentration Pathways or SSPs, Shared Socio-economic Pathways).
            Which RCP you choose to focus on will depend on the costs and
            benefits of each of these possible futures, and the risks associated
            with management choices.
          </li>
          <li>
            <strong>Pick a pertinent time period.</strong> This tool is not
            intended to generate short-term forecasts. Use a time-period for
            model projections of the future climate change consistent with the
            relevant timeframe of the policy, action, or decision being
            considered.
          </li>
          <li>
            <strong>Clearly document outputs from data downloads.</strong> For
            those who choose to download data for tailored uses, particular care
            should be taken to consider the pros and cons of viewing specific
            models, scenarios (RCPs) and time periods, as described above, and
            to record and explain why subsets of the data were selected.
          </li>
          <li>
            <strong>Clearly describe key analysis uncertainties.</strong> In
            conjunction with all of the above, users should take care to include
            caveats and explanations of sources of uncertainty in outputs,
            products, and decisions associated with this tool and the data that
            supports it.
          </li>
        </ul>
      </div>
      <div id="csv" class="content block is-size-5 pt-5 clamp">
        <h3 class="title is-4">What can I do with CSV downloads?</h3>
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
            selected set, calculate deltas between two time periods, or find the
            range or standard deviation across models.
          </li>
          <li>
            <strong>Isolate specific days or custom time periods</strong> that
            monthly averages don&rsquo;t capture, such as an ecologically
            defined window like spawning season or spring thaw.
          </li>
        </ul>
      </div>
      <div id="practical-examples" class="content block is-size-5 clamp pt-5">
        <h3 class="title is-4">Practical examples</h3>
        <div class="block">
          <h4 class="title is-5">
            Dry-season flows in the Mobile River system
          </h4>
          <h5 class="subtitle is-5">&ldquo;Rachel Researcher&rdquo;</h5>
          <p>
            Alabama&rsquo;s rivers support rich aquatic biodiversity, and the
            Mobile River system ranks among the state&rsquo;s highest
            conservation priorities (<NuxtLink
              to="https://www.sciencedirect.com/science/article/pii/S2351989418304451"
              >Elkins et al., 2019</NuxtLink
            >).
            <strong>
              Rachel Researcher wants to know whether headwater streams in the
              Mobile-Tensaw watershed (HUC 03160204) face long-term habitat
              degradation from reduced dry-season flows </strong
            >.
          </p>
          <ol>
            <li>
              She selects by HUC to zoom into the Mobile-Tensaw stream network.
            </li>
            <li>
              She visually identifies headwater streams and selects each in
              turn&mdash;no need to know their names or IDs in advance.
            </li>
            <li>
              Starting with
              <NuxtLink to="/conus/stream/8723">Chickasaw Creek</NuxtLink>, she
              scrolls down to Duration Statistics for each stream.
            </li>
            <li>
              She selects &ldquo;late century (2071&ndash;2100)&rdquo; for a
              long-term view, and leaves the default &ldquo;middle of the
              road&rdquo; scenario selected for the most likely outcome.
            </li>
            <li>
              She compares annual minimum flows&mdash;daily, 3-day average, and
              7-day average&mdash;across four headwater creeks: Chickasaw,
              Cedar, Sisters, and Threemile.
            </li>
          </ol>
          <p>
            Across the watershed, all four creeks show a consistent pattern of
            lower minimum flows, based on a long-term average across thirteen
            models&mdash;informing her recommendations on conservation goals and
            objectives.
          </p>
        </div>
        <div class="block">
          <h4 class="title is-5">Flow timing and Atlantic salmon habitat</h4>
          <h5 class="subtitle is-5">&ldquo;Edmund Ecologist&rdquo;</h5>
          <p>
            Altered timing of snowmelt, runoff, and seasonal precipitation can
            significantly affect hydrologic flow and the ecosystem events tied
            to it. Climate Adaptation Science Center research has documented
            this across many systems, including those that support Atlantic
            salmon (e.g.,
            <a href="https://pubs.usgs.gov/sir/2010/5221/"
              >Dudley and Nielsen, 2011</a
            >). Nature-summarized research,
            <a
              href="https://www.nature.com/nature-index/topics/l4/climate-variability-and-change-in-southeast-u-s-river-basins"
              >Climate Variability and Change in Southeast U.S. River Basins</a
            >, projects that southeastern US river basins will show increased
            variability and directional change, including complex shifts in flow
            timing.
            <strong>
              Edmund Ecologist wants to know how flow timing may change on the
              Sheepscot River, which he has identified as key salmon
              habitat.</strong
            >
          </p>
          <ol>
            <li>
              He zooms in on the map and selects the
              <NuxtLink to="/conus/stream/559">Sheepscot River</NuxtLink
              >&mdash;the outflow segment for a watershed, shown in red.
            </li>
            <li>
              In the results summary, he notes that some model outputs vary by
              more than 50% across the 13 models, and that other metrics point
              to greater variability even though mean annual flow isn&rsquo;t
              projected to change much.
            </li>
            <li>
              He scrolls down to the timing metrics, his primary interest,
              leaving the default selections&mdash;&ldquo;middle of the
              road&rdquo; and &ldquo;mid-century&rdquo;&mdash;since he wants the
              most likely changes over the next couple of decades.
            </li>
            <li>
              He reviews the circular graph of timing and magnitude for the
              highest annual flow rate and sees that nearly all models project a
              markedly earlier annual maximum, consistent with earlier snowmelt.
              He downloads the graphic via the camera icon for his report.
            </li>
            <li>
              He scrolls down further to the &ldquo;Timing Statistics&rdquo;
              tables, which confirm the shift: annual maximum flow is projected
              to occur 27 days earlier on average&mdash;day 54 (February 23)
              versus the historical day 81 (March 22).
            </li>
            <li>
              He notes little projected change in the date of minimum flow, then
              scrolls back up to check mean monthly minimum flow values, which
              show decreases every month from April through November.
            </li>
            <li>
              To examine timing and magnitude for specific summer and autumn
              date ranges&mdash;when salmon migrate and spawn&mdash;he scrolls
              to the bottom of the results page and downloads the &ldquo;modeled
              daily streamflow climatologies&rdquo; CSV, skipping the more
              extensive &ldquo;complete modeled hydrologic statistics&rdquo;
              option.
            </li>
          </ol>
          <p>
            That dataset&mdash;projected mean, minimum, and maximum streamflow
            per model per day of year, in cubic feet per second&mdash;lets
            Edmund run his own analysis of inter-model variability, range, and
            potential extreme low flows for the critical periods, and build
            custom graphs from the results.
          </p>
        </div>
        <div class="block">
          <h4 class="title is-5">Flow timing and Atlantic salmon habitat</h4>
          <h5 class="subtitle is-5">&ldquo;Ida Ichthyologist&rdquo;</h5>

          <p>
            <a href="https://pubmed.ncbi.nlm.nih.gov/38784683/"
              >Non-perennial streams</a
            >
            occur in all river systems, and stream segments can become
            increasingly isolated as the frequency of zero-flow days
            increases&mdash;particularly in
            <a href="https://pubmed.ncbi.nlm.nih.gov/40904370/"
              >xeric ecosystems</a
            >. Climate change may be
            <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC4183275/"
              >threatening connectivity</a
            >, and this fragmentation can reduce opportunities for habitat
            access and spawning.
            <strong>
              Ida Ichthyologist wants to know whether climate projections show
              an increasing frequency of zero-flow days
            </strong>
            across the 23 HUC8 watersheds that form the headwaters of the Upper
            Colorado River, specifically for streams with a historical mean flow
            of about 10 cf/s, during key time periods for at-risk species.
          </p>
          <ol>
            <li>
              Searching by HUC ID, starting with 14010001 (Upper Colorado River
              Headwaters), she uses the map interface to explore streams within
              each of the 23 HUCs.
            </li>
            <li>
              Within each HUC, she looks for streams with a modeled historical
              flow of about 10 cf/s, shown in the first line of output text, and
              notes all that fall between 5 and 20 cf/s&mdash;identifying a set
              of representative streams.
            </li>
            <li>
              She selects &ldquo;early century (2016&ndash;2045)&rdquo; and
              &ldquo;future extremes,&rdquo; since she&rsquo;s most concerned
              with worst-case scenarios in the near term.
            </li>
            <li>
              Winter low or zero flow is generally attributable to freezing
              rather than climate-driven change, so she&rsquo;s not concerned
              with it; for each representative stream, she scrolls to Duration
              Statistics and examines sum_dur3&mdash;the summer
              (July&ndash;September) minimum of 3-day moving average flow.
            </li>
            <li>
              She records this value for the Modeled Historical
              (1976&ndash;2005) period, along with the values for Median,
              Stabilizing Emissions (RCP 4.5) and Median, Increasing Emissions
              (RCP 8.5).
            </li>
            <li>
              Where sum_dur3 decreases between the historical value and either
              or both projected values, she downloads the associated CSV file.
            </li>
          </ol>
          <p>
            Using the complete datasets, Ida runs a deeper analysis of which
            model/scenario combinations project zero-flow periods of various
            durations during summer and autumn.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.subtitle.is-4 {
  font-weight: 400;
}
</style>
