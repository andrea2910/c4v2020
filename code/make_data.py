import sys
import urllib.request
import os
from google.cloud import bigquery
from indicators import * # code.indicators?
from config import CONFIG_JSON
from datetime import datetime
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG_JSON

def load_data():
    '''
    load_data
    ---------
    This function call bigquery and return a dataframe of the most recent survey data

    Input
    -----
    None

    Output
    ------
    Dataframe
    '''

    QUERY = ("""
    WITH all_data as (
        select *, 
        ROW_NUMBER() OVER (PARTITION BY hospital_code ORDER BY timestamp DESC) as latest_date
        from `angostura_dev`.eh_health_survey_response
    )
    SELECT *
    FROM all_data
    where latest_date=1
    """)

    client = bigquery.Client()
    
    df = client.query(QUERY).to_dataframe()  
    return(df)

def hospital_code_dict():
    """
    hospital_code_dict
    ------------------
    This function contains the hardcoded map of the hospital names to hopsital codes.

    Input
    -----
    None

    Output
    ------
    Dictionary

    """
    hard_coded_dict = {
        'AMA000':'Hospital Dr. José Gregorio Hernández. Amazonas',
        'ANZ000':'Hospital Universitario Dr. Luis Razzetti. Anzoátegui',
        'ANZ001':'Hospital Felipe Guevara Rojas. Anzoátegui',
        'ANZ002':'Hospital de Guaraguao. Anzoátegui',
        'APU000':'Hospital Dr. Pablo Acosta Ortiz. Apure',
        'ARA000':'Hospital José María Benítez. Aragua',
        'ARA001':'Hospital Coronel Elbano Paredes Vivas. Aragua',
        'ARA002':'Hospital Central de Maracay. Aragua',
        'BAR000':'Hospital Dr. Luis Razetti. Barinas',
        'BOL000':'Hospital Ruiz y Páez. Bolívar',
        'BOL001':'Hospital Uyapar. Bolívar',
        'CAR000':'Hospital Dr. Ángel Larrralde. Carabobo',
        'CAR001':'Ciudad Hospitalaria Enrique Tejera. Carabobo',
        'COJ000':'Hospital General de San Carlos. Cojedes',
        'DEL000':'Hospital Dr. Luis Razetti. Delta Amacuro',
        'DCA000':'Hospital Militar. Dtto. Capital',
        'DCA001':'Hospital Vargas. Dtto. Capital',
        'DCA002':'Hospital JM de los Ríos. Dtto. Capital',
        'DCA003':'Hospital Universitario de Caracas. Dtto. Capital',
        'DCA004': 'Maternidad Concepción Palacios. Dtto. Capital',
        'DCA005':'Hospital Dr. Miguel Pérez Carreño. Dtto. Capital',
        'DCA006':'Hospital Magallanes de Catia. Dtto. Capital',
        'FAL000':'Hospital Dr. Alfredo Van Grieken. Falcón',
        'GUA000': 'Hospital Dr. Israel Ranuarez Balza. Guárico',
        'LAR000':'Hospital Universitario Dr. Antonio María Pineda. Lara',
        'MER000':'Hospital Universitario de los Andes. Mérida',
        'MIR000':'Hospital Domingo Luciani. Miranda',
        'MIR001':'Hospital General Dr. Victorino Santaella',
        'MON000':'Hospital Universitario Dr. Manuel Núñez Tovar. Monagas',
        'NES000':'Hospital Dr. Luis Ortega. Nueva Esparta',
        'POR000':'Hospital Dr. Miguel Oraa. Portuguesa',
        'SUC000':'Hospital Antonio Patricio de Alcalá. Sucre',
        'TAC000':'Hospital Patrocinio Peñuela. Táchira',
        'TAC001':'Hospital Central de San Cristóbal. Táchira',
        'TRU000':'Hospital Universitario Dr. Pedro Emilio Carrillo. Trujillo',
        'VAR000':'Hospital Dr. José María Vargas. Vargas',
        'YAR000':'Hospital Plácido Rodriguez Rivero , Yaracuy',
        'ZUL000':'Hospital Universitario de Maracaibo. Zulia',
        'ZUL001':'Hospital General del Sur'
    }
    return(hard_coded_dict)

