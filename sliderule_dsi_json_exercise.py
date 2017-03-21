
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas.pydata.org/pandas-docs/stable/io.html#io-json-reader
# + data source: http://jsonstudio.com/resources/
# ****

# In[1]:

import pandas as pd


# ## imports for Python, Pandas

# In[2]:

import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas.pydata.org/pandas-docs/stable/io.html#normalization

# In[11]:

# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': [{'governor': 'Rick Scott'}],
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': [{'governor': 'John Kasich'}],
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[12]:

# use normalization to create tables from nested element
json_normalize(data, 'info')


# In[8]:

# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[9]:

# load json as string
json.load((open('data/world_bank_projects_less.json')))


# In[13]:

# load as Pandas dataframe
sample_json_df = pd.read_json('data/world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[1]:

import os
import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


# In[3]:

# load json as string
json.load((open('data\world_bank_projects.json')))


# In[4]:

# load as Pandas dataframe
json_df = pd.read_json('data\world_bank_projects.json')
json_df.head(5)


# In[5]:

#1.Find the 10 countries with most projects
json_df = pd.read_json('data\world_bank_projects.json')
json_df.countryname.value_counts().head(10)


# In[6]:

#2.Find the top 10 major project themes (using column 'mjtheme_namecode')
json_file=json.load((open('data\world_bank_projects.json')))
project_themes=json_normalize(json_file,'mjtheme_namecode','countryname')
#project_themes.head(10)
project_themes.name.value_counts(dropna=False).head(10)


# In[8]:

#3.In 2. above you will notice that some entries have only the code and the name is missing.
#Create a dataframe with the missing names filled in.

pt=project_themes
pt = pt.replace('', np.nan)
pt1= pt[['code', 'name']]
pt2=pt1.dropna().groupby('code').last()
pt.loc[pt['name'].isnull(),'name'] = pt['code'].map(pt2.name)
pt= pt.set_index('code')
pt.head(10)


# In[ ]:



