# Import necessary libraries
from requests import get
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore, Style


# Initialize colorama for Windows
just_fix_windows_console()

API_KEY = 'u2hXo_FYG-AgZhqTiw3r'
lon = -97.14114474982759 # GPS longitude of location
lat = 49.90047559609474 # GPS latitude of location
distance = 100 # radius in meters to search around GPS coordinates

# url to request stops
url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

# request bus stops nearby
resp_stops = get(url_stops).json()

print(resp_stops)