# Import required libraries
import pandas as pd
import dash
# import dash_core_components as dcc    #deprecated
from dash import dcc 
# import dash_html_components as html    #deprecated
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

LS=spacex_df['Launch Site'].unique()
dropdown_options = [
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': LS[0],     'value': LS[0]},
    {'label': LS[1],     'value': LS[1]},
    {'label': LS[2],     'value': LS[2]},
    {'label': LS[3],     'value': LS[3]},
]

pie_suc_ls=spacex_df.groupby('Launch Site')['class'].sum().reset_index()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown', 
                                             options=dropdown_options,
                                             value='ALL',
                                             placeholder='Select Launch Site',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(
                                    dcc.Graph(id='success-pie-chart',
                                              figure=px.pie(pie_suc_ls,
                                                            values='class',
                                                            names='Launch Site',
                                                            title="total successful launches count for all sites"
                                                            )
                                              )
                                    ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                #value=[min_value, max_value]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart',
                                                   figure=px.scatter(
                                                       x=spacex_df['Payload Mass (kg)'],
                                                       y=spacex_df['class'],
                                                       color=spacex_df['Booster Version Category']
                                                   )
                                             )
                                         
                                         ),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    print('aaaa',entered_site)
    if entered_site == 'ALL':
        fig = px.pie(pie_suc_ls, 
                     values='class',
                     names='Launch Site',
                     title="total successful launches count for all sites"
                     )
        
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        pos, neg = len(filtered_df[filtered_df['class']==1]), len(filtered_df[filtered_df['class']==0])
        new_df=pd.DataFrame({'type':['Success', 'Fail'], 'result': [pos,neg]})
        fig = px.pie(new_df, 
                     values='result', 
                     names='type', 
                     title='successful launches count for ' + entered_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_payload_update(entered_site, payload):
    #print('aaaa',entered_site, payload)
    if entered_site == 'ALL':
        fig=px.scatter(x=spacex_df['Payload Mass (kg)'],
                       y=spacex_df['class'],
                       color=spacex_df['Booster Version Category']
                       )
            
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        fig=px.scatter(x=filtered_df['Payload Mass (kg)'],
                       y=filtered_df['class'],
                       color=filtered_df['Booster Version Category']
                       ) 
    fig.update_layout(xaxis_range=payload)
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
