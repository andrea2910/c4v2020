# C4V Hackathon

We leverage Bigquery to pull data from the `angostura_dev.eh_health_survey_response` and insert it into our own table `event-pipeline.hulthack.dashboard_v1`. This data will go into a Tableau dashboard. The code is automated and any user can run the following function `code/make_data.py` daily. There are no parameters needed in this code (however, the read/write permissions may need to be changed).

For the sample dashboard, you can run the code `sh setup.sh`.

To load the notebooks, type `jupyter lab --no-browser --port=3000` locally.

_Assumptions_
Data quality errors: The column `wahs_failure_sx` is mispelt, and currently the data does not match this. Similarly the columns have differing definitions for not existing/not available ('No operativa', 'No existe', 'No hubo','Nunca ha existido')

_Definitions of Indicators_
Water indicator (based off the 3 columns `wash_failure_icu`, `wash_failure_er`, and `wahs_failure_sx`):
If all 3 water indicators says never exist, then NOT AVAILABLE
If all 3 water indicators always have water, then YES AVAILABLE
Else maybe

Surgery indicator:
If op_pavilions_count = 0 then _cannot do surgery_
If op_pavilions_count > 0 and 
    sx_avail_anesthetics_iv, sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction DOESNT WORK, then _cannot do surgery_
If op_pavilions_count > 0 and sx_avail_anesthetics_iv, sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction ALWAYS works, then _can always do_
Else _maybe_

ICU indicator (`operability_icu`, `operability_icu_p`):
If it never works/doesnt exit then you cannot use the ICU
if it always work then you can go to the ICU
Otherwise maybe
