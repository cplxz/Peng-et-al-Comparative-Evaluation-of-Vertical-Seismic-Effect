import requests
import os
import pandas as pd
import numpy as np
import json
import geopandas as gpd
from shapely.geometry import box, Point, Polygon, MultiPolygon
import math
from math import sqrt
from scipy import interpolate

import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for interactive plotting
from matplotlib.lines import Line2D
import scipy.stats as stats
from scipy.stats import lognorm
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

from io import BytesIO
from PIL import Image

import matplotlib.image as mpimg

################## To Get Coordinates by 0.5 degree ##################

# file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\boarder_CA_excluded.xlsx'
# df = pd.read_excel(file_path)
#
# # Ensure columns are named correctly, if not, you can assign them explicitly
# points = list(zip( df['longitude'],df['latitude']))  # Convert to list of tuples
#
#
# # Create the polygon from the points
# polygon = Polygon(points)
#
# # Get the bounding box (min x, min y, max x, max y)
# minx, miny, maxx, maxy = polygon.bounds
#
# # Generate grid coordinates inside the bounding box with a step of 0.1
# grid_coordinates_degree = []
#
# # Iterate over the grid points within the bounding box, with a step of 0.1
# step_x = 0.05
# step_y = 0.05
# tolerance = 1e-4
# count_points = 0
# x = minx
# while round(x,2) <= round(maxx,2):  # Slightly extend the loop to include maxx
#     y = miny
#     while round(y,2) <= round(maxy,2):  # Slightly extend the loop to include maxy
#         point = Point(round(x, 2), round(y, 2))
#         # Check if the point (x, y) is inside the polygon or on the boundary
#         if polygon.intersects(point):
#             grid_coordinates_degree.append((round(x,2), round(y,2)))
#             count_points += 1
#         elif polygon.distance(point) <= tolerance:
#             grid_coordinates_degree.append((round(x, 2), round(y, 2)))
#             count_points += 1
#         y += step_y
#     x += step_x
#
# # Print the grid coordinates inside the polygon or on the boundary
# print(count_points)
#
# # Write grid coordinates to an Excel file
# grid_df = pd.DataFrame(grid_coordinates_degree, columns=['Longitude', 'Latitude'])
# output_file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\grid_coordinates_by0.05degree.xlsx'
# grid_df.to_excel(output_file_path, index=False)
#
# # Optional: Plot the polygon and grid points
# plt.figure(figsize=(9, 6))
# x, y = zip(*points)
# plt.fill(x + (x[0],), y + (y[0],), alpha=0.3, label='Polygon')
#
# grid_x, grid_y = zip(*grid_coordinates_degree)
# plt.scatter(grid_x, grid_y, color='red', label='Grid Points')
#
# plt.legend()
# plt.show()
#
#





################## To plot boarder (CA_included) ##################
#
# file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\boarder_CA_included.xlsx'
# df = pd.read_excel(file_path)
#
# # Ensure columns are named correctly, if not, you can assign them explicitly
# points = list(zip( df['longitude'],df['latitude']))  # Convert to list of tuples
#
# # Create the polygon from the points
# polygon = Polygon(points)
#
# # Extract x and y from the polygon to plot
# x, y = polygon.exterior.xy
#
# # Plot
# plt.figure(figsize=(8, 6))
# plt.plot(x, y, color='black', linewidth=1.5)
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('CA-included Border Polygon')
# plt.grid(True)
# plt.tight_layout()
# plt.show()



################ To get state boarder coordinates ##################


# import geopandas as gpd
# import matplotlib.pyplot as plt
# import pandas as pd
# from shapely.geometry import box
#
# # Load shapefile from US Census
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs("EPSG:4326")
#
# # Clip to bounding box (CONUS)
# bbox = box(-130, 24, -65, 50)
# clipped_states = states[states.intersects(bbox)]
#
# # Extract coordinates
# rows = []
# for _, row in clipped_states.iterrows():
#     name = row['NAME']
#     abbrev = row['STUSPS']
#     geom = row.geometry
#
#     def extract_coords(geom_part):
#         if geom_part.geom_type == 'Polygon':
#             rings = [geom_part.exterior.coords]
#         elif geom_part.geom_type == 'MultiPolygon':
#             rings = [poly.exterior.coords for poly in geom_part.geoms]
#         else:
#             return []
#
#         for ring in rings:
#             for lon, lat in ring:
#                 rows.append({
#                     'State': name,
#                     'Abbreviation': abbrev,
#                     'Latitude': lat,
#                     'Longitude': lon
#                 })
#
#     extract_coords(geom)
#
# # Export to Excel
# df_coords = pd.DataFrame(rows)
# df_coords.to_excel("us_state_borders.xlsx", index=False)
# print("✅ Coordinates exported to 'us_state_borders.xlsx'")
#
# import geopandas as gpd
# import matplotlib.pyplot as plt
# from shapely.geometry import box
#
# # Load U.S. states from Census shapefile (20m resolution)
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url)
#
# # Reproject to WGS84 (lat/lon) to apply geographic bounding box
# states = states.to_crs("EPSG:4326")
#
# # Define bounding box: (minx, miny, maxx, maxy) = (lon1, lat1, lon2, lat2)
# bbox = box(-130, 24, -65, 50)
#
# # Clip states to bounding box
# clipped_states = states[states.intersects(bbox)]
#
# # Plot
# fig, ax = plt.subplots(figsize=(12, 8))
# clipped_states.plot(ax=ax, edgecolor='black', facecolor='lightblue')
#
# # Add state codes at centroids
# for idx, row in clipped_states.iterrows():
#     if row.geometry.centroid.is_empty:
#         continue
#     x, y = row.geometry.centroid.coords[0]
#     if bbox.contains(row.geometry.centroid):
#         ax.text(x, y, row['STUSPS'], fontsize=8, ha='center')
#
# # Adjust plot
# ax.set_title("Contiguous U.S. States (Clipped to Lat/Lon Bounds)", fontsize=16)
# ax.set_xlim(-130, -65)
# ax.set_ylim(24, 50)
# ax.set_xlabel("Longitude")
# ax.set_ylabel("Latitude")
# plt.grid(True)
# plt.tight_layout()
# plt.show()
#



################## Data Scraping ##################


# file_path=r"C:\Users\cheng\PycharmProjects\pythonProject\lat_long_Vs30.xlsx"
#
# # file_path=r"C:\Users\cheng\PycharmProjects\pythonProject\failed_attempts.xlsx"
#
# # Specify the row range (3001-6000)
# start_row = 311001
# end_row = 312000
#
#
# df = pd.read_excel(file_path,usecols=["Latitude", "Longitude", "Vs30"], skiprows=range(1, start_row), nrows=(end_row - start_row + 1))
#
# response_data_list = []
# # response_data_list2 = []
# failed_attempts = []
#
# # Loop through all rows in the DataFrame
# for i in range(len(df)):  # Loop dynamically based on the number of rows
#     vs30 = df.iloc[i]["Vs30"]
#
#     # Determine the soil class based on VS30 (Table 20.2-1)
#     if vs30 > 1524:
#         soil_class = 'A'
#     elif vs30 > 914.4:
#         soil_class = 'B'
#     elif vs30 > 640.08:
#         soil_class = 'BC'
#     elif vs30 > 441.96:
#         soil_class = 'C'
#     elif vs30 > 304.8:
#         soil_class = 'CD'
#     elif vs30 > 213.36:
#         soil_class = 'D'
#     elif vs30 > 152.4:
#         soil_class = 'DE'
#     else:
#         soil_class = 'E'
#
#     lat = df.iloc[i]["Latitude"]
#     long = df.iloc[i]["Longitude"]
#     risk_category = "II"
#
#     # Construct the URL dynamically
#     url = f'https://ascehazardtool.org/proxy/proxy.ashx?https://earthquake.usgs.gov/ws/designmaps/nehrp-2020.json?latitude={lat}&longitude={long}&referenceDocument=ASCE7-22&riskCategory={risk_category}&siteClass={soil_class}&title=ASCE'
#
#     print(url)
#
#     # Define custom headers
#     headers = {
#         "Cookie": "_ga=GA1.1.373760250.1739330404; cookieconsent_status=dismiss; _ga_NL845079TW=GS1.1.1739501292.4.0.1739501326.0.0.0",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
#         "Accept-Language": "en-US,en;q=0.5",
#         "Referer": "https://ascehazardtool.org/"
#     }
#
#     # Send HTTP request to the URL with custom headers
#     resp = requests.get(url, headers=headers)
#
#     # Check if the request was successful (status code 200)
#     if resp.status_code == 200:
#         print(f"Request successful. Status Code: {resp.status_code}")
#
#         try:
#             # Parse the response as JSON
#             data = resp.json()
#
#             # Access the response data
#             response_imput = data.get('request',{}).get('parameters',{})
#             response_data = data.get('response', {}).get('data', {})
#
#             # to get spectra from ascehazardtool (unused)
#             # response_spectrum_per=data.get('response',{}).get('data',{}).get('twoPeriodDesignSpectrum',{}).get('periods',{})
#             # response_spectrum_ord=data.get('response',{}).get('data',{}).get('twoPeriodDesignSpectrum',{}).get('ordinates',{})
#             if response_data:
#                 # Get only the first 12 key-value pairs
#
#                 # Get the first 4 key-value pairs from response_imput
#                 limited_response_imput = dict(list(response_imput.items())[:4])
#                 if 'siteClass' in limited_response_imput:
#                     limited_response_imput['siteClass'] = soil_class
#
#                 limited_response_data = dict(list(response_data.items())[:12])
#
#                 # Combine both dictionaries into one
#                 combined_data = {**limited_response_imput, **limited_response_data}
#
#                 # Append the combined data to the list
#                 response_data_list.append(combined_data)
#
#                 # to get spectra from ascehazardtool (unused)
#                 # if len(response_spectrum_per) == len(response_spectrum_ord):
#                 #     spectrum_data = {response_spectrum_per[i]: response_spectrum_ord[i] for i in
#                 #                     range(len(response_spectrum_per))}
#                 #
#                 #     response_data_list2.append(spectrum_data)
#
#             else:
#                 print(f"Periods and ordinates count mismatch for Lat={lat}, Long={long}")
#
#         except ValueError as e:
#             print(f"Error parsing JSON: {e}")
#     else:
#         print(f"Failed to retrieve the webpage. Status code: {resp.status_code}")
#         failed_attempts.append((lat, long, vs30))
#
#         # Create a NaN-filled row with expected keys (matching successful ones)
#         nan_row = {
#             "latitude": lat,
#             "longitude": long,
#             "siteClass": soil_class,
#             "riskCategory": risk_category
#         }
#
#         # Fill the rest with NaNs (you can add more keys if needed)
#         for _ in range(12):  # 12 matches your usual response_data length
#             nan_row[f"data_{_ + 1}"] = float('nan')
#
#         response_data_list.append(nan_row)
#
# # Save to Excel if data is available
# if response_data_list:
#     # Convert to a DataFrame
#     df_response_data = pd.DataFrame(response_data_list)
#
#     # # Output to Excel
#     # df_response_data.to_excel('response_data_output.xlsx', index=False)
#     # print("Data has been written to 'response_data_output.xlsx'")
#     df_response_data.to_excel(f'response_data_output_{start_row}-{end_row}.xlsx', index=False)
#     print(f"Data has been written to 'response_data_output_{start_row}-{end_row}.xlsx'")
# else:
#     print("No response data to save.")
#
# if failed_attempts:
#     failed_df = pd.DataFrame(failed_attempts, columns=["Latitude", "Longitude", "Vs30"])
#     output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\failed_attempts.xlsx"
#     # output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\failed_attempts2.xlsx"
#     failed_df.to_excel(output_path, index=False)
#     print(f"Failed attempts saved to {output_path}")
# else:
#     print("No failed attempts to save.")

# to get spectra from ascehazardtool (unused)
# if response_data_list2:
#     # Convert to a DataFrame
#     df_response_data2 = pd.DataFrame(response_data_list2)
#
#     # # Output to Excel
#     # df_response_data2.to_excel('response_spectrum.xlsx', index=False)
#     # print("Data has been written to 'response_spectrum.xlsx'")
#
#     df_response_data2.to_excel(f'response_spectrum_{start_row}-{end_row}.xlsx', index=False)
#     print(f"Data has been written to 'response_spectrum_{start_row}-{end_row}.xlsx'")
# else:
#     print("No response data to save.")





################## To Concatenate the Output Files ##################

#
# # Set the directory containing your Excel files
#
# directory = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA"
#
# # Optional: Filter by specific sheet name (set to None to use the first sheet)
# sheet_name = 'Sheet1'
#
# # List to store dataframes
# excel_data = []
#
# # Loop through all files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".xlsx") or filename.endswith(".xls"):
#         file_path = os.path.join(directory, filename)
#         try:
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             excel_data.append(df)
#         except Exception as e:
#             print(f"Failed to read {filename}: {e}")
#
# # Concatenate all dataframes
# if excel_data:
#     combined_df = pd.concat(excel_data, ignore_index=True)
#     # Optionally, save to a new Excel file
#     combined_df.to_excel('combined_output.xlsx', index=False)
#     print("Successfully combined all Excel files.")
# else:
#     print("No Excel files found or read.")
#







################ To Get cv ##################

# file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\response_data_us_all.xlsx'
# # Read the relevant columns from the Excel file
# with pd.ExcelFile(file_path) as xls:
#     raw_file = pd.read_excel(xls)
#
# # Perform the calculations and add the new columns directly to the DataFrame
# raw_file['t0'] = 0.2 * raw_file['sd1'] / raw_file['sds']
# raw_file['ts'] = raw_file['sd1'] / raw_file['sds']
#
# # Interpolation values (Table 11.9-1)
# Sms_ipl = np.array([2.0, 1.0, 0.6, 0.3, 0.2])
#
# cv_A_B_ipl = np.array([0.9, 0.9, 0.9, 0.8, 0.7])
# cv_BC_ipl = np.array([1.1, 1.0, 0.95, 0.8, 0.7])
# cv_C_ipl = np.array([1.3, 1.1, 1.0, 0.8, 0.7])
# cv_CD_ipl = np.array([1.4, 1.2, 1.05, 0.85, 0.7])
# cv_D_DE_E_F_ipl = np.array([1.5, 1.3, 1.1, 0.9, 0.7])
#
#
# # Function to apply interpolation based on site class
# def interpolate_cv(row):
#     sms = row['sms']
#     site_class = row['siteClass']
#
#     if site_class in ['A', 'B']:
#         interp = interpolate.interp1d(Sms_ipl, cv_A_B_ipl, kind='linear', fill_value="extrapolate")
#         result = sorted([interp(sms), 0.7, 0.9])[1]
#     elif site_class == 'BC':
#         interp = interpolate.interp1d(Sms_ipl, cv_BC_ipl, kind='linear', fill_value="extrapolate")
#         result = sorted([interp(sms), 0.7, 1.1])[1]
#     elif site_class == 'C':
#         interp = interpolate.interp1d(Sms_ipl, cv_C_ipl, kind='linear', fill_value="extrapolate")
#         result = sorted([interp(sms), 0.7, 1.3])[1]
#     elif site_class == 'CD':
#         interp = interpolate.interp1d(Sms_ipl, cv_CD_ipl, kind='linear', fill_value="extrapolate")
#         result = sorted([interp(sms), 0.7, 1.4])[1]
#     else:
#         interp = interpolate.interp1d(Sms_ipl, cv_D_DE_E_F_ipl, kind='linear', fill_value="extrapolate")
#         result = sorted([interp(sms), 0.7, 1.5])[1]
#
#     # Since the result is an array, extract the scalar and round it
#     return round(float(result), 2)
#
#
#
# # Apply the interpolation function row-wise and assign the result to the 'cv' column
# raw_file['cv'] = raw_file.apply(interpolate_cv, axis=1)
#
# # # Save the updated DataFrame to a new Excel file
#
# raw_file.to_excel('response_us_cv_added.xlsx', index=False)
# print("Data has been written to 'response_us_cv_added.xlsx'")
#




################# To Get Ratios (*) ##################


#
# file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\response_us_cv_added.xlsx'
#
#
# # Read the Excel file with specific columns
# df = pd.read_excel(file_path, usecols=["latitude", "longitude", "riskCategory", "siteClass", "sds", "sd1", "sdc", "t0", "ts", "tl", "cv"])
#
# # Create a list to hold the results for all rows
# Sa_list = []
# Sav_list = []
# Ratio_list = []
#
# reduced_T = [0.0, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10]
#
# # Loop through each row of the DataFrame
# for i in range(len(df)):
#     lat = df.iloc[i]['latitude']
#     lon = df.iloc[i]['longitude']
#     riskCategory = df.iloc[i]['riskCategory']
#     siteClass = df.iloc[i]['siteClass']
#     cv = df.iloc[i]['cv']
#     sds = df.iloc[i]['sds']
#     sd1 = df.iloc[i]['sd1']
#     t0 = df.iloc[i]['t0']
#     ts = df.iloc[i]['ts']
#     tl = df.iloc[i]['tl']
#     sdc = df.iloc[i]['sdc']
#
#     # Initialize an empty list to hold the calculated Sa values
#     Sa = []
#     SaM = []
#     SaMv = []
#     Sav = []
#     Ratio = []
#
#
#   for j in range(len(reduced_T)):
#       T = round(reduced_T[j], 3)
# # Calculate the time period for each index 11.4.5.2
#       if T < t0:
#           sa_value = sds * (0.4 + 0.6 * T / t0)
#       elif T <= ts:
#           sa_value = sds
#       elif T <= tl:
#           sa_value = sd1 / T
#       else:
#           sa_value = tl * sd1 / T ** 2
#
#       saM_value = 1.5*sa_value
#
#       Sa.append(sa_value)
#       SaM.append(saM_value)
#
#       # if sdc in ['C', 'D', 'E', 'F'] and float(lon) > -105:
#       if float(lon) > -105:
#       # if False:
#           saMv_value = 2/3*saM_value
#       else:
#           if T <= 0.2:
#               Fmd = 1.2
#           elif T <= 1.0:
#               Fmd = 1.2+0.0625*(T-0.2)
#           else:
#               Fmd = 1.25+0.05*(T-1.0)/9
#
#             if T <= 0.025:
#                 saMv_value = 0.65*cv*saM_value/Fmd
#             elif T <= 0.05:
#                 saMv_value = 16*cv*saM_value/Fmd*(T-0.025)+0.65*cv*saM_value/Fmd
#             elif T <= 0.1:
#                 saMv_value = 1.05*cv*saM_value/Fmd
#             elif T <= 2.0:
#                 saMv_value = max(1.05*cv*(saM_value/Fmd*sqrt(0.1/T)), 0.5*saM_value/Fmd)
#             else:
#                 saMv_value = 0.5*saM_value/Fmd
#
#         Sav_value = 2/3*saMv_value
#         SaMv.append(saMv_value)
#         Sav.append(Sav_value)
#
#         ratio = 0.3*Sav_value/(0.2*sds)
#         Ratio.append(ratio)
#
#     # Append the calculated Sa values (for this row) along with corresponding T values
#     Sa_data = {}
#     # Sa_data = {'': ''}  # First column is blank (unused)
#     Sa_data['latitude'] = lat
#     Sa_data['longitude'] = lon
#     Sa_data['riskCategory'] = riskCategory
#     Sa_data['siteClass'] = siteClass
#     Sa_data['SDC'] = sdc
#     Sa_data['cv'] = cv
#     Sa_data['sds'] = sds  # The second column is sds
#     Sa_data['sd1'] = sd1
#     Sa_data['t0'] = t0
#     Sa_data['ts'] = ts
#     Sa_data['tl'] = tl
#     Sa_data.update({f'{round(reduced_T[j], 3)}': Sa[j] for j in range(len(Sa))})
#     Sa_list.append(Sa_data)
#
#     Sav_data = {}
#     # Sav_data =  {'': ''}
#     Sav_data['latitude'] = lat
#     Sav_data['longitude'] = lon
#     Sav_data['SDC'] = sdc
#     Sav_data.update({f'{round(reduced_T[j], 3)}': Sav[j] for j in range(len(Sav))})
#     Sav_list.append(Sav_data)
#
#     Ratio_data = {}
#     # Ratio_data = {'': ''}
#     Ratio_data['latitude'] = lat
#     Ratio_data['longitude'] = lon
#     Ratio_data['SDC'] = sdc
#     # Ratio_data['sds'] = sds
#     Ratio_data.update({f'{round(reduced_T[j], 3)}': Ratio[j] for j in range(len(Ratio))})
#     Ratio_list.append(Ratio_data)
# # Check if there is any calculated data to save
# if Sa_list and Sav_list and Ratio_list:
#     # Convert the list of Sa values into a DataFrame
#     df_Sa = pd.DataFrame(Sa_list)
#     df_Sav = pd.DataFrame(Sav_list)
#     df_Ratio = pd.DataFrame(Ratio_list)
#
#     # # Specify the output Excel file path
#     output_path = 'us_H_V_VHRatio.xlsx'
#
#     # Use ExcelWriter to save both sheets in the same file
#     with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
#         df_Sa.to_excel(writer, index=False, sheet_name='H')
#         df_Sav.to_excel(writer, index=False, sheet_name='V')
#         df_Ratio.to_excel(writer, index=False, sheet_name='Ratio')
#     print("Data has been written to 'us_H_V_VHRatio.xlsx' with the sheet names 'H' and 'V' and 'Ratio'")
# else:
#     print("No response data to save.")


# ################# To Show Distribution of SDC ##################


