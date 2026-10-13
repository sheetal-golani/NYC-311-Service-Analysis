import requests, pandas as pd, time, os
from io import StringIO

BASE = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
OUT = r"C:\311_data"
os.makedirs(OUT, exist_ok=True)

COLS = ("unique_key,created_date,closed_date,due_date,resolution_action_updated_date,"
        "agency,agency_name,complaint_type,descriptor,status,resolution_description,"
        "open_data_channel_type,borough,incident_zip,city,council_district,"
        "police_precinct,latitude,longitude")

months = pd.period_range("2024-01", "2024-12", freq="M")
PAGE = 50000

for m in months:
    path = f"{OUT}\\311_{m}.csv"
    if os.path.exists(path):
        print("skip", m); continue
    start = m.start_time.strftime("%Y-%m-%dT00:00:00")
    end = (m + 1).start_time.strftime("%Y-%m-%dT00:00:00")
    where = f"created_date >= '{start}' AND created_date < '{end}'"
    frames, offset = [], 0
    while True:
        params = {"$select": COLS, "$where": where,
                  "$order": "created_date, unique_key",
                  "$limit": PAGE, "$offset": offset}
        for attempt in range(4):
            try:
                r = requests.get(BASE, params=params, timeout=120)
                r.raise_for_status(); break
            except Exception as e:
                print("retry", e); time.sleep(5)
        df = pd.read_csv(StringIO(r.text), dtype=str)
        if df.empty: break
        frames.append(df); offset += PAGE
        print(m, offset)
        if len(df) < PAGE: break
    pd.concat(frames).to_csv(path, index=False)
    print("saved", m)