import pandas as pd​

def dialysis_indicator(df):
    
    """
    This function is done to help to make a decision to whether or not a 
    dialysis is possible to be done at the hospital or not.
    """
    
    dialysis = df
    
    # Imputing blank spaces
​
    dialysis.replace(r'^\s*$', "Unknown", regex=True, inplace = True)
​
    # Imputing nulls with 0
​
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
​
​
    # Temp Column, can do surgery or no, based on availability of the supplies (filter : zemblar)
    dialysis['materials_surgery'] = 0
​
​
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
​
​
    dialysis['staff_surgery'] = 0
​
    # Temp Column, can do surgery or no, based on availability of the supplies (filter : zemblar)
    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'staffs'] == 0:
            dialysis.loc[index,'staff_surgery'] = 0
        else:
            dialysis.loc[index,'staff_surgery'] = 1
        
        
        
​
    # Temp feature for RO unit
    dialysis['flag_rrt_reverse_osmosis_unit_operability'] = 0
​
    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'rrt_reverse_osmosis_unit_operability'] == 0:
            dialysis.loc[index,'flag_rrt_reverse_osmosis_unit_operability'] = 0
        else:
            dialysis.loc[index,'flag_rrt_reverse_osmosis_unit_operability'] = 1        
        
        
    # Temp feature for operatibility
    dialysis['flag_rrt_operability'] = 0
​
​
    for index, val in dialysis.iterrows():
        if dialysis.loc[index,'rrt_operability'] == 0:
            dialysis.loc[index,'flag_rrt_operability'] = 0
        else:
            dialysis.loc[index,'flag_rrt_operability'] = 1
    
    # Temp feature for equipment
    dialysis['flag_rrrt_num_hemodialysis_equipments_operability'] = 0
​
​
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
​
    surgery = []
​
    for i in dialysis['temp']:
        if i == 5:
            surgery.append(1)
        else:
            surgery.append(-1)
        
    dialysis['dialysis_indicator'] = pd.Series(surgery)
​
    return dialysis['dialysis_indicator']