# import geopandas as gpd
# from shapely.geometry import box, Point
# import pandas as pd
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# from pyproj import Transformer
#
# # ================= CONFIGURATION & SETUP =================
# SDC_list = ['A', 'B', 'C', 'D', 'E']
# file_path = r'C:\Users\cheng\PycharmProjects\pythonProject\US\us_all_H_V_VHRatio.xlsx'
# output_dir = r"D:\MyPaper\Comparative Evaluation of Vertical Seismic Effect Methods in ASCE 7-22 for the Continental United States\submission\V3"
#
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
# colors = {
#     'A': '#aec7e8',
#     'B': '#98df8a',
#     'C': '#FFFF00',
#     'D': '#ff7f0e',
#     'E': '#FF0000',
# }
#
# # Ensure the output directory exists
# os.makedirs(output_dir, exist_ok=True)
#
# # ================= MAP FEATURES (BORDERS) =================
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Bounding box around the contiguous US
# bbox_geom = box(-125, 24, -66, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states[clipped_states['STUSPS'] != 'DC']
#
# # Project states to Albers
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Setup transformers to convert between meters and degrees back-and-forth
# to_geo = Transformer.from_crs(target_crs, geo_crs, always_xy=True)
# to_proj = Transformer.from_crs(geo_crs, target_crs, always_xy=True)
#
# # Define exact map limits in meters based on the plotted states
# bounds = clipped_states.total_bounds
# xmin, ymin, xmax, ymax = bounds[0], bounds[1], bounds[2], bounds[3]
#
# # Add map padding
# x_pad = (xmax - xmin) * 0.05
# y_pad = (ymax - ymin) * 0.05
# xmin_map, xmax_map = xmin - x_pad, xmax + x_pad
# ymin_map, ymax_map = ymin - y_pad, ymax + y_pad
#
# # ================= PLOTTING =================
# fig, ax = plt.subplots(figsize=(13, 8))
# ax.set_xlim(xmin_map, xmax_map)
# ax.set_ylim(ymin_map, ymax_map)
#
# # 1. Generate and Plot Target Latitudes (Horizontal Curves)
# target_latitudes = np.arange(25, 51, 5)
# for lat in target_latitudes:
#     lon_seq = np.linspace(-140, -50, 200)
#     lat_seq = np.full_like(lon_seq, lat)
#
#     proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#     valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#     if np.any(valid):
#         ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#         idx_left = np.argmin(proj_x[valid])
#         lbl_y = proj_y[valid][idx_left]
#
#         padding_lbl_x = (xmax_map - xmin_map) * 0.015
#         ax.text(xmin_map - padding_lbl_x, lbl_y, f"{lat}°N",
#                 va='center', ha='right', fontsize=14, color='black')
#
# # 2. Generate and Plot Longitudes (Vertical Curves)
# target_longitudes = np.arange(-125, -60, 5)
# for lon in target_longitudes:
#     lat_seq = np.linspace(20, 55, 200)
#     lon_seq = np.full_like(lat_seq, lon)
#
#     proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#     valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#     if np.any(valid):
#         ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#         idx_bottom = np.argmin(proj_y[valid])
#         lbl_x = proj_x[valid][idx_bottom]
#         lbl_y = proj_y[valid][idx_bottom]
#
#         padding_lbl_y = (ymax_map - ymin_map) * 0.015
#         ax.text(lbl_x, ymin_map - padding_lbl_y, f"{abs(lon)}°W",
#                 va='top', ha='center', fontsize=14, color='black')
#
# # 3. Plot SDC points from excel sheets
# for sdc in SDC_list:
#     try:
#         df = pd.read_excel(file_path, sheet_name=sdc)
#         df.columns = [c.lower() for c in df.columns]
#
#         geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
#         gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs=geo_crs).to_crs(target_crs)
#
#         ax.scatter(gdf_points.geometry.x, gdf_points.geometry.y,
#                    c=colors[sdc], s=2.5, alpha=0.7, zorder=2)
#     except Exception as e:
#         print(f"Error processing sheet {sdc}: {e}")
#
# # 4. Plot state boundaries on top of data points
# clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=3)
#
# # 5. Plot state labels at representative locations (Bold removed)
# for _, row in clipped_states.iterrows():
#     centroid = row.geometry.representative_point()
#     ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=14,
#             color='black', ha='center', va='center', zorder=4)
#
# # ================= FINALIZE, SAVE & DISPLAY =================
# legend_elements = [
#     Line2D([0], [0], marker='o', color='w', label=sdc,
#            markerfacecolor=colors[sdc], markersize=10) for sdc in SDC_list
# ]
# ax.legend(handles=legend_elements, title="SDC", loc='lower left', frameon=True,
#           prop={'size': 14}, title_fontsize=14)
#
# ax.set_xticks([])
# ax.set_yticks([])
#
# plt.tight_layout()
#
# # Save the plot with high resolution for publication layout
# save_path = os.path.join(output_dir, "SDC_Continental_US_Distribution.png")
# plt.savefig(save_path, dpi=300, bbox_inches='tight')
# print(f"Plot successfully saved to: {save_path}")
#
# plt.show()


# ################# To find the best fitted lognormal curve for each Tv (West) ##################


# SDC_type = 'E'
# Tv_bins = ['1', '2', '3', '4', '5', '6', '7', '8']
#
# # === Configuration ===
# input_base_path = rf'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_type}'
# output_folder = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\West_CA_included_fitting'
#
# # Create output folders
# os.makedirs(output_folder, exist_ok=True)
# sheet_output_folder = os.path.join(output_folder, SDC_type)
# os.makedirs(sheet_output_folder, exist_ok=True)
#
# for Tv_bin in Tv_bins:
#     input_path = os.path.join(input_base_path, f'interpolated_{SDC_type}_{Tv_bin}.xlsx')
#     excel_output_path = os.path.join(output_folder, f'lognormal_fit_parameters_{SDC_type}_{Tv_bin}.xlsx')
#
#     print(f"\nProcessing SDC Type: {SDC_type}, Tv_bin: {Tv_bin}")
#     df = pd.read_excel(input_path)  # One sheet only
#
#     fit_results = []
#
#     for col_index in range(0, len(df.columns)):
#         col_name = df.columns[col_index]
#
#         # Extract and clean data
#         column_data = df.iloc[:, col_index]
#         data = pd.to_numeric(column_data, errors='coerce').dropna()
#         data = data[data > 0]
#
#         if len(data) < 3:
#             print(f"Skipping column '{col_name}' (not enough valid data)")
#             continue
#
#         # Fit lognormal distribution
#         shape, loc, scale = lognorm.fit(data, floc=0)
#         mu = np.log(scale)
#         sigma = shape
#         std_x = np.sqrt((np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2))
#
#         # Probability ranges (West)
#         p_lt_0_5 = lognorm.cdf(0.5, sigma, loc=0, scale=scale)
#         p_0_5_to_0_8 = lognorm.cdf(0.8, sigma, loc=0, scale=scale) - p_lt_0_5
#         p_0_8_to_1_2 = lognorm.cdf(1.2, sigma, loc=0, scale=scale) - lognorm.cdf(0.8, sigma, loc=0, scale=scale)
#         p_1_2_to_1_5 = lognorm.cdf(1.5, sigma, loc=0, scale=scale) - lognorm.cdf(1.2, sigma, loc=0, scale=scale)
#         p_gt_1_5 = 1.0 - lognorm.cdf(1.5, sigma, loc=0, scale=scale)
#
#         # Fit PDF and compute SSE
#         x = np.linspace(min(data), max(data), 1000)
#         pdf_fitted = lognorm.pdf(x, shape, loc=loc, scale=scale)
#
#         num_bins = min(80, max(1, len(np.unique(data)) // 2))
#         hist_counts, bin_edges = np.histogram(data, bins=num_bins, density=True)
#
#         bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
#         fitted_pdf_vals = lognorm.pdf(bin_centers, shape, loc=loc, scale=scale)
#         sse = np.sum((hist_counts - fitted_pdf_vals) ** 2)
#
#         # Store results
#         fit_results.append({
#             'SDC': SDC_type,
#             'Tv': col_name,
#             'bins': num_bins,
#             'μ (log mean)': mu,
#             'σ (shape)': sigma,
#             'Scale (exp(μ))': scale,
#             'Std(X)': std_x,
#             'SSE': sse,
#             'P(x ≤ 0.5)': p_lt_0_5,
#             'P(0.5 < x ≤ 0.8)': p_0_5_to_0_8,
#             'P(0.8 < x ≤ 1.2)': p_0_8_to_1_2,
#             'P(1.2 < x ≤ 1.5)': p_1_2_to_1_5,
#             'P(x > 1.5)': p_gt_1_5
#         })
#
#         # Plot and save
#         plt.figure(figsize=(10, 6))
#         plt.hist(data, bins=num_bins, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Histogram')
#         plt.plot(x, pdf_fitted, 'r-', lw=2, label='Best Fitted LogNormal PDF')
#         plt.xlabel(f'V/H Ratio at Tv = {col_name}s')
#         plt.ylabel('Frequency')
#         plt.legend()
#         plt.grid(True)
#         plt.tight_layout()
#
#         plot_filename = os.path.join(sheet_output_folder, f"lognormal_fit_{col_name}_Tv{Tv_bin}.png")
#         plt.savefig(plot_filename)
#         plt.close()
#
#         print(f"Saved plot for column '{col_name}' to {plot_filename}")
#         print(f"  μ = {mu:.4f}, σ = {sigma:.4f}, bins = {num_bins}, scale = {scale:.4f}, Std(X) = {std_x:.4f}, SSE = {sse:.4f}")
#
#     # Save Excel for each Tv_bin
#     results_df = pd.DataFrame(fit_results)
#     with pd.ExcelWriter(excel_output_path, engine='xlsxwriter') as writer:
#         results_df.to_excel(writer, index=False, sheet_name='Lognormal_Fits')
#
#     print(f"All fit results saved to: {excel_output_path}")




################# To find the best fitted lognormal curve for each Tv (East) ##################


# SDC_type = 'E'
# Tv_bins = ['1', '2', '3', '4', '5', '6', '7', '8']
#
# long_str='East_-75to_0'
# # === Configuration ===
# input_base_path = rf'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_{long_str}\{SDC_type}'
# output_folder = rf'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\{long_str}_fitting'
#
# # Create output folders
# os.makedirs(output_folder, exist_ok=True)
# sheet_output_folder = os.path.join(output_folder, SDC_type)
# os.makedirs(sheet_output_folder, exist_ok=True)
#
# for Tv_bin in Tv_bins:
#     input_path = os.path.join(input_base_path, f'interpolated_{SDC_type}_{Tv_bin}.xlsx')
#     excel_output_path = os.path.join(output_folder, f'lognormal_fit_parameters_{SDC_type}_{Tv_bin}.xlsx')
#
#     print(f"\nProcessing SDC Type: {SDC_type}, Tv_bin: {Tv_bin}")
#     df = pd.read_excel(input_path)  # One sheet only
#
#     fit_results = []
#
#     for col_index in range(0, len(df.columns)):
#         col_name = df.columns[col_index]
#
#         # Extract and clean data
#         column_data = df.iloc[:, col_index]
#         data = pd.to_numeric(column_data, errors='coerce').dropna()
#         data = data[data > 0]
#
#         if len(data) < 3:
#             print(f"Skipping column '{col_name}' (not enough valid data)")
#             continue
#
#         # Fit lognormal distribution
#         shape, loc, scale = lognorm.fit(data, floc=0)
#         mu = np.log(scale)
#         sigma = shape
#         std_x = np.sqrt((np.exp(sigma ** 2) - 1) * np.exp(2 * mu + sigma ** 2))
#
#         # Probability ranges (East)
#         p_lt_0_5 = lognorm.cdf(0.5, sigma, loc=0, scale=scale)
#         p_0_5_to_0_8 = lognorm.cdf(0.8, sigma, loc=0, scale=scale) - p_lt_0_5
#         p_gt_0_8 = 1.0 - lognorm.cdf(0.8, sigma, loc=0, scale=scale)
#
#         # Fit PDF and compute SSE
#         x = np.linspace(min(data), max(data), 1000)
#         pdf_fitted = lognorm.pdf(x, shape, loc=loc, scale=scale)
#
#         num_bins = min(80, max(1, len(np.unique(data)) // 2))
#         hist_counts, bin_edges = np.histogram(data, bins=num_bins, density=True)
#
#         bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
#         fitted_pdf_vals = lognorm.pdf(bin_centers, shape, loc=loc, scale=scale)
#         sse = np.sum((hist_counts - fitted_pdf_vals) ** 2)
#
#         # Store results
#         fit_results.append({
#             'SDC': SDC_type,
#             'Tv': col_name,
#             'bins': num_bins,
#             'μ (log mean)': mu,
#             'σ (shape)': sigma,
#             'Scale (exp(μ))': scale,
#             'Std(X)': std_x,
#             'SSE': sse,
#             'P(x ≤ 0.5)': p_lt_0_5,
#             'P(0.5 < x ≤ 0.8)': p_0_5_to_0_8,
#             'P(0.8 < x)': p_gt_0_8,
#         })
#
#         # Plot and save
#         plt.figure(figsize=(10, 6))
#         plt.hist(data, bins=num_bins, density=True, alpha=0.6, color='skyblue', edgecolor='black', label='Histogram')
#         plt.plot(x, pdf_fitted, 'r-', lw=2, label='Best Fitted LogNormal PDF')
#         plt.xlabel(f'V/H Ratio at Tv = {col_name}s')
#         plt.ylabel('Frequency')
#         plt.legend()
#         plt.grid(True)
#         plt.tight_layout()
#
#         plot_filename = os.path.join(sheet_output_folder, f"lognormal_fit_{col_name}_Tv{Tv_bin}.png")
#         plt.savefig(plot_filename)
#         plt.close()
#
#         print(f"Saved plot for column '{col_name}' to {plot_filename}")
#         print(f"  μ = {mu:.4f}, σ = {sigma:.4f}, bins = {num_bins}, scale = {scale:.4f}, Std(X) = {std_x:.4f}, SSE = {sse:.4f}")
#
#     # Save Excel for each Tv_bin
#     results_df = pd.DataFrame(fit_results)
#     with pd.ExcelWriter(excel_output_path, engine='xlsxwriter') as writer:
#         results_df.to_excel(writer, index=False, sheet_name='Lognormal_Fits')
#
#     print(f"All fit results saved to: {excel_output_path}")




################# To combine the fitted parameterd (Lognormal fitted) ##################


#
# # Define the base directory
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\East_-75to-0_fitting"
#
# # List of sections to loop through
# sections = ['A', 'B', 'C', 'D', 'E']
#
# # Loop through each section separately
# for section in sections:
#     df_list = []  # Clear list for each section
#     for i in range(1, 9):  # Files 1 through 8
#         filename = f"lognormal_fit_parameters_{section}_{i}.xlsx"
#         file_path = os.path.join(base_dir, filename)
#         if os.path.exists(file_path):
#             df = pd.read_excel(file_path)
#             df_list.append(df)
#         else:
#             print(f"File not found: {file_path}")
#
#     # Concatenate and save for this section
#     if df_list:
#         combined_df = pd.concat(df_list, ignore_index=True)
#         output_filename = f"combined_fit_{section}.xlsx"
#         output_path = os.path.join(base_dir, output_filename)
#         combined_df.to_excel(output_path, index=False)
#         print(f"Saved: {output_path}")
#     else:
#         print(f"No files found for section {section}")




################ To get the probability distribution (Lognormal fitted) ##################
#
# # Base directory
# base_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\East_-75to-0_fitting'
#
# # SDC types to loop through
# sdc_types = ['A', 'B', 'C', 'D', 'E']
#
# # Tv bins and labels
# tv_bins = [0, 0.025, 0.05, 0.1, 0.2, 0.5, 1, 2, 10]
#
# # # (West)
# # tv_labels = [
# #     r'$0 < T_v \leq 0.025$',
# #     r'$0.025 < T_v \leq 0.05$',
# #     r'$0.05 < T_v \leq 0.1$',
# #     r'$0.1 < T_v \leq 0.2$',
# #     r'$0.2 < T_v \leq 0.5$',
# #     r'$0.5 < T_v \leq 1$',
# #     r'$1 < T_v \leq 2$',
# #     r'$2 < T_v \leq 10$'
# # ]
# #
# # # Columns of interest (make sure they match the actual Excel file headers)
# # prob_cols = [
# #     'P(x > 1.5)',
# #     'P(1.2 < x ≤ 1.5)',
# #     'P(0.8 < x ≤ 1.2)',
# #     'P(0.5 < x ≤ 0.8)',
# #     'P(x ≤ 0.5)'
# # ]
#
#
# # (East)
# tv_labels = [
#     r'$0 < T_v \leq 0.025$',
#     r'$0.025 < T_v \leq 0.05$',
#     r'$0.05 < T_v \leq 0.1$',
#     r'$0.1 < T_v \leq 0.2$',
#     r'$0.2 < T_v \leq 0.5$',
#     r'$0.5 < T_v \leq 1$',
#     r'$1 < T_v \leq 2$',
#     r'$2 < T_v \leq 10$'
# ]
#
# # Columns of interest (make sure they match the actual Excel file headers)
# prob_cols = [
#
#     'P(0.8 < x)',
#     'P(0.5 < x ≤ 0.8)',
#     'P(x ≤ 0.5)'
# ]
#
# for sdc_type in sdc_types:
#     file_path = os.path.join(base_dir, f'combined_fit_{sdc_type}.xlsx')
#
#     if not os.path.exists(file_path):
#         print(f"File not found: {file_path}")
#         continue
#
#     df = pd.read_excel(file_path)
#
#     # Bin Tv
#     df['Tv_bin'] = pd.cut(df['Tv'], bins=tv_bins, labels=tv_labels, include_lowest=True)
#
#     # Group by Tv_bin and compute mean
#     result = df.groupby('Tv_bin', observed=False)[prob_cols].mean()
#
#     # Convert to percentages
#     result[prob_cols] = result[prob_cols] * 100
#
#     # Reset and transpose
#     result = result.reset_index()
#     result = result.set_index('Tv_bin').transpose()
#
#     # Save to Excel
#     output_file = os.path.join(base_dir, f'fitted_probability_averages_{sdc_type}.xlsx')
#     result.to_excel(output_file)
#
#     print(f"Saved: {output_file}")





################# To get the probability distribution (slice) ##################


# # File paths
# input_file = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx'
# output_file = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\E\interpolated_E_8.xlsx'
#
# # Load data
# # ABCDE
# df = pd.read_excel(input_file, sheet_name='E', header=None)
#
# # Extract the first row
# first_row = df.iloc[[0]]
#
# # Filter the rest of the DataFrame based on longitude
# filtered_rows = df.iloc[1:]
# filtered_rows = filtered_rows[(filtered_rows.iloc[:, 1] > -160) & (filtered_rows.iloc[:, 1] <= -105)]
#
# # Concatenate the first row with the filtered rows
# df = pd.concat([first_row, filtered_rows], ignore_index=True)
#
#
# ## df_filtered = df.iloc[:, 3:7]
# ## df_filtered = df.iloc[:, 5:8]
# ## df_filtered = df.iloc[:, 7:10]
# ## df_filtered = df.iloc[:, 9:12]
# ## df_filtered = df.iloc[:, 11:16]
# ## df_filtered = df.iloc[:, 15:18]
# ## df_filtered = df.iloc[:, 17:20]
# ## df_filtered = df.iloc[:, 19:25]
#
# # Filter the DataFrame
# df_filtered = df.iloc[:, 19:25]
#
# # Extract x and y data
# x = df_filtered.iloc[0].astype(float).values
# y_data = df_filtered.iloc[1:].astype(float).values
#
# # Check x is strictly increasing
# if not np.all(np.diff(x) > 0):
#     raise ValueError("x must be strictly increasing.")
#
# # Interpolate 0.001 for 1-7, 0.01 for 8
# # x_new = np.arange(x.min(), x.max() + 0.001, 0.001)
# x_new = np.arange(x.min(), x.max() + 0.01, 0.01)
# interpolated_rows = []
# for row in y_data:
#     f = interp1d(x, row, kind='linear', bounds_error=False, fill_value="extrapolate")
#     interpolated_row = f(x_new)
#     interpolated_rows.append(interpolated_row)
#
# interpolated_df = pd.DataFrame(interpolated_rows, columns=np.round(x_new, 3))
#
# os.makedirs(os.path.dirname(output_file), exist_ok=True)
# # Save with ZIP64 enabled
# with pd.ExcelWriter(output_file, engine='xlsxwriter', engine_kwargs={'options': {'use_zip64': True}}) as writer:
#     interpolated_df.to_excel(writer, index=False)




################# To count points (raw data colored grids) ##################

#
#
# # ABCDE
# input_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East_`\E'
# summary_output_path = os.path.join(input_dir, 'counts.xlsx')
#
# # Bins we are interested in
# # (West)
# # bin_labels = ['<0.5', '0.5–0.8', '0.8–1.2', '1.2–1.5', '>1.5']
#
# # (East)
# bin_labels = ['<0.5', '0.5–0.8', '>0.8']
#
# summary_df = pd.DataFrame(index=bin_labels)
#
# # Dictionary to store number of columns in each file
# column_counts = {}
#
# # Iterate over all Excel files in the directory
# for file in os.listdir(input_dir):
#     if file.endswith('.xlsx') and 'interpolated' in file.lower():  # filter only interpolated Excel files
#         file_path = os.path.join(input_dir, file)
#         try:
#             # Read interpolated data (assume first sheet)
#             df = pd.read_excel(file_path)
#
#             # Keep only numeric columns
#             df = df.select_dtypes(include='number')
#
#             # Store number of columns
#             column_counts[file] = df.shape[1]
#
#             # Compute counts in each bin
#             #
#             # (West)
#             # count_lt_0_5 = (df <= 0.5).sum().sum()
#             # count_0_5_to_0_8 = ((df > 0.5) & (df <= 0.8)).sum().sum()
#             # count_0_8_to_1_2 = ((df > 0.8) & (df <= 1.2)).sum().sum()
#             # count_1_2_to_1_5 = ((df > 1.2) & (df <= 1.5)).sum().sum()
#             # count_gt_1_5 = (df > 1.5).sum().sum()
#
#             # (East)
#             count_lt_0_5 = (df <= 0.5).sum().sum()
#             count_0_5_to_0_8 = ((df > 0.5) & (df <= 0.8)).sum().sum()
#             count_gt_0_8 = ((df > 0.8)).sum().sum()
#
#
#             # Append to summary DataFrame
#             #
#             # (West)
#             # summary_df[file] = [
#             #     count_lt_0_5,
#             #     count_0_5_to_0_8,
#             #     count_0_8_to_1_2,
#             #     count_1_2_to_1_5,
#             #     count_gt_1_5
#             # ]
#
#             # (East)
#             summary_df[file] = [
#                 count_lt_0_5,
#                 count_0_5_to_0_8,
#                 count_gt_0_8
#             ]
#
#             # double check the manually spliced column numbers
#             # 25  25  50  100  300  500  1000  800
#
#             print(f"Processed: {file} with {df.shape[1]} columns")
#
#         except Exception as e:
#             print(f"Error processing {file}: {e}")
#
#
# # Save the summary and column counts to Excel
# summary_df.to_excel(summary_output_path)
# print(f"Summary written to: {summary_output_path}")






