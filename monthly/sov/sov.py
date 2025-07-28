import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from datetime import date, timedelta
import pandas as pd
import numpy as np






def monthly_sov(start_date: date, end_date: date):
    '''
        This function calculates the SOV accross different platforms and then return the required output dataframes
    '''


    

    return [[], []]