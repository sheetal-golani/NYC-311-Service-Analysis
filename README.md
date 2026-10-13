# NYC 311 Service Response Dashboard (Power BI)

A Power BI project analysing **3.46 million NYC 311 service requests from year 2024**: how many requests the city receives, who handles them, and how quickly different problems get closed.

**Tools:** Power BI, Power Query (M), DAX, Python Script (data extraction), Data modelling

------------
## How to open

1. **[Download the Power BI file (164 MB)](https://github.com/sheetal-golani/NYC-311-Service-Analysis/releases/download/NYC311-PowerBI-dashboard/NYC-311.Service.Analysis.pbix)**


## Data and method

- **Source:** [NYC Open Data, 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/d/erm2-nwe9) (dataset ID `erm2-nwe9`), calendar year 2024.
- **Extraction:** I downloaded the data with a Python script ([`scripts/extract_311.py`](extract_311.py)) that calls NYC Open Data's API for one month at a time, saving 12 monthly CSV files. I kept only the 19 columns I needed (out of 44) to keep the model light.


## Data model

A star schema with one fact table and five dimensions. All relationships are one-to-many and active.

![Data model](Data%20Model.png)


## Dashboard preview


![Overview](Dashboard/1.%20Dashboard%20Overview.png)

![Agencies](Dashboard/2.%20Agencies.png)

![Problem speed](Dashboard/3.%20Problem%20Speed.png)


## The question

> Which problems do New Yorkers report most, who handles them, and how long do they wait for a response?

## Key findings (2024, 3,456,770 requests)

- **Most requests close fast.** The typical request closes within hours, and 60% are closed within a day. Fewer than 10% take longer than a month, so the overall picture is of a city that responds fast to most things.
- **The type of problem matters more than where it happens.** Quick-fix problems such as illegal parking, noise and blocked driveways are almost always closed within a day (about 99%). Housing-condition problems rarely are: only 3% of unsanitary condition requests and 7% of plumbing requests close within a day. Heat and hot water, one of the most reported problems, closes within a day only 31% of the time.
- **The workload is concentrated in two agencies.** NYPD handles about 45% of all requests and closes them in around an hour. HPD handles about 21%, mostly housing complaints, and its typical request takes a few days. The remaining agencies share a much smaller part of the workload.
- **The slowest problems are licensing and infrastructure requests**, and can take months.