################ To get percentage and plot heatmaps (raw data colored grids) ##################

#
# # Base path where folders A to E are located
# base_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East_-105to-95'
#
# # Folder list
# folders = ['A', 'B', 'C', 'D', 'E']
#
# # Labels
# # # (West)
# # x_labels = [
# #     r'$0 < T_v \leq  0.025$',
# #     r'$0.025 < T_v \leq 0.05$',
# #     r'$0.05 < T_v \leq 0.1$',
# #     r'$0.1 < T_v \leq 0.2$',
# #     r'$0.2 < T_v \leq 0.5$',
# #     r'$0.5 < T_v \leq 1$',
# #     r'$1 < T_v \leq 2$',
# #     r'$2 < T_v \leq 10$'
# # ]
# # y_labels = [
# #     r'$R_{E_{V}} > 1.5$',
# #     r'$1.2 < R_{E_{V}} \leq 1.5$',
# #     r'$0.8 < R_{E_{V}} \leq 1.2$',
# #     r'$0.5 < R_{E_{V}} \leq 0.8$',
# #     r'$R_{E_{V}} \leq 0.5$'
# # ]
#
# # (East)
# x_labels = [
#     r'$0 < T_v \leq  0.025$',
#     r'$0.025 < T_v \leq 0.05$',
#     r'$0.05 < T_v \leq 0.1$',
#     r'$0.1 < T_v \leq 0.2$',
#     r'$0.2 < T_v \leq 0.5$',
#     r'$0.5 < T_v \leq 1$',
#     r'$1 < T_v \leq 2$',
#     r'$2 < T_v \leq 10$'
# ]
# y_labels = [
#     r'$0.8 < R_{E_{V}}$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$R_{E_{V}} \leq 0.5$'
# ]
#
#
# for folder in folders:
#     folder_path = os.path.join(base_dir, folder)
#     input_file = os.path.join(folder_path, 'counts.xlsx')
#
#     if not os.path.exists(folder_path):
#         print(f"Skipping folder {folder}: folder does not exist.")
#         continue
#     if not os.path.isfile(input_file):
#         print(f"Skipping folder {folder}: counts.xlsx not found.")
#         continue
#
#     print(f"Processing folder: {folder}")
#
#     output_file = os.path.join(folder_path, 'ratio_output.xlsx')
#     output_image = os.path.join(base_dir, f'{folder}_percentage_distribution_raw.png')
#
#     # Load data
#     df = pd.read_excel(input_file, index_col=0)
#
#     # Compute ratios
#     column_sums = df.sum(axis=0)
#     ratio_df = df.div(column_sums, axis=1).round(4) * 100
#     ratio_df = ratio_df.iloc[::-1]
#     ratio_df.to_excel(output_file)
#
#     # Plot setup
#     data = ratio_df.values
#     rows, cols = data.shape
#     fig, ax = plt.subplots(figsize=(8, 6))
#     cmap = plt.cm.Blues
#     x = np.arange(cols + 1)
#     y = np.arange(rows + 1)
#
#     # Draw heatmap
#     mesh = ax.pcolormesh(x, y, data, cmap=cmap, shading='auto', edgecolors='none')
#
#     # Dashed grid lines
#     for i in range(1, cols):
#         ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
#     for j in range(1, rows):
#         ax.axhline(j, color='gray', linestyle='--', linewidth=0.5)
#
#     # Annotations
#     for i in range(rows):
#         for j in range(cols):
#             val = data[i, j]
#             color = 'white' if val >= 50 else 'black'
#             ax.text(j + 0.5, i + 0.5, f'{val:.2f}', ha='center', va='center', color=color)
#
#     # Ticks and labels
#     ax.set_xticks(np.arange(cols) + 0.5)
#     ax.set_yticks(np.arange(rows) + 0.5)
#     ax.set_xticklabels(x_labels, rotation=45, ha='right')
#     ax.set_yticklabels(y_labels)
#
#     # Axes limits
#     ax.set_xlim(0, cols)
#     ax.set_ylim(0, rows)
#     ax.invert_yaxis()
#     ax.set_aspect('equal')
#
#     # Colorbar and layout
#     cbar = plt.colorbar(mesh, ax=ax)
#     cbar.set_label("Percentage (%)")
#     plt.tight_layout()
#
#     # Save plot
#     plt.savefig(output_image, dpi=300)
#     plt.close()
#
# print("All available folders processed.")







################# To plot heatmaps (fitted data colored grids) ##################

#
# # Base path where folders A to E are located
# base_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\East_-95to-85_fitting'
#
# # Folder list
# folders = ['A', 'B', 'C', 'D', 'E']
#
#
# # Labels
# # # (West)
# # x_labels = [
# #     r'$0 < T_v \leq  0.025$',
# #     r'$0.025 < T_v \leq 0.05$',
# #     r'$0.05 < T_v \leq 0.1$',
# #     r'$0.1 < T_v \leq 0.2$',
# #     r'$0.2 < T_v \leq 0.5$',
# #     r'$0.5 < T_v \leq 1$',
# #     r'$1 < T_v \leq 2$',
# #     r'$2 < T_v \leq 10$'
# # ]
# # y_labels = [
# #     r'$R_{E_{V}} > 1.5$',
# #     r'$1.2 < R_{E_{V}} \leq 1.5$',
# #     r'$0.8 < R_{E_{V}} \leq 1.2$',
# #     r'$0.5 < R_{E_{V}} \leq 0.8$',
# #     r'$R_{E_{V}} \leq 0.5$'
# # ]
#
# # (East)
# x_labels = [
#     r'$0 < T_v \leq  0.025$',
#     r'$0.025 < T_v \leq 0.05$',
#     r'$0.05 < T_v \leq 0.1$',
#     r'$0.1 < T_v \leq 0.2$',
#     r'$0.2 < T_v \leq 0.5$',
#     r'$0.5 < T_v \leq 1$',
#     r'$1 < T_v \leq 2$',
#     r'$2 < T_v \leq 10$'
# ]
# y_labels = [
#     r'$0.8 < R_{E_{V}}$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$R_{E_{V}} \leq 0.5$'
# ]
#
# for folder in folders:
#     input_file = os.path.join(base_dir, f'fitted_probability_averages_{folder}.xlsx')
#
#     if not os.path.exists(base_dir):
#         print(f"Skipping folder {folder}: folder does not exist.")
#         continue
#     if not os.path.isfile(input_file):
#         print(f"Skipping folder {folder}: fitted_probability_averages_{folder}.xlsx not found.")
#         continue
#
#     print(f"Processing folder: {folder}")
#
#     output_image = os.path.join(base_dir, f'{folder}_percentage_distribution_fitted.png')
#
#     # Load data
#     ratio_df = pd.read_excel(input_file, index_col=0)
#
#     # Plot setup
#     data = ratio_df.values
#     rows, cols = data.shape
#     fig, ax = plt.subplots(figsize=(8, 6))
#     cmap = plt.cm.Blues
#     x = np.arange(cols + 1)
#     y = np.arange(rows + 1)
#
#     # Draw heatmap
#     mesh = ax.pcolormesh(x, y, data, cmap=cmap, shading='auto', edgecolors='none')
#
#     # Dashed grid lines
#     for i in range(1, cols):
#         ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
#     for j in range(1, rows):
#         ax.axhline(j, color='gray', linestyle='--', linewidth=0.5)
#
#     # Annotations
#     for i in range(rows):
#         for j in range(cols):
#             val = data[i, j]
#             color = 'white' if val >= 50 else 'black'
#             ax.text(j + 0.5, i + 0.5, f'{val:.2f}', ha='center', va='center', color=color)
#
#     # Ticks and labels
#     ax.set_xticks(np.arange(cols) + 0.5)
#     ax.set_yticks(np.arange(rows) + 0.5)
#     ax.set_xticklabels(x_labels, rotation=45, ha='right')
#     ax.set_yticklabels(y_labels)
#
#     # Axes limits
#     ax.set_xlim(0, cols)
#     ax.set_ylim(0, rows)
#     ax.invert_yaxis()
#     ax.set_aspect('equal')
#
#     # Colorbar and layout
#     cbar = plt.colorbar(mesh, ax=ax)
#     cbar.set_label("Percentage (%)")
#     plt.tight_layout()
#
#     # Save plot
#     plt.savefig(output_image, dpi=300)
#     plt.close()
#
# print("All available folders processed.")






################# To plot error of fitted and raw data ##################
#
# long_str = 'East_-105to-95'
#
# # Base path where folders A to E are located
# base_dir_raw = rf'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_{long_str}'
# base_dir_fitted = rf'C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\{long_str}_fitting'
#
# # Folder list
# folders = ['A', 'B', 'C', 'D', 'E']
#
# # Labels
# # # （West)
# # x_labels = [
# #     r'$0 < T_v \leq  0.025$',
# #     r'$0.025 < T_v \leq 0.05$',
# #     r'$0.05 < T_v \leq 0.1$',
# #     r'$0.1 < T_v \leq 0.2$',
# #     r'$0.2 < T_v \leq 0.5$',
# #     r'$0.5 < T_v \leq 1$',
# #     r'$1 < T_v \leq 2$',
# #     r'$2 < T_v \leq 10$'
# # ]
# # y_labels = [
# #     r'$R_{E_{V}} > 1.5$',
# #     r'$1.2 < R_{E_{V}} \leq 1.5$',
# #     r'$0.8 < R_{E_{V}} \leq 1.2$',
# #     r'$0.5 < R_{E_{V}} \leq 0.8$',
# #     r'$R_{E_{V}} \leq 0.5$'
# # ]
#
#
# # （East)
# x_labels = [
#     r'$0 < T_v \leq  0.025$',
#     r'$0.025 < T_v \leq 0.05$',
#     r'$0.05 < T_v \leq 0.1$',
#     r'$0.1 < T_v \leq 0.2$',
#     r'$0.2 < T_v \leq 0.5$',
#     r'$0.5 < T_v \leq 1$',
#     r'$1 < T_v \leq 2$',
#     r'$2 < T_v \leq 10$'
# ]
# y_labels = [
#     r'$0.8 < R_{E_{V}}$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$R_{E_{V}} \leq 0.5$'
# ]
#
#
# for folder in folders:
#     input_file_raw = os.path.join(base_dir_raw, folder, f'ratio_output.xlsx')
#     input_file_fitted = os.path.join(base_dir_fitted, f'fitted_probability_averages_{folder}.xlsx')
#
#     if not os.path.exists(base_dir_fitted):
#         print(f"Skipping folder {folder}: fitted folder does not exist.")
#         continue
#     if not os.path.isfile(input_file_fitted):
#         print(f"Skipping folder {folder}: fitted_probability_averages_{folder}.xlsx not found.")
#         continue
#     if not os.path.exists(base_dir_raw):
#         print(f"Skipping folder {folder}: raw folder does not exist.")
#         continue
#     if not os.path.isfile(input_file_raw):
#         print(f"Skipping folder {folder}: raw_probability_averages_{folder}.xlsx not found.")
#         continue
#
#     print(f"Processing folder: {folder}")
#     output_image = os.path.join(base_dir_fitted, f'{folder}_fitting_error.png')
#
#     # Load data
#     ratio_df_raw = pd.read_excel(input_file_raw, index_col=0)
#     ratio_df_fitted = pd.read_excel(input_file_fitted, index_col=0)
#
#     # Calculate difference (fitted - raw), 5x8 matrix
#     raw_data = ratio_df_raw.values
#     fitted_data = ratio_df_fitted.values
#
#     with np.errstate(divide='ignore', invalid='ignore'):
#         err_data = np.where(raw_data == 0, 0, (fitted_data - raw_data))
#
#     err_df = pd.DataFrame(err_data, index=ratio_df_raw.index, columns=ratio_df_raw.columns)
#
#     # Plot setup
#     data = err_df.values
#     rows, cols = data.shape
#     fig, ax = plt.subplots(figsize=(8, 6))
#
#     # Custom colormap: green (neg), white (0), red (pos)
#     cmap = LinearSegmentedColormap.from_list('custom_diverging', ['green', 'white', 'red'], N=256)
#     norm = TwoSlopeNorm(vmin=np.nanmin(data), vcenter=0, vmax=np.nanmax(data))
#
#     x = np.arange(cols + 1)
#     y = np.arange(rows + 1)
#
#     # Draw heatmap
#     mesh = ax.pcolormesh(x, y, data, cmap=cmap, norm=norm, shading='auto', edgecolors='none')
#
#     # Dashed grid lines
#     for i in range(1, cols):
#         ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
#     for j in range(1, rows):
#         ax.axhline(j, color='gray', linestyle='--', linewidth=0.5)
#
#     # Annotations
#     for i in range(rows):
#         for j in range(cols):
#             val = data[i, j]
#             color = 'white' if abs(val) >= 50 else 'black'
#             ax.text(j + 0.5, i + 0.5, f'{val:.2f}', ha='center', va='center', color=color)
#
#     # Ticks and labels
#     ax.set_xticks(np.arange(cols) + 0.5)
#     ax.set_yticks(np.arange(rows) + 0.5)
#     ax.set_xticklabels(x_labels, rotation=45, ha='right')
#     ax.set_yticklabels(y_labels)
#
#     # Axes limits
#     ax.set_xlim(0, cols)
#     ax.set_ylim(0, rows)
#     ax.invert_yaxis()
#     ax.set_aspect('equal')
#
#     # Colorbar and layout
#     cbar = plt.colorbar(mesh, ax=ax)
#     cbar.set_label("Difference (Fitted - Raw)")
#     plt.tight_layout()
#
#     # Save plot
#     plt.savefig(output_image, dpi=300)
#     plt.close()
#
# print("All available folders processed.")







################# To get REV distribution at each Tv ##################

#
# # Set TV threshold string
# Tv_str = '0.0'
#
# # Ensure output directory exists
# output_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\REV distribution'
# os.makedirs(output_dir, exist_ok=True)
#
# # Load your main data
# df = pd.read_excel(
#     r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx",
#     sheet_name='Ratio'
# )
#
# # Load border coordinates from Excel
# border_df = pd.read_excel(r"C:\Users\cheng\PycharmProjects\pythonProject\boarder_CA_included.xlsx")
# border_coords = list(zip(border_df['longitude'], border_df['latitude']))
# border_poly = Polygon(border_coords)
#
# # Drop missing values
# df = df.dropna(subset=['latitude', 'longitude', Tv_str])
#
# # Extract coordinates and values
# lon = df['longitude'].values
# lat = df['latitude'].values
# val = df[Tv_str].values
#
# # Create interpolation grid
# grid_x, grid_y = np.meshgrid(
#     np.linspace(lon.min(), lon.max(), 250),
#     np.linspace(lat.min(), lat.max(), 250)
# )
# grid_z = griddata((lon, lat), val, (grid_x, grid_y), method='linear')
#
# # Mask grid values outside the polygon
# grid_z_masked = np.full(grid_z.shape, np.nan)
# for i in range(grid_x.shape[0]):
#     for j in range(grid_x.shape[1]):
#         point = Point(grid_x[i, j], grid_y[i, j])
#         if border_poly.contains(point):
#             grid_z_masked[i, j] = grid_z[i, j]
#
# # Set colormap normalization to enhance contrast
# norm = colors.Normalize(vmin=0.0, vmax=2.25)
#
# # Plotting
# plt.figure(figsize=(10, 6))
# plt.scatter(lon, lat, c=val, cmap='plasma', s=12, alpha=0.7, norm=norm)
#
# contour = plt.contour(grid_x, grid_y, grid_z_masked,
#                       levels=[0.5, 0.8, 1.0, 1.2, 1.5],
#                       colors='white', linewidths=0.5)
# plt.clabel(contour, fmt='%.1f', inline=True, colors='white', fontsize=8)
#
# # Save scatter to variable to use in colorbar
# sc = plt.scatter(lon, lat, c=val, cmap='plasma', s=12, alpha=0.7, norm=norm)
#
# # Add colorbar
# cbar = plt.colorbar(sc, label=r'$R_{E_{V}}$')
# cbar.ax.tick_params(labelsize=10)
#
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
#
# # Add vertical line at longitude = -105
# plt.axvline(x=-105, color='black', linestyle='--', linewidth=1)
# plt.xticks(list(plt.xticks()[0]) + [-105])
# plt.xlim(-130, -65)
# plt.ylim(24, 50)
# plt.tight_layout()
#
# # Save the figure
# plt.savefig(rf'{output_dir}\Tv={Tv_str}.png', dpi=300, bbox_inches='tight')
# plt.show()






################# To get SDC disaggregated REV distribution for averaged Tv ranges ##################



#
# # ABCDE
# SDC_str='E'
#
# # ================= EAST =================
# file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#
# if 'latitude' in df_East.columns and 'longitude' in df_East.columns:
#     latitudes_East = df_East['latitude']
#     longitudes_East = df_East['longitude']
#     coordinates_East = list(zip(latitudes_East, longitudes_East))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ================= WEST =================
# file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#
# if 'latitude' in df_West.columns and 'longitude' in df_West.columns:
#     latitudes_West = df_West['latitude']
#     longitudes_West = df_West['longitude']
#     coordinates_West = list(zip(latitudes_West, longitudes_West))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ================= Loop Through A_1 to A_8 =================
# for i in range(1, 9):
#     interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_East = pd.read_excel(interpolated_path_East)
#     averages_East = df2_East.iloc[:, :].mean(axis=1).round(4)
#     combined_East = list(zip(coordinates_East, averages_East))
#
#     interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_West = pd.read_excel(interpolated_path_West)
#     averages_West = df2_West.iloc[:, :].mean(axis=1).round(4)
#     combined_West = list(zip(coordinates_West, averages_West))
#
#     # Create the plot
#     plt.figure(figsize=(12, 6))
#     norm = colors.Normalize(vmin=0.0, vmax=2.25)
#     # Plot East
#     east_lats, east_lons = zip(*coordinates_East)
#     plt.scatter(east_lons, east_lats, c=averages_East, s=1, cmap='plasma', norm=norm)
#
#     # Plot West
#     west_lats, west_lons = zip(*coordinates_West)
#     plt.scatter(west_lons, west_lats, c=averages_West, s=1, cmap='plasma', norm=norm)
#
#     # Add labels and legend
#     plt.xlabel("Longitude")
#     plt.ylabel("Latitude")
#     plt.colorbar()
#
#     # Add vertical line at longitude = -105
#     plt.axvline(x=-105, color='black', linestyle='--', linewidth=1)
#     plt.xticks(list(plt.xticks()[0]) + [-105])
#     plt.xlim(-130, -65)
#     plt.ylim(24, 50)
#     plt.tight_layout()
#     plt.grid(True)
#
#     # Ensure the directory exists
#     output_dir = rf"C:\Users\cheng\PycharmProjects\pythonProject\Disaggregated REV\{SDC_str}"
#     os.makedirs(output_dir, exist_ok=True)
#
#     plt.savefig(rf"C:\Users\cheng\PycharmProjects\pythonProject\Disaggregated REV\{SDC_str}\{SDC_str}_Tv{i}.png", dpi=300)
#     plt.close()






