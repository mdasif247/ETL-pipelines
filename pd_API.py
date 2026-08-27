import requests
import pandas as pd

# 1. Get data from API
response = requests.get(
    'https://jsonplaceholder.typicode.com/users',
    timeout=10
)

response.raise_for_status()

data = response.json()

if not isinstance(data, list):
    raise ValueError("Expected a list of users")

# 2. Normalize JSON
df = pd.json_normalize(data)

# 3. Remove duplicates
df = df.drop_duplicates()

# 4. Select required columns
result = df[[
    "id",
    "name",
    "email",
    "address.city",
    "company.name"
]]

# 5. Rename columns
result = result.rename(columns={
    'id': 'user_id',
    'name': 'user_name',
    'address.city': 'City',
    'company.name': 'Organization'
})

# 6. Save to CSV
result.to_csv("api_users.csv", index=False)

# 7. Save to Parquet
result.to_parquet(
    "users.parquet",
    index=False
)

# 8. Read CSV in chunks
chunks = pd.read_csv(
    "api_users.csv",
    usecols=['user_id', 'email'],
    chunksize=5
)

# 9. Process each chunk
biz_count=0;
for chunk in chunks:
    for email in chunk['email']:
        if email.endswith('.biz'):
            biz_count+=1;
print(biz_count)

print("this is a new feature")