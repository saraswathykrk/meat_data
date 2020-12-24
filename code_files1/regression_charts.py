#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import Different pandas lib
# 
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy  as np
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler


# In[2]:


#Create dataframe from source CarPrice_Assignment.csv file
carprice_raw_df2=pd.read_csv("regression.csv")
#Check the sample data once
carprice_raw_df2.head()


# In[3]:


c_list=carprice_raw_df2['Entity'].unique()
for x in c_list:
  print(x)

type(c_list)


# In[4]:


#carprice_raw_df.columns
#carprice_raw_df2['Entity'].unique()
#carprice_raw_df.drop(labels=None, axis=0,inplace=True)


# In[5]:


for i in c_list:
    print(i)
    #i="China"
    carprice_raw_df =carprice_raw_df2.loc[carprice_raw_df2['Entity'] == i]
    plt.figure(figsize=(20, 12))
    plt.subplot(2,3,1)
    sns.lineplot(x = 'Year', y = 'Total_Meat_Consumption', data = carprice_raw_df)
    sns.lineplot(x = 'Year', y = 'Total_CO2_emission', data = carprice_raw_df)
    plt.subplot(2,3,2)
    sns.lineplot(x = 'Year', y = 'Total_CO2_emission', data = carprice_raw_df)
    plt.plot(2,3,3)
    sns.lineplot(x = 'Year', y = 'Total_land_use', data = carprice_raw_df)
    plt.subplot(2,3,4)
    sns.lineplot(x = 'Year', y = 'Total_water_use', data = carprice_raw_df)
    plt.subplot(2,3,5)
    sns.lineplot(x = 'Year', y = 'Total_CO2_emission', data = carprice_raw_df)
    image_name=i+".png"
    plt.savefig(image_name)


# In[6]:


col_list=['Total_Meat_Consumption','Total_CO2_emission','Total_land_use','Total_water_use']


# In[10]:


for cl in col_list:
    plt.figure(figsize=(20, 12))
    counter=1
    for cn in c_list:
        print(cn)
        carprice_raw_df =carprice_raw_df2.loc[carprice_raw_df2['Entity'] == cn]
        plt.subplot(4,3,counter)
        sns.lineplot(x = 'Year', y = 'Total_Meat_Consumption', data = carprice_raw_df,label="Meat_Consumption")
        sns.lineplot(x = 'Year', y = 'Total_CO2_emission', data = carprice_raw_df,label="CO2_emission")
        sns.lineplot(x = 'Year', y = 'Total_land_use', data = carprice_raw_df,label="Land_use")
        sns.lineplot(x = 'Year', y = 'Total_water_use', data = carprice_raw_df,label="Water_use")
        plt.gca().set_title(cn)
        plt.tight_layout()
        counter=counter+1
    image_name=cl+".png"
    plt.savefig(image_name)
    counter=1


# In[ ]:




