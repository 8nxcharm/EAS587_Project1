# Phase 2 Report: The Uber Effect

Aidan Collins, Teslim Carew

## 1. Executive Summary

This project's purpose is to ask the question of how New York City’s for-hire vehicle market has ultimately shifted from traditional taxis to ride-sharing companies such as Uber & Lyft, and whether the data supports the popular claim that ride-sharing has become the dominant option. For our Phase 2 section of the project our team has built a pipeline that profiles, cleans and samples the NYC TLC trip files. Specifically we use 27 trip files from green, yellow and Uber/Lyft for June through August in the years 2019, 2024, and 2025. There are around 221 million raw trips in total so the data amount is plentiful. The data needed to be cleaned carefully and most of the loss came from $0 fare in Uber/Lyft in 2019 as well as from negative fares from the yellow taxis in 2025, which we could not explain at this moment. This really matters to the project because it will limit how trip counts and fares can/will be compared across years. When running this cleaned data through our pipeline it only more supports our theory that Uber/Lyft permanently took over the for-hire vehicle market. The median fare per mile charge for Yellow Taxis is at about $7.30 while Uber undercuts the market at $6.20. While looking at trip distances we saw a lot of trips fall between the 1-3 mile mark and the 15-20 mile mark and we can confirm that those longer mile trips are airport trips with a locked in flat fare of about $70.  


## 2. Connection to Phase 1

Looking back at our Phase 1 research question: how has New York City’s for-hire vehicle market ultimately shifted between traditional taxis and ride-hailing companies such as Uber & Lyfts since their breakout, and does the data behind this support the claim that ride-hailing has become the dominant force in this market? Along with this we had three supporting questions that guided our work. The first question was whether or not Uber & Lyft fares have been undercutting taxi fares and if that gap has changed. Second, how has each one of the service’s shares for total trips changed over our specified time interval. Third and final, have the ride-hailing companies captured a disproportionate share of high-value trips such as airport rides? 

Compared to Phase 2, two thing has changed. The plan before was to compare 2014-2016 which were seen as the breakout years for ride-hailing to more present day years 2024-2026. When we first started working with the TLC data, we found out early that the Uber/Lyft files only started in 2019, so the breakout years were not available to us to use. We pivoted to comparing June through August in 2019,2024,2025 since the Uber/Lyft data was actually available for us. We choose to use the same months through the selected years so that the seasons match. This also allows us to keep the three previously mentioned questions answerable, but means that we will not be able to observe the ride-hailing breakout that was planned in phase 1. The other change is the tools that we are utilizing. Phase 1 mentioned using DuckDB but now we are using Pandas and pyarrow (see Section 8).


## 3. Data Cleaning and Processing

### 3.1 Data profiling

The profile step for our project (profile_file()) reads every single column of each file in chunks of 1,000,000 rows. The counts of rows, minimums, maximums, percent missing and duplicates are exact totals for every single row. The missing values, unique values, data types and quartiles by specific vendors are estimated from a selected 1% sample of each of the chunks. An example of this is the Uber & Lyft data of June 2019 where there are 21,001,990 rows and 24 columns. The missing values are systematic: the airport_fee was missing in all of the rows, and on_scene_datetime and originating_base_num in 28.23% of the data, also almost all of it from two fo the licences (HV0004 & HV0005, against 0% missing for HV0002 & HV0003), so we choose to not fill in these columns. On top of this the file happens to hold impossible values like fares that are negative, extremely long trips and trip times and on_scene_datetime that for example were from 1970. There were also around 1,500 duplicate rows.

### 3.2 Cleaning and transformation

The clean_chunk() function applies the eight set rules in a fixed order, and a single row is counted under the condition of the first rule that row breaks. The removal is then logged into the file cleaning_log.csv.

