import pandas as pd 

def er_indicator(df):
    """
    er_indicator.py
    ------------------
    This Function calculates the ER indicator, a metric that measures the 
    realiability of the Emergency Room.
​
​
    Logic
    -----
    1.- From the input DataFrame, it subsets all the columns referred to the 
    Emergency Room in a DataFrame called 'er_df'.
​
    2.- For the variables referred to the ER supplies (e.g adrenalin, insulin), 
    which comes originally in a Likert scale, it converts them to -1, 0 or 1 
    and stores them in a new column ending with '_scaled' following the logic:
​
        Value == -1 (Bad condition) when:
        ---------------------------------
        'No hubo'
        'Nunca ha existido'
        'No hubo agua ningún dia'
        '< 3 días, sin soporte alterno (cisternas)'
​
        Value == 1 (Good condition) when:
        ---------------------------------
        'Todos los días'
        'Hubo agua todos los días'
        '3 a 5 días, con soporte alterno' 
​
        Value == 0 (Medium condition) when:
        ----------------------------------
        <otherwhise>
​
    3.- For the variables referred to the ER staff (e.g specialists, mic...), 
    which comes originally as natural numers, it converts them to 0 or 1
    and stores them in a new column ending with '_scaled' following the logic:
​
        Value == 0 (Bad condition) when:
        ---------------------------------
        The variable has the value 0 (no staff present)
​
        Value == 1 (Good condition) when:
        ---------------------------------
        The variables has more than 0 (some staff present)
​
    4.- Sum the values in the _scaled columns by hospital and gives a total score 
    for supplies and staff. 
​
    5.- Generates the new preliminary columns following the same logic:
​
        Score for supplies
        ------------------
        More or equal to 10 : Value = 1 
        Less than 1: Value = -1
        Otherwise: Value = 0 
​
        Score for staff
        ------------------
        More or equal to 8 : Value = 1 
        Less than 5: Value = -1
        Otherwise: Value = 0 
​
        Score for critical staff (excluding non proffesionals)
        ------------------
        More or equal to 7 : Value = 1 
        Less than 5: Value = -1
        Otherwise: Value = 0 
​
    6.- Generates a final value for each hospital 1 or 0. If the hospital has 
    three values of 1 in supplies, staff and critical staff, then value = 1, 
    otherwhise 0.
​
​
    Input
    -----
    Pandas Dataframe
    Output
    ------
    Pandas Series
​
​
​
    """    

    df_er = df.copy()
    
    ### Defining the columns for the ER 
    cols_er = [
     'operability_er',
     'er_avail_adrenalin',
     'er_avail_atropine',
     'er_avail_dopamine',
     'er_avail_cephalosporins_betalactams',
     'er_avail_aminoglycosides_quinolone',
     'er_avail_vancomycin_clindamycin',
     'er_avail_lidocaine',
     'er_avail_minor_opioids',
     'er_avail_major_opioids',
     'er_avail_iv_fluids',
     'er_avail_diazepam_dph',
     'er_avail_heparin',
     'er_avail_steroids',
     'er_avail_insulin',
     'er_avail_asthma',
     'er_avail_blood_pressure',
     'er_avail_defibrillator',
     'er_avail_ott_intubation',
     'er_avail_catheter',
     'er_avail_oxygen_suction',
     'op_beds_er_count',
     'er_staff_residents_and_rural_day_on_call',
     'er_staff_specialist_day_on_call',
     'er_staff_mic_day_on_call',
     'er_staff_nurse_day_on_call',
     'er_staff_non_professional_nurse_day_on_call',
     'er_staff_residents_and_rural_night_on_call',
     'er_staff_specialist_night_on_call',
     'er_staff_mic_night_on_call',
     'er_staff_nurse_night_on_call',
     'er_staff_non_professional_nurse_night_on_call',
     'wash_failure_er'
    ]

    df_er = df_er[cols_er]
    
    ### Creating new numerical columns for the likert scale of availability
    for col in df_er.columns:
        if str(df_er[col].dtype) == 'object':
            for index, vals in df_er.iterrows():
                # -1 for the lack of supply
                if 'No hubo' in df_er.loc[index,col] or 'Nunca ha existido' in df_er.loc[index,col] or 'No hubo agua ningún dia' in df_er.loc[index,col] or '< 3 días, sin soporte alterno (cisternas)' in df_er.loc[index,col]:
                    try:
                        df_er.loc[index, '{}_scaled'.format(col)] = -1
                    except:
                        continue
                # 1 for good supply
                elif 'Todos los días' in df_er.loc[index,col] or 'Hubo agua todos los días' in df_er.loc[index,col] or '3 a 5 días, con soporte alterno' in df_er.loc[index,col]:
                    try:
                        df_er.loc[index, '{}_scaled'.format(col)] = 1
                    except:
                        continue
                # 0 otherwise: between 3 and 5 days , might get scarsed
                else:
                    try:
                        df_er.loc[index, '{}_scaled'.format(col)] = 0
                    except:
                        continue
    
    ### Creating new numerical columns for the staff, 0 if not, 1 otherwise
    for col in df_er.columns:
        if str(df_er[col].dtype) == 'int64':
            for index, vals in df_er.iterrows():
                if df_er.loc[index, col] == 0:
                    df_er.loc[index, '{}_scaled'.format(col)] = 0
                else:
                    df_er.loc[index, '{}_scaled'.format(col)] = 1
    
    
    
    ### Creating an overall sum per hospital of the supplies
    df_er['er_general_avail_sum'] = df_er[['operability_er_scaled',
                                  'er_avail_adrenalin_scaled', 
                                  'er_avail_atropine_scaled', 
                                  'er_avail_dopamine_scaled', 
                                  'er_avail_cephalosporins_betalactams_scaled', 
                                  'er_avail_aminoglycosides_quinolone_scaled', 
                                  'er_avail_vancomycin_clindamycin_scaled', 
                                  'er_avail_lidocaine_scaled', 
                                  'er_avail_minor_opioids_scaled', 
                                  'er_avail_major_opioids_scaled', 
                                  'er_avail_iv_fluids_scaled', 
                                  'er_avail_diazepam_dph_scaled', 
                                  'er_avail_heparin_scaled', 
                                  'er_avail_steroids_scaled',
                                  'er_avail_insulin_scaled', 
                                  'er_avail_asthma_scaled', 
                                  'er_avail_blood_pressure_scaled', 
                                  'er_avail_defibrillator_scaled', 
                                  'er_avail_ott_intubation_scaled', 
                                  'er_avail_catheter_scaled', 
                                  'er_avail_oxygen_suction_scaled',
                                  'wash_failure_er_scaled', 
                                  'op_beds_er_count_scaled']].sum(axis = 1)
    # Decision variable, more than 10 = good , 9-1 = medium,  less than 1 = bad
    er_avail_general = []
    for i in df_er['er_general_avail_sum']:
            if i >= 10 :
                er_avail_general.append(1)
            elif i < 1  :
                er_avail_general.append(-1)
            else:
                er_avail_general.append(0)
    
    # Output variable to show to the public: is the hospital well supplied?
    df_er['er_avail_general'] = pd.Series(er_avail_general)
    
    ### Creating an overall sum per hospital of the staff
    df_er['er_general_staff_sum'] = df_er[['er_staff_residents_and_rural_day_on_call_scaled', 
                                 'er_staff_specialist_day_on_call_scaled', 
                                 'er_staff_mic_day_on_call_scaled', 
                                 'er_staff_nurse_day_on_call_scaled', 
                                 'er_staff_non_professional_nurse_day_on_call_scaled',
                                 'er_staff_residents_and_rural_night_on_call_scaled',
                                 'er_staff_specialist_night_on_call_scaled', 
                                 'er_staff_mic_night_on_call_scaled',
                                 'er_staff_nurse_night_on_call_scaled', 
                                 'er_staff_non_professional_nurse_night_on_call_scaled']].sum(axis = 1)

    # Decision variable, more than 8 = good , 7-5 = medium,  less than 5 = bad
    er_staff_general = []
    for i in df_er['er_general_staff_sum']:
            if i >= 8 :
                er_staff_general.append(1)
            elif i < 5  :
                er_staff_general.append(-1)
            else:
                er_staff_general.append(0)
    # Output variable to show to the public: has the hospital personnel?
    df_er['er_staff_general'] = pd.Series(er_staff_general)
    
    ### Creating an overall sum per hospital of the critial supplies
    df_er['er_critical_avail_sum'] = df_er[['er_avail_adrenalin_scaled', 
                                      'er_avail_atropine_scaled', 
                                      'er_avail_dopamine_scaled', 
                                      'er_avail_cephalosporins_betalactams_scaled', 
                                      'er_avail_aminoglycosides_quinolone_scaled', 
                                      'er_avail_vancomycin_clindamycin_scaled', 
                                      'er_avail_lidocaine_scaled', 
                                      'er_avail_minor_opioids_scaled', 
                                      'er_avail_major_opioids_scaled', 
                                      'er_avail_iv_fluids_scaled', 
                                      'er_avail_diazepam_dph_scaled', 
                                      'er_avail_heparin_scaled', 
                                      'er_avail_steroids_scaled',
                                      'er_avail_blood_pressure_scaled', 
                                      'er_avail_defibrillator_scaled', 
                                      'er_avail_ott_intubation_scaled', 
                                      'er_avail_catheter_scaled', 
                                      'er_avail_oxygen_suction_scaled']].sum(axis = 1)
    ##### WANT TO ASK THE DOCTOR WHAT ARE THE MOST CRITICAL SUPPLIES IN ER
    #### ALREADY TAKING OUT INSULINE, ASTHMA AND OTHERS BECAUSE THOSE WILL BE THEIR OWN CATEGORY
    
    ### Creating an overall sum per hospital of the critial staff 
    df_er['er_critial_staff_sum'] = df_er[['er_staff_residents_and_rural_day_on_call_scaled', 
                                 'er_staff_specialist_day_on_call_scaled', 
                                 'er_staff_mic_day_on_call_scaled', 
                                 'er_staff_nurse_day_on_call_scaled',
                                 'er_staff_residents_and_rural_night_on_call_scaled',
                                 'er_staff_specialist_night_on_call_scaled', 
                                 'er_staff_mic_night_on_call_scaled',
                                 'er_staff_nurse_night_on_call_scaled']].sum(axis = 1)
    # Decision variable, more than 7 = good , 7-5 = medium,  less than 5 = bad
    er_staff_critical = []
    for i in df_er['er_critial_staff_sum']:
            if i >= 7 :
                er_staff_critical.append(1)
            elif i < 5  :
                er_staff_critical.append(-1)
            else:
                er_staff_critical.append(0)
    
    # Output variable to show to the public: does the hospital has the most critical personnel?
    df_er['er_staff_critical'] = pd.Series(er_staff_critical)
        
    df_er_return = df_er[['er_avail_general',
                         'er_staff_general',
                         'er_staff_critical',
                        #  'er_avail_insulin_scaled',
                        #  'er_avail_asthma_scaled',
                        #  'er_avail_lidocaine_scaled'
                         ]]
    
    return df_er_return