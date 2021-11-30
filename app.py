# -*- coding: utf-8 -*-
"""Dash Tutorial Testing.
Mainly inspired from https://github.com/STATWORX/blog/tree/master/DashApp
See:

"""
#     ///// //// /// // //    AAAAAAAAAA  MMMM     MMMM  GGGGGGGGGG
#    ///// //// /// // //    AAAA   AAAA  MM MM   MM MM  GG
#   ///// //// /// // //    AAAA    AAAA  MM  MM MM  MM  GG  GGGGGG
#  ///// //// /// // //    AAAAAAAAAAAAA  MM   MMM   MM  GG      GG
# ///// //// /// // //    AAAA      AAAA  MM         MM  GGGGGGGGGG
#                        ANALYTICS

"""
Created on 13.07.2021

@author: Karge, L.
"""


import pandas as pd

import dash
# import dash_auth
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_core_components as dcc
import plotly.express as px
import pathlib as pl
import os
import plotly.graph_objects as go

# from _users import USERNAME_PASSWORD_PAIRS

# Load data
csv_file = pl.Path(os.getcwd()).resolve().joinpath('data/stockdata2.csv').resolve()

feather_file = csv_file.parent.joinpath('stockdata2.feather').resolve()

if feather_file.is_file():
    df = pd.read_feather(feather_file)
else:
    # Convert columns 1 and 2 to pandas datetime for easier calculations
    df = pd.read_csv(csv_file)
    df.to_feather(feather_file)

df.index = pd.to_datetime(df['Date'])


# Creates a list of dictionaries, which have the keys 'label' and 'value'.
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


def amg_you_rock():
    '''
    returns: AMG you rock!
    '''
    return '''AMG you rock!'''


# Initialise the app
app = dash.Dash(__name__)
# auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                    html.Div(className='four columns div-user-controls',
                                        children=[
                                            html.Img(src=app.get_asset_url('Analytics_Logo_weiss_klein.png')),
                                            html.H2('DEMONSTRATOR APP - STOCK PRICES'),
                                            html.P('''Visualising time series with Dash'''),
                                            html.P('''Pick one or more stocks from the dropdown below.'''),
                                            html.P(amg_you_rock()),
                                        ],
                                    ),  # Define the left element
                                    html.Div(className='eight columns div-for-charts bg-grey', 
                                        children=[

                                            dcc.Graph(id='timeseries', config={'displayModeBar': False}),
                                            dcc.Graph(id='change', config={'displayModeBar': False}),
                                    
                                            html.Div(className='div-for-dropdown',
                                                children=[
                                                    dcc.Dropdown(id='stockselector',
                                                                options=get_options(df['stock'].unique()),
                                                                multi=True,
                                                                value=[df['stock'].sort_values()[0]],
                                                                style={'backgroundColor': '#1E1E1E'},
                                                                className='stockselector')
                                                            ],
                                                style={'color': '#1E1E1E'})
                                            ])
                                        ]
                                    ),  # Define the right element
                                ])



@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:   
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))  
    # STEP 3
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure
    
@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    for stock in selected_dropdown_value:
        trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                                 y=df_sub[df_sub['stock'] == stock]['change'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace]
    data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Daily Change', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=5050)

 