| # | Rule | A row is kept only if |
| --- | --- | --- |
| 1 | Missing value | Dropoff, pickup, distance, fare and both zones all exist |
| 2 | Pickup outside month | The pickup is inside the file’s month |
| 3 | Dropoff not after pickup | The dropoff is after (later) the pickup |
| 4 | Duration out of range | The trip must be between 1 to 180 minutes |
| 5 | Distance out of range | The trip distance needs to be above 0 to 100 miles |
| 6 | Fare out of range | The fare needs to be between $2.50 and $500 |
| 7 | Invalid zone | Both zones are 1 to 263 (the last two mean an unknown zone) |
| 8 | Duplicate | It is the first copy of the row |

We choose to drop rows that had missing key values instead of trying to impute them, this is because attempting to impute them would invent trip properties that didn't exist. To deal with outliers we choose to use fixed limits rather than IQR or z-scores, this is because fares are very skewed and longer trips like airport trips are real and we don't want them removed. We also remove outliers instead of setting a cap, this is because some of the trip properties don't have a true value to be capped at. All of the services get the same column names for consistency, this is done with licence codes that are mapped to carriers. We also added seven new columns: carrier, month, service, hour, duration_min, fare_per_mile and airport_trip. The result of this is 13 columns instead of the original 24 for Uber & Lyft.

Using the same example previously mentioned, June of 2019 for Uber and Lyft, cleaning removed 3.85% of the rows, and around 600,000 were saved after sampling. Across all of the 27 files, it removed between 2.77% and 15.08% of rows. The places where the largest losses were seen are from $0 fares in Uber & Lyft  in 2019 and negative fares in yellow 2025. In the month of August in 2019 all 2,30,267 of the zero dollar fare trips are from Uber, and their median duration and distance are pretty close to normal trips, so it makes these look like actual trips with a missing fare. As of now we don't have a rationale behind this, so we choose to use raw_rows that were logged for the trip counts and shares.

### 3.3 Scalable processing

One of the Uber/Lyft would need about 2,163 MBs in memory for only the columns we choose to use, and this would total up to 11,557 MBs with all 24 files. So we choose to read each file independently in chunks of 1,000,000 rows with pyarrow and then only keep the needed columns. Each chunk is first cleaned, the cleaned rows are then counted, and after this is done a random sample is logged before the next chunk gets read. Choosing to count before sampling keeps the row counts and the fare average in the log exact. Overall we kept 10% of the yellow taxi data, 3% of UBER/Lyft and 100% of the green taxi data. This was done using simple random sampling with a fixed seed, not using stratified sampling.

| Measure | Result |
| --- | --- |
| Largest chunk in memory | Uber & Lyft 2019: 103 MB, Uber & Lyft 2025: 95 MB, Yellow: 48 MB |
| Runtime for all 27 files | About 5 minutes |
| Smallest saved samples | 282,235 rows (Yellow) and 512,713 rows (Uber & Lyft) |
| Sample check | Sample mean fare was within $0.06 of the exact mean for every file |

The sampling has limits. The way that we engineered this has a minor flaw of only finding duplicates that are inside one single chunk, not comparing separate chunks for duplicates. The 1% sample can also miss small vendors, and the simple random sampling could leave a possibility of small groups being thin. Also the green taxi files from 2024 and 2025 had only 46,000 to 55,000 rows, so we choose to just keep them whole because they fall well below the 250,000-row guideline.

## 4. Exploratory Data Analysis

The EDA phase was formed by using Tukey's principles where we focused on trying to reflect the volume and skewness of the taxi dataset as best we could. We used re-expression to apply log scale to the histogram for fare distances so that the extreme values were pulled in and by doing this we saw normal fare distances of 1-3 miles and 15-20 miles being peak distances for fares. A hex-bin plot was used to color map the difference in the fares as the distances increased, and by doing this we were able to identify a airport flat rate fee of $70. We also wanted to evaluate the price differences between each taxi type so we used boxplots focused on the median fare per mile to learn that Uber was leading in undercutting the competition with a fare per mile rate of $6.20 compared to a traditional Yellow Taxi fare per mile of $7.30.


## 5. First Analytics Results

