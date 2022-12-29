import plotly.graph_objects as go
import pandas as pd
from IPython.display import display
import plotly.express as px

df = pd.read_csv('job_data.csv') #Read the data from a csv file

companies = list(df.company.unique()) #Collect all the unique companies from in the data

for x in companies: #Remove junk data
    if type(x) == float:
        companies.remove(x)

companyJobs = df['company'].value_counts() #Collect how many job postings each company has

companies.sort()
companyJobs = companyJobs.sort_index()

companyFreq = pd.DataFrame({ #Turn data into dataframe
    'Companies': companies,
    'companyJobs': companyJobs
})

companyFreq = companyFreq.sort_values(by=['companyJobs'], ascending=False) #Sort the data by companies with the most job postings
companyFreq = px.bar(companyFreq.head(15), x='Companies', y='companyJobs') #Create the bar graph using the top 15 companies by job postings


names = []
nums = []

#Fill two lists with the program language names and how often they appear in job postings
for (columnName, columnData) in df.items():
    names.append(columnName)
    if 1 in df[columnName].values:
        nums.append(df[columnName].value_counts()[1])
    else:
        nums.append(0)

#Trim unused columns from result
del names[:3]
del nums[:3]

#Creat a graph of two columns, the programming language and how many jobs it's listed in
pie = pd.DataFrame({
    'name': names,
    'num': nums
})

pieChart = go.Figure(data=[go.Pie(labels=pie.name, values=pie.num)]) #Create pie chart

Jobs = df.groupby(['location']).size() #Count the amount of jobs in each location
states = df.location.unique()
states = list(states)

for x in states: #Remove junk data
    if type(x) == float:
        states.remove(x)
states.sort()

#Turn the data into a dataframe for graph
stateMap = pd.DataFrame({
    'State': states,
    'Jobs': Jobs
})

#constructing the choropleth graph
stateMap = px.choropleth(stateMap, locations='State', locationmode="USA-states", color='Jobs', scope="usa", color_continuous_scale=
    [[0, 'rgb(203,244,253,255)'],
    [1, 'rgb(55, 102, 222)']]
    )

#Labeling the legend for the choropleth graph
stateMap.update_layout(
    coloraxis_colorbar=dict(
        title="Job Postings"
    )
)

#Display created graphs
companyFreq.show()
pieChart.show()
stateMap.show()