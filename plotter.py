import pandas as pd
import os
import matplotlib.pyplot as plt

import mappings
import country_groups
import psr_groups

 
def get_combined_df(region, freq, start, end, columns, type_name):

    df_dict = {}
    # record each year's combined production values in a dictionary to then find min, max, mean
    for year in range(start, end+1):
        df_year = pd.read_excel('./combined/' + region + ' ' + freq + '.xlsx', sheet_name=str(year))
        # add columns for combined production based on psr groups (columns)
        
        existing_columns = [col for col in columns if col in df_year.columns] # this should fix the issue of a region not having certain production tyeps

        df_year[type_name] = df_year[existing_columns].sum(axis=1)
        df_dict[year] = df_year

    # index all dataframes with sequential integers
        # this is okay for days (365 or 366) and months (12) but a
        # little problematic for weeks (mostly gives 53 instead of 52 and cuts off 
        # first and last week weirdly)
    for key, df in df_dict.items():
        df = df.drop('Unnamed: 0', axis=1) # this might be unnecessary now since only storing one column
        df_dict[key] = df

    # i think concat just does all years, not the specified ones
    # SOLVED: only keep the necessary years in df_dict from the beginning
    combined_df = pd.concat(df_dict.values(), keys=df_dict.keys())
    return combined_df


def max(combined_df):
    max_df = combined_df.groupby(level=1).max()
    return max_df

def min(combined_df):
    min_df = combined_df.groupby(level=1).min()
    return min_df

def mean(combined_df):
    # combined_df =pd.DataFrame
    mean_df = combined_df.groupby(level=1).mean()
    return mean_df



def my_plot(region, freq, psr_codes, type_name, range=None, years=None, output_table_file=False):
    '''
    inputs:
    ________
    region: str
    freq: str
    psr_codes: list
    type_name (custom): str
    range (for mean and min-max spread): tuple of shape (year1, year2)
    years (for individual lines): list
    '''

    basename = './combined/' + region + ' ' + freq
    title = region + ' ' + type_name + ' Generation'
    if range is not None:
        range_str = str(range[0]) + '-' + str(range[1])
    else:
        range_str = ''
   
    

    # put all psr types in a list
        # note this is implemented for generation only. 
    columns = []
    for code in psr_codes:
        column = mappings.PSRTYPE_MAPPINGS[code] +' Generation'
        columns.append(column)
    

    plt.figure(figsize=(10,10))

    # FOR SAVING EXCEL FILE
    if not os.path.isdir('plots'):
        os.mkdir('plots')

    writer = pd.ExcelWriter(('./plots/' + title + ' ' + freq + ' ' + range_str + ' spread' + '.xlsx'), mode='w')
    df_to_excel = pd.DataFrame()


    # PLOTTING SPREAD
    
    if range is not None:
        #derive min, max, mean for the specific psr group
        psr_totals_df = get_combined_df(region, freq, range[0], range[1], columns, type_name)

        # access min, max, mean data
        df_max = max(psr_totals_df)
        df_min = min(psr_totals_df)
        df_mean = mean(psr_totals_df)

        #plot

        #plot mean line
        plt.plot(df_mean.index+1, df_mean[type_name]/1000, label=range_str + ' Mean', color='green')

        #plot min_max spread
        plt.fill_between(df_max.index+1, df_max[type_name]/1000, df_min[type_name]/1000, color='grey', alpha=0.3, label=range_str + ' Min-Max Spread')

        df_to_excel['Mean [GWh]'] = df_mean[type_name]/1000
        df_to_excel['Max [GWh]'] = df_max[type_name]/1000
        df_to_excel['Min [GWh]'] = df_min[type_name]/1000
    # END PLOTTING SPREAD

    # PLOTTING YEARS
    if years is not None:
        for year in years:
            # access respective frequency file, year
            df = pd.read_excel(basename + '.xlsx', sheet_name=str(year))
            # add together requested psr types into one df
            existing_columns = [col for col in columns if col in df.columns]
            df[type_name] = df[existing_columns].sum(axis=1)
            # plot that year and psr group
            # print(df.index)
            plt.plot(df.index+1, df[type_name]/1000, label=str(year))

            df_to_excel[str(year) + ' [GWh]'] = df[type_name]/1000
    # END PLOTTING YEARS
    
    time_int = mappings.FREQUENCY_MAPPINGS[freq]

    plt.xlabel(time_int)
    plt.ylabel('GWh/'+time_int)
    plt.title(title)
    plt.legend() # put the legend outside the main frame
    
    #save the plot 
    plt.savefig('./plots/'+ title + ' ' + freq + ' ' + range_str + ' spread')
    # Show the plot
    

    if output_table_file:
        df_to_excel.to_excel(writer)
    writer.close()

    plt.show()

    return




if __name__ == '__main__':

    ### REGION ###
    region = 'Romania'   # name of the combined region as saved in excel files
    freq = '1M'     # frequency as saved in excel files


    ### YEARS FOR MIN-MAX SPREAD, MEAN LINE ###
    start_spread = 2015     
    end_spread = 2023   


    ### GENERATION TYPE/GROUP ###
    psr_codes = psr_groups.TOTAL # group for type of generation (see psr_groups.py and mappings.py)
    psr_label = 'Total' # custom label


    ### YEAR-SPECIFIC LINES ###
    start_year = 2020
    end_year =2024



    ### call to plot ###
    my_plot(region, freq, psr_codes, psr_label, range=(start_spread, end_spread), years=range(start_year, end_year+1), output_table_file=True)

    


