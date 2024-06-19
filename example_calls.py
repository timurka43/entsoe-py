import matplotlib.pyplot as plt
import pandas as pd
import entsoe as ent
import parsers
import mykey
import mappings


# # need these imports???
# import os
# import sys
# nb_dir = os.path.split(os.getcwd())[0]
# if nb_dir not in sys.path:
#     sys.path.append(nb_dir)

KEY = mykey.get_key() # create mykey.py with get_key method that returns YOUR OWN entso-e api key/token

ent_app = ent.Entsoe(KEY) # my api key/token


##########################
### PLOTTING CONSTANTS ###
##########################
FIG_DIMENSION = (15,7)


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


EU_COUNTRY_CODES = ['AT', 'BE', 'BG', 'HR', 'CY',
                    'CZ', 'DK', 'EE', 'FI', 'FR',
                    'DE', 'GR', 'HU', 'IE', 'IT',
                    'LV', 'LT', 'LU', 'MT', 'NL',
                    'PL', 'PT', 'RO', 'SK', 'SI',
                    'ES', 'SE']




# TOP_TEN_CONSUMERS



# df_energy = ent_app.query_price('RO', start_tm, end_tm, as_dataframe=True)
# df_energy = ent_app.query_generation_forecast('RO', start_tm, end_tm, as_dataframe=True)
# df = ent_app.query_generation('RO', start_tm, end_tm, as_dataframe=True)
# df_energy = ent_app.query_installed_generation_capacity('RO', start_tm, end_tm, as_dataframe=True)
''' NOTES ON THE FOUR METHODS ABOVE


method():
    What each one procures,
    * what needs to be fixed/extended


query_price():
    Price document - Transmission day ahead prices


query_generation_forecast():
    Wind and solar forecast for a day ahead

query_generation():
    Actual generation per production type, realised


query_installed_generation_capacity 
    Installed Capacity per Production Type (year ahead?)
    * probably needs a different kind of graph for one-data point per year per generation type, consider pie-chart?

    

all methods localize the time zone to the specified country, assuming the original is in UTC (which entso-e now provides by default).
    * can comment out tz.convert in all methods to standardize the time to UTC if needed.

    

'''





def price(country_code, start, end, freq, df_raw=None):
    country = COUNTRY_MAPPINGS[country_code]

    if df_raw is None:

        start_tm = pd.to_datetime(start)
        end_tm = pd.to_datetime(end)
        
        df_raw = ent_app.query_price(country_code, start_tm, end_tm, as_dataframe=True)

    df = df_raw.resample(freq).mean()
    # print(df.head)

    fig = plt.rcParams["figure.figsize"] = FIG_DIMENSION
    df.plot()
    plt.suptitle('Mean Electricity Price in ' + country)
    plt.ylabel('Mean Price per MTU Over '+ freq+ ' [EUR/MWh]')
    plt.xlabel('Time')
    # plt.legend(title="Production Type", loc='upper left', reverse=True)
    plt.savefig('Electricity Price in ' + country + ', ' + start + ' - ' + end +', '+freq)
    # plt.show()
    plt.close()

    return df_raw





def generation_forecast(country_code, start, end, freq, df_raw=None):
    country = COUNTRY_MAPPINGS[country_code]

    if df_raw is None:

        start_tm = pd.to_datetime(start)
        end_tm = pd.to_datetime(end)
        
        df_raw = ent_app.query_generation_forecast(country_code, start_tm, end_tm, as_dataframe=True)

    df = df_raw.resample(freq).sum()
    # print(df.head)

    fig = plt.rcParams["figure.figsize"] = FIG_DIMENSION
    df.plot.area()
    plt.suptitle('Electricity Generation Forecast in ' + country)
    plt.ylabel('Generation per '+ freq+ ' [MW]')
    plt.xlabel('Time')
    plt.legend(title="Production Type", loc='upper left', reverse=True)
    plt.savefig('Electricity Generation Forecast in ' + country + ', ' + start + ' - ' + end +', '+freq)
    # plt.show()
    plt.close()

    return df_raw





def generation(country_code, start, end, freq, df_raw=None, psr=None):
    country = COUNTRY_MAPPINGS[country_code]

    if df_raw is None:

        start_tm = pd.to_datetime(start)
        end_tm = pd.to_datetime(end)
        
        df_raw = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=True, psr_type=psr)


    df = df_raw.resample(freq).sum()
    # print(df.head)

    fig = plt.rcParams["figure.figsize"] = FIG_DIMENSION
    df.plot.area()

    if psr is None:
        plt.suptitle('Electricity Generation by Production Type in ' + country)
    else:
        plt.suptitle('Electricity Generation by ' + ent.PSRTYPE_MAPPINGS[psr] + ' in ' + country)
    plt.ylabel('Actual Aggregated per '+ freq+ ' [MW]')
    plt.xlabel('Time')


    # figure out a way to position the legend outside the plot
    # might need to shrink the x-axis and then position legend
    # on center left, using bb anchor or smth
    
    plt.legend(title="Production Type", loc='upper left', reverse=True)
    if psr is None:
        plt.savefig('Electricity Generation by Production Type in ' + country + ', ' + start + ' - ' + end +', '+freq)
    else:
        plt.savefig('Electricity Generation by '+ ent.PSRTYPE_MAPPINGS[psr] + ' in ' + country + ', ' + start + ' - ' + end +', '+freq)
    # plt.show()
    plt.close()

    return df_raw