"The Uber Effect" was in full display as we analyzed the calculated market share across the 2019, 2024, and 2025 summer months. We needed to use raw log counts because of a tlc reporting error. In August 2019, 2.3 million valid Uber trips were logged with a $0 fare. The $2.50 minimum fare cleaning rule would have automatically dropped these records which would have been an unexplained loss in Uber ridership for that month. When looking at the 2019 dataset and comparing the 2024 and 2025 analytics we see a lack of recovery for traditional taxis. Where rather than rebounding and stabilizing the market, the Yellow and Green taxi market shares stayed flat and continued to decline into 2025.

## 6. Dead Ends

The 2014 to 2016 comparison. Originally our plan assumed that we could compare the breakout years of Uber with the present day. After looking through the TLC files, unfortunately the Uber/Lyft data that is usable starts in 2019, so we have to reframe the comparison to the years 2019,2024, and 2025. From this we learned that checking what data actually exists before creating a fixed time frame around the plan. With that said, we also learned that the proposed research questions should generally be able to survive a change in data, which was true for our scenario.

Blaming the $2.50 minimum fare. After analyzing the cleaning log we were able to see that some files lost a lot of rows due to our fare rule set in place (as high as ~12%), and our first assumption about this was that the minimum fare was too high for Uber & Lyft rides. This was then tested against the raw fares and found that there were almost no rides between $0 and $2.50. The actual cause was due to negative fares in yellow taxis and $0 fares in Uber &Lyft. We learned from this that testing a cleaning rule against the raw data before you try and alter it, instead of assuming that there is a problem with the threshold.

Explaining the 0$ fares. To explain the $0 fare trips in august of 2019 we compared it with normal trips and this showed that they look like real trips. However the data could not tell us why the fare is actually missing. We decided to stop there and report it as an open question instead of creating a poor-backed up reason that could be incorrect. In the next phase we will try and get to the bottom of this. We learned that the data can show us what a problem looks like without giving us a causation for it.

2025 negative fares. Over 7% of the Yellow taxi records in August 2025 had negative fare amounts, our first thought was that we could track it and fix it by looking at trip distance but based on the data we could not tell why the taxi meters were recording negative numbers. Without inside information from the TLC about how they handle refunds and meter glitches the cause is impossible to determine. We decided to rely on our cleaning rule filter them out. We learned from this that you cannot always solve a data collection error using the dataset alone, and sometimes the best is to acknowledge an anomaly and exclude it rather than creating a fix for it.

## 7. Design Decisions

| Decision | Alternatives Considered | Rationale |
| --- | --- | --- |
| Read in chunks with pyarrow, then sample. | DuckDB, Loading the whole file, or using a database. | Only a single month for Uber/Lyft is around 2 GBs worth of data, and would've been around 11 GBs for all of them. So loading the entire files would let us not be able to scale effectively. Pandas is also simple and easier to check and explain. |
| Choose fixed limits, and remove data that went against them. | Capping, keeping outliers, IQR or z-score. | Since the fares are skewed, the alternative methods would get rid of actual data that we would need. |
| Counting the clean rows before sampling, and using raw rows for counts and shares. | Count after sampling | The log has exact counts, if we counted after sampling it would distort the actuality of the data, especially with the Uber/Lyft files. |

| We used a log scale instead of a linear plot to handle heavily right-skewed trip distances.| We used hex-bins over standard scatterplots to prevent extreme overplotting with millions of data points. | We evaluated pricing using medians rather than averages.

## 8. Reproducibility Statement

To be able to reproduce our results, install all of the necessary packages with `pip install -r requirements.txt` and run the command `python -m src.pipeline --download` from the root folder of the project. This will then download the 27 raw files, clean and sample them, and save the results in `data/processed/`. The EDA and first analytics are not a part of the pipeline at this time so you will need to run them separately afterwards, `src/eda.py` and `src/analytics.py`. All of the sampling uses the fixed see 587, so the results that were seen in the report will repeat. We ran the full pipeline on a desktop PC in Visual Studio, as mentioned before the cleaning/sampling took around 5 minutes and the EDA and first analytics then finished in seconds. 

## 9. References

1. Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.
2. NYC Taxi and Limousine Commission. TLC Trip Record Data. https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
