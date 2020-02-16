import sys
import urllib.request
import os
from google.cloud import bigquery
from code.indicators import *
from config import CONFIG_JSON
from datetime import datetime
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG_JSON

def load_data():

    QUERY = ("""
    WITH all_data as (
    select *, ROW_NUMBER() OVER (PARTITION BY hospital_code ORDER BY timestamp DESC) as latest_date from `angostura_dev`.eh_health_survey_response
    )
    SELECT *
    FROM all_data
    where latest_date=1
    """)

    client = bigquery.Client()
    
    df = client.query(QUERY).to_dataframe()  
    return(df)

def hospital_code_dict():
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
    Create the indcitors:
    - power
    - water 
    - dialysis
    - icu 
    - icu - p
    - pregnancy
    - surgery/appendicites
    - medical supply: asthma, insulin 

    MERGE clean hospital name
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
    cleaned_df.loc[:, '_PARTITIONTIME'] = datetime.today().date()
    
    cleaned_df.loc[:, new_cols] = cleaned_df.loc[:, new_cols].astype(int)

    cleaned_df = cleaned_df.loc[:, keep_cols + new_cols + ['_PARTITIONTIME']]

    return(cleaned_df)

def create_bq_table(df, dataset="hulthack"):
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset)

    table_ref = dataset_ref.table("indicators-dash")
    schema = list()
    
    for column in df.columns:
        if column == "_PARTITIONTIME":
            schema.append(bigquery.SchemaField("_PARTITIONTIME", "DATE"))
        elif column in []:
            schema.append(bigquery.SchemaField(column, "STRING"))
        else:
            bigquery.SchemaField(column, "INT64"),
        
    
    table = bigquery.Table(table_ref, schema=schema)
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="_PARTITIONTIME",  # name of column to use for partitioning
    )

    table = client.create_table(table)

    print(
        "Created table {}, partitioned on column {}".format(
            table.table_id, table.time_partitioning.field
        )
    )

def upload_clean_df(df, dataset="hulthack"):
    client = bigquery.Client()
    dataset_ref = client.dataset(dataset)