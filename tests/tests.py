from config import URL
from code.make_data import load_data, create_clean_df
from code.indicators import *

if __name__ == "__main__":
    df = load_data(URL)
    print(len(df))

    ## test specific indicators
    assert sum(icu_indicator.icu_indicator(df, 'operability_icu')==1) == sum(df.operability_icu=='Todos los días'), 'ICU does not match every day count'
    assert sum(icu_indicator.icu_indicator(df, 'sx_avail_minor_opioids')==1) == sum(df.sx_avail_minor_opioids=='Todos los días'), 'Opiods does not match'

    new_df = create_clean_df(df)
    print(new_df.head())
