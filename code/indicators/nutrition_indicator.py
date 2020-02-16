#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def nutrition(df):
    
    """
    nutrition.py
    ------------------
    This Function calculates the nutrition indicator, a metric that measures 
    a hospital's capability to fulfill nutritions for patients.

    Logic
    -----

    The decision variable ('XXXXX') considers the status of 4 variables:

    Nutrition Operability('nutr_operability'), 
    Nutrition Num ('nutr_num'), 
    Frequent Meal('nutr_daily_freq_meal'), 
    Nutrition Quality('nutr_quality')


    Because these variables are categorical, we convert it to numeric for ease of computation
    'numeric_nutr_operability' 
        1 = functional
        0 = non-functional
    'numeric_nutr_num' 
        1 = Todos los días
        0 = others 
    'numeric_freq_meal' 
        1 = Se sirve  3 comidas al día (desayuno, almuerzo y cena) 
        0 = others
    'numeric_nutr_quality' 
        1 = Se siguen recomendaciones del especialista en cuanto al menú que se sirve
        0 = others

    The decision variable('XXXXX') has 3 values
    1 = best nutrition capability    (more than 3 out of 4 status variables are 1)
    0 = neutral nutrition capability (1 to 2 out of 4 status variables are 1)
    -1 = bad nutrition capability     (0 out of 4 status variables are 1)

    Input
    -----
    Pandas Dataframe

    Output
    ------
    Pandas Series

    """
    nutrition = df.copy()
    
    # Nutrition Available
    
    numeric = []

    for i in nutrition['nutr_avail']:
        if i == 'Sí':
            numeric.append(1)
        else:
            numeric.append(0)

    nutrition['numeric_nutr_avail'] = pd.Series(numeric)   
    
    # Nutrition Operability
    
    numeric = []

    for i in nutrition['nutr_operability']:
        if i == 'Sí':
            numeric.append(1)
        else:
            numeric.append(0)

    nutrition['numeric_nutr_operability'] = pd.Series(numeric)   

    # Nutrition Num
    numeric = []

    for i in nutrition['nutr_num']:
        if i == 'Todos los días':
            numeric.append(1)
        else:
            numeric.append(0)

    nutrition['numeric_nutr_num'] = pd.Series(numeric)   
    
    # Nutrition Daily Frequent Meal
    
    numeric = []

    for i in nutrition['nutr_daily_freq_meal']:
        if i == 'Se sirve  3 comidas al día (desayuno, almuerzo y cena)':
            numeric.append(1)
        else:
            numeric.append(0)

    nutrition['numeric_freq_meal'] = pd.Series(numeric)
    
    # Nutrition Quality
    numeric = []

    for i in nutrition['nutr_quality']:
        if i == 'Se siguen recomendaciones del especialista en cuanto al menú que se sirve':
            numeric.append(1)
        else:
            numeric.append(0)

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
    
    
    # Decision variable, 3-4 = good , 1-2 = medium, 0 = bad
    
    nutrition['temp'] = nutrition[['numeric_nutr_operability',
                                 'numeric_nutr_num',
                                 'numeric_freq_meal',
                                 'numeric_nutr_quality']].sum(axis=1)

    good_nutrition = []

    for i in nutrition['temp']:
        if i >= 3 :
            good_nutrition.append(1)
        elif i == 0  :
            good_nutrition.append(-1)
        else:
            good_nutrition.append(0)
    
    return pd.Series(good_nutrition)

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