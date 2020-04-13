#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


df_names = ['confirmed_global', 'deaths_global', 'recovered_global'] 
df_list = [pd.DataFrame() for df in df_names]
df_dict = dict(zip(df_names, df_list))


# In[3]:


url_part = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'

for key, value in df_dict.items():
    value = pd.read_csv(url_part+key+'.csv', parse_dates=[0])
    
    value.rename(columns={'Province/State': 'Province_State', 'Country/Region': 'Country_Region'}, inplace=True)
    
    dim_col = value.columns[0:4]
    date_col = value.columns[4:]
    
    value = value.melt(id_vars = dim_col, value_vars = date_col, var_name = 'Date', value_name = key)
    
    value['Date'] = pd.to_datetime(value['Date'])
    
    df_dict[key] = value


# In[4]:


join_on_col = ['Province_State','Country_Region','Lat','Long','Date']
df_COVID = df_dict['confirmed_global'].merge(df_dict['deaths_global'], on=join_on_col, how='outer').merge(df_dict['recovered_global'], on=join_on_col, how='outer')
df_COVID.rename(columns = {'confirmed_global':'Confirmed', 'deaths_global':'Deaths', 'recovered_global':'Recovered'}, inplace = True)


# In[5]:


# to fill the NaN in 'Province_State' columns with Countries name in 'Country_Region'
df_COVID['Province_State'] = np.where(df_COVID['Province_State'] == 'nan', df_COVID['Country_Region'], df_COVID['Province_State'])
# to fill the NaN in last three columns
df_COVID.iloc[0:,-3:] = df_COVID.iloc[0:,-3:].fillna(0)


# In[6]:


df_COVID


# In[7]:


import pygsheets
client = pygsheets.authorize(service_file='credentials.json')
print("-----------------Authorized--------------------")


# In[8]:


sheet = client.open('Covid-19-Visualization')
print("-----------------Sheet Opened------------------")


# In[9]:


wks = sheet[0]
print("-----------------First Sheet Accessed----------")


# In[12]:


wks.set_dataframe(df_COVID,(1,1))
print("-----------------Data Updated------------------")


# In[ ]:




