# %%
from datetime import datetime, date, timedelta
import calendar


# %%

def generate_monthly_date_dict(start_date: datetime.date, end_date: datetime.date):
    '''This function will generate the MMM-YY along with the start date and end date for the code.'''

    # create a log here.
    try:
        # Parse string input to datetime.date if needed
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        # Validate
        if start_date > end_date:
            # Create a log here 
            raise ValueError("Start date must be before end date")

        date_dict = {}

        # Special case: same month and less than full month
        if start_date.year == end_date.year and start_date.month == end_date.month:
            key = start_date.strftime("%b-%y")
            date_dict[key] = [start_date, end_date]
            return date_dict

        # Iterate through each month from start to end
        current = start_date.replace(day=1)
        while current <= end_date:
            month_start = current
            last_day = calendar.monthrange(current.year, current.month)[1]
            month_end = date(current.year, current.month, last_day)

            # Clamp to actual start/end bounds
            real_start = max(start_date, month_start)
            real_end = min(end_date, month_end)

            key = current.strftime("%b-%y")
            date_dict[key] = [real_start, real_end]

            # Go to the next month
            if current.month == 12:
                current = date(current.year + 1, 1, 1)
            else:
                current = date(current.year, current.month + 1, 1)

        return date_dict

    except Exception as e:
        print(f"An error occurred: {e}")
        # create a log here.
        # return {}




# %%
def generate_quarterly_date_dict(fiscal_year: int):
    ''' This function creates the required format quarters and returns dict based on the quarter date format for IND DQ'''
    
    quarters = ['AMJ', 'JAS', 'OND', 'JFM']
    str_year = str(fiscal_year)
    year_suffix = str_year[2:]
    quarters_with_year = [q + "-" + year_suffix for q in quarters]

    quarter_date_strings = {
        quarters_with_year[0]: [f"{str_year}-03-26", f"{str_year}-06-25"],
        quarters_with_year[1]: [f"{str_year}-06-26", f"{str_year}-09-25"],
        quarters_with_year[2]: [f"{str_year}-09-26", f"{str_year}-12-25"],
        quarters_with_year[3]: [f"{str_year}-12-26", f"{str(fiscal_year + 1)}-03-25"]
    }


    quarter_dates = {}
    for quarter_name, date_strings in quarter_date_strings.items():
        start_date_str, end_date_str = date_strings
        start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_obj = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        quarter_dates[quarter_name] = [start_date_obj, end_date_obj]

    # create a log here 
    return quarter_dates


# %%
def timePeriodTypeMonthly(month_tag: dict, month: str):
    '''This funtion will return Monthly/MTD based on the input dates'''
    
    if month in month_tag:
        input_date = month_tag[month][0]
        last_day = calendar.monthrange(input_date.year, input_date.month)[1]
        month_end = date(input_date.year, input_date.month, last_day)

        return "Monthly" if month_end == month_tag[month][1] else "MTD"
    
    return None

    


