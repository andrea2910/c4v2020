import pandas as pd

def pregnancy_indicator(df):
    '''
    Logic: 
    If nutr_freq_milk_formulas = Hubo fórmulas lácteas todos los días AND 
    df.operability_uls is Todos los días, then 1 
    If nutr_freq_milk_formulas in ['No hubo fórmulas lácteas ningún día', 'Nunca ha habido fórmulas lácteas']
    OR df.operability_uls  in ['No operativa', 'Nunca ha existido'], then no
    else maybe 
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