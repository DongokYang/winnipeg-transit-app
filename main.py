'''
Name : Dongok Yang
Date : 2025-01-14
Class : ADEV-3005(261246)
'''
# Import necessary libraries
from requests import get
from dateutil.parser import parse
from colorama import just_fix_windows_console, Fore,Back, Style

lon = -97.18763968918854 # GPS longitude of location
lat = 49.89993495309101 # GPS latitude of location
distance = 100 # radius in meters to search around GPS coordinates
api_key = 'u2hXo_FYG-AgZhqTiw3r'

#Get station data
def fetch_station_data(lon,lat,distance,api_key):
  # url to request stops
  url_stops = f"https://api.winnipegtransit.com/v3/stops.json?lon={lon}&lat={lat}&distance={distance}&api-key={api_key}"

  # request bus stops nearby
  resp_stops = get(url_stops).json()
  return resp_stops

#Get stop data
def fetch_stop_data(stop_id, api_key, max_results=3):
    url = f"https://api.winnipegtransit.com/v3/stops/{stop_id}/schedule.json?max-results-per-route={max_results}&api-key={api_key}"
    response = get(url)
    return response.json()

#Get formatted time
def get_formatted_time(data):

    my_datetime_obj = parse(data["query-time"])
    formatted_datetime = my_datetime_obj.strftime("%H:%M:%S")

    return formatted_datetime

#Print the result
def print_result(data, time):
    just_fix_windows_console()
    print(Fore.YELLOW + f"Current time: {time}")
    print(Fore.GREEN + "Nearby Bus Stops:" + Style.RESET_ALL)
    print("--------------------------------------------------")

    # List all stops first
    for i, stop in enumerate(data["stops"], 1):
        print(f"{i}. {stop['name']} (Stop #{stop['key']})")
        print(f"   Direction: {stop['direction']}")
        print(f"   Location: {stop['street']['name']} at {stop['cross-street']['name']}")
        print("--------------------------------------------------")

    # Prompt user to select
    while True:
      choice = int(input("Enter the number of the bus stop you want to check (1-" + str(len(data["stops"])) + "): "))
      if 1 <= choice <= len(data["stops"]):
        break

    chosen_stop = data["stops"][choice-1]
    print("--------------------------------------------------")
    print(Fore.YELLOW + f"\nSelected Station: {chosen_stop['name']} (Stop #{chosen_stop['key']})")
    print(f"Location: {chosen_stop['street']['name']} at {chosen_stop['cross-street']['name']}" + Style.RESET_ALL)

    # Get schedule information
    stop_schedule = fetch_stop_data(chosen_stop['key'], api_key)
    route_schedules = stop_schedule['stop-schedule'].get('route-schedules', [])

    if route_schedules:
        for route in route_schedules:
            route_info = route['route']
            print(Fore.WHITE + f"\nRoute {route_info['number']} - {route_info['name']}" + Style.RESET_ALL)

            scheduled_stops = route.get('scheduled-stops', [])
            print("Upcoming buses:\n")
            for bus in scheduled_stops:
                scheduled_time = parse(bus['times']['arrival']['scheduled'])
                estimated_time = parse(bus['times']['arrival']['estimated'])

                scheduled_str = scheduled_time.strftime("%H:%M:%S")
                estimated_str = estimated_time.strftime("%H:%M:%S")

                # Calculate time difference in minutes
                time_diff = (estimated_time - scheduled_time).total_seconds() / 60

                # Color coding based on timing
                # On time
                if time_diff == 0:
                    color = Fore.GREEN
                    status = "On Time"
                # Late
                elif time_diff > 0:
                    color = Fore.RED
                    status = f"Late by {int(time_diff)} min"
                # Early
                else:
                    color = Fore.BLUE
                    status = f"Early by {int(abs(time_diff))} min"

                print(color + f"  Scheduled: {scheduled_str}")
                print(f"  Estimated: {estimated_str}")
                print(f"  Status: {status}" + Style.RESET_ALL)
                print()
    else:
        print(Fore.RED + "No scheduled bus now" + Style.RESET_ALL)

    print("--------------------------------------------------")
    print(Style.RESET_ALL)

data = fetch_station_data(lon,lat,distance,api_key)
time = get_formatted_time(data)
print_result(data,time)