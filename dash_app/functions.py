from google.cloud import bigquery
from config import CONFIG_JSON
import os 

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG_JSON

def pull_latest_data():

    client = bigquery.Client()
    sql = """
    DECLARE max_date DATE;
    SET max_date = (
    SELECT MAX(insert_date) FROM `hulthack.dashboard_v1`);
    SELECT *
    FROM `hulthack.dashboard_v1`
    WHERE insert_date = max_date
    """
    df = client.query(sql).to_dataframe()
    return(df)

def get_unique_states_labels(df):
    unique_vals = df.federal_entity.unique()
    list_of_dicts = []
    for v in unique_vals:
        list_of_dicts.append({'label': v, 'value':v})
    list_of_dicts.append({'label':'All', 'value':'all'})
    #print(list_of_dicts)
    return(list_of_dicts)

def get_unique_hospitals_labels(df):
    unique_vals = df.Hospital.unique()
    list_of_dicts = []
    for v in unique_vals:
        list_of_dicts.append({'label': v, 'value':v})
    list_of_dicts.append({'label':'All', 'value':'all'})
    #print(list_of_dicts)
    return(list_of_dicts)

def transform_to_unicode(df):
    new_cols = ['power', 'water','safety', 'surgery', 'er_avail_general', 'icu', 'icu_p', 'pregnancy', 'dialysis', 'machine',
    'med_supply_asthma', 'med_supply_insulin', 'med_supply_lidocaine', 'er_staff_general','er_staff_critical','disease']
    #map_vals = {'1':'\U\0002705', '0':'\U\00026A0', '-1':'\u\0001F6D1'}
    map_vals = {'1':'\u0002705', '0':'\u00026A0', '-1':'\u0001F6D1'}
    df.loc[:, new_cols] = df.loc[:,new_cols].apply(lambda x: x.map(map_vals))
    return(df)

def transform_column_names(df):
    return()

data = pull_latest_data()

df_unicode = transform_to_unicode(data)
df_unicode_default = df_unicode.copy()
# print(df_unicode_default.head())
unique_states = get_unique_states_labels(data)
unique_hospitals = get_unique_hospitals_labels(data)


