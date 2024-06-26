import pandas as pd
import os
import matplotlib.pyplot as plt

import mappings
import country_groups
import psr_groups


def max(region, freq, start, end, psr_codes):
    

    return

def min(region, freq, start, end, psr_codes):
    return

def mean(region, freq, start, end, psr_codes):
    return






if __name__ == '__main__':

    # country_codes = country_groups.EU
    # country_codes = ['PL', 'PT']
    region = 'EU'
    freq = '1M'
    start_year = 2015
    end_year = 2023
    psr_codes = psr_groups.SOLAR_WIND

    df = min(region, freq, start_year, end_year, psr_codes)
