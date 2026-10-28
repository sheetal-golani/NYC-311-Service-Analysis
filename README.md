# NYC 311 Service Response Dashboard (Power BI)

A Power BI project analysing **3.46 million NYC 311 service requests from year 2024**: how many requests the city receives, who handles them, and how quickly different problems get closed.

**Tools:** Power BI, Power Query (M), DAX, Python Script (data extraction), Data modelling

------------
## How to open

1. **[Download the Power BI file (164 MB)](https://github.com/sheetal-golani/NYC-311-Service-Analysis/releases/download/NYC311-PowerBI-dashboard/NYC-311.Service.Analysis.pbix)**


## Data and method

- **Source:** [NYC Open Data, 311 Service Requests from 2020 to Present](https://data.cityofnewyork.us/d/erm2-nwe9) (dataset ID `erm2-nwe9`), calendar year 2024.
- **Raw data:** [Download the dataset (zip)](https://github.com/sheetal-golani/NYC-311-Service-Analysis/releases/download/NYC311-PowerBI-dashboard/Dataset.zip) 
- **Extraction:** I downloaded the data with a Python script ([`extract_311.py`](extract_311.py)) that calls NYC Open Data's API for one month at a time, saving 12 monthly CSV files. I kept only the 19 columns I needed (out of 44) to keep the model light.


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

- **Most requests close fast.** The typical request closes within hours, and 60% are closed within a day. Fewer than 10% take longer than a month, so most requests are closed quickly.
- **The type of problem matters more than where it happens.** Quick-fix problems such as illegal parking, noise and blocked driveways are almost always closed within a day (about 99%). Housing-condition problems rarely are: only 3% of unsanitary condition requests and 7% of plumbing requests close within a day. Heat and hot water, one of the most reported problems, closes within a day only 31% of the time.
- **The workload is concentrated in two agencies.** NYPD handles about 45% of all requests and closes them in around an hour. HPD handles about 21%, mostly housing complaints, and its typical request takes a few days. The remaining agencies share a much smaller part of the workload.
- **The slowest problems are licensing and infrastructure requests**, such as tree requests and food vendor complaints. They are relatively rare, but they can take months to close.
- **Requests are spread across all boroughs, but not evenly.** Brooklyn has the most requests (about 30%), followed by Queens, the Bronx and Manhattan, and Staten Island has the fewest (under 4%). These are raw counts, not adjusted for population, so they show where the volume is, not which borough has the most problems per resident.


## How I built it

### 1. Transform the data (Power Query)
I split the cleaning into three layers, so each step is easy to trace:
- **Raw query:** the 12 monthly CSV files combined into one table, with data types set.
- **Staging query:** where all the cleaning happened.
- **Fact query:** the final table loaded into the model.

Cleaning steps:
- Trimmed extra spaces in text columns.
- Replaced missing or "Unspecified" boroughs with "Unknown".
- Calculated **resolution time in hours** (closed date minus created date).
- Added **flag columns** for open requests, invalid timestamps (closed before created) and zero-duration requests. I labelled these rows instead of deleting them, so they can be excluded from the time measures but still count in the totals.
- Added a **created day** column to connect to the date table.

### 2. Build the star schema
The source was one flat table of 3.46 million rows, with the same descriptive text repeated on every row. I split it into a fact table and dimension tables:
- **Dimensions** (agency, problem, location, channel): for each one, I referenced the staging query, kept only the descriptive columns, removed duplicates and added an index as the key.
- **Fact table:** I merged those keys back into the cleaned table, using the descriptive columns to match each request to its dimension row, then removed the repeated text. It keeps only the keys, dates, resolution time and flags.
- **Date table:** created with DAX (`CALENDAR`) and marked as the date table, linked to the request's creation date.
- **Relationships:** each dimension connects to the fact table with a one-to-many relationship.

Why a star schema: the model is smaller and faster, filters work cleanly across tables, and the DAX stays simple.

### 3. Write the DAX measures, such as:
- **Counts:** total, open and closed requests.
- **Median time to close:** excludes open requests and invalid timestamps.
- **Closed within 1 day:** the share of closed requests resolved within 24 hours.
- **Speed buckets:** a calculated column that groups requests (under 1 hour, 1 to 24 hours, 1 to 7 days, and so on), with a sort-order column.
- **Share of requests:** uses `REMOVEFILTERS` so each bar shows its share of the total.
- **Fast-problem ranking:** a measure that sets a minimum request count and picks problems where most requests close within a day, used inside a Top N filter.

### 4. Design the report
The report has three pages, each answering one part of the question:
- **Overview:** KPI cards, the top 10 complaint types, requests by borough, the time-to-close distribution, and agency and borough slicers.
- **Agencies:** agency workload and typical time to close by agency, shown as simple bar charts, plus a chart of the complaints that take the longest to close. 
- **Problem speed:** how quickly each type of problem gets closed, using the speed buckets and the fast-problem ranking.
