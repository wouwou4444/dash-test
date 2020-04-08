import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_table

import pandas as pd

import dash_section
from dash_section import split_filter_part

import json

BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cosmo/bootstrap.min.css"
BS = "dbc.themes.BOOTSTRAP"

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    #external_stylesheets=[BS]
)

app.layout = dash_section.alerts2



@app.callback(
    [Output('dd-output-container', 'children'),
    Output('filter-hidden-value','children')]
    ,
    [Input('dropdown-up', 'value'),
    Input('dropdown-up', 'options')
    ])
def update_output(value,options):
    #previous_hidden = json.loads('')
    hidden = (value, options)
    return ('You have selected "{} {}"'.format(value,options),
            json.dumps(hidden))
            
@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('dataframe-hidden-value', 'children')]
)
def update_table(page_current, page_size, sort_by, dataframe):
    dff = pd.read_json(dataframe, orient = 'split')
    
    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
            
    return dff.iloc[ 
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@app.callback(
    Output('dataframe-hidden-value', "children"),
    [
     Input('dropdown-up', 'value')
     ])

def update_hidden_dataframe(value):

    dff = dash_section.df
    print("in update_table(1), {}, value: {}".format(type(value),value))
    
    if (value is None) or( value == []):
        pass
    else:
        print("in update_table(2), {}, value: {}".format(type(value),value))
        for filter in value:
            col_name, operator, filter_value = filter.split()

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    return dff.to_json(date_format='iso', orient='split')

@app.callback(
    [Output('dropdown-up', 'options'),Output('dropdown-up', 'value')],
    [Input('filter-button-selection', "n_clicks")],
    [State('filter-column-selection', "value"),
     State('filter-operator-selection', "value"),
     State('filter-value-selection', "value"),
     State('dropdown-up', 'options'),
     State('dropdown-up', 'value')]
)

def update_dropdown_2(n_clicks, column, operator, value, previous_dropdown_options, previous_dropdown_value ):
    print("in update_dropdown_2: {}".format(column))
    print("in update_dropdown_2: {}".format(operator))
    print("in update_dropdown_2: {}".format(value))
    print("in update_dropdown_2: {}".format(n_clicks))
    print("in update_dropdown_2: {}".format(previous_dropdown_options))
    print("in update_dropdown_2: {}".format(previous_dropdown_value))
    str_output = '{} {} {}'.format(column, operator, value)
    #return ([{'label': str_output, 'value': str_output}],
            #[str_output])
    if n_clicks:
        previous_dropdown_options = list(previous_dropdown_options)
        previous_dropdown_value = list(previous_dropdown_value)
        previous_dropdown_options.append({'label': str_output, 'value': str_output})
        new_dropdown_options = previous_dropdown_options
        previous_dropdown_value.append(str_output)
        new_dropdown_value = previous_dropdown_value
        print("in update_dropdown2_2(21): {}".format(new_dropdown_value))
        print("in update_dropdown2_2(22): {}".format(new_dropdown_options))
        print("in update_dropdown2_2(23): {}".format(str_output))
    
        return (new_dropdown_options, new_dropdown_value)
    else:
        return ([],[])




"""@app.callback(
    [Output('dropdown-up', 'options'),Output('dropdown-up', 'value')],
    [Input('table-paging-with-graph', "filter_query")
    ])

def update_dropdown(filter):
    print("in update_dropdown filter {}, value: {}".format(type(filter),filter))
    filtering_expressions = filter.split(' && ')

    col_name_list = []
    filter_list = []
    operator_list = []
    for filter_part in filtering_expressions:
        print("in update_dropdown {}".format((filter_part)))
        col_name,operator,filter_value = split_filter_part(filter_part)
        print("in update_dropdown {}".format(type(filter_value)))

        col_name_list.append(col_name)
        filter_list.append(filter_value)
        operator_list.append(operator)
       
        test = [{"label":str(col_name) +" " + str(operator) +" " + str(filter), "value": str(col_name) +" " + str(operator) +" " + str(filter)} for col_name, operator, filter in zip(col_name_list,operator_list, filter_list)]
        value = [filter['label'] for filter in test]
        print("in update_dropdown test var {}".format(type(test)))
    return test , value
"""

if __name__ == "__main__":
    app.run_server()