import pandas as pd

def pregnancy_indicator(df):
    '''
    pregnancy_indicator.py
    ------------------
    This Function calculates the surgery indicator, a metric that measures
    whether or pregnancy can be supported by  the hospital in that particular state
​
    Logic
    ----- 
    If nutr_freq_milk_formulas = Hubo fórmulas lácteas todos los días AND 
    df.operability_uls is Todos los días, then 1 
    If nutr_freq_milk_formulas in ['No hubo fórmulas lácteas ningún día', 'Nunca ha habido fórmulas lácteas']
    OR df.operability_uls  in ['No operativa', 'Nunca ha existido'], then no
    else maybe 
​
    Input
    -----
    Pandas Dataframe
​
    Output
    ------
    Pandas Series 
    '''
    tmp = df.copy()
    tmp['preg_indicator'] = 0
    tmp.loc[ (tmp['nutr_freq_milk_formulas'].isin(
        ['No hubo fórmulas lácteas ningún día', 'Nunca ha habido fórmulas lácteas'])) |
               (tmp['operability_uls'].isin(['No operativa', 'Nunca ha existido'])),
       'preg_indicator'] = -1
    tmp.loc[ (tmp['nutr_freq_milk_formulas']=='Hubo fórmulas lácteas todos') &
               (tmp['operability_uls']=='Todos los días'),
      'preg_indicator'] = 1
    
    return(tmp['preg_indicator'])