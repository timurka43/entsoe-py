'''
Name: psr_groups.py
Author: Timur Kasimov
Created: June 2024
Updated: June 2024

Purpose: 
    Defining lists of various sources for 
    electricity generation
'''

CARBON_NEUTRAL = []

SOLAR_WIND = ['B16', 'B18', 'B19']

NUCLEAR = ['B14']

HYDRO_SOLAR_WIND = ['B10', 'B11', 'B12', 'B16', 'B18', 'B19'] # marine? excluded
 
FOSSIL = ['B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08'] # fossil peat?? included

TOTAL = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10',
         'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B18', 'B19', 'B20',
         'B21', 'B22', 'B23', 'B24']