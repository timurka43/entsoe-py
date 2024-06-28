'''
Author: Bertfried Fauser
Contributor: Timur Kasimov
Created: 2017? by Author
Updated: June 2024 by Contributor

Purpose: 
    Defining lists of various country groups/ regions 
    for data grouping and subsequent data generation
'''


import logging
import pytz
import requests
from bs4 import BeautifulSoup
from time import sleep
import parsers
import mappings

__title__ = "entsoe-py"
__version__ = "0.1.12"
__author__ = "EnergieID.be"
__license__ = "MIT"

BASE_URL = 'https://web-api.tp.entsoe.eu/api?'


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
        # print(url)
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
        domain = mappings.DOMAIN_MAPPINGS[country_code]
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
            series = series.tz_convert(mappings.TIMEZONE_MAPPINGS[country_code])
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

        domain = mappings.DOMAIN_MAPPINGS[country_code]
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
            df = df.tz_convert(mappings.TIMEZONE_MAPPINGS[country_code])
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

        domain = mappings.DOMAIN_MAPPINGS[country_code]
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
        #     df = df.tz_convert(mappings.TIMEZONE_MAPPINGS[country_code])
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
        domain = mappings.DOMAIN_MAPPINGS[country_code]
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
            df = df.tz_convert(mappings.TIMEZONE_MAPPINGS[country_code])
            if squeeze:
                df = df.squeeze()
            self.logger.info('HTTP request processed - pandas')
            return df

