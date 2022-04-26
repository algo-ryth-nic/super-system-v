# import subprocess
import requests 
import timeit
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python3 apriori-script.py <path-to-dataset>")
    exit(1)

path = sys.argv[1]
df = pd.read_csv(path)
data = df.to_json(orient='records')

headers = {'Content-type': 'application/json'}
start = timeit.default_timer()
res = requests.post('http://localhost:5000/aprori', data=data, headers=headers)
end = timeit.default_timer()

if res.ok:
  print(res.content.decode('utf-8'))
else:
  print(res.status_code)

print(f"Time Taken: {end - start} seconds")