################# To get SDC disaggregated categorized heatmaps (5 subgroups) ##################
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib import colors
#
# # ABCDE
# SDC_str = 'D'
#
# # ================= EAST =================
# file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#
# if 'latitude' in df_East.columns and 'longitude' in df_East.columns:
#     latitudes_East = df_East['latitude']
#     longitudes_East = df_East['longitude']
#     coordinates_East = list(zip(latitudes_East, longitudes_East))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ================= WEST =================
# file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#
# if 'latitude' in df_West.columns and 'longitude' in df_West.columns:
#     latitudes_West = df_West['latitude']
#     longitudes_West = df_West['longitude']
#     coordinates_West = list(zip(latitudes_West, longitudes_West))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ======= Remap Function =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
# # ======= Color Map Setup =======
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [
#     r'$R_{E_{V}} \leq 0.5$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$0.8 < R_{E_{V}} \leq 1.2$',
#     r'$1.2 < R_{E_{V}} \leq 1.5$',
#     r'$1.5 < R_{E_{V}}$'
# ]
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ================= Loop Through A_1 to A_8 =================
# for i in range(1, 9):
#     interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_East = pd.read_excel(interpolated_path_East)
#     averages_East_raw = df2_East.iloc[:, :].mean(axis=1).round(4)
#     averages_East = averages_East_raw.apply(remap_average)
#     combined_East = list(zip(coordinates_East, averages_East))
#
#     interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_West = pd.read_excel(interpolated_path_West)
#     averages_West_raw = df2_West.iloc[:, :].mean(axis=1).round(4)
#     averages_West = averages_West_raw.apply(remap_average)
#     combined_West = list(zip(coordinates_West, averages_West))
#
#     # Create the plot
#     plt.figure(figsize=(12, 6))
#
#     # Plot East
#     east_lats, east_lons = zip(*coordinates_East)
#     plt.scatter(east_lons, east_lats, c=averages_East, s=1, cmap=cmap, norm=norm)
#
#     # Plot West
#     west_lats, west_lons = zip(*coordinates_West)
#     plt.scatter(west_lons, west_lats, c=averages_West, s=1, cmap=cmap, norm=norm)
#
#     # Add labels and colorbar
#     plt.xlabel("Longitude")
#     plt.ylabel("Latitude")
#     cbar = plt.colorbar(ticks=ticks)
#     cbar.set_ticks(ticks)
#     cbar.set_ticklabels(tick_labels)
#     cbar.ax.tick_params(length=0)
#
#     # Add vertical line at longitude = -105
#     plt.axvline(x=-105, color='black', linestyle='--', linewidth=1)
#     plt.xticks(list(plt.xticks()[0]) + [-105])
#     plt.xlim(-130, -65)
#     plt.ylim(24, 50)
#     plt.tight_layout()
#     plt.grid(True)
#
#     # Ensure the directory exists
#     output_dir = rf"C:\Users\cheng\PycharmProjects\pythonProject\Categorized disaggregated REV\{SDC_str}"
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Save the plot
#     plt.savefig(rf"{output_dir}\{SDC_str}_Tv{i}.png", dpi=300)
#     plt.close()







################# To get SDC disaggregated categorized heatmaps (4 subgroups) ##################

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib import colors
#
# # ABCDE
# SDC_str = 'A'
#
# # ================= EAST =================
# file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#
# if 'latitude' in df_East.columns and 'longitude' in df_East.columns:
#     latitudes_East = df_East['latitude']
#     longitudes_East = df_East['longitude']
#     coordinates_East = list(zip(latitudes_East, longitudes_East))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ================= WEST =================
# file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#
# if 'latitude' in df_West.columns and 'longitude' in df_West.columns:
#     latitudes_West = df_West['latitude']
#     longitudes_West = df_West['longitude']
#     coordinates_West = list(zip(latitudes_West, longitudes_West))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ======= Remap Function =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 1.0:
#         return 0.75
#     elif val <= 1.5:
#         return 1.25
#     else:
#         return 1.75
#
# # ======= Color Map Setup =======
# boundaries = [0.0, 0.5, 1, 1.5, 2.25]
# ticks = [0.25, 0.75, 1.25, 1.875]
# tick_labels = [
#     r'$R_{E_{V}} \leq 0.5$',
#     r'$0.5 < R_{E_{V}} \leq 1.0$',
#     r'$1.0 < R_{E_{V}} \leq 1.5$',
#     r'$1.5 < R_{E_{V}}$'
# ]
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ================= Loop Through A_1 to A_8 =================
# for i in range(1, 9):
#     interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_East = pd.read_excel(interpolated_path_East)
#     averages_East_raw = df2_East.iloc[:, :].mean(axis=1).round(4)
#     averages_East = averages_East_raw.apply(remap_average)
#     combined_East = list(zip(coordinates_East, averages_East))
#
#     interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_West = pd.read_excel(interpolated_path_West)
#     averages_West_raw = df2_West.iloc[:, :].mean(axis=1).round(4)
#     averages_West = averages_West_raw.apply(remap_average)
#     combined_West = list(zip(coordinates_West, averages_West))
#
#     # Create the plot
#     plt.figure(figsize=(12, 6))
#
#     # Plot East
#     east_lats, east_lons = zip(*coordinates_East)
#     plt.scatter(east_lons, east_lats, c=averages_East, s=1, cmap=cmap, norm=norm)
#
#     # Plot West
#     west_lats, west_lons = zip(*coordinates_West)
#     plt.scatter(west_lons, west_lats, c=averages_West, s=1, cmap=cmap, norm=norm)
#
#     # Add labels and colorbar
#     plt.xlabel("Longitude")
#     plt.ylabel("Latitude")
#     cbar = plt.colorbar(ticks=ticks)
#     cbar.set_ticks(ticks)
#     cbar.set_ticklabels(tick_labels)
#     cbar.ax.tick_params(length=0)
#
#     # Add vertical line at longitude = -105
#     plt.axvline(x=-105, color='black', linestyle='--', linewidth=1)
#     plt.xticks(list(plt.xticks()[0]) + [-105])
#     plt.xlim(-130, -65)
#     plt.ylim(24, 50)
#     plt.tight_layout()
#     plt.grid(True)
#
#     # Ensure the directory exists
#     output_dir = rf"C:\Users\cheng\PycharmProjects\pythonProject\Generic disaggregated REV\{SDC_str}"
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Save the plot
#     plt.savefig(rf"{output_dir}\{SDC_str}_Tv{i}.png", dpi=300)
#     plt.close()


#
#
# ################# To get SDC at Los Angeles (34.05, -118.25) ##################
#
# # === Coordinate to search for ===
# target_lat = 34.05
# target_lon = -118.25
#
# # === Step 1: Find the row index of the target coordinate ===
# base_file_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_base = pd.read_excel(base_file_path, sheet_name='D')
#
# match = df_base[(df_base['latitude'] == target_lat) & (df_base['longitude'] == target_lon)]
#
# if match.empty:
#     print(f"No match found at ({target_lat}, {target_lon})")
# else:
#     row_index = match.index[0]
#     print(f"Match found at row index: {row_index}")
#
#     # === Step 2: Collect data from all interpolated files ===
#     periods_list = []
#     revs_list = []
#
#     for i in range(1, 9):
#         interp_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\D\interpolated_D_{i}.xlsx"
#         if not os.path.exists(interp_path):
#             continue
#
#         df_interp = pd.read_excel(interp_path)
#         if row_index >= len(df_interp):
#             continue
#
#         periods = df_interp.columns[:].astype(float)
#         rev_values = df_interp.iloc[row_index, :].values
#
#         periods_list.append(periods)
#         revs_list.append(rev_values)
#
#     # === Step 3: Merge and sort all data by period ===
#     all_periods = np.concatenate(periods_list).astype(float)
#     all_revs = np.concatenate(revs_list)
#     sort_idx = np.argsort(all_periods)
#     all_periods = all_periods[sort_idx]
#     all_revs = all_revs[sort_idx]
#
#     # === Step 4: Plot ===
#     plt.figure(figsize=(8, 6))
#     plt.plot(all_periods, all_revs, color='black')
#
#     # Draw and label vertical lines
#     tv_values = [0.05, 0.1, 0.2, 0.5, 1.0]
#     for tv in tv_values:
#         plt.axvline(x=tv, color='gray', linestyle='-', linewidth=0.5)
#         plt.text(tv, max(all_revs)*0.98, rf'$T_v = {tv}$', rotation=90,
#                  color='gray', ha='right', va='top', fontsize=9)
#
#     plt.xlim(0.01, 10)
#     plt.grid(axis='y')
#     plt.xscale('log')
#     # Bold axis labels
#     plt.xlabel("Period (s)", fontsize=14, fontweight='bold')
#     plt.ylabel(r"$\boldsymbol{R}_{\boldsymbol{E}_{\boldsymbol{v}}}$", fontsize=14)
#     plt.title(
#         r"$R_{E_{V}}$ Spectrum at Los Angeles (34.05$^{\circ}$N, 118.25$^{\circ}$W)",
#         fontsize=12)
#     plt.tight_layout()
#     # Save to PNG
#     output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\D\Los Angeles.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     plt.show()
#
#
#
# ################ To get SDC at Seattle (47.65, -122.35) ##################
#
#
# # === Coordinate to search for ===
# target_lat = 47.65
# target_lon = -122.35
#
# # === Step 1: Find the row index of the target coordinate ===
# base_file_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_base = pd.read_excel(base_file_path, sheet_name='D')
#
# match = df_base[(df_base['latitude'] == target_lat) & (df_base['longitude'] == target_lon)]
#
# if match.empty:
#     print(f"No match found at ({target_lat}, {target_lon})")
# else:
#     row_index = match.index[0]
#     print(f"Match found at row index: {row_index}")
#
#     # === Step 2: Collect data from all interpolated files ===
#     periods_list = []
#     revs_list = []
#
#     for i in range(1, 9):
#         interp_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\D\interpolated_D_{i}.xlsx"
#         if not os.path.exists(interp_path):
#             continue
#
#         df_interp = pd.read_excel(interp_path)
#         if row_index >= len(df_interp):
#             continue
#
#         periods = df_interp.columns[:].astype(float)
#         rev_values = df_interp.iloc[row_index, :].values
#
#         periods_list.append(periods)
#         revs_list.append(rev_values)
#
#     # === Step 3: Merge and sort all data by period ===
#     all_periods = np.concatenate(periods_list).astype(float)
#     all_revs = np.concatenate(revs_list)
#     sort_idx = np.argsort(all_periods)
#     all_periods = all_periods[sort_idx]
#     all_revs = all_revs[sort_idx]
#
#     # === Step 4: Plot ===
#     plt.figure(figsize=(8, 6))
#     plt.plot(all_periods, all_revs, color='black')
#
#     # Draw and label vertical lines
#     tv_values = [0.05, 0.1, 0.2, 0.5, 1.0]
#     for tv in tv_values:
#         plt.axvline(x=tv, color='gray', linestyle='-', linewidth=0.5)
#         plt.text(tv, max(all_revs)*0.98, rf'$T_v = {tv}$', rotation=90,
#                  color='gray', ha='right', va='top', fontsize=9)
#     # Draw horizontal REV lines
#
#     plt.xlim(0.01, 10)
#     plt.grid(axis='y')
#     plt.xscale('log')
#     # Bold axis labels
#     plt.xlabel("Period (s)", fontsize=14, fontweight='bold')
#     plt.ylabel(r"$\boldsymbol{R}_{\boldsymbol{E}_{\boldsymbol{v}}}$", fontsize=14)
#     plt.title(
#         r"$R_{E_{V}}$ Spectrum at Seattle (47.65$^{\circ}$N, 122.35$^{\circ}$W)",
#         fontsize=12)
#     plt.tight_layout()
#     output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\D\Seattle.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     plt.show()
#
#
#
#
# ################# To get SDC at Charleston (32.80, -79.95) ##################
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
#
# # === Coordinate to search for ===
# target_lat = 32.80
# target_lon = -79.95
#
# # === Step 1: Find the row index of the target coordinate ===
# base_file_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_base = pd.read_excel(base_file_path, sheet_name='D')
#
# match = df_base[(df_base['latitude'] == target_lat) & (df_base['longitude'] == target_lon)]
#
# if match.empty:
#     print(f"No match found at ({target_lat}, {target_lon})")
# else:
#     row_index = match.index[0]
#     print(f"Match found at row index: {row_index}")
#
#     # === Step 2: Collect data from all interpolated files ===
#     periods_list = []
#     revs_list = []
#
#     for i in range(1, 9):
#         interp_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\D\interpolated_D_{i}.xlsx"
#         if not os.path.exists(interp_path):
#             continue
#
#         df_interp = pd.read_excel(interp_path)
#         if row_index >= len(df_interp):
#             continue
#
#         periods = df_interp.columns[:].astype(float)
#         rev_values = df_interp.iloc[row_index, :].values
#
#         periods_list.append(periods)
#         revs_list.append(rev_values)
#
#     # === Step 3: Merge and sort all data by period ===
#     all_periods = np.concatenate(periods_list).astype(float)
#     all_revs = np.concatenate(revs_list)
#     sort_idx = np.argsort(all_periods)
#     all_periods = all_periods[sort_idx]
#     all_revs = all_revs[sort_idx]
#
#     # === Step 4: Plot ===
#     plt.figure(figsize=(8, 6))
#     plt.plot(all_periods, all_revs, color='black')
#
#     # Draw and label vertical lines
#     tv_values = [0.05, 0.1, 0.2, 0.5, 1.0]
#     for tv in tv_values:
#         plt.axvline(x=tv, color='gray', linestyle='-', linewidth=0.5)
#         plt.text(tv, max(all_revs)*0.98, rf'$T_v = {tv}$', rotation=90,
#                  color='gray', ha='right', va='top', fontsize=9)
#
#     plt.xlim(0.01, 10)
#     plt.xscale('log')
#     plt.grid(axis='y')
#     plt.xlabel("Period (s)", fontsize=14, fontweight='bold')
#     plt.ylabel(r"$\boldsymbol{R}_{\boldsymbol{E}_{\boldsymbol{v}}}$", fontsize=14)
#     plt.title(
#         r"$R_{E_{V}}$ Spectrum at Charleston (32.80$^{\circ}$N, 79.95$^{\circ}$W)",
#         fontsize=12)
#     plt.tight_layout()
#
#     # Save to PNG
#     output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\D\Charleston.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     plt.show()
#
#
#
#
#
#
#
# ################ To get SDC at St. Louis (36.60, -90.25) ##################
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
#
# # === Coordinate to search for ===
# target_lat = 36.60
# target_lon = -90.25
#
# # === Step 1: Find the row index of the target coordinate ===
# base_file_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_base = pd.read_excel(base_file_path, sheet_name='D')
#
# match = df_base[(df_base['latitude'] == target_lat) & (df_base['longitude'] == target_lon)]
#
# if match.empty:
#     print(f"No match found at ({target_lat}, {target_lon})")
# else:
#     row_index = match.index[0]
#     print(f"Match found at row index: {row_index}")
#
#     # === Step 2: Collect data from all interpolated files ===
#     periods_list = []
#     revs_list = []
#
#     for i in range(1, 9):
#         interp_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\D\interpolated_d_{i}.xlsx"
#         if not os.path.exists(interp_path):
#             continue
#
#         df_interp = pd.read_excel(interp_path)
#         if row_index >= len(df_interp):
#             continue
#
#         periods = df_interp.columns[:].astype(float)
#         rev_values = df_interp.iloc[row_index, :].values
#
#         periods_list.append(periods)
#         revs_list.append(rev_values)
#
#     # === Step 3: Merge and sort all data by period ===
#     all_periods = np.concatenate(periods_list).astype(float)
#     all_revs = np.concatenate(revs_list)
#     sort_idx = np.argsort(all_periods)
#     all_periods = all_periods[sort_idx]
#     all_revs = all_revs[sort_idx]
#
#     # === Step 4: Plot ===
#     plt.figure(figsize=(8, 6))
#     plt.plot(all_periods, all_revs, color='black')
#
#     # Draw and label vertical lines
#     tv_values = [0.05, 0.1, 0.2, 0.5, 1.0]
#     for tv in tv_values:
#         plt.axvline(x=tv, color='gray', linestyle='-', linewidth=0.5)
#         plt.text(tv, max(all_revs)*0.98, rf'$T_v = {tv}$', rotation=90,
#                  color='gray', ha='right', va='top', fontsize=9)
#     plt.xlim(0.01, 10)
#     plt.xscale('log')
#     plt.grid(axis='y')
#     plt.xlabel("Period (s)", fontsize=14, fontweight='bold')
#     plt.ylabel(r"$\boldsymbol{R}_{\boldsymbol{E}_{\boldsymbol{v}}}$", fontsize=14)
#     plt.title(
#         r"$R_{E_{V}}$ Spectrum at St. Louis (36.60$^{\circ}$N, 90.25$^{\circ}$W)",
#         fontsize=12)
#     plt.tight_layout()
#
#
#     # Save to PNG
#     output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\D\St. Louis.png"
#     plt.savefig(output_path, dpi=300, bbox_inches='tight')
#     plt.show()



################# To get SDC disaggregated categorized heatmaps (5 sungroups) (borders added) ##################

#
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib import colors
# import geopandas as gpd
# from shapely.geometry import box
#
# # ABCDE
# SDC_str = 'E'
#
# # ================= EAST =================
# file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
# df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#
# if 'latitude' in df_East.columns and 'longitude' in df_East.columns:
#     latitudes_East = df_East['latitude']
#     longitudes_East = df_East['longitude']
#     coordinates_East = list(zip(latitudes_East, longitudes_East))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ================= WEST =================
# file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#
# if 'latitude' in df_West.columns and 'longitude' in df_West.columns:
#     latitudes_West = df_West['latitude']
#     longitudes_West = df_West['longitude']
#     coordinates_West = list(zip(latitudes_West, longitudes_West))
# else:
#     print("The required columns 'Latitude' and 'Longitude' were not found.")
#
# # ======= Remap Function =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
# # ======= Color Map Setup =======
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [
#     r'$R_{E_{V}} \leq 0.5$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$0.8 < R_{E_{V}} \leq 1.2$',
#     r'$1.2 < R_{E_{V}} \leq 1.5$',
#     r'$1.5 < R_{E_{V}}$'
# ]
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ======= Load and Clip State Borders =======
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs("EPSG:4326")
# bbox = box(-130, 24, -65, 50)
# clipped_states = states[states.intersects(bbox)]
#
# # ================= Loop Through A_1 to A_8 =================
# for i in range(3, 5):
#     interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_East = pd.read_excel(interpolated_path_East)
#     averages_East_raw = df2_East.iloc[:, :].mean(axis=1).round(4)
#     averages_East = averages_East_raw.apply(remap_average)
#     combined_East = list(zip(coordinates_East, averages_East))
#
#     interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#     df2_West = pd.read_excel(interpolated_path_West)
#     averages_West_raw = df2_West.iloc[:, :].mean(axis=1).round(4)
#     averages_West = averages_West_raw.apply(remap_average)
#     combined_West = list(zip(coordinates_West, averages_West))
#
#     # Create the plot
#     plt.figure(figsize=(12, 6))
#
#     # Plot East
#     east_lats, east_lons = zip(*coordinates_East)
#     plt.scatter(east_lons, east_lats, c=averages_East, s=1, cmap=cmap, norm=norm)
#
#     # Plot West
#     west_lats, west_lons = zip(*coordinates_West)
#     plt.scatter(west_lons, west_lats, c=averages_West, s=1, cmap=cmap, norm=norm)
#
#     # Plot state borders
#     for geometry in clipped_states.geometry:
#         if geometry.geom_type == 'Polygon':
#             x, y = geometry.exterior.xy
#             plt.plot(x, y, color='grey', linewidth=0.5)
#         elif geometry.geom_type == 'MultiPolygon':
#             for poly in geometry.geoms:
#                 x, y = poly.exterior.xy
#                 plt.plot(x, y, color='grey', linewidth=0.5)
#
#     # Add state labels if SDC is 'E'
#     if SDC_str == 'E':
#         highlight_states = {'WA', 'OR', 'CA', 'NV',
#                             'MO', 'AR', 'TN', 'KY', 'IL'}
#         for _, row in clipped_states.iterrows():
#             abbrev = row['STUSPS']
#             if abbrev in highlight_states:
#                 centroid = row.geometry.centroid
#                 plt.text(
#                     centroid.x, centroid.y, abbrev,
#                     fontsize=8, color='lightblue',
#                     ha='center', va='center', fontweight='bold'
#                 )
#     elif SDC_str == 'D':
#         highlight_states = {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#                             'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC'}
#         for _, row in clipped_states.iterrows():
#             abbrev = row['STUSPS']
#             if abbrev in highlight_states:
#                 centroid = row.geometry.centroid
#                 plt.text(
#                     centroid.x, centroid.y, abbrev,
#                     fontsize=8, color='lightblue',
#                     ha='center', va='center', fontweight='bold'
#                 )
#     elif SDC_str == 'C':
#         highlight_states = {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#                             'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA', 'ME', 'NY'}
#         for _, row in clipped_states.iterrows():
#             abbrev = row['STUSPS']
#             if abbrev in highlight_states:
#                 centroid = row.geometry.centroid
#                 plt.text(
#                     centroid.x, centroid.y, abbrev,
#                     fontsize=8, color='lightblue',
#                     ha='center', va='center', fontweight='bold'
#                 )
#     elif SDC_str == 'B':
#         highlight_states = {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#                             'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA',
#                             'KS', 'NE', 'IA', 'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY',
#                             'CT', 'RI', 'MA', 'VT', 'NH', 'ME', 'MN'}
#         for _, row in clipped_states.iterrows():
#             abbrev = row['STUSPS']
#             if abbrev in highlight_states:
#                 centroid = row.geometry.centroid
#                 plt.text(
#                     centroid.x, centroid.y, abbrev,
#                     fontsize=8, color='lightblue',
#                     ha='center', va='center', fontweight='bold'
#                 )
#     elif SDC_str == 'A':
#         highlight_states = {'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX', 'SD', 'ND',
#                             'OK', 'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA',
#                             'KS', 'NE', 'IA', 'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY',
#                             'CT', 'RI', 'MA', 'VT', 'NH', 'ME', 'MN', 'MD'}
#         for _, row in clipped_states.iterrows():
#             abbrev = row['STUSPS']
#             if abbrev in highlight_states:
#                 centroid = row.geometry.centroid
#                 plt.text(
#                     centroid.x, centroid.y, abbrev,
#                     fontsize=8, color='lightblue',
#                     ha='center', va='center', fontweight='bold'
#                 )
#     # Add labels and colorbar
#
#     cbar = plt.colorbar(ticks=ticks)
#     cbar.set_ticks(ticks)
#     cbar.set_ticklabels(tick_labels)
#
#     cbar.ax.tick_params(labelsize=14)
#     plt.xlabel('Longitude', fontsize=14)  # Increase font size
#     plt.ylabel('Latitude', fontsize=14)
#     # Add vertical line at longitude = -105
#     plt.axvline(x=-105, color='black', linestyle='--', linewidth=1)
#     plt.xticks(list(plt.xticks()[0]) + [-105])
#     plt.xlim(-130, -65)
#     plt.ylim(24, 50)
#     plt.tight_layout()
#
#     # Ensure the directory exists
#     output_dir = rf"C:\Users\cheng\PycharmProjects\pythonProject\Categorized disaggregated REV with boarders_new\{SDC_str}"
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Save the plot
#     plt.savefig(rf"{output_dir}\{SDC_str}_Tv{i}.png", dpi=300)
#     plt.close()
#





################ To combine 3 colored grids (postprocessing) ##################

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import os
#
# # Load images
# img1 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\D_percentage_distribution_raw.png")
# img2 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\West_CA_included_fitting\D_percentage_distribution_fitted.png")
# img3 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\West_CA_included_fitting\D_fitting_error.png")
#
# img4 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\A_percentage_distribution_raw.png")
# img5 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\East_fitting\A_percentage_distribution_fitted.png")
# img6 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\East_fitting\A_fitting_error.png")
#
# # Crop margins: [top:bottom, left:right]
# def crop_image(img, top=20, bottom=20, left=20, right=20):
#     return img[top:img.shape[0]-bottom, left:img.shape[1]-right]
#
# img1 = crop_image(img1)
# img2 = crop_image(img2)
# img3 = crop_image(img3)
#
# img4 = crop_image(img4)
# img5 = crop_image(img5)
# img6 = crop_image(img6)
#
# # Create subplots
# fig, axes = plt.subplots(3, 2, figsize=(8.5, 9))
# axes = axes.T.flatten()
# for ax, img, label in zip(axes, [img1, img2, img3, img4, img5, img6], ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)']):
#     ax.imshow(img)
#     ax.axis('off')
#     ax.text(
#         0.01, 0.99, label,
#         transform=ax.transAxes,
#         fontsize=10,
#         fontname='Times New Roman',
#         va='top', ha='left',
#         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
#     )
#
# # Adjust spacing: negative wspace to tighten columns, zero hspace
# plt.subplots_adjust(hspace=0, wspace=-0.1)
#
# # Save to output directory
# output_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\model_subplots"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "combined_plot_cropped.png")
#
# plt.savefig(output_path, dpi=300, bbox_inches='tight')
# plt.show()



# ################# To get SDC disaggregated REV=1.0 distribution for averaged Tv ranges (entire US) ##################

# import geopandas as gpd
# from shapely.geometry import box, Point
# import pandas as pd
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# from pyproj import Transformer
#
# # ================= CONFIGURATION & SETUP =================
# SDC_list = ['A', 'B', 'C', 'D', 'E']
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
# # Publication Target Root Directory
# output_root = r"D:\MyPaper\Comparative Evaluation of Vertical Seismic Effect Methods in ASCE 7-22 for the Continental United States\submission\V3\ALL_SDCs"
# os.makedirs(output_root, exist_ok=True)
#
# # ================= MAP FEATURES (BORDERS) =================
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Bounding box safely covering the entire Conterminous US
# bbox_geom = box(-125, 24, -66, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states[clipped_states['STUSPS'] != 'DC']
#
# # Project states to Albers
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Setup transformer to convert from degrees to projected meters
# to_proj = Transformer.from_crs(geo_crs, target_crs, always_xy=True)
#
# # Define exact map limits in meters based on the plotted states
# bounds = clipped_states.total_bounds
# xmin, ymin, xmax, ymax = bounds[0], bounds[1], bounds[2], bounds[3]
#
# # Add layout padding adjustments
# x_pad = (xmax - xmin) * 0.05
# y_pad = (ymax - ymin) * 0.05
# xmin_map, xmax_map = xmin - x_pad, xmax + x_pad
# ymin_map, ymax_map = ymin - y_pad, ymax + y_pad
#
# # =====================================================
# #           LOOP THROUGH Tv = 3 TO 4
# # =====================================================
# for i in range(3, 5):
#     all_points_gpd = []  # List to store separate GeoDataFrames for plotting
#     label_added = False
#
#     print(f"\nTv{i}:")
#
#     # -------------------------------------------------
#     #          LOOP THROUGH SDC = A–E DATA FILTER
#     # -------------------------------------------------
#     for SDC_str in SDC_list:
#         try:
#             # ===== EAST =====
#             file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
#             df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#             df_East.columns = [c.lower() for c in df_East.columns]
#
#             if 'latitude' not in df_East.columns or 'longitude' not in df_East.columns:
#                 print(f"  SDC {SDC_str} East: Missing coordinates.")
#                 continue
#
#             interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#             df2_East = pd.read_excel(interpolated_path_East)
#             averages_East = df2_East.mean(axis=1).round(4)
#
#             # Mask out values within 0.999 and 1.001
#             east_mask = (averages_East >= 0.999) & (averages_East <= 1.001)
#             df_East_filtered = df_East[east_mask].copy()
#
#             # ===== WEST =====
#             file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
#             df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#             df_West.columns = [c.lower() for c in df_West.columns]
#
#             if 'latitude' not in df_West.columns or 'longitude' not in df_West.columns:
#                 print(f"  SDC {SDC_str} West: Missing coordinates.")
#                 continue
#
#             interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#             df2_West = pd.read_excel(interpolated_path_West)
#             averages_West = df2_West.mean(axis=1).round(4)
#
#             # Mask out values within 0.999 and 1.001
#             west_mask = (averages_West >= 0.999) & (averages_West <= 1.001)
#             df_West_filtered = df_West[west_mask].copy()
#
#             print(f"  SDC {SDC_str}: {len(df_East_filtered) + len(df_West_filtered)} site(s) "
#                   f"(East: {len(df_East_filtered)}, West: {len(df_West_filtered)})")
#
#             # Store the valid projected locations if any exist
#             if not df_East_filtered.empty:
#                 geom_e = [Point(xy) for xy in zip(df_East_filtered['longitude'], df_East_filtered['latitude'])]
#                 gdf_e = gpd.GeoDataFrame(df_East_filtered, geometry=geom_e, crs=geo_crs).to_crs(target_crs)
#                 all_points_gpd.append(gdf_e)
#
#             if not df_West_filtered.empty:
#                 geom_w = [Point(xy) for xy in zip(df_West_filtered['longitude'], df_West_filtered['latitude'])]
#                 gdf_w = gpd.GeoDataFrame(df_West_filtered, geometry=geom_w, crs=geo_crs).to_crs(target_crs)
#                 all_points_gpd.append(gdf_w)
#
#         except Exception as e:
#             print(f"Error filtering SDC {SDC_str} for Tv{i}: {e}")
#
#     # If absolutely no points matched across all SDCs, skip figure creation
#     if not all_points_gpd:
#         print(f"No target sites found for Tv{i}. Skipping plot.")
#         continue
#
#     # -------------------------------------------------
#     #                MAP LAYOUT BUILD
#     # -------------------------------------------------
#     fig, ax = plt.subplots(figsize=(13, 8))
#     ax.set_xlim(xmin_map, xmax_map)
#     ax.set_ylim(ymin_map, ymax_map)
#
#     # 1. Generate and Plot Target Latitudes (Horizontal Curves)
#     target_latitudes = np.arange(25, 51, 5)
#     for lat in target_latitudes:
#         lon_seq = np.linspace(-140, -50, 200)
#         lat_seq = np.full_like(lon_seq, lat)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_left = np.argmin(proj_x[valid])
#             lbl_y = proj_y[valid][idx_left]
#
#             # Increased padding to clean up boundary alignments for 14pt fonts
#             padding_lbl_x = (xmax_map - xmin_map) * 0.015
#             ax.text(xmin_map - padding_lbl_x, lbl_y, f"{lat}°N",
#                     va='center', ha='right', fontsize=14, color='black')
#
#     # 2. Generate and Plot Longitudes (Vertical Curves)
#     target_longitudes = np.arange(-125, -60, 5)
#     for lon in target_longitudes:
#         lat_seq = np.linspace(20, 55, 200)
#         lon_seq = np.full_like(lat_seq, lon)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_bottom = np.argmin(proj_y[valid])
#             lbl_x = proj_x[valid][idx_bottom]
#             lbl_y = proj_y[valid][idx_bottom]
#
#             # Increased padding to clean up boundary alignments for 14pt fonts
#             padding_lbl_y = (ymax_map - ymin_map) * 0.015
#             ax.text(lbl_x, ymin_map - padding_lbl_y, f"{abs(lon)}°W",
#                     va='top', ha='center', fontsize=14, color='black')
#
#     # 3. Generate and Plot the -105° Longitude Separation Curve
#     lat_seq_boundary = np.linspace(20, 55, 200)
#     lon_seq_boundary = np.full_like(lat_seq_boundary, -105)
#     b_x, b_y = to_proj.transform(lon_seq_boundary, lat_seq_boundary)
#     ax.plot(b_x, b_y, color='black', linestyle='-', linewidth=1.2, zorder=3)
#
#     # 4. Scatter Filtered Data Targets
#     for gdf_subset in all_points_gpd:
#         ax.scatter(
#             gdf_subset.geometry.x, gdf_subset.geometry.y,
#             color='green', s=12, marker='o',
#             label='~1.0' if not label_added else None, zorder=2
#         )
#         label_added = True
#
#     # 5. Plot state borders on top of markers
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=4)
#
#     # 6. Plot state labels (Font 14, Bold removed)
#     for _, row in clipped_states.iterrows():
#         centroid = row.geometry.representative_point()
#         ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=14,
#                 color='black', ha='center', va='center', zorder=5)
#
#     # Clean borders and setup layout legend
#     ax.set_xticks([])
#     ax.set_yticks([])
#     # Title removed completely
#
#     if label_added:
#         ax.legend(loc='lower left', frameon=True, prop={'size': 14})
#
#     plt.tight_layout()
#
#     # Save Output
#     save_path = os.path.join(output_root, f"ALL_Tv{i}_only_1pt.png")
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Saved: {save_path}")


#
# ################# To get all SDC heatmaps (5 sungroups) on 1 map ##################

# import geopandas as gpd
# from shapely.geometry import box, Point
# import pandas as pd
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from matplotlib import colors
# from matplotlib.lines import Line2D
# from pyproj import Transformer
#
# # ================= CONFIGURATION & SETUP =================
# SDC_list = ['A', 'B', 'C', 'D', 'E']
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
# # New output root path requested
# output_root = r"D:\MyPaper\Comparative Evaluation of Vertical Seismic Effect Methods in ASCE 7-22 for the Continental United States\submission\V3"
# os.makedirs(output_root, exist_ok=True)
#
#
# # ===== Remap Function =====
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# # ===== Color Map Setup =====
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [
#     r'$R_{E_{V}} \leq 0.5$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$0.8 < R_{E_{V}} \leq 1.2$',
#     r'$1.2 < R_{E_{V}} \leq 1.5$',
#     r'$1.5 < R_{E_{V}}$'
# ]
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ================= MAP FEATURES (BORDERS) =================
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Bounding box safely covering the entire Conterminous US
# bbox_geom = box(-125, 24, -66, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states[clipped_states['STUSPS'] != 'DC']
#
# # Project states to Albers
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Setup transformers to convert between meters and degrees back-and-forth
# to_proj = Transformer.from_crs(geo_crs, target_crs, always_xy=True)
#
# # Define exact map limits in meters based on the plotted states
# bounds = clipped_states.total_bounds
# xmin, ymin, xmax, ymax = bounds[0], bounds[1], bounds[2], bounds[3]
#
# # Add standard layout padding
# x_pad = (xmax - xmin) * 0.05
# y_pad = (ymax - ymin) * 0.05
# xmin_map, xmax_map = xmin - x_pad, xmax + x_pad
# ymin_map, ymax_map = ymin - y_pad, ymax + y_pad
#
# # =====================================================
# #           LOOP THROUGH Tv = 3 TO 4
# # =====================================================
# for i in range(3, 5):
#
#     fig, ax = plt.subplots(figsize=(13, 8))
#     ax.set_xlim(xmin_map, xmax_map)
#     ax.set_ylim(ymin_map, ymax_map)
#
#     scat = None  # To capture the plot reference for the colorbar
#
#     # 1. Generate and Plot Target Latitudes (Horizontal Curves)
#     target_latitudes = np.arange(25, 51, 5)
#     for lat in target_latitudes:
#         lon_seq = np.linspace(-140, -50, 200)
#         lat_seq = np.full_like(lon_seq, lat)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_left = np.argmin(proj_x[valid])
#             lbl_y = proj_y[valid][idx_left]
#
#             # Increased padding to accommodate larger 14pt text cleanly
#             padding_lbl_x = (xmax_map - xmin_map) * 0.015
#             ax.text(xmin_map - padding_lbl_x, lbl_y, f"{lat}°N",
#                     va='center', ha='right', fontsize=14, color='black')
#
#     # 2. Generate and Plot Longitudes (Vertical Curves)
#     target_longitudes = np.arange(-125, -60, 5)
#     for lon in target_longitudes:
#         lat_seq = np.linspace(20, 55, 200)
#         lon_seq = np.full_like(lat_seq, lon)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_bottom = np.argmin(proj_y[valid])
#             lbl_x = proj_x[valid][idx_bottom]
#             lbl_y = proj_y[valid][idx_bottom]
#
#             # Increased padding to accommodate larger 14pt text cleanly
#             padding_lbl_y = (ymax_map - ymin_map) * 0.015
#             ax.text(lbl_x, ymin_map - padding_lbl_y, f"{abs(lon)}°W",
#                     va='top', ha='center', fontsize=14, color='black')
#
#     # 3. Generate and Plot the -105° Longitude Separation Boundary
#     lat_seq_boundary = np.linspace(20, 55, 200)
#     lon_seq_boundary = np.full_like(lat_seq_boundary, -105)
#     b_x, b_y = to_proj.transform(lon_seq_boundary, lat_seq_boundary)
#     ax.plot(b_x, b_y, color='black', linestyle='-', linewidth=1.2, zorder=3, label='-105° Boundary')
#
#     # -------------------------------------------------
#     #          LOOP THROUGH SDC = A–E
#     # -------------------------------------------------
#     for SDC_str in SDC_list:
#         try:
#             # ---------- EAST OF -105 ----------
#             file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
#             df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#             df_East.columns = [c.lower() for c in df_East.columns]
#
#             geometry_east = [Point(xy) for xy in zip(df_East['longitude'], df_East['latitude'])]
#             gdf_east = gpd.GeoDataFrame(df_East, geometry=geometry_east, crs=geo_crs).to_crs(target_crs)
#
#             interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#             df2_East = pd.read_excel(interpolated_path_East)
#             averages_East = df2_East.mean(axis=1).apply(remap_average)
#
#             scat = ax.scatter(
#                 gdf_east.geometry.x, gdf_east.geometry.y,
#                 c=averages_East, s=1.5, cmap=cmap, norm=norm, zorder=2
#             )
#
#             # ---------- AT OR WEST OF -105 ----------
#             file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
#             df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#             df_West.columns = [c.lower() for c in df_West.columns]
#
#             geometry_west = [Point(xy) for xy in zip(df_West['longitude'], df_West['latitude'])]
#             gdf_west = gpd.GeoDataFrame(df_West, geometry=geometry_west, crs=geo_crs).to_crs(target_crs)
#
#             interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#             df2_West = pd.read_excel(interpolated_path_West)
#             averages_West = df2_West.mean(axis=1).apply(remap_average)
#
#             scat = ax.scatter(
#                 gdf_west.geometry.x, gdf_west.geometry.y,
#                 c=averages_West, s=1.5, cmap=cmap, norm=norm, zorder=2
#             )
#         except Exception as e:
#             print(f"Error handling SDC {SDC_str} for Step Tv{i}: {e}")
#
#     # 4. Plot state boundaries on top of data points
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=4)
#
#     # 5. Plot state text labels (Font 14, Bold removed)
#     for _, row in clipped_states.iterrows():
#         centroid = row.geometry.representative_point()
#         ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=14,
#                 color='black', ha='center', va='center', zorder=5)
#
#     # 6. Discrete Bounds Colorbar
#     if scat is not None:
#         cbar = fig.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#         cbar.set_ticklabels(tick_labels)
#         cbar.ax.tick_params(labelsize=14)  # Adjusted colorbar font to 14pt
#
#     # Frame cleanup
#     ax.set_xticks([])
#     ax.set_yticks([])
#     ax.set_title(f'Continental US Distribution of $R_{{E_{{V}}}}$ (Step Tv{i})', fontsize=14, pad=20)
#     plt.tight_layout()
#
#     # Save Layout Output directly to your paper folder path
#     save_path = os.path.join(output_root, f"ALL_SDC_Tv{i}.png")
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully generated and saved: {save_path}")




################ To get REV at Major Cities (postprocessing) ##################


# ################ 4 city rev spectra on 1 figure ##################

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
#
#
# # ------------------------------
# # Helper function to load REV curve for a given city
# # ------------------------------
# def get_rev_curve(base_file_path, interp_dir, target_lat, target_lon):
#     df_base = pd.read_excel(base_file_path, sheet_name='D')
#     match = df_base[(df_base['latitude'] == target_lat) & (df_base['longitude'] == target_lon)]
#
#     if match.empty:
#         print(f"No match found at ({target_lat}, {target_lon})")
#         return None, None
#
#     row_index = match.index[0]
#     print(f"Match found at row index: {row_index}")
#
#     periods_list, revs_list = [], []
#
#     for i in range(1, 9):
#         interp_path = rf"{interp_dir}\interpolated_D_{i}.xlsx"
#         if not os.path.exists(interp_path):
#             continue
#
#         df_interp = pd.read_excel(interp_path)
#         if row_index >= len(df_interp):
#             continue
#
#         periods = df_interp.columns[:].astype(float)
#         revs = df_interp.iloc[row_index, :].values
#
#         periods_list.append(periods)
#         revs_list.append(revs)
#
#     if not periods_list:
#         return None, None
#
#     all_periods = np.concatenate(periods_list).astype(float)
#     all_revs = np.concatenate(revs_list)
#     idx = np.argsort(all_periods)
#
#     return all_periods[idx], all_revs[idx]
#
#
# # ------------------------------
# # Paths & City Definitions
# # ------------------------------
# west_base_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
# east_base_path = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
#
# city_list = [
#     ("Los Angeles", 34.05, -118.25, west_base_path,
#      r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\D"),
#
#     ("Seattle", 47.65, -122.35, west_base_path,
#      r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\D"),
#
#     ("Charleston", 32.80, -79.95, east_base_path,
#      r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\D"),
#
#     ("St. Louis", 36.60, -90.25, east_base_path,
#      r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\D"),
# ]
#
# # ------------------------------
# # Plot all cities
# # ------------------------------
# plt.figure(figsize=(9, 7))
# colors = [
#     "purple",      # Los Angeles
#     "red",         # Seattle
#     "skyblue",     # Charleston (light blue)
#     "lightgreen"   # St. Louis (light green)
# ]
#
# for (city, lat, lon, base_path, interp_dir), color in zip(city_list, colors):
#     periods, revs = get_rev_curve(base_path, interp_dir, lat, lon)
#     if periods is not None:
#         plt.plot(periods, revs, label=city, linewidth=1.8, color=color)
#
# # Vertical reference lines
# for tv in [0.05, 0.1, 0.2, 0.5, 1.0]:
#     plt.axvline(x=tv, color='gray', linestyle='--', linewidth=0.6)
#
# plt.xlim(0.01, 10)
# plt.xscale('log')
# plt.xlabel("Period (s)", fontsize=16)
# plt.ylabel(r"$R_{E_{V}}$", fontsize=16)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# plt.grid(axis='y', linestyle='--', linewidth=0.5)
# plt.legend(fontsize=13)
# plt.tight_layout()
#
# # Save to PNG
# output_path = r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\crop_title\D\All_Cities_REV.png"
# plt.savefig(output_path, dpi=300, bbox_inches='tight')
#
# plt.show()

# ################ To combine 4 major city REV spectra ##################
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import os
#
# # Load images
# img1 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\crop_title\D\Seattle_1.png")
# img3 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\crop_title\D\Los Angeles_1.png")
# img2 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\crop_title\D\St. Louis_1.png")
# img4 = mpimg.imread(r"C:\Users\cheng\PycharmProjects\pythonProject\Major cities\crop_title\D\Charleston_1.png")
#
# # Crop margins function (if needed)
# def crop_image(img, top=0, bottom=0, left=0, right=0):
#     return img[top:img.shape[0]-bottom, left:img.shape[1]-right]
#
# img1 = crop_image(img1)
# img2 = crop_image(img2)
# img3 = crop_image(img3)
# img4 = crop_image(img4)
#
# # Create figure and axes
# fig, axes = plt.subplots(2, 2, figsize=(9, 9))
# axes = axes.T.flatten()  # transpose and flatten for custom order
#
# # Plot images and remove axes
# for ax, img in zip(axes, [img1, img2, img3, img4]):
#     ax.imshow(img)
#     ax.axis('off')
#
# # Tighten subplot spacing
# plt.subplots_adjust(hspace=-0.4, wspace=0.1)
#
# # Labels to place outside upper-left corner of each subplot
# labels = ['(a)', '(c)', '(b)', '(d)']
#
# for ax, label in zip(axes, labels):
#     pos = ax.get_position()
#     fig.text(
#         pos.x0 - 0.01,  # a little left of the axes
#         pos.y1 - 0.02,  # a little above the axes
#         label,
#         fontsize=10,
#         fontname='Times New Roman',
#         ha='left',
#         va='bottom',
#         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2')
#     )
#
# # Create output directory if not exists
# output_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\model_subplots"
# os.makedirs(output_dir, exist_ok=True)
# output_path = os.path.join(output_dir, "combined_REV_spectra_cropped_1.png")
#
# # Save and show
# plt.savefig(output_path, dpi=300, bbox_inches='tight')
# plt.show()




# ################ CEUS data scrapping ##################
#
# import pandas as pd
# import requests
# import os
#
# file_path = r"C:\Users\cheng\PycharmProjects\pythonProject\lat_long_CEUS.xlsx"
# base_output_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
#
# # Specify the row range 207370
# start_row = 206001
# end_row = 208000
#
# # List of all soil classes to iterate through
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# # Load the base coordinate data
# df = pd.read_excel(file_path, usecols=["Latitude", "Longitude"], skiprows=range(1, start_row),
#                    nrows=(end_row - start_row + 1))
#
# # Loop through each soil class
# for soil_class in soil_classes:
#     print(f"\n--- Processing Soil Class: {soil_class} ---")
#
#     # Create subfolder if it doesn't exist
#     class_dir = os.path.join(base_output_dir, soil_class)
#     if not os.path.exists(class_dir):
#         os.makedirs(class_dir)
#
#     response_data_list = []
#     failed_attempts = []
#
#     # Loop through all rows in the DataFrame for the current soil class
#     for i in range(len(df)):
#         lat = df.iloc[i]["Latitude"]
#         long = df.iloc[i]["Longitude"]
#         risk_category = "II"
#
#         # Construct the URL dynamically (using the loop's current soil_class)
#         url = f'https://ascehazardtool.org/proxy/proxy.ashx?https://earthquake.usgs.gov/ws/designmaps/nehrp-2020.json?latitude={lat}&longitude={long}&referenceDocument=ASCE7-22&riskCategory={risk_category}&siteClass={soil_class}&title=ASCE'
#
#         print(url)
#
#         headers = {
#             "Cookie": "_ga=GA1.1.373760250.1739330404; cookieconsent_status=dismiss; _ga_NL845079TW=GS1.1.1739501292.4.0.1739501326.0.0.0",
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Referer": "https://ascehazardtool.org/"
#         }
#
#         try:
#             resp = requests.get(url, headers=headers)
#
#             if resp.status_code == 200:
#                 print(f"Request successful. Status Code: {resp.status_code}")
#                 data = resp.json()
#
#                 response_imput = data.get('request', {}).get('parameters', {})
#                 response_data = data.get('response', {}).get('data', {})
#
#                 if response_data:
#                     limited_response_imput = dict(list(response_imput.items())[:4])
#                     if 'siteClass' in limited_response_imput:
#                         limited_response_imput['siteClass'] = soil_class
#
#                     limited_response_data = dict(list(response_data.items())[:12])
#                     combined_data = {**limited_response_imput, **limited_response_data}
#                     response_data_list.append(combined_data)
#                 else:
#                     print(f"No response data for Lat={lat}, Long={long}")
#             else:
#                 raise ValueError(f"Status Code {resp.status_code}")
#
#         except Exception as e:
#             print(f"Failed to retrieve/parse: {e}")
#             failed_attempts.append((lat, long, soil_class))
#
#             nan_row = {
#                 "latitude": lat,
#                 "longitude": long,
#                 "siteClass": soil_class,
#                 "riskCategory": risk_category
#             }
#             for _ in range(12):
#                 nan_row[f"data_{_ + 1}"] = float('nan')
#             response_data_list.append(nan_row)
#
#     # Save Success Results for this Soil Class
#     if response_data_list:
#         df_response_data = pd.DataFrame(response_data_list)
#         output_file = os.path.join(class_dir, f'response_data_{start_row}-{end_row}.xlsx')
#         df_response_data.to_excel(output_file, index=False)
#         print(f"Saved: {output_file}")
#
#     # Save Failed Results for this Soil Class
#     if failed_attempts:
#         failed_df = pd.DataFrame(failed_attempts, columns=["Latitude", "Longitude", "Soil_Class"])
#         failed_output_path = os.path.join(class_dir, f"failed_attempts_{start_row}-{end_row}.xlsx")
#         failed_df.to_excel(failed_output_path, index=False)



# ################ CEUS data scrapping recovering failed attempts ##################

# import pandas as pd
# import requests
# import os
#
# # Base directory
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# for soil_class in soil_classes:
#     class_dir = os.path.join(base_dir, soil_class)
#
#     if not os.path.exists(class_dir):
#         continue
#
#     # Find all failed_attempts files in this specific subfolder
#     failed_files = [f for f in os.listdir(class_dir) if f.startswith("failed_attempts") and f.endswith(".xlsx")]
#
#     for file_name in failed_files:
#         failed_file_path = os.path.join(class_dir, file_name)
#         print(f"\n--- Processing: {failed_file_path} ---")
#
#         df_failed = pd.read_excel(failed_file_path)
#         recovered_data_list = []
#         still_failed = []
#
#         for i in range(len(df_failed)):
#             lat = df_failed.iloc[i]["Latitude"]
#             long = df_failed.iloc[i]["Longitude"]
#             # Pulling Soil_Class directly from the file to ensure API accuracy
#             current_soil = df_failed.iloc[i]["Soil_Class"]
#             risk_category = "II"
#
#             url = f'https://ascehazardtool.org/proxy/proxy.ashx?https://earthquake.usgs.gov/ws/designmaps/nehrp-2020.json?latitude={lat}&longitude={long}&referenceDocument=ASCE7-22&riskCategory={risk_category}&siteClass={current_soil}&title=ASCE'
#
#             headers = {
#                 "Cookie": "_ga=GA1.1.373760250.1739330404; cookieconsent_status=dismiss; _ga_NL845079TW=GS1.1.1739501292.4.0.1739501326.0.0.0",
#                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
#                 "Accept-Language": "en-US,en;q=0.5",
#                 "Referer": "https://ascehazardtool.org/"
#             }
#
#             try:
#                 # 20 second timeout to handle slow ASCE proxy responses
#                 resp = requests.get(url, headers=headers, timeout=20)
#
#                 if resp.status_code == 200:
#                     data = resp.json()
#                     response_imput = data.get('request', {}).get('parameters', {})
#                     response_data = data.get('response', {}).get('data', {})
#
#                     if response_data:
#                         limited_input = dict(list(response_imput.items())[:4])
#                         if 'siteClass' in limited_input:
#                             limited_input['siteClass'] = current_soil
#
#                         limited_data = dict(list(response_data.items())[:12])
#                         combined_data = {**limited_input, **limited_data}
#                         recovered_data_list.append(combined_data)
#                         print(f"Success: {current_soil} | Lat {lat}, Long {long}")
#                     else:
#                         still_failed.append(df_failed.iloc[i])
#                 else:
#                     still_failed.append(df_failed.iloc[i])
#                     print(f"Status {resp.status_code} for Lat {lat}")
#
#             except Exception as e:
#                 print(f"Error: {e}")
#                 still_failed.append(df_failed.iloc[i])
#
#         # Save recovered data with a unique name based on the original range
#         if recovered_data_list:
#             range_info = file_name.replace("failed_attempts_", "")
#             recovered_path = os.path.join(class_dir, f"recovered_{range_info}")
#             pd.DataFrame(recovered_data_list).to_excel(recovered_path, index=False)
#             print(f"Saved recovered data to {recovered_path}")
#
#         # Overwrite the specific failed file with ONLY the ones that failed again
#         if still_failed:
#             pd.DataFrame(still_failed).to_excel(failed_file_path, index=False)
#             print(f"Updated {file_name} with remaining failures.")
#         else:
#             os.remove(failed_file_path)
#             print(f"All records recovered. Deleted {file_name}")



################## To Concatenate the Output Files ##################


# # Set the directory containing your Excel files
#
# directory = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\A"
#
# # Optional: Filter by specific sheet name (set to None to use the first sheet)
# sheet_name = 'Sheet1'
#
# # List to store dataframes
# excel_data = []
#
# # Loop through all files in the directory
# for filename in os.listdir(directory):
#     if filename.endswith(".xlsx") or filename.endswith(".xls"):
#         file_path = os.path.join(directory, filename)
#         try:
#             df = pd.read_excel(file_path, sheet_name=sheet_name)
#             excel_data.append(df)
#         except Exception as e:
#             print(f"Failed to read {filename}: {e}")
#
# # Concatenate all dataframes
# if excel_data:
#     combined_df = pd.concat(excel_data, ignore_index=True)
#     # Optionally, save to a new Excel file
#     combined_df.to_excel('combined_output.xlsx', index=False)
#     print("Successfully combined all Excel files.")
# else:
#     print("No Excel files found or read.")
#



################ To concatenate all scrapped data per site class ##################

# import pandas as pd
# import os
#
# # Base directory where all soil folders live
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# for soil_class in soil_classes:
#     class_dir = os.path.join(base_dir, soil_class)
#
#     if not os.path.exists(class_dir):
#         print(f"Skipping {soil_class}: Folder not found.")
#         continue
#
#     excel_data = []
#     print(f"Combining files in: {class_dir}")
#
#     # Loop through all files in the soil class directory
#     for filename in os.listdir(class_dir):
#         # Only grab the actual data files, skip any "failed_attempts" if they still exist
#         if (filename.endswith(".xlsx") or filename.endswith(".xls")) and "failed" not in filename:
#             file_path = os.path.join(class_dir, filename)
#             try:
#                 # Note: No need to specify sheet_name if it's the first sheet
#                 df = pd.read_excel(file_path)
#                 excel_data.append(df)
#             except Exception as e:
#                 print(f"   Error reading {filename}: {e}")
#
#     # Concatenate and save inside the main CEUS folder
#     if excel_data:
#         combined_df = pd.concat(excel_data, ignore_index=True)
#         output_name = os.path.join(base_dir, f"combined_{soil_class}.xlsx")
#         combined_df.to_excel(output_name, index=False)
#         print(f"--> Successfully created: {output_name}")
#     else:
#         print(f"   No valid data files found for Class {soil_class}.")
#
# print("\nAll soil classes processed!")




################ To Get cv ##################

# import pandas as pd
# import numpy as np
# import os
#
# # Base directory
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# # Define Table 11.9-1 Data (Sorted x-axis for np.interp)
# Sms_x = np.array([0.2, 0.3, 0.6, 1.0, 2.0])
#
# cv_map = {
#     'A_B': np.array([0.7, 0.8, 0.9, 0.9, 0.9]),
#     'BC': np.array([0.7, 0.8, 0.95, 1.0, 1.1]),
#     'C': np.array([0.7, 0.8, 1.0, 1.1, 1.3]),
#     'CD': np.array([0.7, 0.85, 1.05, 1.2, 1.4]),
#     'D_DE_E': np.array([0.7, 0.9, 1.1, 1.3, 1.5])
# }
#
#
# def calculate_cv(row):
#     sms = row['sms']
#     # Ensure siteClass is a string and handle potential NaNs
#     sc = str(row['siteClass']).upper() if pd.notnull(row['siteClass']) else 'D'
#
#     if sc in ['A', 'B']:
#         y_vals = cv_map['A_B']
#     elif sc == 'BC':
#         y_vals = cv_map['BC']
#     elif sc == 'C':
#         y_vals = cv_map['C']
#     elif sc == 'CD':
#         y_vals = cv_map['CD']
#     else:
#         y_vals = cv_map['D_DE_E']
#
#     # Linear interpolation with automatic capping at endpoints
#     return round(np.interp(sms, Sms_x, y_vals), 2)
#
#
# # Loop through each soil class
# for sc_name in soil_classes:
#     input_filename = f"combined_{sc_name}.xlsx"
#     input_path = os.path.join(base_dir, input_filename)
#     output_path = os.path.join(base_dir, f"combined_{sc_name}_cv_added.xlsx")
#
#     if not os.path.exists(input_path):
#         print(f"Skipping: {input_filename} not found.")
#         continue
#
#     print(f"Processing {input_filename}...")
#
#     # Load the data
#     df = pd.read_excel(input_path)
#
#     # 1. Period calculations (T0 and Ts)
#     # Check if columns exist to avoid KeyErrors
#     if 'sd1' in df.columns and 'sds' in df.columns:
#         df['t0'] = 0.2 * df['sd1'] / df['sds']
#         df['ts'] = df['sd1'] / df['sds']
#     else:
#         print(f"   Warning: 'sd1' or 'sds' missing in {input_filename}. Skipping periods.")
#
#     # 2. Vertical Coefficient (Cv) calculation
#     if 'sms' in df.columns and 'siteClass' in df.columns:
#         df['cv'] = df.apply(calculate_cv, axis=1)
#     else:
#         print(f"   Warning: 'sms' or 'siteClass' missing in {input_filename}. Skipping Cv.")
#
#     # 3. Save the updated file
#     df.to_excel(output_path, index=False)
#     print(f"   --> Saved to: {os.path.basename(output_path)}")
#
# print("\nAll soil classes processed successfully!")



################ To Get ratios ##################

# import pandas as pd
# import numpy as np
# import os
# from math import sqrt
#
# # Base directory matching your pattern
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# # The spectrum periods defined in your code
# reduced_T = [0.0, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0,
#              5.0, 7.5, 10]
#
# for sc_name in soil_classes:
#     # Match the specific "cv_added" file pattern
#     file_name = f"combined_{sc_name}_cv_added.xlsx"
#     file_path = os.path.join(base_dir, file_name)
#
#     if not os.path.exists(file_path):
#         print(f"Skipping: {file_name} not found in {base_dir}")
#         continue
#
#     print(f"Processing Spectra for Soil Class {sc_name}...")
#
#     # Read the Excel file
#     df = pd.read_excel(file_path)
#
#     Sa_list = []
#     Sav_list = []
#     Ratio_list = []
#
#     for i in range(len(df)):
#         row = df.iloc[i]
#         lat = row['latitude']
#         lon = row['longitude']
#         riskCategory = row['riskCategory']
#         siteClass = row['siteClass']
#         cv = row['cv']
#         sds = row['sds']
#         sd1 = row['sd1']
#         t0 = row['t0']
#         ts = row['ts']
#         tl = row['tl']
#         # Use .get to safely handle potential missing SDC column
#         sdc = row.get('sdc', row.get('SDC', 'N/A'))
#
#         Sa_row = []
#         Sav_row = []
#         Ratio_row = []
#
#         for T_raw in reduced_T:
#             T = round(T_raw, 3)
#
#             # --- 1. Horizontal Sa (ASCE 7-22 11.4.5.2) ---
#             if T < t0:
#                 sa_value = sds * (0.4 + 0.6 * T / t0) if t0 != 0 else sds
#             elif T <= ts:
#                 sa_value = sds
#             elif T <= tl:
#                 sa_value = sd1 / T if T != 0 else sds
#             else:
#                 sa_value = (tl * sd1) / (T ** 2)
#
#             saM_value = 1.5 * sa_value
#
#             # --- 2. Vertical SaMv (ASCE 7-22 Section 11.9) ---
#             # Condition for CEUS vs WUS based on Longitude
#             if float(lon) > -105:
#                 saMv_value = (2 / 3) * saM_value
#             else:
#                 # Fmd calculation for Western US
#                 if T <= 0.2:
#                     Fmd = 1.2
#                 elif T <= 1.0:
#                     Fmd = 1.2 + 0.0625 * (T - 0.2)
#                 else:
#                     Fmd = 1.25 + 0.05 * (T - 1.0) / 9.0
#
#                 # Vertical Spectrum Shape logic
#                 if T <= 0.025:
#                     saMv_value = 0.65 * cv * saM_value / Fmd
#                 elif T <= 0.05:
#                     saMv_value = (16 * cv * saM_value / Fmd * (T - 0.025)) + (0.65 * cv * saM_value / Fmd)
#                 elif T <= 0.1:
#                     saMv_value = 1.05 * cv * saM_value / Fmd
#                 elif T <= 2.0:
#                     # Added safety for T=0 in sqrt
#                     sqrt_factor = sqrt(0.1 / T) if T > 0 else 1.0
#                     saMv_value = max(1.05 * cv * (saM_value / Fmd * sqrt_factor), 0.5 * saM_value / Fmd)
#                 else:
#                     saMv_value = 0.5 * saM_value / Fmd
#
#             Sav_value = (2 / 3) * saMv_value
#
#             # Ratio calculation (0.3*Sav / 0.2*Sds)
#             # Added sds check to prevent division by zero
#             ratio = (0.3 * Sav_value) / (0.2 * sds) if sds > 0 else 0
#
#             Sa_row.append(sa_value)
#             Sav_row.append(Sav_value)
#             Ratio_row.append(ratio)
#
#         # Prepare base metadata for the rows
#         meta = {
#             'latitude': lat, 'longitude': lon, 'riskCategory': riskCategory,
#             'siteClass': siteClass, 'SDC': sdc, 'cv': cv, 'sds': sds,
#             'sd1': sd1, 't0': t0, 'ts': ts, 'tl': tl
#         }
#
#         # Horizontal Data
#         Sa_data = meta.copy()
#         Sa_data.update({f'{round(reduced_T[j], 3)}': Sa_row[j] for j in range(len(Sa_row))})
#         Sa_list.append(Sa_data)
#
#         # Vertical Data
#         Sav_data = {'latitude': lat, 'longitude': lon, 'siteClass': siteClass, 'SDC': sdc}
#         Sav_data.update({f'{round(reduced_T[j], 3)}': Sav_row[j] for j in range(len(Sav_row))})
#         Sav_list.append(Sav_data)
#
#         # Ratio Data
#         Ratio_data = {'latitude': lat, 'longitude': lon, 'siteClass': siteClass, 'SDC': sdc}
#         Ratio_data.update({f'{round(reduced_T[j], 3)}': Ratio_row[j] for j in range(len(Ratio_row))})
#         Ratio_list.append(Ratio_data)
#
#     # Save to Excel with three sheets
#     output_path = os.path.join(base_dir, f"Spectra_{sc_name}_H_V_Ratio.xlsx")
#     with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
#         pd.DataFrame(Sa_list).to_excel(writer, index=False, sheet_name='H')
#         pd.DataFrame(Sav_list).to_excel(writer, index=False, sheet_name='V')
#         pd.DataFrame(Ratio_list).to_excel(writer, index=False, sheet_name='Ratio')
#
#     print(f"   --> Created: {output_path}")
#
# print("\nDone! All soil class spectra have been generated.")



################# To get ratios by SDC ##################

# import pandas as pd
# import os
#
# # Base directory
# base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS"
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
#
# for sc_name in soil_classes:
#     input_file = f"Spectra_{sc_name}_H_V_Ratio.xlsx"
#     input_path = os.path.join(base_dir, input_file)
#
#     output_file = f"Final_Grouped_{sc_name}.xlsx"
#     output_path = os.path.join(base_dir, output_file)
#
#     if not os.path.exists(input_path):
#         print(f"Skipping: {input_file} not found.")
#         continue
#
#     print(f"Processing {sc_name} (Ratio sheet only)...")
#
#     # Load only the 'Ratio' sheet from the input
#     try:
#         df_ratio = pd.read_excel(input_path, sheet_name='Ratio')
#     except Exception as e:
#         print(f"   Error: Could not find 'Ratio' sheet in {input_file}: {e}")
#         continue
#
#     # Identify the unique SDC categories (A, B, C, D, etc.)
#     # We dropna() to ensure we don't try to create a sheet named 'nan'
#     sdc_categories = df_ratio['SDC'].dropna().unique()
#
#     with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
#         # 1. Save the full Ratio data as the first sheet
#         df_ratio.to_excel(writer, sheet_name='Ratio_All', index=False)
#
#         # 2. Loop through each SDC and create a filtered sheet from the Ratio data
#         for sdc in sdc_categories:
#             df_sdc_filtered = df_ratio[df_ratio['SDC'] == sdc]
#
#             # Sheet names must be <= 31 characters
#             sheet_name = f"Ratio_SDC_{sdc}"
#
#             if not df_sdc_filtered.empty:
#                 df_sdc_filtered.to_excel(writer, sheet_name=sheet_name[:31], index=False)
#                 print(f"   Added sheet: {sheet_name}")
#
#     print(f"--> Finished: {output_file}")
#
# print("\nAll files reorganized successfully.")



################# To get the probability distribution (slice) ##################

#
# import pandas as pd
# import numpy as np
# import os
# from scipy.interpolate import interp1d
#
# # Base directory for CEUS
# base_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS'
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
# sdc = 'E' # Targeting Seismic Design Category A
#
# for sc in soil_classes:
#     # Set the input and output file paths
#     input_file = os.path.join(base_dir, f'Final_Grouped_{sc}.xlsx')
#     # Output name reflects the SDC and the specific slice (1)
#     output_file = os.path.join(base_dir, f'interpolated_results', sc, f'interpolated_sc_{sc}_sdc_{sdc}_8.xlsx')
#
#     if not os.path.exists(input_file):
#         print(f"Skipping {sc}: File not found.")
#         continue
#
#     print(f"Interpolating Soil Class {sc} for SDC {sdc}...")
#
#     try:
#         # Load the specific SDC sheet
#         df = pd.read_excel(input_file, sheet_name=f'Ratio_SDC_{sdc}', header=None)
#     except Exception as e:
#         print(f"   Warning: Could not find sheet 'Ratio_SDC_{sdc}' in {sc}. Skipping.")
#         continue
#
#     # --- EXACTLY YOUR SCRIPT START ---
#     # Extract the first row
#     first_row = df.iloc[[0]]
#
#     # Filter the rest of the DataFrame based on longitude (CEUS: > -105)
#     filtered_rows = df.iloc[1:]
#     filtered_rows = filtered_rows[(filtered_rows.iloc[:, 1] > -105)]
#
#     # Concatenate the first row with the filtered rows
#     df = pd.concat([first_row, filtered_rows], ignore_index=True)
#
#     # Filter the DataFrame
#     # ## df_filtered = df.iloc[:, 4:8]
#     # ## df_filtered = df.iloc[:, 6:9]
#     # ## df_filtered = df.iloc[:, 8:11]
#     # ## df_filtered = df.iloc[:, 10:13]
#     # ## df_filtered = df.iloc[:, 12:17]
#     # ## df_filtered = df.iloc[:, 16:19]
#     # ## df_filtered = df.iloc[:, 18:21]
#     # ## df_filtered = df.iloc[:, 20:26]
#     # Filter the DataFrame for the first slice (columns 4 to 8)
#     df_filtered = df.iloc[:, 20:26]
#
#     # Extract x and y data
#     x = df_filtered.iloc[0].astype(float).values
#     y_data = df_filtered.iloc[1:].astype(float).values
#
#     # Check x is strictly increasing
#     if not np.all(np.diff(x) > 0):
#         raise ValueError(f"x must be strictly increasing for class {sc} SDC {sdc}.")
#
#
#     # Interpolate with 0.01 step
#     x_new = np.arange(x.min(), x.max() + 0.01, 0.01)
#     interpolated_rows = []
#     for row in y_data:
#         f = interp1d(x, row, kind='linear', bounds_error=False, fill_value="extrapolate")
#         interpolated_row = f(x_new)
#         interpolated_rows.append(interpolated_row)
#
#     interpolated_df = pd.DataFrame(interpolated_rows, columns=np.round(x_new, 3))
#
#     os.makedirs(os.path.dirname(output_file), exist_ok=True)
#     # Save with ZIP64 enabled
#     with pd.ExcelWriter(output_file, engine='xlsxwriter', engine_kwargs={'options': {'use_zip64': True}}) as writer:
#         interpolated_df.to_excel(writer, index=False)
#     # --- EXACTLY YOUR SCRIPT END ---
#
#     print(f"Successfully saved slice 1 for {sc} (SDC {sdc})")
#
# print("\nBatch processing for SDC A Slice 1 complete.")
#




################# To count points (raw data colored grids) ##################

# import pandas as pd
# import os
#
# # ======= Configuration =======
# SC_str = 'DE'  # Targeted Soil Class
# sdc_list = ['A', 'B', 'C', 'D', 'E']
# input_dir = rf'C:\Users\cheng\PycharmProjects\pythonProject\CEUS\interpolated_results\{SC_str}'
# output_root = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Summary_Reports'
# os.makedirs(output_root, exist_ok=True)
#
# summary_output_path = os.path.join(output_root, f'Counts_Summary_Soil_{SC_str}_Steps_1-8.xlsx')
#
# # Bins (East/CEUS logic)
# bin_labels = ['<0.5', '0.5–0.8', '>0.8']
#
# # ======= Process with ExcelWriter =======
# with pd.ExcelWriter(summary_output_path) as writer:
#     for current_sdc in sdc_list:
#         sdc_results = []
#         print(f"Processing SDC {current_sdc}...")
#
#         # Loop through exactly steps 1 to 8
#         for i in range(1, 9):
#             file_name = f"interpolated_sc_{SC_str}_sdc_{current_sdc}_{i}.xlsx"
#             file_path = os.path.join(input_dir, file_name)
#
#             if not os.path.exists(file_path):
#                 print(f"  ! Missing: {file_name}")
#                 continue
#
#             try:
#                 # Load only numeric data
#                 df = pd.read_excel(file_path)
#                 df_numeric = df.select_dtypes(include='number')
#
#                 total_points = df_numeric.size
#
#                 # Calculate Bin Counts
#                 c1 = (df_numeric <= 0.5).sum().sum()
#                 c2 = ((df_numeric > 0.5) & (df_numeric <= 0.8)).sum().sum()
#                 c3 = (df_numeric > 0.8).sum().sum()
#
#                 sdc_results.append({
#                     'Step': f"Step {i}",
#                     'File Name': file_name,
#                     'Total Points': total_points,
#                     '<0.5': c1,
#                     '0.5–0.8': c2,
#                     '>0.8': c3,
#                     '% >0.8': round((c3 / total_points * 100), 2) if total_points > 0 else 0
#                 })
#             except Exception as e:
#                 print(f"  Error in {file_name}: {e}")
#
#         # Create sheet if data exists
#         if sdc_results:
#             df_sdc = pd.DataFrame(sdc_results).set_index('Step')
#             df_sdc.to_excel(writer, sheet_name=f'SDC_{current_sdc}')
#         else:
#             print(f"  No data found for SDC {current_sdc}")
#
# print("-" * 30)
# print(f"Processing complete. File saved at:\n{summary_output_path}")





################# CEUS SDC by Soil Class ##################
#
# import geopandas as gpd
# from shapely.geometry import box
# import pandas as pd
# import matplotlib.gridspec as gridspec
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# import os
#
# # ================= SETTINGS =================
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
# SDC_list = ['A', 'B', 'C', 'D', 'E']
#
# # Define soft pastel-like colors
# colors = {
#     'A': '#aec7e8',  # Light Blue
#     'B': '#98df8a',  # Light Green
#     'C': '#FFFF00',  # Yellow
#     'D': '#ff7f0e',  # Orange
#     'E': '#FF0000',  # Red
# }
#
# input_base_path = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS'
# output_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS_SDC_Distribution_Maps'
# os.makedirs(output_dir, exist_ok=True)
#
# # Load US states shapefile and clip to bounding box
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs("EPSG:4326")
# # Clipping focused on CEUS area
# bbox = box(-107, 24, -65, 50)
# clipped_states = states[states.intersects(bbox)]
# clipped_states = clipped_states[clipped_states['STUSPS'] != 'DC']
#
# # ================= LOOP THROUGH SOIL CLASSES =================
# for sc in soil_classes:
#     file_path = os.path.join(input_base_path, f'Final_Grouped_{sc}.xlsx')
#
#     if not os.path.exists(file_path):
#         print(f"Skipping Soil Class {sc}: File not found.")
#         continue
#
#     print(f"Generating SDC Distribution Map for Soil Class: {sc}")
#
#     fig, ax = plt.subplots(figsize=(9, 6))
#
#     # 1. Plot SDC points (zorder=2)
#     for sdc in SDC_list:
#         sheet_name = f'Ratio_SDC_{sdc}'
#         try:
#             df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=['latitude', 'longitude'])
#
#             # edgecolors='none' ensures points don't "bleed" over the state lines
#             ax.scatter(df['longitude'], df['latitude'],
#                        c=colors[sdc], label=sdc, alpha=0.7, s=1.5,
#                        edgecolors='none', zorder=2)
#         except Exception:
#             continue
#
#     # 2. Plot state boundaries (zorder=3 - draws OVER the points)
#     clipped_states.boundary.plot(ax=ax, linewidth=0.6, color='#444444', zorder=3)
#
#     # 3. Vertical dashed line at -105 (no label so it stays off the legend)
#     ax.axvline(x=-105, color='black', linestyle='--', linewidth=1.0, zorder=4)
#
#     # Legend - Positioned at Bottom Right
#     legend_elements = [
#         Line2D([0], [0], marker='o', color='w', label=sdc,
#                markerfacecolor=colors[sdc], markersize=8) for sdc in SDC_list
#     ]
#     ax.legend(handles=legend_elements, title="SDC", loc='lower right', frameon=True, fontsize=9)
#
#     ax.set_xlabel('Longitude')
#     ax.set_ylabel('Latitude')
#     ax.set_title(f'Distribution of SDC - Soil Class {sc}')
#
#     # Static limits for consistency across all maps
#     ax.set_xlim(-107, -65)
#     ax.set_ylim(24, 50)
#     plt.tight_layout()
#
#     # Save
#     save_path = os.path.join(output_dir, f'SDC_Distribution_Soil_{sc}.png')
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#
# print(f"Success! Maps saved to: {output_dir}")



################ To get percentage and plot heatmaps (raw data colored grids) ##################

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
#
# # ======= Configuration =======
# # Updated to include all requested soil classes
# soil_classes = ['A', 'B', 'BC', 'C', 'CD', 'D', 'DE', 'E']
# sdc_list = ['A', 'B', 'C', 'D', 'E']
#
# # Root directory for inputs and outputs
# # Assumes input files follow the pattern: Counts_Summary_Soil_{SC}_Steps_1-8.xlsx
# base_input_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Summary_Reports'
# base_output_dir = r'C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Heatmaps_Output'
# os.makedirs(base_output_dir, exist_ok=True)
#
# # (East) Labels
# x_labels = [
#     r'$0 < T_v \leq  0.025$', r'$0.025 < T_v \leq 0.05$',
#     r'$0.05 < T_v \leq 0.1$', r'$0.1 < T_v \leq 0.2$',
#     r'$0.2 < T_v \leq 0.5$', r'$0.5 < T_v \leq 1$',
#     r'$1 < T_v \leq 2$', r'$2 < T_v \leq 10$'
# ]
# y_labels = [
#     r'$0.8 < R_{E_{V}}$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$R_{E_{V}} \leq 0.5$'
# ]
#
# # ======= Nested Loops: Soil Class -> SDC =======
# for sc in soil_classes:
#     input_file = os.path.join(base_input_dir, f'Counts_Summary_Soil_{sc}_Steps_1-8.xlsx')
#
#     # Check if the summary file for this Soil Class exists
#     if not os.path.exists(input_file):
#         print(f"Skipping Soil Class {sc}: File not found ({input_file})")
#         continue
#
#     print(f"\n--- Processing Soil Class: {sc} ---")
#
#     for sdc in sdc_list:
#         try:
#             # 1. Load data from specific sheet
#             # sheet_name pattern remains SDC_{sdc}
#             df_raw = pd.read_excel(input_file, sheet_name=f'SDC_{sdc}')
#
#             # 2. Robust Identification of Count Columns
#             col_lt_05 = [c for c in df_raw.columns if '<0.5' in str(c).replace(" ", "")][0]
#             col_mid = [c for c in df_raw.columns if '0.5' in str(c) and '0.8' in str(c)][0]
#             col_gt_08 = [c for c in df_raw.columns if '>0.8' in str(c).replace(" ", "")][0]
#
#             # 3. Create the ratio DataFrame
#             df_counts = df_raw[[col_lt_05, col_mid, col_gt_08]].T
#             column_sums = df_counts.sum(axis=0)
#
#             # Use fillna(0) to handle steps with zero total points
#             ratio_df = df_counts.div(column_sums, axis=1).fillna(0).round(4) * 100
#             ratio_df = ratio_df.iloc[::-1]
#
#             # Save ratios to a specific subfolder: {Output}/Soil_{sc}/SDC_{sdc}/
#             sdc_folder = os.path.join(base_output_dir, f'Soil_{sc}', sdc)
#             os.makedirs(sdc_folder, exist_ok=True)
#             ratio_df.to_excel(os.path.join(sdc_folder, 'ratio_output.xlsx'))
#
#             # 4. Plot setup (Exactly matching your template)
#             data = ratio_df.values
#             rows, cols = data.shape
#             fig, ax = plt.subplots(figsize=(8, 6))
#             cmap = plt.cm.Blues
#             x = np.arange(cols + 1)
#             y = np.arange(rows + 1)
#
#             # Draw heatmap
#             mesh = ax.pcolormesh(x, y, data, cmap=cmap, shading='auto', edgecolors='none')
#
#             # Dashed grid lines
#             for i in range(1, cols):
#                 ax.axvline(i, color='gray', linestyle='--', linewidth=0.5)
#             for j in range(1, rows):
#                 ax.axhline(j, color='gray', linestyle='--', linewidth=0.5)
#
#             # Annotations
#             for i in range(rows):
#                 for j in range(cols):
#                     val = data[i, j]
#                     color = 'white' if val >= 50 else 'black'
#                     text_val = f'{val:.2f}' if not np.isnan(val) else "0.00"
#                     ax.text(j + 0.5, i + 0.5, text_val, ha='center', va='center', color=color)
#
#             # Ticks and labels
#             ax.set_xticks(np.arange(cols) + 0.5)
#             ax.set_yticks(np.arange(rows) + 0.5)
#             ax.set_xticklabels(x_labels, rotation=45, ha='right')
#             ax.set_yticklabels(y_labels)
#
#             # Axes limits and formatting
#             ax.set_xlim(0, cols)
#             ax.set_ylim(0, rows)
#             ax.invert_yaxis()
#             ax.set_aspect('equal')
#
#             # Colorbar and layout
#             cbar = plt.colorbar(mesh, ax=ax)
#             cbar.set_label("Percentage (%)")
#             plt.tight_layout()
#
#             # Save plot: {Output}/Soil_{sc}_SDC_{sdc}_percentage_distribution.png
#             output_image = os.path.join(base_output_dir, f'Soil_{sc}_SDC_{sdc}_distribution.png')
#             plt.savefig(output_image, dpi=300)
#             plt.close()
#             print(f"  Successfully processed SDC {sdc}")
#
#         except Exception as e:
#             print(f"  Error processing Soil {sc}, SDC {sdc}: {e}")
#
# print(f"\nAll soil classes processed. Outputs available in: {base_output_dir}")
#



################# To get SDC disaggregated categorized heatmaps (5 sungroups) (borders added) ##################

# import geopandas as gpd
# from shapely.geometry import box, Point
# import pandas as pd
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from matplotlib import colors
# from pyproj import Transformer
#
# # ================= CONFIGURATION & SETUP =================
# SDC_str = 'E'  # Can be changed to 'A', 'B', 'C', 'D', 'E'
#
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
# # Publication Target Directory requested
# output_root = r"D:\MyPaper\Comparative Evaluation of Vertical Seismic Effect Methods in ASCE 7-22 for the Continental United States\submission\V3"
# output_dir = os.path.join(output_root, SDC_str)
# os.makedirs(output_dir, exist_ok=True)
#
#
# # ===== Remap Function =====
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# # ===== Color Map Setup =====
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [
#     r'$R_{E_{V}} \leq 0.5$',
#     r'$0.5 < R_{E_{V}} \leq 0.8$',
#     r'$0.8 < R_{E_{V}} \leq 1.2$',
#     r'$1.2 < R_{E_{V}} \leq 1.5$',
#     r'$1.5 < R_{E_{V}}$'
# ]
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ================= MAP FEATURES (BORDERS) =================
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Bounding box safely covering the entire Conterminous US
# bbox_geom = box(-125, 24, -66, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states[clipped_states['STUSPS'] != 'DC']
#
# # Project states to Albers
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Setup transformers to convert between meters and degrees back-and-forth
# to_proj = Transformer.from_crs(geo_crs, target_crs, always_xy=True)
#
# # Define exact map limits in meters based on the plotted states
# bounds = clipped_states.total_bounds
# xmin, ymin, xmax, ymax = bounds[0], bounds[1], bounds[2], bounds[3]
#
# # Add standard layout padding
# x_pad = (xmax - xmin) * 0.05
# y_pad = (ymax - ymin) * 0.05
# xmin_map, xmax_map = xmin - x_pad, xmax + x_pad
# ymin_map, ymax_map = ymin - y_pad, ymax + y_pad
#
# # ================= STATE HIGHLIGHT MAPS DEFINITIONS =================
# state_highlights = {
#     'E': {'WA', 'OR', 'CA', 'NV', 'MO', 'AR', 'TN', 'KY', 'IL'},
#     'D': {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#           'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC'},
#     'C': {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#           'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA', 'ME', 'NY'},
#     'B': {'WA', 'OR', 'CA', 'NV', 'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX',
#           'OK', 'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA',
#           'KS', 'NE', 'IA', 'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY',
#           'CT', 'RI', 'MA', 'VT', 'NH', 'ME', 'MN'},
#     'A': {'AZ', 'UT', 'ID', 'MT', 'WY', 'CO', 'NM', 'TX', 'SD', 'ND',
#           'OK', 'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA',
#           'KS', 'NE', 'IA', 'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY',
#           'CT', 'RI', 'MA', 'VT', 'NH', 'ME', 'MN', 'MD'}
# }
#
# highlight_states = state_highlights.get(SDC_str, set())
#
# # =====================================================
# #           LOOP THROUGH Tv = 3 TO 4
# # =====================================================
# for i in range(3, 5):
#
#     fig, ax = plt.subplots(figsize=(13, 8))
#     ax.set_xlim(xmin_map, xmax_map)
#     ax.set_ylim(ymin_map, ymax_map)
#
#     scat = None
#
#     # 1. Generate and Plot Target Latitudes (Horizontal Curves)
#     target_latitudes = np.arange(25, 51, 5)
#     for lat in target_latitudes:
#         lon_seq = np.linspace(-140, -50, 200)
#         lat_seq = np.full_like(lon_seq, lat)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_left = np.argmin(proj_x[valid])
#             lbl_y = proj_y[valid][idx_left]
#
#             # Increased padding to accommodate larger 14pt text cleanly
#             padding_lbl_x = (xmax_map - xmin_map) * 0.015
#             ax.text(xmin_map - padding_lbl_x, lbl_y, f"{lat}°N",
#                     va='center', ha='right', fontsize=14, color='black')
#
#     # 2. Generate and Plot Longitudes (Vertical Curves)
#     target_longitudes = np.arange(-125, -60, 5)
#     for lon in target_longitudes:
#         lat_seq = np.linspace(20, 55, 200)
#         lon_seq = np.full_like(lat_seq, lon)
#
#         proj_x, proj_y = to_proj.transform(lon_seq, lat_seq)
#         valid = (proj_x >= xmin_map) & (proj_x <= xmax_map) & (proj_y >= ymin_map) & (proj_y <= ymax_map)
#
#         if np.any(valid):
#             ax.plot(proj_x, proj_y, color='black', linestyle='--', linewidth=0.6, alpha=0.45, zorder=1)
#
#             idx_bottom = np.argmin(proj_y[valid])
#             lbl_x = proj_x[valid][idx_bottom]
#             lbl_y = proj_y[valid][idx_bottom]
#
#             # Increased padding to accommodate larger 14pt text cleanly
#             padding_lbl_y = (ymax_map - ymin_map) * 0.015
#             ax.text(lbl_x, ymin_map - padding_lbl_y, f"{abs(lon)}°W",
#                     va='top', ha='center', fontsize=14, color='black')
#
#     # 3. Generate and Plot the -105° Longitude Separation Boundary Curve
#     lat_seq_boundary = np.linspace(20, 55, 200)
#     lon_seq_boundary = np.full_like(lat_seq_boundary, -105)
#     b_x, b_y = to_proj.transform(lon_seq_boundary, lat_seq_boundary)
#     ax.plot(b_x, b_y, color='black', linestyle='-', linewidth=1.2, zorder=3)
#
#     # -------------------------------------------------
#     #          LOAD AND SCATTER SC ELEMENT DATA
#     # -------------------------------------------------
#     try:
#         # ---------- EAST OF -105 ----------
#         file_path_East = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_excluded_VHRatio - east of -105.xlsx"
#         df_East = pd.read_excel(file_path_East, sheet_name=SDC_str)
#         df_East.columns = [c.lower() for c in df_East.columns]
#
#         geometry_east = [Point(xy) for xy in zip(df_East['longitude'], df_East['latitude'])]
#         gdf_east = gpd.GeoDataFrame(df_East, geometry=geometry_east, crs=geo_crs).to_crs(target_crs)
#
#         interpolated_path_East = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_East\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#         df2_East = pd.read_excel(interpolated_path_East)
#         averages_East = df2_East.mean(axis=1).round(4).apply(remap_average)
#
#         scat = ax.scatter(
#             gdf_east.geometry.x, gdf_east.geometry.y,
#             c=averages_East, s=1.5, cmap=cmap, norm=norm, zorder=2
#         )
#
#         # ---------- AT OR WEST OF -105 ----------
#         file_path_West = r"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\CA_included_VHRatio - at or west of -105.xlsx"
#         df_West = pd.read_excel(file_path_West, sheet_name=SDC_str)
#         df_West.columns = [c.lower() for c in df_West.columns]
#
#         geometry_west = [Point(xy) for xy in zip(df_West['longitude'], df_West['latitude'])]
#         gdf_west = gpd.GeoDataFrame(df_West, geometry=geometry_west, crs=geo_crs).to_crs(target_crs)
#
#         interpolated_path_West = fr"C:\Users\cheng\PycharmProjects\pythonProject\US_excluding_CA\interpolated_West_CA_included\{SDC_str}\interpolated_{SDC_str}_{i}.xlsx"
#         df2_West = pd.read_excel(interpolated_path_West)
#         averages_West = df2_West.mean(axis=1).round(4).apply(remap_average)
#
#         scat = ax.scatter(
#             gdf_west.geometry.x, gdf_west.geometry.y,
#             c=averages_West, s=1.5, cmap=cmap, norm=norm, zorder=2
#         )
#     except Exception as e:
#         print(f"Error handling execution layers for SDC {SDC_str}, Step {i}: {e}")
#
#     # 4. Plot state boundaries on top of data points
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=4)
#
#     # 5. Conditional State Labeling Engine (Font 14, Bold removed)
#     for _, row in clipped_states.iterrows():
#         abbrev = row['STUSPS']
#         if abbrev in highlight_states:
#             centroid = row.geometry.representative_point()
#             ax.text(
#                 centroid.x, centroid.y, abbrev,
#                 fontsize=14, color='lightblue',
#                 ha='center', va='center', zorder=5
#             )
#
#     # 6. Discrete Bounds Colorbar Setup
#     if scat is not None:
#         cbar = fig.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#         cbar.set_ticklabels(tick_labels)
#         cbar.ax.tick_params(labelsize=14)  # Adjusted colorbar font to 14pt
#
#     # Clean border frame controls
#     ax.set_xticks([])
#     ax.set_yticks([])
#     # Title removed completely
#
#     plt.tight_layout()
#
#     # Save Output
#     save_path = os.path.join(output_dir, f"{SDC_str}_Tv{i}.png")
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully generated map: {save_path}")

################# To get SDC disaggregated categorized heatmaps (5 sungroups) (by Soil Class) ##################

#
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib import colors
# import geopandas as gpd
# from shapely.geometry import box
#
# # ======= Configuration =======
# SC_str = 'A'  # Soil Class (Change this to B, C, etc. as needed)
# SDC_str = 'A'  # Seismic Design Category
# interpolated_base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\interpolated_results"
# output_root = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Soil_Analysis_Output"
#
# # Construct Coords Path and Sheet Name
# coords_file = rf"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\Final_Grouped_{SC_str}.xlsx"
# sheet_name = f"Ratio_SDC_{SDC_str}"
#
# # ======= Load Coordinates from the Grouped Soil File =======
# if not os.path.exists(coords_file):
#     raise FileNotFoundError(f"Could not find coordinate file: {coords_file}")
#
# df_coords = pd.read_excel(coords_file, sheet_name=sheet_name)
#
# # Ensure columns are lowercase or handle case sensitivity
# df_coords.columns = [c.lower() for c in df_coords.columns]
#
# if 'latitude' in df_coords.columns and 'longitude' in df_coords.columns:
#     latitudes = df_coords['latitude']
#     longitudes = df_coords['longitude']
# else:
#     raise ValueError(f"Columns 'latitude'/'longitude' not found in {sheet_name}")
#
#
# # ======= Remap and Color Setup =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [r'$R_{E_{V}} \leq 0.5$', r'$0.5 < R_{E_{V}} \leq 0.8$',
#                r'$0.8 < R_{E_{V}} \leq 1.2$', r'$1.2 < R_{E_{V}} \leq 1.5$', r'$1.5 < R_{E_{V}}$']
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ======= Map Features (Borders) =======
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs("EPSG:4326")
# bbox_geom = box(-107, 24, -65, 50)  # Focused on CEUS
# clipped_states = states[states.intersects(bbox_geom)]
#
# # State highlight mapping (Cleaned for CEUS/East only)
# state_highlights = {
#     'E': {'MO', 'AR', 'TN', 'KY', 'IL'},
#     'D': {'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC'},
#     'C': {'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA', 'ME', 'NY'},
#     'B': {'MO', 'AR', 'TN', 'KY', 'IL', 'IN', 'AL', 'MS', 'SC', 'LA', 'NC', 'GA',
#           'KS', 'NE', 'IA', 'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY',
#           'CT', 'RI', 'MA', 'VT', 'NH', 'ME', 'MN'},
#     'A': {'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA', 'KS', 'NE', 'IA',
#           'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY', 'CT', 'RI',
#           'MA', 'VT', 'NH', 'ME', 'MN', 'MD'}
# }
#
# # ======= Loop Through Interpolated Files (1 to 8) =======
# for i in range(3, 5):
#     file_name = f"interpolated_sc_{SC_str}_sdc_{SDC_str}_{i}.xlsx"
#     file_path = os.path.join(interpolated_base_dir, SC_str, file_name)
#
#     if not os.path.exists(file_path):
#         print(f"Skipping: {file_name} (File not found)")
#         continue
#
#     # Load data and calculate remapped averages
#     df_data = pd.read_excel(file_path)
#     averages = df_data.mean(axis=1).round(4).apply(remap_average)
#
#     # --- Plotting ---
#     fig, ax = plt.subplots(figsize=(10, 7))
#
#     # Scatter plot of data points
#     scat = ax.scatter(longitudes, latitudes, c=averages, s=1.5, cmap=cmap, norm=norm, zorder=2)
#
#     # Plot state borders
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=3)
#
#     # State Labels
#     highlight = state_highlights.get(SDC_str, set())
#     for _, row in clipped_states.iterrows():
#         if row['STUSPS'] in highlight:
#             centroid = row.geometry.centroid
#             ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=7,
#                     color='lightblue', ha='center', fontweight='bold', zorder=4)
#
#     # Plot Formatting
#     cbar = plt.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#     cbar.set_ticklabels(tick_labels)
#     cbar.ax.tick_params(labelsize=10)
#
#     ax.set_title(f"Soil Class: {SC_str} | SDC: {SDC_str} | Step: {i}", fontsize=14)
#     ax.set_xlabel('Longitude', fontsize=12)
#     ax.set_ylabel('Latitude', fontsize=12)
#     ax.set_xlim(-107, -65)
#     ax.set_ylim(24, 50)
#
#     # Add vertical line at -105 for context
#     ax.axvline(x=-105, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
#
#     # --- Save ---
#     save_dir = os.path.join(output_root, f"Soil_Class_{SC_str}", SDC_str)
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"SC{SC_str}_{SDC_str}_Step{i}.png")
#
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully saved: {save_path}")



