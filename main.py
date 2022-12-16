#importing required libraries and modules
import dash #framework for building web apps
from dash import dcc #core components of dash used to create interactive applications
from dash import html # html components to style the application using html
import plotly.express as px #easy and quick way to make use of plotly to visualise data
import pandas as pd #for creating and handling dataframes
from dash.dependencies import Input, Output #to specify the inputs and outputs for app callbacks
import dash_bootstrap_components as dbc # to use inbuilt bootstrap features like themes 
import os
#importing dataset from kaggle
dir_name = os.path.abspath(os.path.dirname(__file__))
location = os.path.join(dir_name, 'country.csv')
df=pd.read_csv(location)
#This is an extensive dataset containg data regarding various variables that can be used for measuring the developement of a
#country. A subset of those parameters have been used for visualisation to analyse the developement of each country.
app = dash.Dash(external_stylesheets=[dbc.themes.MATERIA])#starting the dash framework and specifying materia theme

#Dash web application has 2 parts, layout and interactivity
#Specifying the layout using HTML as Dash provides layout specification using HTML like tags
app.layout = html.Div([
    html.H1("Country Profiles' Study",style={"margin": "0.5em 1em 0.5em 1em",
                                                "font-weight": "600",
                                                "font-family": 'Trebuchet MS', 
                                                "font-size": "36px",
                                                "line-height": '40px',
                                                "text-align":"center",
                                                "padding": "15px 15px 15px",
                                                "color": "#355681",
                                                "box-shadow":
                                                    ["inset 0 0 0 1px rgba(53,86,129, 0.4)", 
                                                    "inset 0 0 5px rgba(53,86,129, 0.5)",
                                                    "inset -285px 0 35px white"],
                                                "border-radius": "0 10px 0 10px"}),
    #inline styling is being used for each component
    html.Div(id='speck-control-tabs', className='control-tabs', style={'backgroundColor':'blue'},children=[
            dcc.Tabs(id='graph', value='scatter', children=[#specifying tabs for each component of study
                dcc.Tab(
                    label='Population',
                    value='scatter',style={"background-color":"#99ccff"}
                    ),
                dcc.Tab(
                    label='Sociological Analysis',
                    value='bar',style={"background-color":"#99ffcc"}
                    ),
                dcc.Tab(
                    label='Economy and Employment',
                    value='pie',style={"background-color":"#ffcc99"}
                    ),
                dcc.Tab(
                    label='GDP Study',
                    value='hist',style={"background-color":"#ffff99"}
                    )])]),
    html.Div(id="plotval")#empty div to show results after callbacks

])
#Specifying second component i.e. interactivity
#callbacks monitor changes in the webapp and execute the function below them automatically as and when changes occur
#here the tabs are being monitored for change i.e. being pressed. and the empty div is populated with the required plot
@app.callback(
    Output(component_id='plotval', component_property='children'),#component to change as a result of some change in exising components
    Input(component_id='graph', component_property='value')# component to monitor for changes
)
#update graph function is being executed by callback. 
#whenever the value property of component with id "graph" i.e. DCC Tabs changes, the changed "value" is  passed as 
#an argument to the function and the requiured plot is displayed accordingly
def update_graph(option):
    if(option=="scatter"): #i.e. if the tab with value "scatter" is selected
        #creating scatter plot using plotly express
        fig=px.scatter(
            df, #dataframe to use
            x=df.columns[2], #name of column of dataframe to be plotted on x axis
            y=df.columns[3], #name of column of dataframe to be plotted on y axis
            color="Region", #name of column of dataframe to be used for assigning colours, each unique value is assigned a different colour
            hover_name="country", # heading to be shown when pointer hovers over a data component
            log_x=True, #as x axis values are not well distributed with some very high values, logarithm of the values is plotted to improve readability
            log_y=True, #as y axis values are not well distributed with some very high values, logarithm of the values is plotted to improve readability
            size=df.columns[4] # size of the points is being specified by the dataframe's population density column
        )
         #returning the plotted graph as "children" of the "plotval" id component(empty div)
        return dcc.Graph(id="plot1",style={'width': '90vw', 'height': '90vh'},figure=fig)

    elif option=="hist": #i.e. if the tab with value "hist" is selected
        temp=df[df.columns[6]].values #storing the GDP column temporarily for plotting
        temp=temp[temp>0] # removing rows with -ve GDP as it is incorrect, data is removed from temp so original dataframe is not affected
        fig=  px.histogram(
            x=temp, #data to use for plotting
            labels={"x":"GDP: Gross domestic product (million current US$)"}, #labels to be assigned to each axis
            color_discrete_sequence=['#ffcc99'] # colour to be assigned to the bars
        )
        #plotting a boxplot for outlier detection, outliers are not being removed as they have significance in GDP study
        fig1=px.box(y=temp,labels={"y":"GDP: Gross domestic product (million current US$)"})
        #returning the plotted graphs as "children" of the "plotval" id component (empty div)
        return [dcc.Graph(id="plot2",style={'width': '90vw', 'height': '90vh'},figure=fig),dcc.Graph(id="plot7",style={'width': '90vw', 'height': '90vh'},figure=fig1)]

    elif option=="bar": #i.e. if the tab with value "bar" is selected
        temp=df[df.columns[26]].values # storing data regarding Fertility rate
        temp3=df[df.columns[27]].values# storing data regarding Life expectancy
        temp4=df[df.columns[31]].values# storing data regarding Infant Mortality Rate
        female=[float(x.split("/")[0]) for x in temp3] #extracting female life expectancy
        male=[float(x.split("/")[1]) for x in temp3] #extracting male life expectancy
        temp2=df[df.columns[0]].values # for temporary deletion
        temp1=df[df.columns[0]].values # for temporary deletion
        temp=temp[temp>0] # removing rows with -ve Fertility rate as it is incorrect, data is removed from temp so original dataframe is not affected
        temp2=temp2[temp>0]# removing country rows with -ve Fertility rate as it is incorrect, data is removed from temp so original dataframe is not affected
        fig=  px.bar( # bar charts being plotted
            df,
            x=temp2,
            y=temp,
            color="Region",
            labels={"y":"Fertility rate, total (live births per woman)","x":"Country"},
            title="Fertility Rate"
        )
        fig1=px.bar(
            df,
            x=temp1,
            y=[female,male],
            labels={"value":"Life Expectancy","x":"Country","variable":"Gender"},
            barmode="group", #both the bar charts will be plotted on the same axis
            title="Life Expectancy"
        )
        fig2=px.bar(
            df,
            x=temp1,
            y=temp4,color="Region",
            labels={"y":"Infant Mortality Rate(per 1000 live births)","x":"Country"},
            title="Infant Mortality Rate"
        )
        newnames={"wide_variable_0":"female","wide_variable_1":"male"}
        fig1.for_each_trace(lambda t: t.update(name = newnames[t.name])) # changing the variable names in the legend
        #returning the plotted graphs as "children" of the "plotval" id component
        return [dcc.Graph(id="plot3",style={'width': '95vw', 'height': '90vh'},figure=fig),dcc.Graph(id="plot4",style={'width': '90vw', 'height': '90vh'},figure=fig1),dcc.Graph(id="plot5",style={'width': '90vw', 'height': '90vh'},figure=fig2)]
    elif option=="pie": #i.e. if the tab with value "bar" is selected
        x=html.Div([
        html.P("Country:",style={"padding":"1em"}),
        dcc.Dropdown( #dropdown to select the country for which the pie charts have to be displayed
            id='drop', 
            value='country', 
            options=[{'value': x, 'label': x}  for x in df.iloc[:,0]], #setting the options from the dataframe
        ),
        html.Div(id="piechart")]) #Empty div to show piechart
        return x #returning the div as value of "children" for the empty div so that country can be selected and piechart can be displayed
