import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from functions import df_unicode, unique_states, unique_hospitals, df_unicode_default # this is our clean data
'''
children of layout and in order
'''

state_filter = html.Div([
    html.Div([
        html.H4('Select State'),
        dcc.Dropdown(
        id='state',
        options=unique_states,
        multi=True,
        value="all"
        )])],
        style={'width': '48%', 'display': 'inline-block'})

hospital_filter = html.Div([
    html.Div([
        html.H4('Select Hospital'),
        dcc.Dropdown(
        id='hospital',
        options=unique_hospitals,
        multi=True,
        value="all"
        )])],
        style={'width': '48%', 'display': 'inline-block'}
)

default_table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df_unicode_default.columns],
    data=df_unicode_default.to_dict('records'),
)