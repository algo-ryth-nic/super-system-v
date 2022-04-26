# import subprocess
import requests 
import timeit
import pandas as pd
import sys

if len(sys.argv) < 2:
    print("Usage: python3 apriori-script.py <path-to-dataset>")
    exit(1)

path = sys.argv[1]

files = {
  "file": open(path, "rb")
  }

session = requests.Session()
start = timeit.default_timer()
res = session.post('http://localhost:5000/upload', files=files)
end = timeit.default_timer()

if res.ok:
  print(res.content.decode('utf-8'))
else:
  print(res.status_code)

print(f"Time Taken: {end - start} seconds")