@app.callback( #callback for getting the country and displaying the appropriate pie charts
Output(component_id='piechart', component_property='children'), #output given to the empty div with id "piechart"
Input(component_id='drop',component_property='value') #input taken from the dropdown menu
)
def print_chart(x):# function called by callback to display the appropriate piechart
    if x!="country":# i.e. some country is being selected 
        ind=list(df.iloc[:,0]).index(x) # getting index values corresponding to each country
        df1=pd.DataFrame(columns=["Indicator","Value"])# creating dataframe for the Economy sectors of selected country
        for i in range(0,3):
            df1.loc[i]=[df.columns[9+i],df.iloc[ind,9+i]] #saving the economy sectors names and values
        df2=pd.DataFrame(columns=["Indicator","Value"])# creating dataframe for the Employment sectors of selected country
        for i in range(0,3):
            df2.loc[i]=[df.columns[12+i],df.iloc[ind,12+i]] #saving the employment sectors names and values
        fig = px.pie(df1,values="Value",names="Indicator",title="Economy Divisions",color="Value",color_discrete_map={df1["Indicator"][0]:'#ffff99',df1["Indicator"][1]:'#cc99ff',df1["Indicator"][2]:'#66ffcc'})
        fig.update_layout(legend_orientation="h")
        #plotting pie chart and changing legend position
        fig2 =px.pie(df2,values="Value",names="Indicator",title="Employment Divisions")
        fig2.update_layout(legend_orientation="h")
        #plotting pie chart and changing legend position
        #returning the plotted graphs as "children" of the empty div
        return [dcc.Graph(id="plot6",style={'width': '49vw', 'height': '50vh','display': 'inline-block'},figure=fig),dcc.Graph(id="plot6",style={'width': '49vw', 'height': '50vh','display': 'inline-block'},figure=fig2)]
    
        
        
        


app.run_server() #Specifications for Dash components are complete so the server is now deployed on local host
#port used is 8050