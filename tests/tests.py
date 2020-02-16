from code.make_data import load_data, create_clean_df, create_bq_table, upload_clean_df
from code.indicators import *
from google.cloud import bigquery
import os 
from config import CONFIG_JSON

if __name__ == "__main__":
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = CONFIG_JSON
    df = load_data()
    print(len(df))

    ## test specific indicators
    assert sum(icu_indicator.icu_indicator(df, 'operability_icu')==1) == sum(df.operability_icu=='Todos los días'), 'ICU does not match every day count'
    assert sum(icu_indicator.icu_indicator(df, 'sx_avail_minor_opioids')==1) == sum(df.sx_avail_minor_opioids=='Todos los días'), 'Opiods does not match'

    new_df = create_clean_df(df)
    print(new_df.head())

    #create_bq_table(new_df)
    # from datetime import datetime, timedelta
    # new_df['insert_date'] = (datetime.today() - timedelta(days=1)).date()
    # upload_clean_df(new_df)

    client = bigquery.Client()
    sql = """
    DECLARE max_date DATE;
    SET max_date = (
    SELECT MAX(insert_date) FROM `hulthack.dashboard_v1`);
    SELECT *
    FROM `hulthack.dashboard_v1`
    WHERE insert_date = max_date
    """
    assert len(df) == len(client.query(sql).to_dataframe()), 'mismatch type'