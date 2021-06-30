#import libraries
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px 
import matplotlib.pyplot as plt
#Introduction (main section)
st.image('Depression.jpg')
st.write("""
# The Effect of COVID-19 on Anxiety & Depression in the USA
## Intro

Rates of anxiety and depression among adults were increasing before the outbreak of COVID. Causes of depression are often listed as some combination of family history, early childhood trauma, medical conditions, isolation, poor habits, substance dependency, financial worry, and/or stress. Therefore, Covid-19 has unfortunately accelerated the rates of anxiety and depression on a national front.
The motivation behind creating this tool is to be able to identify across the US the people that need this the most by assessing the rates nationwide.
By using CDC’s data from April 23- December 21, 2020 we are going to explore the impact of Covid-19 on mental well being at a state, regional & demographic level.).

""")

st.sidebar.image('Anxietypic.png')

file = 'Anxiety.csv'
df = pd.read_csv(file)


drop_cols = ['Phase','Time Period Start Date', 'Time Period End Date', 'Low CI', 'High CI', 'Confidence Interval', 'Quartile Range']
df = df.drop(columns=drop_cols)

df = df[df.Indicator == 'Symptoms of Anxiety Disorder or Depressive Disorder'] 

#Rename columns for easier access/ identification
df = df.rename(columns={'Time Period': 'Interval', 'Time Period Label': 'IntervalRange', 'Value': 'Rate'})

#Convert Interval column to type integer
df['Interval'] = pd.to_numeric(df['Interval'])

#Filter Interval feature for April thru December 2020
df = df[df.Interval <= 21]

#Drop repeat observations from Interval
df = df.dropna()

#Filter for Group = State, National Estimate
desired_groups = ['National Estimate', 'By State']
df1 = df[df.Group.isin(desired_groups)]

#Prepare df3 for 2nd plot (State data)
drop_cols1 = ['Indicator', 'Group', 'Subgroup', 'Interval']
df1 = df1.drop(columns=drop_cols1)

#Rename United States --> National Average
df1['State'] = df1['State'].replace(['United States'],'National Average')

#State name tuple
state_names = ("Alaska", "Alabama", "Arkansas", "Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming")

#Region name tuple
region_names = ("Midwest", "Northeast", "Southeast", "Southwest", "West")

#Region selector sidebar
region = st.sidebar.radio("Select the region  to view the average rate of anxiety :",region_names)
st.sidebar.write('You selected:', region)

#Select states based on region
if region == 'Northeast':
    state_list = ["Connecticut", "Delaware", "Maine", "Maryland", "Massachusetts", "New Hampshire", "New Jersey", "New York", "Pennsylvania", "Rhode Island", "Vermont"]
elif region == 'Southeast':
    state_list = ["Alabama", "Arkansas", "Florida", "Georgia", "Kentucky", "Louisiana", "Mississippi", "North Carolina", "South Carolina", "Tennessee", "Virginia", "West Virginia"]
elif region == 'Southwest':
    state_list = ["Arizona", "New Mexico", "Oklahoma", "Texas"]
elif region == 'West':
    state_list = ["Alaska", "California", "Colorado", "Hawaii", "Idaho", "Montana", "Nevada", "Oregon", "Utah", "Washington", "Wyoming"]
else:
    state_list = ["Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota", "Missouri", "Nebraska", "North Dakota", "Ohio", "South Dakota", "Wisconsin"]

#Subset based on all states in region
df_region = df1[df1.State.isin(state_list)]

#Create dataframe of average rates per state
avg_df = pd.DataFrame()
avg_df['State'] = state_list
seq = []

#Subset df_region based on each state in avg_df, sum the Rates, divide by 21 (the # of entries per State), and round to 2 places
for x in avg_df['State']:
    x_df = df_region[df_region['State'] == x]
    seq.append(round(sum(x_df['Rate']/21),2))

avg_df['Avg Rate'] = seq

#Bar chart of average rates per state in region
st.write("## Average Rate of Anxiety and Depressive Disorder in the ", region)
fig1 = px.bar(avg_df, x='State', y="Avg Rate")
st.plotly_chart(fig1)

#Single state selector sidebar - not useful?
state = st.sidebar.text_input("Type in the State you want to plot on the graph")
if state in state_names:
    st.sidebar.write('You entered:', state)
    comp_list = [state, 'National Average']
    df_state = df1[df1.State.isin(comp_list)]
    
    st.write("## Rate of Anxiety and Depressive Disorder for ", state)
    fig2 = px.line(df_state, x='IntervalRange', y='Rate', color='State')
    st.plotly_chart(fig2)

else:
    st.sidebar.write('Improper entry, please try again (ie. New York).')

#Prepare df2 (Group data)
drop_cols2 = ['Indicator', 'State']
df2 = df.drop(columns=drop_cols2)

#Simplify group labels (ie. 'By Race ...' = 'Race')
df2['Group'] = df2['Group'].replace(['By Race/Hispanic ethnicity'],'Race')
df2['Group'] = df2['Group'].replace(['By Age'],'Age')
df2['Group'] = df2['Group'].replace(['By Education'],'Education')
df2['Group'] = df2['Group'].replace(['By Sex'],'Sex')

#Simplify Race subgroup labels (ie. 'Non-Hispanic white ...' --> 'White')
df2['Subgroup'] = df2['Subgroup'].replace(['Hispanic or Latino'],'Hispanic')
df2['Subgroup'] = df2['Subgroup'].replace(['Non-Hispanic white, single race'],'White')
df2['Subgroup'] = df2['Subgroup'].replace(['Non-Hispanic black, single race'],'Black')
df2['Subgroup'] = df2['Subgroup'].replace(['Non-Hispanic Asian, single race'],'Asian')
df2['Subgroup'] = df2['Subgroup'].replace(['Non-Hispanic, other races and multiple races'],'Other/Mixed')

#Simplify Education subgroup labels
df2['Subgroup'] = df2['Subgroup'].replace(['Less than a high school diploma'],'Less than High School')
df2['Subgroup'] = df2['Subgroup'].replace(['High school diploma or GED'],'High School')
df2['Subgroup'] = df2['Subgroup'].replace(["Some college/Associate's degree"],'Some College')
df2['Subgroup'] = df2['Subgroup'].replace(["Bachelor's degree or higher"],"Bachelor's or Higher")

#Read in user specified group (for 1st plot)
group = st.sidebar.radio("Click on the Demographic data you want to plot on the graph",('Age', 'Education', 'Race', 'Sex'))
st.sidebar.write('You selected:', group) #default: By Age
df_group = df2[df2.Group == group]

st.write("## Rate of Anxiety and Depressive Disorder by ", group)
fig3 = px.line(df_group, x='IntervalRange', y='Rate', color='Subgroup')
st.plotly_chart(fig3)
fig = px.choropleth(df, locations="State",
                    color="Rate", # lifeExp is a column of gapminder
                    hover_name="Rate", # column to add to hover information
                    color_continuous_scale=px.colors.sequential.Plasma)
st.plotly_chart(fig)
