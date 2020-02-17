import pandas as pd

def dialysis_indicator(df):
    """
    dialysis.py
    ------------------
    This Function calculates the dialysis indicator, a metric that measures
    whether or not dialysis can be performed in the hospital in that particular state

    Logic
    -----
    First, the function cleans the variables that is related to dialysis by imputing
    missing values to 0 or converting necessary categorical columns to numerical values
    Then it manually classifies the components required for a dialysis into 5 types and their indicator variables:
    Materials ('materials_surgery'), staff ('staff_surgery'),
    Reverse Osmosis unit operability ('flag_rrt_reverse_osmosis_unit_operability'),
    hospital operability('flag_rrt_operability'), and
    Number of Hemodialysis equipments operability('flag_rrrt_num_hemodialysis_equipments_operability').

    Value:
    1 would indicate the components required is fulfilled
    0 would indicate there is at least one missing component
    The following variables from the dataset will be classified into 'materials_surgery'
        'rrt_hemodialysis_avail_filter',
        'rrt_hemodialysis_avail_lines',
        'rrt_hemodialysis_avail_kit_hemodialysis',
        'rrt_hemodialysis_avail_iron',
        'rrt_hemodialysis_avail_b_complex',
        'rrt_hemodialysis_avail_calcium',
        'rrt_hemodialysis_avail_zemblar',
        'rrt_reverse_osmosis_unit_operability'
    The following variables from the dataset will be classified into 'staff_surgery'
        'rrt_staff_nephrology',
        'rrt_staff_md',
        'rrt_staff_resident',
        'rrt_staff_nurse',
        'rrt_staff_nurse_nephrologist'
    Then a status indicator variable is created for these 5 types of data: ('XXXXX')
    When all 5 of the indicator variables is met, it means that the dialysis can be done
    Value of ('XXXXX'):
    1 = dialysis can be performed
    0 = dialysis cannot be performed

    Input
    -----
    Pandas Dataframe

    Output
    ------
    Pandas Series
    """
    
    dialysis = df.copy()
    
    # Imputing blank spaces

    dialysis.replace(r'^\s*$', "Unknown", regex=True, inplace = True)

    # Imputing nulls with 0
    dialysis = dialysis.fillna(0)
    
    # Temp column for feature engineering for material
    dialysis['materials'] =  dialysis[[
    'rrt_hemodialysis_avail_filter',
    'rrt_hemodialysis_avail_lines',
    'rrt_hemodialysis_avail_kit_hemodialysis',
    'rrt_hemodialysis_avail_iron',
    'rrt_hemodialysis_avail_b_complex',
    'rrt_hemodialysis_avail_calcium',
    'rrt_hemodialysis_avail_zemblar',
    'rrt_reverse_osmosis_unit_operability',
    ]].sum(axis=1)

    # Temp Column, can do surgery or no, based on availability of the supplies (filter : zemblar)
    dialysis['materials_surgery'] = 0

    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'materials'] == 0:
            dialysis.loc[index,'materials_surgery'] = 0
        else:
            dialysis.loc[index,'materials_surgery'] = 1

     # Temp column for feature engineering for material
    dialysis['staffs'] =  dialysis[[
    'rrt_staff_nephrology',
    'rrt_staff_md',
    'rrt_staff_resident',
    'rrt_staff_nurse',
    'rrt_staff_nurse_nephrologist']].sum(axis=1)

    dialysis['staff_surgery'] = 0

    # Temp Column, can do surgery or no, based on availability of the supplies (filter : zemblar)
    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'staffs'] == 0:
            dialysis.loc[index,'staff_surgery'] = 0
        else:
            dialysis.loc[index,'staff_surgery'] = 1
        
        
        
    # Temp feature for RO unit
    dialysis['flag_rrt_reverse_osmosis_unit_operability'] = 0

    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'rrt_reverse_osmosis_unit_operability'] == 0:
            dialysis.loc[index,'flag_rrt_reverse_osmosis_unit_operability'] = 0
        else:
            dialysis.loc[index,'flag_rrt_reverse_osmosis_unit_operability'] = 1        
        
        
    # Temp feature for operatibility
    dialysis['flag_rrt_operability'] = 0

    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'rrt_operability'] == 0:
            dialysis.loc[index,'flag_rrt_operability'] = 0
        else:
            dialysis.loc[index,'flag_rrt_operability'] = 1
    
    # Temp feature for equipment
    dialysis['flag_rrrt_num_hemodialysis_equipments_operability'] = 0
    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'rrt_num_hemodialysis_equipments_operability'] == 0:
            dialysis.loc[index,'flag_rrrt_num_hemodialysis_equipments_operability'] = 0
        else:
            dialysis.loc[index,'flag_rrrt_num_hemodialysis_equipments_operability'] = 1
            
            
    # Decision Variable
    dialysis['temp'] = dialysis[['materials_surgery',
                 'staff_surgery',
                 'flag_rrt_reverse_osmosis_unit_operability',
                 'flag_rrt_operability',
                 'flag_rrrt_num_hemodialysis_equipments_operability']].sum(axis=1)

    surgery = []
    for i in dialysis['temp']:
        if i == 5:
            surgery.append(1)
        else:
            surgery.append(-1)
        
    dialysis['dialysis_indicator'] = pd.Series(surgery)
    
    return dialysis['dialysis_indicator']