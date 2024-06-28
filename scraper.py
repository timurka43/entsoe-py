'''
Name: scraper.py
Author: Timur Kasimov
Created: June 2024
Updated: June 2024

Purpose: Scrapes generation data from ENTSO-E Transparency Platform
'''

import pandas as pd
import entsoe as ent
import parsers
import mykey
import mappings
import country_groups

# libraries needed for syncronous get calls
import aiohttp
import asyncio


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
def generation_scraper(start_year, end_year, country_code_list, appending_data=True):
    
    for country_code in country_code_list:
 
        country = mappings.COUNTRY_MAPPINGS[country_code]
        print(country)

        # name of the file
        filename = country+".xlsx"

        # set the append setting for either creating/overwriting a new excel file
        # or appending to the existing excel file
        if (appending_data):
            writer = pd.ExcelWriter(filename, mode='a', if_sheet_exists='replace' )
        else:
            writer = pd.ExcelWriter(filename, mode='w' )


        urls = []
        # get all urls first
        for year in range(start_year, end_year+1):
            # print(year)
            df_dates = pd.DataFrame({'year': [year, year+1],
                            'month': [1, 1],
                            'day': [1, 1]})

            start_tm, end_tm = pd.to_datetime(df_dates) # one-year periods separatel

            # get all urls first?
            url = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=False)
            urls.append(url)
            

            # xml_year = ent_app.query_generation(country_code, start_tm, end_tm, as_dataframe=False)
        # print("got all urls")



        # now collect responses from all get calls
        loop = asyncio.get_event_loop()
        xml_responses = loop.run_until_complete(fetch_all(urls))

        print("completed all get requests")


        year = start_year
        # now parse through each xml response
        for xml_year in xml_responses:
            print("Parsing " + str(year))

            # xml text output (open in notepad or the likes) for debugging
            file = open('./xmls/' + country+' '+str(year), 'w', encoding='utf-8')
            file.write(xml_year)

            df_year = parsers.parse_generation(xml_year) # BOTTLENECK WITH LONGER XML STRINGS

            # print("Writing " + str(year))

            ## record each year in a separate sheet:
            df_year.to_excel(writer, sheet_name=str(year))
            year += 1
        
        print()
        # finished writing one sheet
        writer.close() # save excel file after writing sheets
        #finished one country

    # finished all countries
    return




async def fetch(session, url):
    # print("GET START")
    async with session.get(url) as response:
        print("GET returning??")
        return await response.text()

async def fetch_all(urls):
    timeout = aiohttp.ClientTimeout(total=1200) # 1200 seconds = 20 minutes for 10 get simultaneous get requests
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [asyncio.create_task(fetch(session, url)) for url in urls]
        # print("AWAITING")
        responses = await asyncio.gather(*tasks)
        # print("recorded in fetch_all")
        return responses


if __name__ == '__main__':

    ent_app = ent.Entsoe(KEY) # my api key/token
    
    
    start = 2015 # 2015 is the earliest year available
    end = 2024 # current year is the latest available

    # time of the day defaults to 00:00

    country_code_list = country_groups.EU
    # country_code_list = []
    
 
    #
    generation_scraper(start, end, country_code_list, appending_data=True)

    