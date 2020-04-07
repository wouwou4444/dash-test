import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_table

import pandas as pd

import dash_section
from dash_section import split_filter_part

BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/cosmo/bootstrap.min.css"

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

app = dash.Dash(
    #external_stylesheets=[dbc.themes.BOOTSTRAP]
    external_stylesheets=[BS]
)

app.layout = dash_section.alerts2



@app.callback(
    Output('dd-output-container', 'children'),
    [Input('dropdown-up', 'value'),
    Input('dropdown-up', 'options')
    ])
def update_output(value,options):
    return 'You have selected "{} {}"'.format(value,options)


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('dropdown-up', 'value')
     ])

def update_table(page_current, page_size, sort_by, value):

    dff = dash_section.df
    print("in update_table, {}, value: {}".format(type(value),value))
    if value is None:
        return dff
    
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
    [Output('dropdown-up', 'options'),Output('dropdown-up', 'value')],
    [Input('table-paging-with-graph', "filter_query")
    ])

def update_dropdown(filter):
    print("in update_dropdown filter {}, value: {}".format(type(filter),filter))
    filtering_expressions = filter.split(' && ')
    #dff = df
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


if __name__ == "__main__":
    app.run_server()