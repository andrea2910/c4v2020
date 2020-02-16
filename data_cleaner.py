"""
data_cleaner.py
---------------
This script prepares the data for data visualization.
"""
import os
import sys

import argparse
from google.cloud import bigquery
import urllib.request

def main(args):
    ### Load Data Key
    urllib.request.urlretrieve(args.key_url, './hult-hackathon-key.json')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './hult-hackathon-key.json'

    ### Get Data from Big Query Client
    client = bigquery.Client()
    query = ('select * from `angostura_dev`.eh_health_survey_response')
    df = client.query(query).to_dataframe() 
    print("")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="")
	parser.add_argument("key_url", help="", action='store', 
                        default='https://storage.googleapis.com/angostura-public/hult-hackathon-key.json')
	argv = parser.parse_args()
	sys.exit(main(args=argv))