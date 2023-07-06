from datetime import datetime
import pytz

# return the current time in PT Naive format
def get_current_time():

    # Get the current time in UTC
    current_time_utc = datetime.now(pytz.utc)

    # Convert UTC time to Pacific Time
    pacific_tz = pytz.timezone('US/Pacific')
    current_time_pacific = current_time_utc.astimezone(pacific_tz)

    # Convert current_time_pacific to an offset-naive datetime object
    current_time_pt_naive = current_time_pacific.replace(tzinfo=None)

    return current_time_pt_naive


# receives the start time from API call (which is in Pacific Time Long Form)
# returns the start time in PT Naive format
def get_start_time(start_time):
    
    # Convert the start_time of the VM to the correct format
    start_time_datetime = datetime.fromisoformat(start_time)

    # Convert start_time_datetime object to an offset-naive datetime object
    start_time_datetime_naive = start_time_datetime.replace(tzinfo=None)

    return start_time_datetime_naive


# receives the VM instance's start time and the current time
# returns the elapsed time between the two
def get_total_uptime(vm_start_time, current_time):
    elapsed_time_object = current_time - vm_start_time
    return convert_time_to_hours(elapsed_time_object)

# receives an elapsed time string
# returns the total number of hours that have passed
def convert_time_to_hours(time_object):
    # Convert the time object to a string
    time_string = str(time_object)

    # Split the time into its components
    hours, minutes, seconds = map(float, time_string.split(':'))
    
    # Convert minutes and seconds to hours
    minutes_in_hours = minutes / 60
    seconds_in_hours = seconds / 3600
    
    # Add up all the hours components
    total_hours = hours + minutes_in_hours + seconds_in_hours
    
    return total_hours