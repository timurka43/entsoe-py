import pandas as pd
import os
import matplotlib.pyplot as plt

import mappings
import country_groups
import psr_groups


def max(combined_df):
    max_df = combined_df.groupby(level=1).max()

    filename = './combined/' + region + ' ' + freq + ' ' + str(start_year) + '-' + str(end_year) + ' '+ 'max.xlsx'
    writer = pd.ExcelWriter(filename, mode='w')
    max_df.to_excel(writer)
    writer.close()

    return max_df

def min(combined_df):
    min_df = combined_df.groupby(level=1).min()

    filename = './combined/' +  region + ' ' + freq + ' ' + str(start_year) + '-' + str(end_year) + ' '+ 'min.xlsx'
    writer = pd.ExcelWriter(filename, mode='w')
    min_df.to_excel(writer)
    writer.close()

    return min_df

def mean(combined_df):
    # combined_df =pd.DataFrame
    mean_df = combined_df.groupby(level=1).mean()

    filename = './combined/' +  region + ' ' + freq + ' ' + str(start_year) + '-' + str(end_year) + ' '+ 'mean.xlsx'
    writer = pd.ExcelWriter(filename, mode='w')
    mean_df.to_excel(writer)
    writer.close()

    return mean_df



def get_combined_df(region, freq, start, end):

    df_dict = {}
    for year in range(start, end+1):
        df_dict[year] = pd.read_excel('./combined/' + region + ' ' + freq + '.xlsx', sheet_name=str(year))

    # index all dataframes with sequential integers
    for key, df in df_dict.items():

        df.index = (val+1 for val in df.index) # make index start from 1
        df = df.drop('Unnamed: 0', axis=1)
        df_dict[key] = df

    # i think concat just does all years, not the specified ones
    # SOLVED: only keep the necessary years in df_dict from the beginning
    combined_df = pd.concat(df_dict.values(), keys=df_dict.keys())
    return combined_df




def my_plot(region, freq, psr_codes, type_name, range=None, years=None):
    '''
    inputs:
    ________
    region: str
    freq: str
    psr_codes: list
    type_name: str
    range: tuple of shape (year1, year2)
    years: list
    '''

    basename = './combined/' + region + ' ' + freq

    # put all psr types in a list
        # note this is implemented for generation only. 
    columns = []
    for code in psr_codes:
        column = mappings.PSRTYPE_MAPPINGS[code] +' Generation'
        columns.append(column)
    

    plt.figure(figsize=(10,10))

    if range is not None:
        # access min, max, mean data
        range_str = str(range[0]) + '-' + str(range[1])
        filename = basename + ' ' + range_str
        df_max = pd.read_excel(filename + ' max.xlsx')
        df_min = pd.read_excel(filename + ' min.xlsx')
        df_mean = pd.read_excel(filename + ' mean.xlsx')

        # add together requested psr types into one column

        # sums up max/min for each respective production type, where each production type max can come from different year!!!!!
        #so when you combine multiple production types, your max,min spread becomes obsolete
        # need different max-min pullers that first aggregate geneation per year based on requested psr group
        # and then find min/max
        # mean should be fine though
        df_max[type_name] = df_max[columns].sum(axis=1) 
        df_min[type_name] = df_min[columns].sum(axis=1)
        df_mean[type_name] = df_mean[columns].sum(axis=1)

        #plot

        #plot mean line
        plt.plot(df_mean.index+1, df_mean[type_name], label=range_str + ' Mean', color='green')

        #plot min_max spread
        plt.fill_between(df_max.index+1, df_max[type_name], df_min[type_name], color='grey', alpha=0.3, label=range_str + ' Min-Max Spread')



    if years is not None:
        for year in years:
            # access respective frequency file, year
            df = pd.read_excel(basename + '.xlsx', sheet_name=str(year))
            # add together requested psr types into one df
            df[type_name] = df[columns].sum(axis=1)
            # plot that year and psr group
            # print(df.index)
            plt.plot(df.index+1, df[type_name], label=type_name + ' ' + str(year))
    


    plt.xlabel(mappings.FREQUENCY_MAPPINGS[freq])
    plt.ylabel('[MW]')
    plt.title(region + ' ' + type_name + ' Generation')
    plt.legend() # put the legend outside the main frame

    # Show the plot
    plt.show()

    return




if __name__ == '__main__':

    # country_codes = country_groups.EU
    # country_codes = ['PL', 'PT']
    region = 'EU' # name of the region as saved in excel files
    freq = '1M' 
    start_year = 2015
    end_year = 2023

    # head = 60


    # psr_codes = psr_groups.SOLAR_WIND
    psr_codes = ['B18']
    psr_label = 'Biomass'


    # required for max, min, mean data frames
    combined_df = get_combined_df(region, freq, start_year, end_year)

    # both returns and plots respective dfs
    max_df = max(combined_df)
    min_df = min(combined_df)
    mean_df = mean(combined_df).convert_dtypes(convert_floating=True)


    my_plot(region, freq, psr_codes, psr_label, range=(start_year, end_year), years=range(2015, 2025))
    # min_max spread doesn't add up, check what's wrong
    # doesn't quite add up when using more than one psr_code in psr_codes
    


