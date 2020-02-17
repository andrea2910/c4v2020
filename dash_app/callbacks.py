# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# @app.callback(
#     dash.dependencies.Output(component_id='state',component_property='options'),
#     [dash.dependencies.Input(component_id='hospital',component_property='value')]
# )
# def update_Menu_dropdown(selected_POS):
#     return [{'label': i, 'value': i} for i in input_data[input_data['POS'] == selected_POS]['MenuItem'].unique()]