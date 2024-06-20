"""
parser
======

parse XML document and time series data from Entso-e API into a pandas data
frame.
"""

import logging
import bs4
import pandas as pd



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



logger = logging.getLogger(__name__ +'-api')
logger.addHandler(logging.NullHandler())
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

def _extract_timeseries(xml_text):
    """
    Parameters
    ----------
    xml_text : str

    Yields
    -------
    bs4.element.tag
    """
    if not xml_text:
        print("NOT XML TEXT")
        return
    soup = bs4.BeautifulSoup(xml_text, 'xml')
    for timeseries in soup.find_all('TimeSeries'):
        yield timeseries




def parse_prices(xml_text):
    """
    Parameters
    ----------
    xml_text : str

    Returns
    -------
    pd.Series
    """
    series = pd.Series()
    for soup in _extract_timeseries(xml_text):
        series = series._append(_parse_price_timeseries(soup))
    series = series.sort_index() # can potentially get away without sorting as everything should be sorted already
    return series




def parse_generation(xml_text):
    """
    Parameters
    ----------
    xml_text : str

    Returns
    -------
    pd.DataFrame
    """
    all_series = {} # initialize all series as a dictionary
    for soup in _extract_timeseries(xml_text):

        #produce a single ts for one production type and the specified interval
        ts = _parse_generation_forecast_timeseries(soup)

        series = all_series.get(ts.name)
        if series is None:
            all_series[ts.name] = ts 
        else:
            series = series._append(ts)  
            series.sort_index()
            all_series[series.name] = series
    # put together all series into a single dataframe
    df = pd.DataFrame.from_dict(all_series)
    return df



def _parse_price_timeseries(soup):
    """
    Parameters
    ----------
    soup : bs4.element.tag

    Returns
    -------
    pd.Series
    """
    positions = []
    prices = []
    for point in soup.find_all('Point'):
        positions.append(int(point.find('position').text))
        prices.append(float(point.find('price.amount').text))

    series = pd.Series(index=positions, data=prices)
    series = series.sort_index()
    series.index = _parse_datetimeindex(soup)

    return series



def _parse_generation_forecast_timeseries(soup):
    """
    Parameters
    ----------
    # soup : bs4.element.tag

    Returns
    -------
    pd.Series
    """
    # soup is just one timeseries
    psrtype = soup.find('psrType').text
    production_type = 'Generation'
    
    # consumption case
    is_out = soup.find('outBiddingZone_Domain.mRID')
    if is_out is not None:
        production_type  = 'Consumption'
        
    positions = []
    quantities = []
    # record each quantity with corresponding position
    for point in soup.find_all('Point'):
        position = point.find('position')
        quantity = point.find('quantity')
        if (position is not None):
            positions.append(int(position.text))
        if (quantity is not None):
            quantities.append(float(quantity.text))

    series = pd.Series(index=positions, data=quantities)
    series = series.sort_index() # is this line even necessary?

    # negate consumption values for plotting
    if (production_type == 'Consumption'):
        series *= -1


    # replaces df's series' indices with time stamps 
    series.index = _parse_datetimeindex(soup)



    #name the series according to production type
    series.name = PSRTYPE_MAPPINGS[psrtype]  + ' ' + production_type
    return series



def _parse_datetimeindex(soup):
    """
    Create a datetimeindex from a parsed beautifulsoup,
    given that it contains the elements 'start', 'end'
    and 'resolution'

    Parameters
    ----------
    soup : bs4.element.tag

    Returns
    -------
    pd.DatetimeIndex
    """
    start = pd.Timestamp(soup.find('start').text.rstrip("Z")) #manually remove UTC's timezone info
    end = pd.Timestamp(soup.find('end').text.rstrip("Z"))
    delta = _resolution_to_timedelta(res_text=soup.find('resolution').text) #specified time interval between points
    logger.info('delta is %s', delta)
    # index = pd.date_range(start=start, end=end, freq=delta, closed='left')
    index = pd.date_range(start=start, end=end, freq=delta, inclusive='left') # replaces df's series' indices with time stamps in increments on delta
    return index



def _resolution_to_timedelta(res_text):
    """
    Convert an Entsoe resolution to something that pandas can understand

    Parameters
    ----------
    res_text : str

    Returns
    -------
    str
    """
    if res_text == 'PT15M':
        delta = '15min'
    elif res_text == 'PT60M':
        delta = '60min'
    elif res_text == 'P1Y':
        delta = '12M'
    elif res_text == 'PT30M':
        delta = '30min'
    else:
        raise NotImplementedError("Sorry, I don't know what to do with the "
                                  "resolution '{}', because there was no "
                                  "documentation to be found of this format "
                                  "everything is hard coded. Please open an "
                                  "issue.".format(res_text))
    return delta
