import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

print("===== ENVIRONMENT CHECK =====")

print("Pandas:", pd.__version__)
print("NumPy:", np.__version__)
print("Requests:", requests.__version__)

print("BeautifulSoup: Ready")

data = {
    "property_type": ["house", "land"],
    "asking_price": [8500000000, 3000000000],
    "area_m2": [65, 100]
}

df = pd.DataFrame(data)

print("\nSample Dataset:")
print(df)

print("\nEnvironment is ready!")