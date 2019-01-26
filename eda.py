import os 
import pandas as pd 
import plotly as py
import seaborn as sns 
import matplotlib.pyplot as plt

# set dir
os.chdir("C://Users//mandy//Desktop//DataForGood")

data = pd.read_csv("multipleChoiceResponses.csv", low_memory = False)
colnames = data.iloc[0,:]
data = data.iloc[1:,:]

""" Exploratory stuff """ 



# Talk to them about plotly and how they can use the tool 

# <------- Plot countries on a chlorepath chart ------> 
country_freq = data["Q3"].value_counts().reset_index()
country_freq.columns = ["country", "num respondants"]

# obtain country codes 
# Note: not all countries are in codes (just map US to it?)
codes = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
country_freq = pd.merge(country_freq, codes, how = "inner", left_on = ['country'], right_on = ['COUNTRY'])

# Plot respondants by country  
key = None
py.tools.set_credentials_file(username='happilyeverafter95',api_key=key)

country_plot = [ dict(
        type = 'choropleth',
        locations = country_freq['CODE'],
        z = country_freq["num respondants"],
        text = country_freq['COUNTRY'],
        colorscale = "Jet",
        autocolorscale = False,
        reversescale = True,
        marker = dict(
            line = dict (
                color = 'rgb(180,180,180)',
                width = 0.5
            ) ),
        colorbar = dict(
            autotick = False,
            title = 'Number of Responders'),
      ) ]

layout = dict(
    title = 'Responders by country',
    geo = dict(
        showframe = False,
        showcoastlines = False,
        projection = dict(
            type = 'Mercator'
        )
    )
)

# See plot at https://plot.ly/~happilyeverafter95/0
fig = dict( data=country_plot, layout=layout )
py.plotly.iplot(fig, validate=False, filename='d3-world-map')

# <----------- Visualization of education level versus job -------------> 

# Education: Q4, Job Q6
# Note do the job normalization at the begining

education = data[["Q4", "Q6"]].dropna(how = "any")
education = education[(education["Q6"] != "Student") & (education["Q4"] != "I prefer not to answer")]
education["Q6"] = education["Q6"].apply(lambda x: x if x in ["Data Scientist", "Software Engineer", "Data Analyst", "Data Engineer"] else "Other")

education = education.groupby(["Q6", "Q4"]).size().reset_index()
education.columns = ["Q6", "Q4", "Num"]
ax = sns.barplot(x="Q6", y="Num", hue = "Q4",data=education)

# <-------------- Visualization of salary by job --------------> 

# Salary: Q9 

salary = data[["Q6", "Q9"]].dropna(how = "any")
salary = salary[(salary["Q6"] != "Student") & (salary["Q9"] != "I do not wish to disclose my approximate yearly compensation")]
salary["Q6"] = salary["Q6"].apply(lambda x: x if x in ["Data Scientist", "Software Engineer", "Data Analyst", "Data Engineer"] else "Other")

# Map salary to upper limit
def map_salary(amt):
    amt = amt.split("-")
    if len(amt) == 2:
        amt = amt[1]
    else: 
        amt = amt[0]
    amt = [c for c in amt if c.isdigit()]
    amt = "".join(amt)
    return int(amt)

salary["Q9"] = salary["Q9"].apply(map_salary)

ax = sns.boxplot(x="Q6", y = "Q9",data=salary)

# create new visualization removing outliers
# Removing true outlier observation
salary = salary[salary["Q9"] <= 250000]
ax = sns.boxplot(x="Q6", y = "Q9",data=salary)

# Other visualizations to explore: 
# how do kagglers learn? 
# gender/age divide in data science 