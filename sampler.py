'''
Name: sampler.py
Author: Timur Kasimov
Created: June 2024
Updated: July 2024

Purpose: 
    Allows for resampling of raw country data to generate
    aggregated region data of specified frequency or country
    specific data of specified frequency
'''
import pandas as pd
import os

import mappings
import country_groups


###################
### resample_df ###
###################
'''
Inputs:
    df: pandas data frame
    freq: pandas-supported frequency (e.g. '1M')

Outputs: 
    df: pandas data frame

Purpose:
    resamples the data in df to a specified frequency
'''
def resample_df(df, freq):
    # print(df.head(2))

    df.index = df['Unnamed: 0'] # set index for the df
    df = df.drop('Unnamed: 0', axis=1) # drop timestamp from the explicit columns to perform resampling

    df = df.resample(freq).sum() # resample
    # print(df.head(10))

    return df 


############################
### record_new_frequency ###
############################
'''
Inputs:
    country_codes: list
    freq: pandas-supported frequency (e.g. '1M')
    start_year: int
    end_year: int
    append: Bool

Outputs: 
    saves xlsx files in the frequency folder (e.g. ./data/1M)

Purpose:
    records desired frequncy for specified countries in a respective folder
'''
def record_new_frequency(country_codes, freq, start_year, end_year, append=True):

    for country_code in country_codes: 

        country = mappings.COUNTRY_MAPPINGS[country_code] # get country name from its code
        print(country)


        dfs_country = pd.read_excel(country+'.xlsx', sheet_name=None) # read raw data for the country
        #dfs_country is a dictionary with sheets as keys and dfs as values 
        
        # create new filename that displays frequency
        filename = country + ' ' + freq + '.xlsx'

        # need the folder in the directory for specified frequency 
        if not os.path.isdir(freq):
            os.mkdir(freq)

        # initialize writer to create new or update existing files
        if (append):
            writer = pd.ExcelWriter('./'+freq+'/'+filename, mode='a', if_sheet_exists='replace')
        else:
            writer = pd.ExcelWriter('./'+freq+'/'+filename, mode='w')

        # every excel sheet is just one year
        # this design causes some problems with weeks as weeks don't cut off evenly on each year's start/end 
        for sheet in range(start_year, end_year+1):
            sheet = str(sheet) #manage types
            df = dfs_country[sheet] # pull year-specific dataframe

            if not df.empty:
                df = resample_df(df, freq) # save the resampled dataframe back into dictionary

            df.to_excel(writer, sheet_name=sheet)
        
        writer.close()
    return 



########################
### aggregate_region ###
########################
'''
Inputs:
    country_codes: list
    freq: pandas-supported frequency (e.g. '1M')
    start_year: int
    end_year: int
    name: str

Outputs: 
    saves xlsx file in the combined folder for the name/region

Purpose:
    records desired frequncy for specified region 
'''
def aggregate_region(country_codes, freq, start_year, end_year, name):
    # create a filename based on region's name and specified frequency
    filename = name + ' ' + freq + '.xlsx'

    # designed to have combined folder for region specific data
    if not os.path.isdir('combined'):
        os.mkdir('combined')

    writer = pd.ExcelWriter('./'+ 'combined' +'/'+filename, mode='w')

    for year in range(start_year, end_year+1):
        print(year)
        sheet = str(year) #manage types
    
        df_year = pd.DataFrame

        for country_code in country_codes:

            country = mappings.COUNTRY_MAPPINGS[country_code]
            # print(country)

            sheet_country = pd.read_excel('./' + freq + '/' + country + ' ' + freq +'.xlsx', sheet_name=sheet)
            
            if (not df_year.empty):
                if (not sheet_country.empty):
                    df_year = combine_sheets(df_year, sheet_country)
                    # add country and year specific values to the aggregated df_year
                    # note there may be new columns
                    # do it column wise?
                    # print()
            else:
                df_year = sheet_country # first country
                df_year.index = df_year['Unnamed: 0']
                df_year = df_year.drop('Unnamed: 0', axis=1)


        df_year.to_excel(writer, sheet_name=sheet)
            
    writer.close()

    return
    


######################
### combine_sheets ###
######################
'''
Inputs:
    region_year: pandas df
    country_year: pandas df

Outputs: 
    region_year: pandas df

Purpose:
    adds country and year specific values to the aggregated region values
'''
def combine_sheets(region_year, country_year):
    country_year.index = country_year['Unnamed: 0']
    country_year = country_year.drop('Unnamed: 0', axis=1)

    region_year = region_year.add(country_year, fill_value=0)

    return region_year 




############
### MAIN ###
############
if __name__ == '__main__':

    # country_codes = country_groups.EU
    country_codes = ['RO']
    freq = '1M'
    start_year = 2015
    end_year = 2024


    # #########################################################
    # ### RUN THIS ONLY WHEN UPDATING COUNTRY-SPECIFIC DATA ###
    # #########################################################
    # # record new frequency for each country in a respective folder
    # # SHOULD BE APPENDING ONLY AFTER INITIAL RUNS
    record_new_frequency(country_codes, freq, start_year, end_year, append=True)


    
    # # records combined values for the region in the ./combined folder
    aggregate_region(country_codes, freq, 2015, 2024, name='Romania') # rather change years manually here
