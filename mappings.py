'''
Name: mappings.py
Author: Timur Kasimov
Created: June 2024
Updated: June 2024

Purpose: 
    Provide dicotinary-like mappings for use with API coded values
    and for country codes/ full names
'''

################
################
### MAPPINGS ###
################
################

##########################
###  COUNTRY_MAPPINGS  ###
##########################
COUNTRY_MAPPINGS = {
    'AL': 'Albania',
    'AT': 'Austria',
    'BA': 'Bosnia and Herz.',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'BY': 'Belarus',
    'CH': 'Switzerland',
    'CZ': 'Czech Republic',
    'CY': 'Cyprus',
    'DE': 'Germany',
    'DE-AT-LU': '',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'GB': 'United Kingdom',
    'GB-NIR': '',
    'GR': 'Greece',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IT': 'Italy',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    # 'MD': 'MD',
    'ME': 'Montenegro',
    'MK': 'North Macedonia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PL': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'RS': 'Serbia',
    'RU': '',
    'RU-KGD': '',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
    'TR': 'Turkey',
    'UA': 'Ukraine'
}


#######################
### DOMAIN_MAPPINGS ###
#######################
DOMAIN_MAPPINGS = {
    'AL': '10YAL-KESH-----5',
    'AT': '10YAT-APG------L',
    'BA': '10YBA-JPCC-----D',
    'BE': '10YBE----------2',
    'BG': '10YCA-BULGARIA-R',
    'BY': '10Y1001A1001A51S',
    'CH': '10YCH-SWISSGRIDZ',
    'CZ': '10YCZ-CEPS-----N',
    'CY': '10YCY-1001A0003J',
    'DE': '10Y1001A1001A83F',
    'DE-AT-LU': '10Y1001A1001A63L',
    'DK': '10Y1001A1001A65H',
    'EE': '10Y1001A1001A39I',
    'ES': '10YES-REE------0',
    'FI': '10YFI-1--------U',
    'FR': '10YFR-RTE------C',
    'GB': '10YGB----------A',
    'GB-NIR': '10Y1001A1001A016',
    'GR': '10YGR-HTSO-----Y',
    'HR': '10YHR-HEP------M',
    'HU': '10YHU-MAVIR----U',
    'IE': '10YIE-1001A00010',
    'IT': '10YIT-GRTN-----B',
    'LT': '10YLT-1001A0008Q',
    'LU': '10YLU-CEGEDEL-NQ',
    'LV': '10YLV-1001A00074',
    # 'MD': 'MD',
    'ME': '10YCS-CG-TSO---S',
    'MK': '10YMK-MEPSO----8',
    'MT': '10Y1001A1001A93C',
    'NL': '10YNL----------L',
    'NO': '10YNO-0--------C',
    'PL': '10YPL-AREA-----S',
    'PT': '10YPT-REN------W',
    'RO': '10YRO-TEL------P',
    'RS': '10YCS-SERBIATSOV',
    'RU': '10Y1001A1001A49F',
    'RU-KGD': '10Y1001A1001A50U',
    'SE': '10YSE-1--------K',
    'SI': '10YSI-ELES-----O',
    'SK': '10YSK-SEPS-----K',
    'TR': '10YTR-TEIAS----W',
    'UA': '10YUA-WEPS-----0'
}


#########################
### TIMEZONE_MAPPINGS ###
#########################
TIMEZONE_MAPPINGS = {
    'AL': 'Europe/Tirane',
    'AT': 'Europe/Vienna',
    'BA': 'Europe/Sarajevo',
    'BE': 'Europe/Brussels',
    'BG': 'Europe/Sofia',
    'BY': 'Europe/Minsk',
    'CH': 'Europe/Zurich',
    'CZ': 'Europe/Prague',
    'DE': 'Europe/Berlin',
    'DK': 'Europe/Copenhagen',
    'EE': 'Europe/Talinn',
    'ES': 'Europe/Madrid',
    'FI': 'Europe/Helsinki',
    'FR': 'Europe/Paris',
    'GB': 'Europe/London',
    'GB-NIR': 'Europe/Belfast',
    'GR': 'Europe/Athens',
    'HR': 'Europe/Zagreb',
    'HU': 'Europe/Budapest',
    'IE': 'Europe/Dublin',
    'IT': 'Europe/Rome',
    'LT': 'Europe/Vilnius',
    'LU': 'Europe/Luxembourg',
    'LV': 'Europe/Riga',
    # 'MD': 'MD',
    'ME': 'Europe/Podgorica',
    'MK': 'Europe/Skopje',
    'MT': 'Europe/Malta',
    'NL': 'Europe/Amsterdam',
    'NO': 'Europe/Oslo',
    'PL': 'Europe/Warsaw',
    'PT': 'Europe/Lisbon',
    'RO': 'Europe/Bucharest',
    'RS': 'Europe/Belgrade',
    'RU': 'Europe/Moscow',
    'RU-KGD': 'Europe/Kaliningrad',
    'SE': 'Europe/Stockholm',
    'SI': 'Europe/Ljubljana',
    'SK': 'Europe/Bratislava',
    'TR': 'Europe/Istanbul',
    'UA': 'Europe/Kiev'
}


########################
### PSRTYPE_MAPPINGS ###
########################
PSRTYPE_MAPPINGS = {
    'A03': 'Mixed',
    'A04': 'Generation',
    'A05': 'Load',
    'B01': 'Biomass',
    'B02': 'Fossil Brown coal/Lignite',
    'B03': 'Fossil Coal-derived gas',
    'B04': 'Fossil Gas',
    'B05': 'Fossil Hard coal',
    'B06': 'Fossil Oil',
    'B07': 'Fossil Oil shale',
    'B08': 'Fossil Peat',
    'B09': 'Geothermal',
    'B10': 'Hydro Pumped Storage',
    'B11': 'Hydro Run-of-river and poundage',
    'B12': 'Hydro Water Reservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'Wind Offshore',
    'B19': 'Wind Onshore',
    'B20': 'Other',
    'B21': 'AC Link',
    'B22': 'DC Link',
    'B23': 'Substation',
    'B24': 'Transformer'
}


##########################
### FREQUENCY_MAPPINGS ###
##########################
FREQUENCY_MAPPINGS = {
    '1M' : 'Month',
    '1W' : 'Week',
    '1D' : 'Day'
}


#######################
### DELTA_TO_SCALER ###
#######################
DELTA_TO_SCALER = {
    '15min' : 1/4,
    '30min' : 1/2,
    '60min' : 1
}