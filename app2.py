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

app.layout = dash_section.row






if __name__ == "__main__":
    app.run_server(port = 8051)