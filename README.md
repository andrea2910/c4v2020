# C4V Hackathon

To load the notebooks, type `jupyter lab --no-browser --port=3000` locally.

Get dashboard to work....
To set up dashboard directly run the file `setup.sh` and you can go to localhost:8050

_Assumptions_
Data quality errors: The column `wahs_failure_sx` is mispelt, and currently the data does not match this. Similarly the columns have differing definitions for not existing/not available. 

_Definitions of Indicators_
Water indicator:
If all 3 water indicators do not exist, then no water
If all 3 water indicators always have water, then water
Else maybe

Surgery indicator:
If op_pavilions_count = 0 then cannot do surgery
If op_pavilions_count > 0 and 
    sx_avail_anesthetics_iv, sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction DOESNT WORK, then cannot do
If op_pavilions_count > 0 and sx_avail_anesthetics_iv,           sx_avail_anesthetic_gases, 
    sx_avail_ott_intubation,sx_avail_oxygen_suction ALWAYS works, then can always do

ICU indicator:
If it never works/doesnt exit then it is a no
if it always work then it is a yes
otherwise maybe