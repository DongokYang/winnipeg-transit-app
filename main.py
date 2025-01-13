# Import necessary libraries
from requests import get
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore,Back, Style

just_fix_windows_console()
print(Fore.RED + 'some red text')
print(Back.GREEN + 'and with a green background')
print(Style.DIM + 'and in dim text')
print(Style.RESET_ALL)
print('back to normal now')


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

#show formatted time on the terminal
my_datetime_obj = parse(resp_stops["query-time"])
print(my_datetime_obj.strftime("%H:%M:%S"))
