#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
dropdown_style = style={'width':'80%', 'text-align-last':'center', 'font-size':20, 'padding':3}
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1(app.title,style={'color':'#503D36', 'text-align':'center', 'font-size':24}), #May include style for title
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Select Statistics',
            placeholder='Select a report type',
            style=dropdown_style
        )
    ]),
    html.Label("Select Year:"),
    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select year',
            style=dropdown_style,
            disabled=False
        )),
    html.Div([#TASK 2.3: Add a division for output display
        html.Div(id='output-container', className='chart-grid', style={'display':'flex'})
    ])
])
#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics',component_property='value'))

def update_input_container(report_type):
    if report_type == 'Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])


def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure = px.line(yearly_rec, 
                x = 'Year',
                y = 'Automobile_Sales',
                labels = {'Year':'Year','Automobile_Sales':'Avg. Sales'},
                title = 'Average Automobile Sales fluctuation over Recession Period'))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(
            figure=px.bar(data_frame = average_sales,
                          x = 'Vehicle_Type',
                          y = 'Automobile_Sales',
                          labels = {'Vehicle_Type':'Vehicle Type','Automobile_Sales':'Avg. Sales'},
                          title='Average number of vehicles sold by vehicle type'))

# # Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(data_frame=exp_rec,
                          names=exp_rec['Vehicle_Type'],
                          values=exp_rec['Automobile_Sales'],
                          title='Total expenditure share by vehicle type during recession' ))
        
# # Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
                       
        R_chart4  = dcc.Graph(
            figure=px.histogram(recession_data,
                          x = 'unemployment_rate', barmode='group',
                          color="Vehicle_Type",
                          labels = {'unemployment_rate':'Unemployment Rate','Automobile_Sales':'Sales'},
                          title='Effect of unemployment rate on vehicle type and sales'))        

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)] )
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              
#TASK 2.5: Creating Graphs Yearly data
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas,
                           x='Year',
                           y='Automobile_Sales',
                           labels = {'Year':'Year','Automobile_Sales':'Avg. Sales'},
                           title='Yearly Average Automobile sales'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        mas['Month'] = pd.Categorical(mas['Month'], categories=months, ordered=True)
        mas.sort_values(by='Month',ascending=True,inplace=True)  # same as you have now; can use inplace=True

        Y_chart2 = dcc.Graph(
            figure=px.line(mas,
                           x='Month',
                           y='Automobile_Sales',
                           labels={'Automobile_Sales':'Total sales'},
                           title='Total Monthly Automobile sales in the year {}'.format(input_year)
            )
        )
        
        # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                          x= 'Vehicle_Type',
                          y= 'Automobile_Sales',
                          labels={'Vehicle_Type':'Vehicle Type','Automobile_Sales':'Avg. Sales'},
                          title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            ))
        
        # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data,
            names=exp_data['Vehicle_Type'],
            values=exp_data['Advertising_Expenditure'],
            title='Total Advertisement Expenditure by vehicle type in the year {}'.format(input_year)
        ))

# #TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)] )
            ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

