import pandas as pd 

def is_available(df, column, map_dict):
    return df[column].map(map_dict)
    
def power_indicator(df):
    """
    power_indicator
    ---------------
    The function caluates the reliablity of power at a hospital.

    Logic
    -----
    If there are no power outages, a generator avaiable, and they have power all days, then 1
    If there are power outages and (there is no generator or the hospital has less than 3 days of power), then -1
    Else 0

    Input
    -----
    Pandas Dataframe

    Output
    ------
    Pandas Series
    """
    tmp = df.copy()
    ### Maps to Scores
    power = {"Menos de 3 días":-1, "Entre 3 y 5 días":0, "Todos los días":1}
    si_no = {"Sí":1, "No":-1}
    tmp['score_power_outage'] = is_available(tmp, "power_outage", si_no)
    tmp['score_power_generator_available'] = is_available(tmp, "power_generator_available", power)
    tmp['score_power_outage_days_count'] = is_available(tmp, "power_outage_days_count", power)
    tmp['power_indicator'] = 0
    # Positive Case
    tmp.loc[((tmp['score_power_outage']==-1) |
            (tmp['score_power_generator_available']==1)) &
            (tmp['score_power_outage_days_count']==1), 'power_indicator'] = 1
    # Negative Case
    tmp.loc[(tmp['score_power_outage']==1) &
        ((tmp['score_power_outage_days_count']==-1) |
        (tmp['score_power_generator_available']==-1)), 'power_indicator'] = -1
    return tmp['power_indicator']
    
def machine_indicator(df):
    """
    machine_indicator
    -----------------
    The function caluates the reliablity of medical equipment of a hospital.

    Logic
    -----
    If Hospitals has no equipment failures due to power outage and all medical equipment, then 1
    If Hopsitals have equipment failures due to power outage or missing two of three medical equipment,
    then -1
    Else 0

    Input
    -----
    Pandas Dataframe

    Output
    ------
    Pandas Series
    """
    tmp = df.copy()
    ### Maps to Scores
    machines = {"Nunca ha existido":-1, "No operativa":-1, "Menos de 3 de días":0, 
                "Entre 3 y 5 días":0, "Todos los días":1}
    si_no = {"Sí":1, "No":-1}
    tmp['score_power_outage_equipment_failure'] = is_available(tmp, "power_outage_equipment_failure", si_no)
    for column in ['operability_uls', 'operability_ct_mri', 'operability_xr']:
        tmp["score_{}".format(column)] = is_available(tmp, column, machines)
    tmp['machine_indicator'] = 0
    tmp.loc[(tmp['score_power_outage_equipment_failure']==1) &
            (tmp['score_operability_uls']==1) &
            (tmp['score_operability_ct_mri']==1) &
            (tmp['score_operability_xr']==1), 'machine_indicator'] = 1
    tmp.loc[(tmp['score_power_outage_equipment_failure']==-1) |
            (tmp[['score_operability_uls', 
                 'score_operability_ct_mri', 
                 'score_operability_xr']].sum(axis=0) < -1), 'machine_indicator'] = -1
    return tmp['machine_indicator']