import pandas as pd

def medical_supply_indicator(df,column, 
                    common_map = {"Nunca ha existido":-1, "No hay":-1,
                     "Menos de 3 de días":0, "Entre 3 y 5 días":0, "Todos los días":1}):
    '''
    medical_supply_indicator
    ------------------------
    This function calculates and indicator for medical supplies in hospitals.

    Logic
    -----
    Logic if every day, then 1,
    if not every day then 0
    if never existed, no longer exists, or never existed then -1

    Input
    -----
    Pandas Dataframe

    Output
    ------
    Pandas Series
    '''
    return(df[column].map(common_map).fillna(0))