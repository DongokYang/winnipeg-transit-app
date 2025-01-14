# Import necessary libraries
from requests import get
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore,Back, Style

lon = -97.18763968918854 # GPS longitude of location
lat = 49.89993495309101 # GPS latitude of location
distance = 100 # radius in meters to search around GPS coordinates

def fetch_station_data(lon,lat,distance):
  API_KEY = 'u2hXo_FYG-AgZhqTiw3r'

  # url to request stops
  url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={API_KEY}"

  # request bus stops nearby
  resp_stops = get(url_stops).json()

  return resp_stops

def get_formatted_time(data):

    my_datetime_obj = parse(data["query-time"])
    formatted_datetime = my_datetime_obj.strftime("%H:%M:%S")

    return formatted_datetime

def print_result(data,time):
  just_fix_windows_console()
  print(Fore.YELLOW+f"current time is {time}")
  print("Here are the nearby bus stops and related information")
  for i in range(len(data)):
    print(data["stops"][i])
    print(f"At station {data['stops'][i]['name']} ({data['stops'][i]['key']})")
    print(f"")

  print(Style.RESET_ALL)


data = fetch_station_data(lon,lat,distance)
time = get_formatted_time(data)


print_result(data,time)