def create_clean_df(df):
    '''
    create_clean_df
    ---------------
    This function uploadas a clean df to get the data into a correct format. 
    We create the following indicators where 1 = YES/SI, 0 = MAYBE/BRING SUPPLIES, -1 = NO:
    - power
    - water 
    - safety
    - surgery/appendicitis
    - er
    - icu 
    - icu - p
    - pregnancy
    - dialysis
    - machine
    - medical supply: asthma, insulin, lidocaine
    - staff: ER staff general, staff critical
    - disease: can handle infectious disease
    Input
    -----
    Pandas Data Frame

    Output
    ------
    Pandas Data Frame
    '''
    hospital_map = hospital_code_dict()
    df['Hospital'] = df['hospital_code'].map(hospital_map)

    keep_cols = ['report_week', 'Hospital', 'federal_entity']
    new_cols = ['power', 'water','safety', 'surgery', 'er_avail_general', 'icu', 'icu_p', 'pregnancy', 'dialysis', 'machine',
    'med_supply_asthma', 'med_supply_insulin', 'med_supply_lidocaine', 'er_staff_general','er_staff_critical','disease']
    cleaned_df = df[keep_cols]

    cleaned_df.loc[:, 'power'] = power_indicator.power_indicator(df)
    cleaned_df.loc[:, 'water'] = water_indicator.water_indicator(df)
    cleaned_df.loc[:, 'safety'] = safety_indicator.safety_indicator(df)
    cleaned_df.loc[:, 'surgery'] = sx_indicator.surgery_indicator(df)
    er_tmp = er_indicator.er_indicator(df)
    for c in er_tmp.columns:
        cleaned_df.loc[:, c] = er_tmp.loc[:, c]
    cleaned_df.loc[:, 'icu'] = icu_indicator.icu_indicator(df,'operability_icu')
    cleaned_df.loc[:, 'icu_p'] = icu_indicator.icu_indicator(df,'operability_icu_p')
    cleaned_df.loc[:, 'pregnancy'] = pregnancy_indicator.pregnancy_indicator(df)
    cleaned_df.loc[:, 'dialysis'] = dialysis_indicator.dialysis_indicator(df)
    # change logic if no power then change dialysis to no
    cleaned_df.loc[cleaned_df.power==-1, 'dialysis'] = -1 
    cleaned_df.loc[:, 'disease'] = nutrition_indicator.disease_indicator(df)
    cleaned_df.loc[:, 'machine'] = power_indicator.machine_indicator(df)
    cleaned_df.loc[:, 'med_supply_asthma'] = medical_supply_indicator.medical_supply_indicator(df, 'er_avail_asthma')
    cleaned_df.loc[:, 'med_supply_insulin'] = medical_supply_indicator.medical_supply_indicator(df, 'er_avail_insulin')
    cleaned_df.loc[:, 'med_supply_lidocaine'] = medical_supply_indicator.medical_supply_indicator(df, 'er_avail_lidocaine')
    
    cleaned_df = cleaned_df.astype(str)

    cleaned_df.loc[:, 'insert_date'] = datetime.today().date()
    
    #cleaned_df.loc[:, new_cols] = cleaned_df.loc[:, new_cols].apply(pd.to_numeric)

    cleaned_df = cleaned_df.loc[:, keep_cols + new_cols + ['insert_date']]

    return(cleaned_df)

def create_bq_table(df, dataset="hulthack", table_name="dashboard_v1"):
    """
    creat_bq_table
    --------------
    This function creates a bigquery table from the schema of a pandas dataframe.
    It partitions the table based on insert_date (the day the partition was inserted
    into the table).

    Input
    -----
    Pandas Data Frame
    dataset (optional)
    table_name (optional)

    Output
    ------
    None
    """
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset)

    table_ref = dataset_ref.table(table_name)
    schema = list()
    
    for column in df.columns:
        if column == "insert_date":
            schema.append(bigquery.SchemaField("insert_date", "DATE"))
        else:
            schema.append(bigquery.SchemaField(column, "STRING"))

    
    table = bigquery.Table(table_ref, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="insert_date",  # name of column to use for partitioning
    )

    table = client.create_table(table)

    print(
        "Created table {}, partitioned on column {}".format(
            table.table_id, table.time_partitioning.field
        )
    )

def drop_table(table_ref):
    """
    drop_table
    ----------
    This function drops a bigquery table.

    Input
    -----
    table_ref

    Output
    ------
    None
    """
    client = bigquery.Client()
    client.delete_table(table_ref, not_found_ok=True)

def upload_clean_df(df, table_id = "event-pipeline.hulthack.dashboard_v1"):
    """
    upload_clean_df
    ---------------
    This function uploads a clean df to a bigquery table.

    Input
    -----
    Pandas Data Frame
    table_id (optional)

    Output
    ------
    None
    """
    client = bigquery.Client()

    schema = list()
    
    for column in df.columns:
        if column == "insert_date":
            schema.append(bigquery.SchemaField("insert_date", "DATE"))
        else: #column in ['report_week', 'Hospital', 'federal_entity']:
            schema.append(bigquery.SchemaField(column, "STRING"))
        
    
    time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="insert_date",  # name of column to use for partitioning
    )

    job_config = bigquery.LoadJobConfig(schema=schema,
                                        time_partitioning=time_partitioning)
    
    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )

def upload_dashboard_data():
    """
    upload_dashboard_data
    ---------------------
    This function gathers data from a big query table, cleans data, and 
    then uploads data to a bigquery table.

    Input
    -----
    None

    Output
    ------
    None
    """
    try:
        df = load_data()
        new_df = create_clean_df(df)
        upload_clean_df(new_df)
    except Exception as e:
        print(e)
    print('Uploaded Data...')

if __name__ == "__main__":
    upload_dashboard_data() # can run query make_data.py and this will work