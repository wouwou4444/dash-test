
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_table

import pandas as pd

df = pd.read_csv('./gapminder2007.csv',sep=";")

alert = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("Hello Bootstrap!"), width = 12)),
        dbc.Row(
            [
                dbc.Col(html.Div("Hello Second time!")),
                dbc.Col(html.Div("Hello third time!"))
            ]
        )
    ]
)

alert1 = html.Div(

    children=[

        dbc.Row([

            dbc.Col(dcc.Dropdown(id = 'dropdown-up',
                            options=[  
                                
                                     {'label': 'New York City', 'value': 'NYC'},
                                        {'label': 'Montreal', 'value': 'MTL'},
                                        {'label': 'San Francisco', 'value': 'SF'},
                                    ],
                            value= [] ,
                            multi=True
                        )

                   )],
        id='table-paging-with-graph-container'
        ),

        dbc.Row(dbc.Col(id = 'dd-output-container')),


        dbc.Row(
            
            dbc.Col(dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in sorted(df.columns)
                ],
                page_current=0,
                page_size=20,
                page_action='custom',

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[]
            ),
            style={'height': 750, 'overflowY': 'scroll'}
        )),

         dbc.Row(dbc.Col(id = 'dd2-output-container')),
        
    ]
)

alerts2 = dbc.Container(
    [
        alert,
        alert1
    ],
    className="p-5"
)

# Function Helper
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3