################# To get All SDC on 1 heatmap (5 sungroups) (by Soil Class) ##################

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# from matplotlib import colors
# import geopandas as gpd
# from shapely.geometry import box
#
# # ======= Configuration =======
# SC_str = 'DE'  # Soil Class
# sdc_list = ['A', 'B', 'C', 'D', 'E']  # All SDCs to include
# interpolated_base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\interpolated_results"
# output_root = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Soil_Analysis_Output_final"
# coords_file_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\Final_Grouped_{SC_str}.xlsx"
#
#
# # ======= Remap and Color Setup =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [r'$R_{E_{V}} \leq 0.5$', r'$0.5 < R_{E_{V}} \leq 0.8$',
#                r'$0.8 < R_{E_{V}} \leq 1.2$', r'$1.2 < R_{E_{V}} \leq 1.5$', r'$1.5 < R_{E_{V}}$']
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ======= Map Features (Borders) =======
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs("EPSG:4326")
# bbox_geom = box(-107, 24, -65, 50)
# clipped_states = states[states.intersects(bbox_geom)]
#
# # We use the 'A' highlight set as the superset for all SDCs on one map
# highlight_states = {'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA', 'KS', 'NE', 'IA',
#                     'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY', 'CT', 'RI',
#                     'MA', 'VT', 'NH', 'ME', 'MN', 'MD', 'ND', 'SD', 'OK', 'TX', 'TN', 'SC', 'AR'}
#
# # ======= Loop Through Steps (e.g., Tv3 and Tv4) =======
# for i in range(3, 5):
#     fig, ax = plt.subplots(figsize=(12, 8))
#
#     # Inner loop to overlay each SDC
#     for current_sdc in sdc_list:
#         sheet_name = f"Ratio_SDC_{current_sdc}"
#
#         # 1. Load Coordinates for this specific SDC
#         try:
#             df_coords = pd.read_excel(coords_file_path, sheet_name=sheet_name)
#             df_coords.columns = [c.lower() for c in df_coords.columns]
#             lats = df_coords['latitude']
#             lons = df_coords['longitude']
#         except Exception as e:
#             print(f"Error loading coords for SDC {current_sdc}: {e}")
#             continue
#
#         # 2. Load Interpolated Data for this specific SDC
#         file_name = f"interpolated_sc_{SC_str}_sdc_{current_sdc}_{i}.xlsx"
#         file_path = os.path.join(interpolated_base_dir, SC_str, file_name)
#
#         if not os.path.exists(file_path):
#             print(f"Skipping: {file_name} (Not found)")
#             continue
#
#         df_data = pd.read_excel(file_path)
#         averages = df_data.mean(axis=1).round(4).apply(remap_average)
#
#         # 3. Plot this SDC's points
#         scat = ax.scatter(lons, lats, c=averages, s=1.5, cmap=cmap, norm=norm, zorder=2)
#
#     # --- Finalize Map Decorations ---
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=3)
#
#     for _, row in clipped_states.iterrows():
#         if row['STUSPS'] in highlight_states:
#             centroid = row.geometry.centroid
#             ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=7,
#                     color='lightblue', ha='center', fontweight='bold', zorder=4)
#
#     cbar = plt.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#     cbar.set_ticklabels(tick_labels)
#
#     # ax.set_title(f"Soil Class: {SC_str} | Combined SDC A-E | Step: {i}", fontsize=14)
#     ax.set_xlim(-107, -65)
#     ax.set_ylim(24, 50)
#     ax.axvline(x=-105, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
#
#     # --- Save ---
#     save_dir = os.path.join(output_root, f"Soil_Class_{SC_str}", "Combined_SDC")
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"SC{SC_str}_AllSDC_Step{i}.png")
#
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully saved combined map: {save_path}")




