# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
# Create a dash application
app = dash.Dash(__name__)

spacex_df =  pd.read_csv('spacex_launch_dash.csv')
min_value=spacex_df['Payload Mass (kg)'].min()
max_value=spacex_df['Payload Mass (kg)'].max()
app.layout = html.Div(children=[html.H1('ٍSpacex Dashboard', 
                    style={'textAlign': 'center', 'color': '#503D36',
                    'font-size': 40}),
                    dcc.Dropdown(id='site-dropdown',
                        options=[
                            {'label': 'All Sites', 'value': 'ALL'},
                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                            {'label': 'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                        ],
                        value='ALL',
                        placeholder="Select a launch site here",
                        searchable=True),
                    html.Br(),
                    html.Div(dcc.Graph(id = 'success-pie-chart')),
                       
                    dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    # marks={i: '{}'.format(2500 +i) for i in range(3)},
                                    marks={0:'0',100:'100'},
                                    value=[min_value, max_value]
                                    ),
                    html.Br(),
                    html.Div(dcc.Graph(id= "success-payload-scatter-chart"))
                    ])  
# 
# Task 2 Add a callback function to render
# Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
    # data=filtered_df['class']
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', # names of column use to set values
        title='Total success launch by site')
        return fig
        
    else:
    # return the outcomes piechart for a selected site
    # data=spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        data=spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        data=data.groupby(['Launch Site', 'class']).size().reset_index(name ='Launch_Class count')
        fig=px.pie(data,values='Launch_Class count',
        names='class',
        title= f'Success launch for {entered_site}')
        return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site,slider): 

    filtered_df=spacex_df[(spacex_df['Payload Mass (kg)']>=slider[0])&(spacex_df['Payload Mass (kg)']<slider[1])]
    if entered_site == 'ALL':
        fig1= px.scatter(filtered_df, x= 'Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig1
        
    else:
    # return the outcomes scatter chart for a selected site
        data = filtered_df.loc[filtered_df['Launch Site']== entered_site]
        fig1= px.scatter(data, x= 'Payload Mass (kg)', y='class', color="Booster Version Category")
        return fig1
# Run the app
if __name__ == '__main__':
    app.run_server()
