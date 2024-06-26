
import pandas as pd
import os

import mappings
import country_groups



def resample_df(df, freq):
    # print(df.head(2))

    #solve the issue of empty dataframe
    df.index = df['Unnamed: 0'] # set index for the df
    df = df.drop('Unnamed: 0', axis=1) # drop timestamp from the explicit columns to perform resampling

    df = df.resample(freq).sum() # resample
    # print(df.head(10))

    return df 



def record_new_frequency(country_codes, freq, start_year, end_year, append=True):

    for country_code in country_codes:

        country = mappings.COUNTRY_MAPPINGS[country_code]
        print(country)


        dfs_country = pd.read_excel(country+'.xlsx', sheet_name=None)
        #dfs_country is a dictionary with sheets as keys and dfs as values 
        
        filename = country + ' ' + freq + '.xlsx'

        if not os.path.isdir(freq):
            os.mkdir(freq)



        if (append):
            writer = pd.ExcelWriter('./'+freq+'/'+filename, mode='a', if_sheet_exists='replace')
        else:
            writer = pd.ExcelWriter('./'+freq+'/'+filename, mode='w')

        
        for sheet in range(start_year, end_year+1):
            sheet = str(sheet) #manage types
            df = dfs_country[sheet] # pull year-specific dataframe

            if not df.empty:
                df = resample_df(df, freq) # save the resampled dataframe back into dictionary


            df.to_excel(writer, sheet_name=sheet)
        
        writer.close()
    return 




# def test_pull():


    
#     df = pd.read_excel('test2.xlsx', sheet_name='Romania')

#     df.index = df['Unnamed: 0']

#     df =  df.drop('Unnamed: 0', axis=1)

#     df = df.resample('3h').sum()


#     return


def aggregate_region(country_codes, freq, start_year, end_year, name):

    filename = name + ' ' + freq + '.xlsx'

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
    






def combine_sheets(region_year, country_year):
    country_year.index = country_year['Unnamed: 0']
    country_year = country_year.drop('Unnamed: 0', axis=1)

    region_year = region_year.add(country_year, fill_value=0)

    return region_year 






if __name__ == '__main__':

    country_codes = country_groups.EU
    # country_codes = ['PL', 'PT']
    freq = '1D'
    start_year = 2015
    end_year = 2024


    record_new_frequency(country_codes, freq, start_year, end_year, append=False)

    aggregate_region(country_codes, freq, start_year, end_year, 'EU')
