import pandas as pd 

def er_indicator(df):
    
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