import pandas as pd

def surgery_indicator(df):
    '''
    Logic: 
    If op_pavilions_count = 0 then cannot do surgery
    If op_pavilions_count > 0 and 
    sx_avail_anesthetics_iv, sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction DOESNT WORK, then cannot do
    If op_pavilions_count > 0 and sx_avail_anesthetics_iv, sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction ALWAYS works, then can always do
    '''
    tmp = df.copy()
    tmp['sx_indicator'] = 0
    tmp.loc[ (tmp['op_pavilions_count'].astype(int)>0) & 
                (tmp['sx_avail_anesthetics_iv'].isin(['No hubo','Nunca ha existido','No operativa'])) &
               (tmp['sx_avail_anesthetic_gases'].isin(['No hubo','Nunca ha existido','No operativa'])) &
                (tmp['sx_avail_ott_intubation'].isin(['No hubo','Nunca ha existido','No operativa'])) & 
               (tmp['sx_avail_oxygen_suction'].isin(['No hubo','Nunca ha existido','No operativa'])),
       'sx_indicator'] = -1
    tmp.loc[ (tmp['op_pavilions_count'].astype(int)>0) & 
                (tmp['sx_avail_anesthetics_iv']=='Todos los días') &
               (tmp['sx_avail_anesthetic_gases']=='Todos los días') &
                (tmp['sx_avail_ott_intubation']=='Todos los días') & 
               (tmp['sx_avail_oxygen_suction']=='Todos los días'),
      'sx_indicator'] = 1
    tmp.loc[tmp['op_pavilions_count'].astype(int) == 0, 'sx_indicator'] = -1
    return(tmp['sx_indicator'])


