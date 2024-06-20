# _*_ encoding utf-8 _*_
"""
entsoe-py package has some constants, it exports

- ``__title__``
- ``__version__``
- ``__author__``
- ``__license__``
- ``URL``
- ``DOMAIN_MAPPINGS``
- ``TIMEZONE_MAPPINGS``
- ``Entsoe``
"""

import logging
import pytz
import requests
from bs4 import BeautifulSoup
from time import sleep
import parsers

__title__ = "entsoe-py"
__version__ = "0.1.12"
__author__ = "EnergieID.be"
__license__ = "MIT"

BASE_URL = 'https://web-api.tp.entsoe.eu/api?'


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
    'B24': 'Transformer'}

log = logging.getLogger(__name__ +'-api')
log.addHandler(logging.NullHandler())

class Entsoe:
    """
    Attributions: Parts of the code for parsing Entsoe responses were copied
    from https://github.com/tmrowco/electricitymap
    """


    
    ###############################
    ###   CONSTRUCTOR: Entsoe   ###
    ###############################
    '''
    Parameters
        api_key : str
        session : requests.Session
        proxies : dict
            requests proxies
    '''
    def __init__(self, api_key, session=None, retry_count=1, retry_delay=0,
                 proxies=None):
        
        self.logger = log
        if api_key is None:
            raise TypeError("API key cannot be None")
        self.api_key = api_key

        if session is None:
            session = requests.Session()
        self.session = session
        self.proxies = proxies
        self.retry_count = retry_count
        self.retry_delay = retry_delay


    ########################
    ###    getFinalURL   ###
    ########################
    '''
    Parameters:
        url_header: base url for the api
        params: dictionary of parameters for the query

    Returns: 
        url: final url for the query by requests.get()

    Purpose: 
        Added this function to get the actual URL printed out for debugging and inspecting
    '''
    def getFinalURL(self, url_header, params):
        url = url_header
        for k, v in params.items():
            # print(k+"="+v)
            url += (k+"="+v+"&")
        url.rstrip("&") #remove the trailing "&"" character
        return url
    


    #########################
    ###    base_request   ###
    #########################
    '''
    Parameters:
        params : dict
        start : pd.Timestamp
        end : pd.Timestamp

    Returns: 
        requests.Response

    Purpose: 

    '''

    def base_request(self, params, start, end):

        start_str = self._datetime_to_str(start)
        end_str = self._datetime_to_str(end)
        base_params = {
            'securityToken': self.api_key,
            'periodStart': start_str,
            'periodEnd': end_str
        }
        # add security token and timestamps to parameters dictionary
        params.update(base_params)

        error = None #?

        # my addition for restructuring and debugging get call
        final_url = self.getFinalURL(BASE_URL, params)
        return final_url
        # print(final_url) # use for debugging
    
#         for _ in range(self.retry_count):
#             # print("start get request, bottleneck?")
#             response = self.session.get(url=final_url, ### MASSIVE BOTTLENECK
#                                         proxies=self.proxies)
#             # print("end get request")
            
