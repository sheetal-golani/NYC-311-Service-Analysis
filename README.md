# NYC 311 Service Response Dashboard (Power BI)

A Power BI project analysing **3.46 million NYC 311 service requests from year 2024**: how many requests the city receives, who handles them, and how quickly different problems get closed.

**Tools:** Power BI, Power Query (M), DAX, Python Script (data extraction), Data modelling

------------
## How to open

1. **[Download the Power BI file (164 MB)](https://github.com/sheetal-golani/NYC-311-Service-Analysis/releases/download/NYC311-PowerBI-dashboard/NYC-311.Service.Analysis.pbix)**

## Data and method

- **Source:** [NYC Open Data, 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/d/erm2-nwe9) (dataset ID `erm2-nwe9`), calendar year 2024.
- **Extraction:** I downloaded the data with a Python script ([`scripts/extract_311.py`](scripts/extract_311.py)) that calls NYC Open Data's API for one month at a time, saving 12 monthly CSV files. I kept only the 19 columns I needed (out of 44) to keep the model light.

## The question

> Which problems do New Yorkers report most, who handles them, and how long do they wait for a response?

## Key findings (2024, 3,456,770 requests)

- **Most requests close fast.** The typical request closes within hours, and only a small share take over a month.
- **Problem type decides speed.** Parking and noise close within a day. Housing problems like plumbing and unsanitary conditions take much longer.
- **Workload is concentrated.** NYPD handles the largest share of requests and closes them fastest. HPD handles the second largest share and takes days.
- **The slowest problems are licensing and infrastructure requests**, and can take months.


## Data model
A star schema with one fact table and five dimensions. All relationships are one-to-many and active.

![Data model](images/04_data_model.png)


