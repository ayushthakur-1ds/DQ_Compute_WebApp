

import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from datetime import date, datetime, timedelta
import pandas, numpy

from monthly.availability import availability
from monthly.sov import sov

# ------------------------------------------------------------------------------------------


def monthly_compile(compile_list: list, start_date: date, end_date: date, avail_qtr: str):
    """
    Returns:
        - raw_data_dict: { "Availability": [df1, df2], "SOV": [df3, df4] }
        - final_dfs: [formatted_avail_df, formatted_sov_df]
    """
    
    raw_data_dict = {}
    final_dfs = []

    if "Availability" in compile_list:
        avail_raw, avail_formatted = availability.monthly_availability(start_date, end_date, avail_qtr)
        raw_data_dict["Availability"] = avail_raw
        final_dfs.extend(avail_formatted)  # Should be a list, even if one element

    if "Share Of Visibility Search" in compile_list:
        sov_raw, sov_formatted = sov.monthly_sov(start_date, end_date)
        raw_data_dict["SOV"] = sov_raw
        final_dfs.extend(sov_formatted)

    
    # add the cases for compilation here then finally return the dict & final formatted df.
    
    
    
    return raw_data_dict, final_dfs
