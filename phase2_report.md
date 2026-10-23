# Phase 2 Report: The Uber Effect

Aidan Collins, Teslim Carew

## 1. Executive Summary

This project's purpose is to ask the question of how New York City’s for-hire vehicle market has ultimately shifted from traditional taxis to ride-sharing companies such as Uber & Lyft, and whether the data supports the popular claim that ride-sharing has become the dominant option. For our Phase 2 section of the project our team has built a pipeline that profiles, cleans and samples the NYC TLC trip files. Specifically we use 27 trip files from green, yellow and Uber/Lyft for June through August in the years 2019, 2024, and 2025. There are around 221 million raw trips in total so the data amount is plentiful. The data needed to be cleaned carefully and most of the loss came from $0 fare in Uber/Lyft in 2019 as well as from negative fares from the yellow taxis in 2025, which we could not explain at this moment. This really matters to the project because it will limit how trip counts and fares can/will be compared across years. [ADD IN MAIN FINDINGS FROM SEC. 5 & 6 HERE @TES]


## 2. Connection to Phase 1

Looking back at our Phase 1 research question: how has New York City’s for-hire vehicle market ultimately shifted between traditional taxis and ride-hailing companies such as Uber & Lyfts since their breakout, and does the data behind this support the claim that ride-hailing has become the dominant force in this market? Along with this we had three supporting questions that guided our work. The first question was whether or not Uber & Lyft fares have been undercutting taxi fares and if that gap has changed. Second, how has each one of the service’s shares for total trips changed over our specified time interval. Third and final, have the ride-hailing companies captured a disproportionate share of high-value trips such as airport rides? 

Compared to Phase 2, two thing has changed. The plan before was to compare 2014-2016 which were seen as the breakout years for ride-hailing to more present day years 2024-2026. When we first started working with the TLC data, we found out early that the Uber/Lyft files only started in 2019, so the breakout years were not available to us to use. We pivoted to comparing June through August in 2019,2024,2025 since the Uber/Lyft data was actually available for us. We choose to use the same months through the selected years so that the seasons match. This also allows us to keep the three previously mentioned questions answerable, but means that we will not be able to observe the ride-hailing breakout that was planned in phase 1. The other change is the tools that we are utilizing. Phase 1 mentioned using DuckDB but now we are using Pandas and pyarrow (see Section 8).


## 3. Data Cleaning and Processing

### 3.1 Data profiling

### 3.2 Cleaning and transformation

### 3.3 Scalable processing


## 4. Exploratory Data Analysis


## 5. First Analytics Results


## 6. Dead Ends


## 7. Design Decisions

| Decision | Alternatives Considered | Rationale |
| --- | --- | --- |
| Read in chunks with pyarrow, then sample. | DuckDB, Loading the whole file, or using a database. | Only a single month for Uber/Lyft is around 2 GBs worth of data, and would've been around 11 GBs for all of them. So loading the entire files would let us not be able to scale effectively. Pandas is also simple and easier to check and explain. |
| Choose fixed limits, and remove data that went against them. | Capping, keeping outliers, IQR or z-score. | Since the fares are skewed, the alternative methods would get rid of actual data that we would need. |
| Counting the clean rows before sampling, and using raw rows for counts and shares. | Count after sampling | The log has exact counts, if we counted after sampling it would distort the actuality of the data, especially with the Uber/Lyft files. |

[ADD YOUR DESIGN DECISIONS HERE HERE @TES]

## 8. Reproducibility Statement


## 9. References

1. Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.
2. NYC Taxi and Limousine Commission. TLC Trip Record Data. https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
