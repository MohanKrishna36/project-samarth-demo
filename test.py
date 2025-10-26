# import requests
# import pandas as pd

# API_KEY = "579b464db66ec23bdd000001eda1c220604348d94d38b6c38e094c35"
# resource_id = "35be999b-0208-4354-b557-f6ca9a5355de"
# url = f"https://api.data.gov.in/resource/{resource_id}"
# params = {
#     "api-key": API_KEY,
#     "format": "json",
#     "offset": 0,
#     "limit": 100
# }

# r = requests.get(url, params=params)

# print("Status code:", r.status_code)
# print("Response headers:", r.headers)
# print("Response text (first 300 chars):", r.text[:300])

# try:
#     j = r.json()
#     df = pd.DataFrame(j['records'])
#     print(df.head())
# except ValueError:
#     print("❌ The response is not valid JSON. Check your API key or resource ID.")


import pandas as pd
df = pd.read_csv('processed_data/crop_data_cleaned.csv')
print("States:", df['state_name'].unique())
print("Years:", df['crop_year'].unique())
print("Crops:", df['crop'].unique())
print("Districts:", df['district_name'].unique())
