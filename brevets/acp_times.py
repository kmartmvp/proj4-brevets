"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # Referenced https://stackoverflow.com/questions/39358092/range-as-dictionary-key-in-python
    # to see if ranges could be used as keys. (Apparently) ranges are immutable. Specifically, the most
    # upvoted answer was used for the usage of ranges as keys.
    max_speed_dict = {
        range(0,200): 34, 
        range(200,400): 32, 
        range(400,600): 30, 
        range(600,1000): 28, 
        range(1000,1300): 26
        }

    distance = None
    for key in max_speed_dict:
        if control_dist_km in key:
            distance = max_speed_dict[key]
    
    open_time_base  = control_dist_km / distance                      # Use dict of max speeds to determine base calculation of controle open time
    open_time_hours = open_time_base // 1                             # Integer division by 1 will rid us of fractional portion
    open_time_min   = (open_time_base - open_time_hours) * 60         # Multiply fractional portion by 60 to recieve minutes

    # Shift given ISO time by appropriate hours and minutes
    controle_open   = arrow.get(brevet_start_time).shift(
            hours=open_time_hours, minutes=open_time_min)

    controle_format = controle_open.format("ddd M/D H:mm")

    return controle_format


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    min_speed_dict = {
        range(0,200): 15, 
        range(200,400): 15, 
        range(400,600): 15, 
        range(600,1000): 11.428, 
        range(1000,1300): 13.333
        }

    distance = None
    for key in min_speed_dict:
        if control_dist_km in key:
            distance = min_speed_dict[key]
    
    open_time_base  = control_dist_km / distance                      # Use dict of max speeds to determine base calculation of controle open time
    open_time_hours = open_time_base // 1                             # Integer division by 1 will rid us of fractional portion
    open_time_min   = (open_time_base - open_time_hours) * 60         # Multiply fractional portion by 60 to recieve minutes

    # Shift given ISO time by appropriate hours and minutes
    controle_close   = arrow.get(brevet_start_time).shift(
            hours=open_time_hours, minutes=open_time_min)
    controle_format = controle_close.format("ddd M/D H:mm")

    return controle_format
