
import sys
import urllib.request
import os
from google.cloud import bigquery

def load_data():
    url = 'https://storage.googleapis.com/angostura-public/hult-hackathon-key.json'
    urllib.request.urlretrieve(url, './hult-hackathon-key.json')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './hult-hackathon-key.json'

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
