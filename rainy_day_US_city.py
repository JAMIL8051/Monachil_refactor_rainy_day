# This script is the modularized and refactored version of the source code: https://pastebin.com/GhHeKeK4  
# rain data from .
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.html
# used dataset:
# https://coastwatch.pfeg.noaa.gov/erddap/griddap/chirps20GlobalPentadP05.csv?precip%5B(2021-8-01T00:00:00Z):1:(2021-11-26T00:00:00Z)%5D%5B(30.0):.25:(42.0)%5D%5B(-123.0):.25:(-113.0)%5D
# Author: Jamil Chowdhury


import csv
import requests
import pprint
import os.path
from os import path


# Opening the file, processing the file, closing the file
def process_rain_data_csv_file(full_csv_file_path):
  """
  Input: 
    full_csv_file_path: The full string-path to the CSV file containing rain-data
  Output: 
    rain_data: A Python list containing rain data
  """
    while True:
        if path.isfile(full_csv_file_path):
            full_csv_file_path = full_csv_file_path
            break
        else:
            full_csv_file_path = str(input('The file is not valid. Please provide the correct path.'))


    csv_file = open(full_csv_file_path)
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    rain_data = list()

    for row in csv_reader:
        line_count += 1
        if line_count <= 2:
        # print(f'Column names are {", ".join(row)}')
            continue
        elif line_count >= 10e10:
            break
        rain_data.append(row)
    
    csv_file.close()
    
    return rain_data


# Processing  the User input
def process_user_input(val, rain_data, dist_thresh = 0.05, rain_thresh = 8.0):
  """
  Input:  
    val: A string from the user
    rain_data: a Python list obtained from the function process_rain_data_csv_file
    dist_thres: A float value to setup a threshold value of distnace using latitude and longitude (optional)
    rain_thres: A float value to setup a threshold value to call a day rainy (optional)
  Output: 
    dates: A Python list containing the dates
  """ 
    while True:
        if val == None or val == '' or val == ' ':
            print("Please give a valid string")
            val = str(input("Enter city name:[San Jose]") or "San Jose")
        else:
            val = val
            break

    response = requests.get("https://nominatim.openstreetmap.org/search.php?city="+val+"&format=jsonv2&namedetails=0&addressdetails=0&limit=1")
    city_data = response.json()
    c_lat = city_data[0]['lat']
    c_lon = city_data[0]['lon']  
    
    dates = set()

    for row in rain_data:
        t, lat, lon, rain = row
        t = t[:10]
        lat_diff = abs(float(lat)-float(c_lat))
        lon_diff = abs(float(lon)-float(c_lon))
        if rain != "NaN" and float(rain) >= rain_thresh and lat_diff < dist_thresh and lon_diff < dist_thresh:
            dates.append((t,rain))                
    
    dates = list(dates).sort()

    return dates


if __name__ == "__main__":
    # Taking iput as a CSV file:    
    full_csv_file_path = str(input("Please enter full file path to the rain_data CSV file))
    rain_data = process_raind_data_csv_file(full_csv_file_path = '/home/ali/Downloads/chirps20GlobalPentadP05_233e_7ccc_b137.csv')

    # User input
    val = str(input("Enter city name:[San Jose]") or "San Jose")
    data = process_user_input(val, rain_data)

    # Show output to the user
    print("Number of rainy 5-days: "+ str(len(dates)))
    
    # Showing the more details
    for item in dates:
        print("Detailed view: ", item)



