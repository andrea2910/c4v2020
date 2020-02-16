import pandas as pd

def nutrition_indicator(df):
    """
    This function is creats a global nutrition indicator.
    If a hospital has nutrition available, operable, and server 3 nurtionist approved 
    meals a day everyday, nutrition indicator is 1
    If a hospital does not have nutrition available or operable, does not serve any 
    meals, nor have any nurtionist approved meals, nutrition indicator is -1
    Else is 0
    """
    
    nutrition = df.copy()
    
    # Nutrition Available
    
    numeric = []
    for i in nutrition['nutr_avail']:
        if i == 'Sí':
            numeric.append(1)
        else:
            numeric.append(-1)

    nutrition['numeric_nutr_avail'] = pd.Series(numeric)   
    
    # Nutrition Operability
    
    numeric = []
    for i in nutrition['nutr_operability']:
        if i == 'Sí':
            numeric.append(1)
        else:
            numeric.append(-1)

    nutrition['numeric_nutr_operability'] = pd.Series(numeric)   

    # Nutrition Num
    numeric = []

    for i in nutrition['nutr_num']:
        if i == 'Todos los días':
            numeric.append(1)
        elif i == 'Ningún día':
            numeric.append(-1)
        else:
            numeric.append(0)

    nutrition['numeric_nutr_num'] = pd.Series(numeric)   
    
    # Nutrition Daily Frequent Meal
    
    numeric = []

    for i in nutrition['nutr_daily_freq_meal']:
        if i == 'Se sirven menos de 3 comidas al día':
            numeric.append(0)
        else:
            numeric.append(1)

    nutrition['numeric_freq_meal'] = pd.Series(numeric)
    
    # Nutrition Quality
    numeric = []

    for i in nutrition['nutr_quality']:
        if i == 'No se siguen recomendaciones del especialista en cuanto al menú que se sirve ':
            numeric.append(-1)
        else:
            numeric.append(1)

    nutrition['numeric_nutr_quality'] = pd.Series(numeric)
    
    # Nutrition Frequent Milk Formula
    
    numeric = []

    for i in nutrition['nutr_freq_milk_formulas']:
        if i == 'No hubo fórmulas lácteas ningún día':
            numeric.append(-1)
        elif i == 'Nunca ha habido fórmulas lácteas':
            numeric.append(-1)
        elif i == 'Hubo fórmulas lácteas todos los días':
            numeric.append(1)
        else:
            numeric.append(0)

    nutrition['numeric_milk_formulas'] = pd.Series(numeric)
    
    nutrition.loc[(nutrition['numeric_nutr_avail']==1) & 
                  (nutrition['numeric_nutr_operability']==1) & 
                  (nutrition['numeric_nutr_quality']==1) &
                  (nutrition['numeric_nutr_num']==1) &
                  (nutrition['numeric_freq_meal']==1),'nutrition_indicator'] = 1
    
    nutrition.loc[(nutrition['numeric_nutr_avail']==-1) |
                (nutrition['numeric_nutr_operability']==-1) |
                (nutrition['numeric_nutr_num']==-1),'nutrition_indicator'] = -1

    return nutrition['nutrition_indicator'] # , nutrition['numeric_milk_formulas']

def disease_indicator(df):
    """
    This function is to determine the ability to handle an outbreak of a disease
    """
    disease = df
    numeric = []
    for i in disease['nCoV_face_mask_avail']:
        if i == 'Option 1':
            numeric.append(1)
        else:
            numeric.append(0)
    disease['numeric_nCoV_face_mask'] = pd.Series(numeric)
    numeric = []
    for i in disease['nCoV_isolation_area_avail']:
        if i == 'No':
            numeric.append(-1)
        elif i == 'Sí':
            numeric.append(1)
        else:
            numeric.append(0)
    disease['numeric_nCoV_isolation'] = pd.Series(numeric)

    disease_ind = []
    for fm, isolation in zip(disease['numeric_nCoV_face_mask'], disease['numeric_nCoV_isolation']):
        if fm==isolation & fm==1:
            disease_ind.append(1)
        elif isolation==-1:
            disease_ind.append(-1)
        else:
            disease_ind.append(0)

    return disease_ind