####### REV map by soil classes #######
# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from matplotlib import colors
# import geopandas as gpd
# from shapely.geometry import box, Point, LineString
#
# # ======= Configuration =======
# SC_str = 'DE'  # Soil Class
# sdc_list = ['A', 'B', 'C', 'D', 'E']  # All SDCs to include
# interpolated_base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\interpolated_results"
# coords_file_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\Final_Grouped_{SC_str}.xlsx"
#
# # UPDATE THIS TO YOUR NEW DESIRED OUTPUT PATH:
# output_root = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Soil_Analysis_Output_Projected"
#
# # ======= Projection Setup =======
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
#
# # ======= Remap and Color Setup =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [r'$R_{E_{V}} \leq 0.5$', r'$0.5 < R_{E_{V}} \leq 0.8$',
#                r'$0.8 < R_{E_{V}} \leq 1.2$', r'$1.2 < R_{E_{V}} \leq 1.5$', r'$1.5 < R_{E_{V}}$']
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ======= Map Features (Borders) =======
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Clip the states in geographic coordinates first
# bbox_geom = box(-107, 24, -65, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Get the new bounding box limits in the projected coordinate system for map extent
# bbox_projected = gpd.GeoSeries([bbox_geom], crs=geo_crs).to_crs(target_crs).bounds.iloc[0]
# xmin, ymin, xmax, ymax = bbox_projected['minx'], bbox_projected['miny'], bbox_projected['maxx'], bbox_projected['maxy']
#
# highlight_states = {'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA', 'KS', 'NE', 'IA',
#                     'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY', 'CT', 'RI',
#                     'MA', 'VT', 'NH', 'ME', 'MN', 'MD', 'ND', 'SD', 'OK', 'TX', 'TN', 'SC', 'AR'}
#
# # ======= Generate 5-Degree Gridlines (Graticules) =======
# grid_lines = []
# grid_labels = []
#
# # Generate Longitudinal lines (every 5 degrees from -105 to -65)
# longitudes = np.arange(-105, -60, 5)
# for lon in longitudes:
#     lats_seq = np.linspace(20, 55, 100)
#     line = LineString([(lon, lat) for lat in lats_seq])
#     grid_lines.append(line)
#     # Track metadata for labeling later
#     grid_labels.append({'type': 'lon', 'value': lon, 'label': f"{abs(lon)}°W"})
#
# # Generate Latitudinal lines (every 5 degrees from 25 to 50)
# latitudes = np.arange(25, 55, 5)
# for lat in latitudes:
#     lons_seq = np.linspace(-110, -60, 100)
#     line = LineString([(lon, lat) for lon in lons_seq])
#     grid_lines.append(line)
#     # Track metadata for labeling later
#     grid_labels.append({'type': 'lat', 'value': lat, 'label': f"{lat}°N"})
#
# # Package gridlines into a GeoDataFrame and project them
# gdf_gridlines = gpd.GeoDataFrame(geometry=grid_lines, crs=geo_crs).to_crs(target_crs)
# # Add metadata to the geodataframe so we know which line is what during the loop
# gdf_gridlines['type'] = [item['type'] for item in grid_labels]
# gdf_gridlines['label'] = [item['label'] for item in grid_labels]
#
# # ======= Loop Through Steps (e.g., Tv3 and Tv4) =======
# for i in range(3, 5):
#     fig, ax = plt.subplots(figsize=(12, 8))
#     scat = None
#
#     # Inner loop to overlay each SDC
#     for current_sdc in sdc_list:
#         sheet_name = f"Ratio_SDC_{current_sdc}"
#
#         # 1. Load Coordinates
#         try:
#             df_coords = pd.read_excel(coords_file_path, sheet_name=sheet_name)
#             df_coords.columns = [c.lower() for c in df_coords.columns]
#         except Exception as e:
#             print(f"Error loading coords for SDC {current_sdc}: {e}")
#             continue
#
#         # 2. Load Interpolated Data
#         file_name = f"interpolated_sc_{SC_str}_sdc_{current_sdc}_{i}.xlsx"
#         file_path = os.path.join(interpolated_base_dir, SC_str, file_name)
#
#         if not os.path.exists(file_path):
#             print(f"Skipping: {file_name} (Not found)")
#             continue
#
#         df_data = pd.read_excel(file_path)
#         averages = df_data.mean(axis=1).round(4).apply(remap_average)
#
#         # 3. Convert Points to GeoDataFrame and Project Them
#         geometry = [Point(xy) for xy in zip(df_coords['longitude'], df_coords['latitude'])]
#         gdf_points = gpd.GeoDataFrame(df_coords, geometry=geometry, crs=geo_crs)
#         gdf_points = gdf_points.to_crs(target_crs)
#
#         # 4. Plot points
#         scat = ax.scatter(gdf_points.geometry.x, gdf_points.geometry.y,
#                           c=averages, s=1.5, cmap=cmap, norm=norm, zorder=2)
#
#     # --- Finalize Map Decorations ---
#     # Plot state boundaries
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=3)
#
#     # Plot the 5-degree dashed gridlines (both lat and lon)
#     gdf_gridlines.plot(ax=ax, color='black', linestyle='--', linewidth=0.5, alpha=0.4, zorder=1)
#
#     # --- Label Gridlines along the edges ---
#     padding = (xmax - xmin) * 0.008  # Tiny offset to keep text clean off the border line
#
#     for _, row in gdf_gridlines.iterrows():
#         geom = row.geometry
#         # Find where the curved grid line intersects the boundary box edges
#         if geom.geom_type == 'LineString':
#             coords = np.array(geom.coords)
#             x_coords = coords[:, 0]
#             y_coords = coords[:, 1]
#
#             if row['type'] == 'lon':
#                 # Longitude lines hit the bottom edge (ymin)
#                 # Find the point on the line closest to the bottom boundary
#                 idx = np.argmin(np.abs(y_coords - ymin))
#                 label_x = x_coords[idx]
#                 # Only draw if it's within our visible X bounds
#                 if xmin <= label_x <= xmax:
#                     ax.text(label_x, ymin - padding, row['label'],
#                             va='top', ha='center', fontsize=8, color='black')
#
#             elif row['type'] == 'lat':
#                 # Latitude lines hit the left edge (xmin)
#                 # Find the point on the line closest to the left boundary
#                 idx = np.argmin(np.abs(x_coords - xmin))
#                 label_y = y_coords[idx]
#                 # Only draw if it's within our visible Y bounds
#                 if ymin <= label_y <= ymax:
#                     ax.text(xmin - padding, label_y, row['label'],
#                             va='center', ha='right', fontsize=8, color='black')
#
#     # Plot state text labels
#     for _, row in clipped_states.iterrows():
#         if row['STUSPS'] in highlight_states:
#             centroid = row.geometry.centroid
#             ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=7,
#                     color='lightblue', ha='center', fontweight='bold', zorder=4)
#
#     # Add Colorbar
#     if scat is not None:
#         cbar = plt.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#         cbar.set_ticklabels(tick_labels)
#
#     # Set map limits
#     ax.set_xlim(xmin, xmax)
#     ax.set_ylim(ymin, ymax)
#
#     # Remove default ticks/labels, but keep the bounding box frame visible
#     ax.set_xticks([])
#     ax.set_yticks([])
#
#     # --- Save ---
#     save_dir = os.path.join(output_root, f"Soil_Class_{SC_str}", "Combined_SDC")
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"SC{SC_str}_AllSDC_Step{i}.png")
#
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully saved combined map with 5° gridlines and labels: {save_path}")



