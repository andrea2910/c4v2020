# C4V Hackathon

Our project addresses the question: `can I go to my local hospital for xyz?`. We created a process that takes the survey data and answers that question for 17 types of cases. We also created telegram bot that allows individuals to text and receive information about their local hospitals (details below).

We leverage Bigquery to pull data from the `angostura_dev.eh_health_survey_response` and insert it into our own table `event-pipeline.hulthack.dashboard_v1`. This data went into Tableau dashboard (attached). The code is automated and any user can run the following function `code/make_data.py` daily. There are no parameters needed in this code (however, the read/write permissions may need to be changed).

For the sample dashboard, you can run the code `sh setup.sh`. We use dash to create a sample dashboard but the interactivity does not work and the text must be mapped to colors/unicode text. 

For the sample bot, you can run the code `code/bot.py` and the application will be live with the name `c4v_bot`. The commands are `ayuda`, `empieza` with the name of the `state` every hospital with all the main information. 

To load the notebooks, type `jupyter lab --no-browser --port=3000` locally.

## Data Quality Errors
Details can be found here: `C4V_Data_Quality_Issues.pdf`.  For example, the column `wahs_failure_sx` is mispelt, and currently the data does not match this. Similarly the columns have differing definitions for not existing/not available ('No operativa', 'No existe', 'No hubo','Nunca ha existido').
