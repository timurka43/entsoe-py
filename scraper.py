# Entso-e scraper
# for years 2015-now...

import pandas as pd
import entsoe as ent
import parsers
import mykey
import mappings
import country_groups


KEY = mykey.get_key() # create mykey.py with get_key method that returns YOUR OWN entso-e api key/token


##########################
### generation_scraper ###
##########################
'''
Inputs:

Outputs:

Purpose:
'''




##########################
### generation_scraper ###
##########################
'''
Inputs: 
    start_year: int (2015 - earliest year available)
    end_year: int (inclusive)
    country_list: list of countries for which to scrape
    name (optinal): name to name the resulting csv file

Outputs:
    csv file: saved into current directory

Purpose:
    scrapes data about energy generation for a specified
    country list and time period. 

Issues/Improvements:
    want to be able to dynamically update this as new data comes out
    without repeating any work that's already done. This could be a 
    separate function that checks the last data available and then
    adds new data to the dataframe
'''
def generation_scraper(start_year, end_year, country_code_list, name=None, append=False):
    
    # name of the file
    if name is not None:
        filename = name+'.xlsx'
    else:
        filename = "generation.xlsx"

    # set the append setting for either creating/overwriting a new excel file
    # or appending to the existing excel file
    if (append):
        mode = 'a'
    else:
        mode = 'w'

    writer = pd.ExcelWriter(filename, mode=mode)


    for country_code in country_code_list:
        
        country = mappings.COUNTRY_MAPPINGS[country_code]
        print(country)


        
        if (country in writer.sheets):
            print(country+' already exists in this excel file. Skipping')
        else:

            xml_country = '<MY_XML>'
            for year in range(start_year, end_year+1):
                print(year)
                df_dates = pd.DataFrame({'year': [year, year+1],
                                'month': [1, 1],
                                'day': [1, 1]})

                start_tm, end_tm = pd.to_datetime(df_dates) # one-year periods separatel
                xml_year = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=False)
                ## keep appending xml texts to each other
                xml_country += xml_year

            xml_country += '</MY_XML>'
            # print(xml_year)  # what do we get for the last year queried?  
            #aggregated generation values for all years for one country in xml_country
            print("Parsing " + country) #QUITE A BOTTLENECK BUT PROBABLY OKAY
            df_country = parsers.parse_generation(xml_country) 
            # df_country = df_country.tz_convert(mappings.TIMEZONE_MAPPINGS[country_code]) # this messes up saving into excel
            # just have naive time values all standardized to UTC

            print("Writing " + country)



            ## record country in a separate sheet:
            df_country.to_excel(writer, sheet_name=country)
        print()
        # finished writing one sheet
        
    
    writer.close() # save excel file after writing sheets

    return





if __name__ == '__main__':

    ent_app = ent.Entsoe(KEY) # my api key/token
    
    
    start = 2015 # 2015 is the earliest year available
    end = 2025 # current year is the latest available

    # time of the day defaults to 00:00

    country_code_list = country_groups.EU1


    generation_scraper(start, end, country_code_list, 'EU_generation', append=False)


