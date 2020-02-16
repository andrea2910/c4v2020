def icu_indicator(df,column, 
                    common_map = {'Todos los días': 1,
                                  'No operativa': -1,
                                  'No existe': -1,
                                  'No hubo': -1,
                                  'Nunca ha existido': -1}):
    '''
    Logic if every day, then 1,
    if not every day then 0
    if never existed, no longer exists, or never existed then -1
    '''
    return(df[column].map(common_map).fillna(0))