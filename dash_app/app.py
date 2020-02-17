import dash
import dash_core_components as dcc
import dash_html_components as html

from layouts import state_filter, hospital_filter, default_table

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Code 4 Venezuela: Born in Venezuela'),
    html.Div([
        state_filter,
        hospital_filter
    ]),
    html.Div([default_table])
])

if __name__ == '__main__':
    app.run_server(host="0.0.0.0",debug=True) # 8050