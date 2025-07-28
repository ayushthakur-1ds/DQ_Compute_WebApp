# Dynamically setting terminal in parent directory
import os, sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..'))
sys.path.append(parent_dir)


# importing necessary libraries
from io import BytesIO
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pickle
import pandas as pd
import numpy as np
import psycopg2


from datetime import date, datetime, timedelta
from openpyxl import load_workbook

from connection_utils import gsheet_processings, posgresconn
from utils import formatting_code, date_map

# -------------------------------------------------------------------------------------------------------


# AVAIL_QUARTER = 'FY2025 Q3 OND'   #will have to take this input from ui itself just hanging here for now
BASE_PATH = os.path.join(parent_dir, "connection_utils/")


def monthly_availability(start_date: date, end_date: date, avail_quarter: str):
    '''This function performs the monthly availability calculations 
    & returns list containing base sheets at 0 & final formatted file at 1'''

    gsheet_obj =  gsheet_processings.GsheetPreProcessing(BASE_PATH)

    conn = posgresconn.postgres_conn().getConn()
    conn2 = posgresconn.postgres_conn().getConn2()

    BRAND_MAPPING = gsheet_obj.fetch_sheet_data('Avail Mapping', '1w_b_L98NWFtbKDKvW6-DEDAs-jJWbuemsY55ywYLB_Q')
    KPI_NO_MAPPING = gsheet_obj.fetch_sheet_data('KPI Category', '1EJ6pF9JdeXT-sES0TH0gR_vUyZq0_fcH-hMaGYnuHCA')  # Needs to remove this dependancy
    

    
    # if pd.Timestamp(end_date).is_month_end:
    #     TimePeriod_Type = 'Monthly'
    # else:
    #     TimePeriod_Type = 'MTD'

    sql_query = f'''
    with avail as (SELECT
        case availability_marketplace.channel_id when 1 then 'Amazon'
            when 2 then 'Flipkart'
            when 25 then 'Nykaa'
            when 40 then 'Firstcry'
            when 80 then '1mg'
            when 26 then 'bigbasket'
            when 27  then 'blinkit' end as channel_name,
        lower(master_brand.BRAND) as brand,
        availability_marketplace.sku,
        availability_marketplace.title,
        availability_marketplace.date,
        availability_marketplace.mrp,
        availability_marketplace.price,
        availability_marketplace.availability,
        'NATIONAL' as city,
        '0' as pincode,
        buybox,
        case when lower(availability_marketplace.availability) = 'unavailable' then 1 else 0 end as oos,
        1 as entry,
    master_brand.time_period AS time_period,
        availability_marketplace.channel_id as channel_id
    FROM
        marico.marico_availability_marketplace AS availability_marketplace
        INNER JOIN marico.mst_dq_availability_master as master_brand
            ON lower(master_brand.ASIN) = lower(availability_marketplace.SKU)
            AND master_brand.channel_id = availability_marketplace.channel_id
        LEFT JOIN marico.mst_dq_availability_seller_master as master_seller
            ON lower(master_seller.ASIN) = lower(availability_marketplace.SKU)
        LEFT JOIN
        (SELECT channel_id, sku, sum(case when availability = 'unavailable' then 1 else 0 end) as oos, count(*) as entries
        FROM marico.marico_availability_marketplace
        WHERE date >= now()::date - 45
        GROUP BY channel_id, sku
        HAVING count(*) > 30 AND count(*) = sum(case when availability = 'unavailable' then 1 else 0 end)
        ) as last_45_days
        ON last_45_days.channel_id = availability_marketplace.channel_id
        AND last_45_days.sku = availability_marketplace.sku
    WHERE
        date(availability_marketplace.date) >= '{start_date}'
        AND date(availability_marketplace.date) <= '{end_date}'
        and master_brand.time_period = '{avail_quarter}'
        AND (master_seller.CONSIDERED = 1 OR availability_marketplace.channel_id <> 1 or true)
        AND availability_marketplace.pincode is null
    ),
    grocery as(SELECT
        case availability_grocery.channel_id 
            when 26 then 'Big Basket'
            when 39 then 'Flipkart Grocery'
            when 27 then 'Blinkit'
            when 32 then 'Amazon Fresh'
            when 65 then 'Swiggy'
            when 109 then 'Zepto'
        end as channel_name,
        lower(master_brand.BRAND) as brand,
        availability_grocery.sku,
        availability_grocery.title,
        availability_grocery.date,
        availability_grocery.mrp,
        availability_grocery.price,
        availability_grocery.availability,
        case cast(availability_grocery.pincode AS varchar(256))
            WHEN '600010' THEN 'CHENNAI' WHEN '600018' THEN 'CHENNAI' WHEN '600042' THEN 'CHENNAI' WHEN '600090' THEN 'CHENNAI'
            WHEN '600100' THEN 'CHENNAI' WHEN '600119' THEN 'CHENNAI' WHEN '110001' THEN 'DELHI' WHEN '110007' THEN 'DELHI'
            WHEN '110009' THEN 'DELHI' WHEN '110016' THEN 'DELHI' WHEN '110054' THEN 'DELHI' WHEN '110085' THEN 'DELHI'
            WHEN '400052' THEN 'MUMBAI' WHEN '400053' THEN 'MUMBAI' WHEN '400064' THEN 'MUMBAI' WHEN '400094' THEN 'MUMBAI'
            WHEN '400101' THEN 'MUMBAI' WHEN '400104' THEN 'MUMBAI' WHEN '400607' THEN 'MUMBAI' WHEN '500015' THEN 'HYDERABAD'
            WHEN '500019' THEN 'HYDERABAD' WHEN '500028' THEN 'HYDERABAD' WHEN '500032' THEN 'HYDERABAD' WHEN '500034' THEN 'HYDERABAD'
            WHEN '500084' THEN 'HYDERABAD' WHEN '201002' THEN 'GHAZIABAD' WHEN '201009' THEN 'GHAZIABAD' WHEN '700019' THEN 'KOLKATA'
            WHEN '700025' THEN 'KOLKATA' WHEN '700027' THEN 'KOLKATA' WHEN '700055' THEN 'KOLKATA' WHEN '700075' THEN 'KOLKATA'
            WHEN '700103' THEN 'KOLKATA' WHEN '201301' THEN 'NOIDA' WHEN '201303' THEN 'NOIDA' WHEN '201309' THEN 'NOIDA'
            WHEN '201318' THEN 'NOIDA' WHEN '560009' THEN 'BANGALORE' WHEN '560022' THEN 'BANGALORE' WHEN '560037' THEN 'BANGALORE'
            WHEN '560038' THEN 'BANGALORE' WHEN '560050' THEN 'BANGALORE' WHEN '560052' THEN 'BANGALORE' WHEN '560066' THEN 'BANGALORE'
            WHEN '122001' THEN 'GURGAON' WHEN '122002' THEN 'GURGAON' WHEN '122009' THEN 'GURGAON' WHEN '380054' THEN 'AHMEDABAD'
            WHEN '380058' THEN 'AHMEDABAD' WHEN '302006' THEN 'JAIPUR' WHEN '302012' THEN 'JAIPUR' WHEN '302020' THEN 'JAIPUR'
            WHEN '411001' THEN 'PUNE' WHEN '411002' THEN 'PUNE' WHEN '411006' THEN 'PUNE' WHEN '411052' THEN 'PUNE'
            WHEN '411057' THEN 'PUNE' WHEN '208002' THEN 'LUCKNOW' WHEN '226010' THEN 'LUCKNOW'
        end as city,
        cast(availability_grocery.pincode AS varchar(256)) as pincode,
        '-'  as buybox,
        case when lower(availability_grocery.availability) = 'unavailable' then 1 else 0 end as oos,
        1 as entry,
        master_brand.time_period as time_period,
        availability_grocery.channel_id as channel_id
    FROM
        marico.marico_availability_grocery AS availability_grocery
        INNER JOIN marico.mst_dq_availability_master as master_brand
            ON lower(master_brand.ASIN) = lower(availability_grocery.SKU)
            AND master_brand.channel_id = availability_grocery.channel_id
        LEFT JOIN
        (SELECT channel_id, sku, pincode, sum(case when availability = 'unavailable' then 1 else 0 end) as oos, count(*) as entries
        FROM marico.marico_availability_grocery
        WHERE date >= now()::date - 45
        GROUP BY channel_id, sku, pincode
        HAVING count(*) > 30 AND count(*) = sum(case when availability = 'unavailable' then 1 else 0 end)
        ) as last_45_days
        ON last_45_days.channel_id = availability_grocery.channel_id
        AND lower(last_45_days.sku)= lower(availability_grocery.sku)
        AND last_45_days.pincode = availability_grocery.pincode
    WHERE
        date(availability_grocery.date) >= '{start_date}'
        AND date(availability_grocery.date) <= '{end_date}'
    AND master_brand.time_period = '{avail_quarter}'
    )

    select * from avail union select * from grocery
    '''

    try:
        raw_data = pd.read_sql_query(sql_query, conn[1])

        raw_data_final = raw_data.rename(columns={'date': 'report_date'})
        raw_data_final['report_date'] = pd.to_datetime(raw_data_final['report_date'])

        monthly_tag = date_map.generate_monthly_date_dict(start_date, end_date)

        # this loop will map the months based on raw date
        for index, row in raw_data_final.iterrows():
            report_date = row['report_date'].date()
            for tag, (start_dt, end_dt) in monthly_tag.items():
                if start_dt <= report_date <= end_dt:
                    raw_data_final.at[index, 'month_year'] = tag
                    break

        # print(raw_data_final)
    
    except Exception as e:
        print(f"Error Occured: {e}")


    try:
        # add the log here.: 
        df_raw = pd.merge(raw_data_final, BRAND_MAPPING, on='brand',how='left')
        brand_pivot = df_raw.groupby(['DQ Brand','month_year'])[['oos','entry']].sum().reset_index()

        brand_pivot['OOS %'] = brand_pivot.apply(lambda x : x['oos'] / x['entry'],axis=1)
        brand_pivot['Availability%'] = brand_pivot.apply(lambda x : 1 - (x['oos'] / x['entry']), axis =1)
        brand_pivot = brand_pivot.rename(columns = {'month_year' : 'Time Interval'})

        # this will auto map the monthly or mtd based on the months mapped earlier.
        brand_pivot['TimePeriod Type'] = brand_pivot['Time Interval'].apply(lambda x: date_map.timePeriodTypeMonthly(monthly_tag, x))

        final_values = brand_pivot[['DQ Brand' ,'Availability%' ,'Time Interval','TimePeriod Type']]
        final_values = final_values.rename(columns = {'Availability%': 'Value'})
        final_values['Key'] = 'Availability'

        final_brand_pivot = pd.merge(final_values, KPI_NO_MAPPING[['Key','KPI#','Category','Attributes (L2)']],on='Key',how='left')
        final_brand_pivot.rename(columns = {'DQ Brand' : 'DQ_Brand'}, inplace=True)
        final_brand_pivot['Lookup Key'] = final_brand_pivot.apply(lambda x: str(x['KPI#']) + "_" + str(x['DQ_Brand']) + "_" + str(x['Time Interval']) + "_" + str(x['TimePeriod Type'])+ "_IN",axis =1)
        final_brand_pivot = final_brand_pivot.replace([np.inf, -np.inf], np.nan)

        # Adding start date and end dates 
        final_brand_pivot['Start Date'] = final_brand_pivot['Time Interval'].apply(
            lambda x: monthly_tag.get(x)[0]
        )

        final_brand_pivot['End Date'] = final_brand_pivot['Time Interval'].apply(
            lambda x: monthly_tag.get(x)[1]
        )

            
        Final_formatted_data = final_brand_pivot[['KPI#','DQ_Brand','Attributes (L2)','Category','Start Date', 'End Date','TimePeriod Type','Time Interval','Value','Lookup Key']]    
        Final_formatted_data = Final_formatted_data.dropna(subset=['KPI#'])   
        Final_formatted_data = Final_formatted_data.drop(Final_formatted_data[Final_formatted_data['DQ_Brand'].isin(['NA',''])].index)


        # will be adding the logic to return the files and formats to web-app

        print(Final_formatted_data)

        availability_set = [[raw_data_final, final_values, Final_formatted_data], [Final_formatted_data]]

        return availability_set


    except Exception as e:
        print(f"There is an error: {e}")






# monthly_availability(date(2025, 1, 25), date(2025, 2, 2), "#Blah Blah it will be picked up from app")


