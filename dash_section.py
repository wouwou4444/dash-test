
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_table

import pandas as pd

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

df = pd.read_csv('./gapminder2007.csv',sep=";")

alert = html.Div(
    [
        dbc.Alert("Filters applied", color ="success"),
        dbc.Row(
            [
                dbc.Col(dbc.Alert("Column Name", color = "primary")),
                dbc.Col(dbc.Alert("Operator", color = "primary")),
                dbc.Col(dbc.Alert("value", color = "primary"))
            ]
        )
    ]
)

row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("Application Dash"))),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns"), align="center"),
                dbc.Col(html.Div("One of three columns")),
                dbc.Col(html.Div("One of three columns"))
            ]
        )
    ]
)


################

filter_entry_bar = html.Div(

    children=[

        dbc.Row([

            dbc.Col(
                dcc.Dropdown(id = 'filter-column-selection',
                             options = [
                                 {'label': column, 'value': column} for column in df.columns
                             ],
                             multi=False,
                             placeholder="Select a column on which to filter"
                                )
                   ),
            dbc.Col(
                dcc.Dropdown(id = 'filter-operator-selection',
                             options = [
                                 {'label': op[0], 'value': op[0]} for op in operators
                             ],
                             multi=False,
                             placeholder="Select the type of filter"
                                )
                   ),
            dbc.Col(
                dbc.Input(id = "filter-value-selection",
                     placeholder="Enter a value here")
            )
        ],
        id='filter-entry-container'
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Filter", 
                           color = "primary", 
                           className="mr-1", 
                           block=True,
                           id = "filter-button-selection"),
                width=6,
                align="center"
            ),
            justify="center"
        ),
        html.Div(id="filter-output-selection")
        
    ]
)

##############

alert1 = html.Div(

    children=[

        dbc.Row([

            dbc.Col(dcc.Dropdown(id = 'dropdown-up',
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

# Hidden div inside the app that stores the intermediate value
hidden = html.Div(id='filter-hidden-value')#, style={'display': 'none'})
    
alerts2 = dbc.Container(
    [
        row,
        alert,
        filter_entry_bar,
        alert1,
        hidden
    ], 
    style={'margin': 10}
)


# Function Helper


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
