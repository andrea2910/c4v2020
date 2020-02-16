import pandas as pd

def white_space_filler(df, column):
    df.loc[~df[column].str.match(r'^\s*$'), column] = "1"
    df.loc[df[column].str.match(r'^\s*$'), column] = "0"

def safety_indicator(df):
    '''
    safety_indicator.py
    ------------------
    This Function calculates the surgery indicator, a metric that measures
    whether or not there are protests or violence in the hospital in that particular state
​
    Logic
    ----- 
    If there is violence towards hospital, then -1
    If there is protest towards hospital, then 0
    If there is no violence or protest, then 1 
    Else maybe
​
    Input
    -----
    Pandas Dataframe
​
    Output
    ------
    Pandas Series
    '''
    protest_violence = ['strike_medical_staff_affected',
                    'strike_nurses_affected',
                    'strike_other_staff_affected',
                    'strike_patients_affected',
                    'strike_other_affected',
                    'staff_violence_affected_reasons']
    
    tmp = df.copy()
    for column in protest_violence:
        white_space_filler(tmp, column)
        tmp[column] = pd.to_numeric(tmp[column])
    
    tmp['safety_indicator'] = 1
    
    tmp.loc[(tmp['staff_violence_affected_reasons'] == 1), 'safety_indicator'] = -1
    
    protest_logic = ((tmp['staff_violence_affected_reasons'] == 0) & 
                     ((tmp['strike_medical_staff_affected'] == 1) |
                      (tmp['strike_nurses_affected'] == 1) |
                      (tmp['strike_other_staff_affected'] == 1) |
                      (tmp['strike_patients_affected'] == 1) |
                      (tmp['strike_other_affected'] == 1))
                    )
    tmp.loc[protest_logic, 'safety_indicator'] = 0
    
    return(tmp['safety_indicator'])