############

# import pandas as pd
# import matplotlib.pyplot as plt
# import os
# import numpy as np
# from matplotlib import colors
# import geopandas as gpd
# from shapely.geometry import box, Point, LineString
#
# # ======= Configuration =======
# SC_str = 'A'  # Soil Class
# sdc_list = ['A', 'B', 'C', 'D', 'E']  # All SDCs to include
# interpolated_base_dir = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\interpolated_results"
# coords_file_path = rf"C:\Users\cheng\PycharmProjects\pythonProject\CEUS\Final_Grouped_{SC_str}.xlsx"
#
# # UPDATE THIS TO YOUR NEW DESIRED OUTPUT PATH:
# output_root = r"C:\Users\cheng\PycharmProjects\pythonProject\CEUS_Soil_Analysis_Output_Projected"
#
# # ======= Projection Setup =======
# geo_crs = "EPSG:4326"
# target_crs = "ESRI:102003"  # Albers Equal Area for North America
#
#
# # ======= Remap and Color Setup =======
# def remap_average(val):
#     if val <= 0.5:
#         return 0.0
#     elif val <= 0.8:
#         return 0.65
#     elif val <= 1.2:
#         return 1.0
#     elif val <= 1.5:
#         return 1.35
#     else:
#         return 2.0
#
#
# boundaries = [0.0, 0.5, 0.8, 1.2, 1.5, 2.25]
# ticks = [0.25, 0.65, 1.0, 1.35, 1.875]
# tick_labels = [r'$R_{E_{V}} \leq 0.5$', r'$0.5 < R_{E_{V}} \leq 0.8$',
#                r'$0.8 < R_{E_{V}} \leq 1.2$', r'$1.2 < R_{E_{V}} \leq 1.5$', r'$1.5 < R_{E_{V}}$']
#
# cmap = plt.cm.plasma
# norm = colors.BoundaryNorm(boundaries, ncolors=cmap.N, clip=True)
#
# # ======= Map Features (Borders) =======
# url = "https://www2.census.gov/geo/tiger/GENZ2022/shp/cb_2022_us_state_20m.zip"
# states = gpd.read_file(url).to_crs(geo_crs)
#
# # Clip the states in geographic coordinates first
# bbox_geom = box(-107, 24, -65, 50)
# clipped_states = states[states.intersects(bbox_geom)].copy()
# clipped_states = clipped_states.to_crs(target_crs)
#
# # Get the new bounding box limits in the projected coordinate system for map extent
# bbox_projected = gpd.GeoSeries([bbox_geom], crs=geo_crs).to_crs(target_crs).bounds.iloc[0]
# xmin, ymin, xmax, ymax = bbox_projected['minx'], bbox_projected['miny'], bbox_projected['maxx'], bbox_projected['maxy']
#
# highlight_states = {'MO', 'KY', 'IL', 'IN', 'AL', 'MS', 'LA', 'NC', 'GA', 'KS', 'NE', 'IA',
#                     'WI', 'MI', 'OH', 'WV', 'PA', 'FL', 'VA', 'DE', 'NJ', 'NY', 'CT', 'RI',
#                     'MA', 'VT', 'NH', 'ME', 'MN', 'MD', 'ND', 'SD', 'OK', 'TX', 'TN', 'SC', 'AR'}
#
# # ======= Generate 5-Degree Gridlines (Graticules) =======
# grid_lines = []
# grid_labels = []
#
# # Generate Longitudinal lines (every 5 degrees from -105 to -65)
# longitudes = np.arange(-105, -60, 5)
# for lon in longitudes:
#     lats_seq = np.linspace(20, 55, 100)
#     line = LineString([(lon, lat) for lat in lats_seq])
#     grid_lines.append(line)
#     # Track metadata for labeling later
#     grid_labels.append({'type': 'lon', 'value': lon, 'label': f"{abs(lon)}°W"})
#
# # Generate Latitudinal lines (every 5 degrees from 25 to 50)
# latitudes = np.arange(25, 55, 5)
# for lat in latitudes:
#     lons_seq = np.linspace(-110, -60, 100)
#     line = LineString([(lon, lat) for lon in lons_seq])
#     grid_lines.append(line)
#     # Track metadata for labeling later
#     grid_labels.append({'type': 'lat', 'value': lat, 'label': f"{lat}°N"})
#
# # Package gridlines into a GeoDataFrame and project them
# gdf_gridlines = gpd.GeoDataFrame(geometry=grid_lines, crs=geo_crs).to_crs(target_crs)
# # Add metadata to the geodataframe so we know which line is what during the loop
# gdf_gridlines['type'] = [item['type'] for item in grid_labels]
# gdf_gridlines['label'] = [item['label'] for item in grid_labels]
#
# # ======= Loop Through Steps (e.g., Tv3 and Tv4) =======
# for i in range(3, 5):
#     fig, ax = plt.subplots(figsize=(12, 8))
#     scat = None
#
#     # Inner loop to overlay each SDC
#     for current_sdc in sdc_list:
#         sheet_name = f"Ratio_SDC_{current_sdc}"
#
#         # 1. Load Coordinates
#         try:
#             df_coords = pd.read_excel(coords_file_path, sheet_name=sheet_name)
#             df_coords.columns = [c.lower() for c in df_coords.columns]
#         except Exception as e:
#             print(f"Error loading coords for SDC {current_sdc}: {e}")
#             continue
#
#         # 2. Load Interpolated Data
#         file_name = f"interpolated_sc_{SC_str}_sdc_{current_sdc}_{i}.xlsx"
#         file_path = os.path.join(interpolated_base_dir, SC_str, file_name)
#
#         if not os.path.exists(file_path):
#             print(f"Skipping: {file_name} (Not found)")
#             continue
#
#         df_data = pd.read_excel(file_path)
#         averages = df_data.mean(axis=1).round(4).apply(remap_average)
#
#         # 3. Convert Points to GeoDataFrame and Project Them
#         geometry = [Point(xy) for xy in zip(df_coords['longitude'], df_coords['latitude'])]
#         gdf_points = gpd.GeoDataFrame(df_coords, geometry=geometry, crs=geo_crs)
#         gdf_points = gdf_points.to_crs(target_crs)
#
#         # 4. Plot points
#         scat = ax.scatter(gdf_points.geometry.x, gdf_points.geometry.y,
#                           c=averages, s=1.5, cmap=cmap, norm=norm, zorder=2)
#
#     # --- Finalize Map Decorations ---
#     # Plot state boundaries
#     clipped_states.boundary.plot(ax=ax, color='grey', linewidth=0.6, zorder=3)
#
#     # Plot the 5-degree dashed gridlines (both lat and lon)
#     gdf_gridlines.plot(ax=ax, color='black', linestyle='--', linewidth=0.5, alpha=0.4, zorder=1)
#
#     # --- Label Gridlines along the edges ---
#     padding = (xmax - xmin) * 0.008  # Tiny offset to keep text clean off the border line
#
#     for _, row in gdf_gridlines.iterrows():
#         geom = row.geometry
#         # Find where the curved grid line intersects the boundary box edges
#         if geom.geom_type == 'LineString':
#             coords = np.array(geom.coords)
#             x_coords = coords[:, 0]
#             y_coords = coords[:, 1]
#
#             if row['type'] == 'lon':
#                 # Longitude lines hit the bottom edge (ymin)
#                 # Find the point on the line closest to the bottom boundary
#                 idx = np.argmin(np.abs(y_coords - ymin))
#                 label_x = x_coords[idx]
#                 # Only draw if it's within our visible X bounds
#                 if xmin <= label_x <= xmax:
#                     ax.text(label_x, ymin - padding, row['label'],
#                             va='top', ha='center', fontsize=8, color='black')
#
#             elif row['type'] == 'lat':
#                 # Latitude lines hit the left edge (xmin)
#                 # Find the point on the line closest to the left boundary
#                 idx = np.argmin(np.abs(x_coords - xmin))
#                 label_y = y_coords[idx]
#                 # Only draw if it's within our visible Y bounds
#                 if ymin <= label_y <= ymax:
#                     ax.text(xmin - padding, label_y, row['label'],
#                             va='center', ha='right', fontsize=8, color='black')
#
#     # Plot state text labels
#     for _, row in clipped_states.iterrows():
#         if row['STUSPS'] in highlight_states:
#             centroid = row.geometry.centroid
#             ax.text(centroid.x, centroid.y, row['STUSPS'], fontsize=7,
#                     color='lightblue', ha='center', fontweight='bold', zorder=4)
#
#     # Add Colorbar
#     if scat is not None:
#         cbar = plt.colorbar(scat, ticks=ticks, ax=ax, fraction=0.03, pad=0.04)
#         cbar.set_ticklabels(tick_labels)
#
#     # Set map limits
#     ax.set_xlim(xmin, xmax)
#     ax.set_ylim(ymin, ymax)
#
#     # Remove default ticks/labels, but keep the bounding box frame visible
#     ax.set_xticks([])
#     ax.set_yticks([])
#
#     # --- Save ---
#     save_dir = os.path.join(output_root, f"Soil_Class_{SC_str}", "Combined_SDC")
#     os.makedirs(save_dir, exist_ok=True)
#     save_path = os.path.join(save_dir, f"SC{SC_str}_AllSDC_Step{i}.png")
#
#     plt.savefig(save_path, dpi=300, bbox_inches='tight')
#     plt.close()
#     print(f"Successfully saved combined map with 5° gridlines and labels: {save_path}")