#             try:
#                 response.raise_for_status()
#             except requests.HTTPError as e:
#                 error = e
#                 soup = BeautifulSoup(response.text, 'xml')
#                 text = soup.find_all('text')
#                 if len(text):
#                     error_text = soup.find('text').text
#                     if 'No matching data found' in error_text:
#                         self.logger.error('HTTP Error, no data found in %s', error_text)
#                         return None
#                 print("HTTP Error, retrying in {} seconds".format(self.retry_delay))
#                 self.logger.info('HTTP Error, retrying in %s seconds', self.retry_delay)
#                 sleep(self.retry_delay)
#             else:
#                 self.logger.info('HTTP request processed')
#                 return response
#         else:
#             self.logger.info('HTTP request did not succeed after %s retries', self.retry_delay)
#             print("HTTP request did not succed after %s retries", self.retry_delay)
#             return None
# #           raise IOError(error) # or raise Error?




    @staticmethod
    def _datetime_to_str(dtm):
        """
        Convert a datetime object to a string in UTC
        of the form YYYYMMDDhh00

        Parameters
        ----------
        dtm : pd.Timestamp
            Recommended to use a timezone-aware object!
            If timezone-naive, UTC is assumed

        Returns
        -------
        str
        """
        if dtm.tzinfo is not None and dtm.tzinfo != pytz.UTC:
            dtm = dtm.tz_convert("UTC")
        fmt = '%Y%m%d%H00'
        ret_str = dtm.strftime(fmt)
        return ret_str





    def query_price(self, country_code, start, end, as_dataframe=False):
        """
        Parameters
        ----------
        country_code : str
        start : pd.Timestamp
        end : pd.Timestamp
        as_series : bool
            Default False
            If True: Return the response as a Pandas Series
            If False: Return the response as raw XML

        Returns
        -------
        str | pd.Series
        """
        domain = DOMAIN_MAPPINGS[country_code]
        params = {
            'documentType': 'A44', # Price Document, Transmission dah-ahead price
            'in_Domain': domain, 
            'out_Domain': domain
        }
        response = self.base_request(params=params, start=start, end=end)
        if response is None:
            self.logger.info('HTTP request returned nothing')
            return None
        if not as_dataframe:
            self.logger.info('HTTP request processed - XML')
            return response.text
        else:
            series = parsers.parse_prices(response.text)
            series = series.tz_convert(TIMEZONE_MAPPINGS[country_code])
            self.logger.info('HTTP request processed - pandas')
            df = series.to_frame() # ensure working with dataframe and not series
            return df





    def query_generation_forecast(self, country_code, start, end, as_dataframe=False, psr_type=None, squeeze=False):
        """
        Parameters
        ----------
        country_code : str
        start : pd.Timestamp
        end : pd.Timestamp
        as_dataframe : bool
            Default False
            If True: Return the response as a Pandas DataFrame
            If False: Return the response as raw XML
        psr_type : str, 3-letter code (refer to PSR_MAPPINGS)
            filter on a single psr type
        squeeze : bool
            If a single column is requested, return it as a Series instead of a DataFrame
            If there is just a single value, return it as a float

        Returns
        -------
        str | pd.DataFrame
        """

        domain = DOMAIN_MAPPINGS[country_code]
        params = {
            'documentType': 'A69', 	# Wind and solar forecast
            'processType': 'A01', # DayAhead
            'in_Domain': domain,
        }
        if psr_type:
            params.update({'psrType': psr_type})
        response = self.base_request(params=params, start=start, end=end)
        if response is None:
            self.logger.info('HTTP request returned nothing')
            return None
        if not as_dataframe:
            self.logger.info('HTTP request processed - XML')
            return response.text
        else:
            df = parsers.parse_generation(response.text)
            df = df.tz_convert(TIMEZONE_MAPPINGS[country_code])
            if squeeze:
                df = df.squeeze()
            self.logger.info('HTTP request processed - pandas')
            return df





    def query_generation(self, country_code, start, end, as_dataframe=False, psr_type=None, squeeze=False):
        """
        Parameters
        ----------
        country_code : str, 2-letter capitalized code (e.g. RO for Romania)
        start : pd.Timestamp
        end : pd.Timestamp
        as_dataframe : bool
            Default False
            If True: Return the response as a Pandas DataFrame
            If False: Return the response as raw XML
        psr_type : str, 3-letter code (refer to PSR_MAPPINGS)
            filter on a single psr type
        squeeze : bool
            If a single column is requested, return it as a Series instead of a DataFrame
            If there is just a single value, return it as a float

        Returns
        -------
        str | pd.DataFrame
        """

        domain = DOMAIN_MAPPINGS[country_code]
        params = {
            'documentType': 'A75', # Actual generation per type
            'processType': 'A16', # Realised
            'in_Domain': domain,
        }
        if psr_type:
            params.update({'psrType': psr_type}) # filter on one production type if psr_type specified
        # response = self.base_request(params=params, start=start, end=end)
        url = self.base_request(params=params, start=start, end=end)
        return url
        
        # if response is None:
        #     self.logger.info('HTTP request returned nothing')
        #     print("HTTP request returned nothing")
        #     return None
        # if not as_dataframe:
        #     self.logger.info('HTTP request processed - XML')
        #     return response.text
        # else:
        #     # print("Enter parsing zone")
        #     df = parsers.parse_generation(response.content) 
        #     df = df.tz_convert(TIMEZONE_MAPPINGS[country_code])
        #     if squeeze:
        #         df = df.squeeze()
        #     self.logger.info('HTTP request processed - pandas')
        #     return df





    def query_installed_generation_capacity(self, country_code, start, end, as_dataframe=False, psr_type=None, squeeze=False):
        """
        Parameters
        ----------
        country_code : str
        start : pd.Timestamp
        end : pd.Timestamp
        as_dataframe : bool
            Default False
            If True: Return the response as a Pandas DataFrame
            If False: Return the response as raw XML
        psr_type : str
            filter query for a specific psr type
        squeeze : bool
            If a single column is requested, return it as a Series instead of a DataFrame
            If there is just a single value, return it as a float

        Returns
        -------
        str | pd.DataFrame
        """
        domain = DOMAIN_MAPPINGS[country_code]
        params = {
            'documentType': 'A68',  # A68: Installed generation per type, Entso-e: Installed Capacity per Production Type
            'processType': 'A33', #Year ahead
            'in_Domain': domain,
        }
        if psr_type:
            params.update({'psrType': psr_type})
        response = self.base_request(params=params, start=start, end=end)
        if response is None:
            self.logger.info('HTTP request returned nothing')
            return None
        if not as_dataframe:
            self.logger.info('HTTP request processed - XML')
            return response.text
        else:
            df = parsers.parse_generation(response.text)
            df = df.tz_convert(TIMEZONE_MAPPINGS[country_code])
            if squeeze:
                df = df.squeeze()
            self.logger.info('HTTP request processed - pandas')
            return df

