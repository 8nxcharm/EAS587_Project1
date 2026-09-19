# The Uber Effect: A Decade of Disruption in NYC's Taxi Industry

**Authers:** Aidan Collins, Teslim Carew

**Version:** 1.0

**Target Community of Intrest**:

**Date Created:** 9/16/2026

**Last Updated:** 9/17/2026

**Github Repository**: https://github.com/8nxcharm/EAS587_Project1


## Section 1. Research Goal

NYC's for-hire vehicle market has quickly shifted after companies like Uber and Lyft have entered the scene around 2014, causing the traditional taxi trip volume to fail as the ride-hailing industry grew. 
There is a common narrative that ride-hailing has ultimately "taken over", but little to no work has been done to test this claim against the full TLC datasets across ride-hailling breakout period and present day. 
This project will use NYC TLC Trip Record Data; millions of trips per year, with single months containing anywhere from 15 to 20 million records. The data will be used to compare their market shares, fares, and high-value 
trips that were captured between 2014-2016 and 2024 to 2026. Since this data set is comparatively large there will be a requirement of delibertaly sampling rather than using every record for processing, which is central to 
answering the question. We expect there to be a more nuance outcome than than a polarizing "Uber Won" story, since the data from TLC shows a little bit of taxi recovery.

Primary Research Question: How has NYC's for-hire vehicle market shifted between tradtional taxis and ride-hailing since ride-hailing breakout, and does the data support the claim that uber has become cominant?

Supporting Questions:
  - Have the ride-hailing companies fares consistently undercut the traditional taxi fares, and has that gap changed over time?
  - How has each of the sector's share of the total NYC trips changed between 2014-2016 and 2024-2026?
  - Has ride-hailing disproportionately captured the high-value trips (ex. rides to airports) relative to the shorter trips?


## Section 2. Background and Motivation

Uber's expansion in New York City began around 2014 and this paired with the sharp taxi decline. During this period the average daily trips for taxis had fallen between April 2014 to 2015. Also, yellow taxis were 
providing 10's of thousands of less trips per day by the start of 2016. On the other hand, Uber's fleet of drivers had almost tripled by early 2016. This severely affected medallion owners whose assets had virtually collapsed onto them 
in this short period of time. 

What is less settled at this point is weather this represents a permanent ride-hailing dominance or if present day shows a partially rebalanced market. 2024 TLC data shows some sings of taxi recovery, which complicates the presented 
narrative. Most of exsisting work focuses on only the 2014-2016 disruption without any comparison to the present-day conditions. This project aims to contribute a direct comparison across both periods instead of a single snapshot of time. 
This would be very relevant to policymakers that are weighing driver pay rules, overcrowding pricing and the cap of vehicles that are allowed to be on the road.


## Section 3. Research Objectives and Scope

The specific objectives of the project is to see the initial and long term impact forhire services had on the traditional cab services in NYC. The expected outcome we are looking for is a clear indication that when the forhire services are introduced into the economy there was a dip in the use of traditional cabs. The project will address the trip amount of each type of cab service and compare them. During this project we will not try to attempt to see if things like city wide events affect the use of certain services vs others. 

## Section 4. Prior Research and References
https://thelittledataset.com/2015/03/30/the-rise-of-the-new-kind-of-cabbie-a-comparison-of-uber-and-taxi-drivers/ - This reference uses race of drivers as a dataset to compare cab services and we will not put race into our project as the race of drivers doesnt matter.
https://blogs.pugetsound.edu/econ/2015/10/06/uber-vs-taxis-in-new-york-city/ - This reference uses specific data from certain districts within NYC which is someone we might touch on. 
https://www.smartcitiesdive.com/ex/sustainablecitiescollective/how-much-market-share-are-new-york-s-yellow-cabs-losing-uber/1169427/ - This reference uses similar data with us to show that uber had an impact on yellow cabs during the specific time frames we wanted to use also.
https://www.investopedia.com/articles/personal-finance/021015/uber-versus-yellow-cabs-new-york-city.asp - This reference brakes down the specific types of uber rides users can order but we in this project will just look at uber trips as a whole not the specific package types.
https://nymag.com/intelligencer/2016/01/uber-is-making-nyc-cab-drivers-nicer.html - This reference details the emotional impact for hire cars are having on yellow back but we arent looking into the emotional side of this data. 




## Section 5. Supporting Data and Resources

The primary dataset that we will be using is the NYC TLC Trip Record Data. Inside this dataset there are records for Yellow Taxi, Green Taxi, and HVFHV (Uber/Lyft). This dataset is publicly available for download as monthly Parquet files. 
A single month for the HVFHV data alone exceeds our 250k-record min. and combined with sampled months we will exceed the 10 GB memory threshold. In the TLC data there is also a Taxi Zone Lookup table that can help us with identifying long costly 
trips like rides to the airport. Same with the trip record data there is no constraint to the access. At this time we expect to be using Python (pandas and more) and DuckDB for querying the Parquet without loading the whole set. Along with Jupyter/VS code 
and of course GitHub.


## Section 6. Risks, Constraints, Assumptions

The project could see delays if we decide to switch the time frames for which we pull data from, and specifically if we change this time frame too late. When analyzing the data if we don't reach our foreseen objective we might have to pivot to a different time frame of years to show what we already have an idea happened to the cab services in NYC. 


## Section 7. Research Approach Tasks and Timeline

Weeks 1-4:

  - Week 1: Finalize the scope of the project, verification of the access to the dataset, inspecting sample months for all of the differnt ride types, set up GitHub.
  - Week 2: We will need to select the final sampling months across both of our chosen time periods. Build out data_access.py and data_sampling.py
  - Week 3: Align the fare fields across all of the datasets so we can compare, run data quality checks
  - Week 4: Begin EDA


Weeks 5-12:

  - Week 5-8: Complete EDA; build visualizations and prepare for Phase 2 Presentation
  - Week 9-10: Move pipeline to Apache Spark possibly for distributed processing, also add in factors like weather or holidays which could affect data.
  - Week 11-12: Finalize analysis, put together all of our findings and prepare for the final presentation

