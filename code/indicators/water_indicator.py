import pandas as pd

def water_indicator(df):
    '''
    Logic:
    If all 3 water indicators do not exist, then no water
    If all 3 water indicators always have water, then water
    Else maybe
    '''
    tmp = df.copy()
    tmp['water_indicator'] = 0
    tmp.loc[(tmp['wash_failure_icu'] == 'No hubo agua ningún dia') & 
           (tmp['wash_failure_er'] == 'No hubo agua ningún dia') & 
           (tmp['wahs_failure_sx'] == 'No hubo agua ningún dia') ,'water_indicator'] = -1
    tmp.loc[(tmp['wash_failure_icu'] == 'Hubo agua todos los días') & 
           (tmp['wash_failure_er'] == 'Hubo agua todos los días') & 
           (tmp['wahs_failure_sx'] == 'Hubo agua todos los días') ,'water_indicator'] = 1
    return(tmp['water_indicator'])