def capacity(country_code, start, end, freq, df_raw=None):

    return df_raw








def generation_wind_solar(country_code, start, end, freq, df_raw=None):
    
    country = COUNTRY_MAPPINGS[country_code]

    if df_raw is None:

        start_tm = pd.to_datetime(start)
        end_tm = pd.to_datetime(end)
        
        # separately generate wind, solar dataframes
        df_raw = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=True, psr_type='B16')
        df_raw2 = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=True, psr_type='B18')
        df_raw3 = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=True, psr_type='B19')
        # combine them into one dataframe

        for col_name in df_raw2.columns:
            df_raw[col_name] = df_raw2[col_name]
        
        for col_name in df_raw3.columns:
            df_raw[col_name] = df_raw3[col_name]        


    df = df_raw.resample(freq).sum()
    # print(df.head)

    fig = plt.rcParams["figure.figsize"] = FIG_DIMENSION
    df.plot.area()
    plt.suptitle('Electricity Generation by Wind and Solar in ' + country)
    plt.ylabel('Actual Aggregated per '+ freq+ ' [MW]')
    plt.xlabel('Time')


    # figure out a way to position the legend outside the plot
    # might need to shrink the x-axis and then position legend
    # on center left, using bb anchor or smth
    
    plt.legend(title="Production Type", loc='upper left', reverse=True)
    plt.savefig('Electricity Generation by Wind and Solar in ' + country + ', ' + start + ' - ' + end +', '+freq)
    # plt.show()
    plt.close()

    return df_raw




# aggregates generation values for 27 EU countries
def EU_generation(start, end, freq, df_raw=None, psr=None):
    
    if df_raw is None:

            start_tm = pd.to_datetime(start)
            end_tm = pd.to_datetime(end)

            df_raw = pd.DataFrame()
    
            for country_code in EU_COUNTRY_CODES:
                
                print(COUNTRY_MAPPINGS[country_code])

                df_raw1 = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=True, psr_type=psr)


                all_columns = df_raw1.columns.union(df_raw)



    df = df_raw.resample(freq).sum()
    # print(df.head)

    fig = plt.rcParams["figure.figsize"] = FIG_DIMENSION
    df.plot.area()

    if psr is None:
        plt.suptitle('Electricity Generation by Production Type in EU')
    else:
        plt.suptitle('Electricity Generation by ' + ent.PSRTYPE_MAPPINGS[psr] + ' in  EU')
    plt.ylabel('Actual Aggregated per '+ freq+ ' [MW]')
    plt.xlabel('Time')


    # figure out a way to position the legend outside the plot
    # might need to shrink the x-axis and then position legend
    # on center left, using bb anchor or smth
    
    plt.legend(title="Production Type", loc='upper left', reverse=True)
    if psr is None:
        plt.savefig('Electricity Generation by Production Type in EU, ' + start + ' - ' + end +', '+freq)
    else:
        plt.savefig('Electricity Generation by '+ ent.PSRTYPE_MAPPINGS[psr] + ' in EU, ' + start + ' - ' + end +', '+freq)
    # plt.show()
    plt.close()

    return df_raw







if __name__ == '__main__':
    
    # time of the day defaults to 00:00
    start = '2024-01-01'
    end = '2024-05-31'
    # MAX PERIOD ALLOWED IS 1 YEAR
        # will have to later adjust this by concating dataframes

    country_code = 'RO'


    # electricity generation BY SOURCE, hourly, daily, weekly, monthly sums
    df_generation = generation(country_code, start, end, '1h')
    generation(country_code, start, end, '1D', df_generation)
    generation(country_code, start, end, '1W', df_generation)
    generation(country_code, start, end, '1ME', df_generation)


    # electricity generation FORECAST, hourly, daily, weekly, monthly sums
    df_forecast = generation_forecast(country_code, start, end, '1h')
    generation_forecast(country_code, start, end, '1D', df_forecast)
    generation_forecast(country_code, start, end, '1W', df_forecast)
    generation_forecast(country_code, start, end, '1ME', df_forecast)
    

    # electricity PRICE; hourly, daily, weekly, monthly means
    df_price = price(country_code, start, end, '1h')
    price(country_code, start, end, '1D', df_price)
    price(country_code, start, end, '1W', df_price)
    price(country_code, start, end, '1ME', df_price)


    # electricity generation by SOLAR, hourly, daily, weekly, monthly sums
    df_generation = generation(country_code, start, end, '1h', psr='B16')
    generation(country_code, start, end, '1D', df_generation, psr='B16')
    generation(country_code, start, end, '1W', df_generation, psr='B16')
    generation(country_code, start, end, '1ME', df_generation, psr='B16')


    # electricity generation by WIND ONSHORE, hourly, daily, weekly, monthly sums
    df_generation = generation(country_code, start, end, '1h', psr='B19')
    generation(country_code, start, end, '1D', df_generation, psr='B19')
    generation(country_code, start, end, '1W', df_generation, psr='B19')
    generation(country_code, start, end, '1ME', df_generation, psr='B19')

    # electricity generation by SOLAR+WIND:
    df_solarwind = generation_wind_solar(country_code, start, end, '1h')
    df_solarwind = generation_wind_solar(country_code, start, end, '1D', df_solarwind)
    df_solarwind = generation_wind_solar(country_code, start, end, '1W', df_solarwind)
    df_solarwind = generation_wind_solar(country_code, start, end, '1ME', df_solarwind)


    # EU electricity generation
