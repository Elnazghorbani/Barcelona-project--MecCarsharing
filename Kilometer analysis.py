# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 12:24:59 2022

@author: Elnaz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Dataset
users = pd.read_excel('C://export miembros 20220316v2.xlsx')
bookings = pd.read_excel('C://RESERVES MEC UOC.xlsx')

bookings.info()
users.info()

# reviewing the information from the dataframe we considered these 3 columns are not relevant
bookings= bookings.drop(['Número de reserva','Número de factura','Estado civil'],axis=1)

'''
Extracting unique values for both data sets
'''

#getting the unique values for each column in bookings dataset
r_compl_info_book =[]
for column in bookings:
     value = bookings[column].unique()
     r_compl_info_book.append(value)

# A dictionary with the column name and the unique values per column for bookings dataset
keys_list_book = list(bookings.columns)
#values_list = r_compl_info_book
zip_iterator = zip(keys_list_book, r_compl_info_book)
a_dic_book = dict(zip_iterator)
#print(a_dictionary)

#Unique values to a dataframe for bookings dataset
Unique_values_book=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in a_dic_book.items() ]))
# saving Unique values in a excel file for bookings dataset
Unique_values_book.to_excel('unique_values_bookings.xlsx')

#getting the unique values for each column in users dataset
r_compl_info_user =[]
for column in users:
     value = users[column].unique()
     r_compl_info_user.append(value)

# A dictionary with the column name and the unique values per column for users dataset
keys_list_user = list(users.columns)
values_list_user = r_compl_info_user
zip_iterator_user = zip(keys_list_user, values_list_user)
user_dict = dict(zip_iterator_user)
#print(a_dictionary)

#Unique values to a dataframe for users dataset
Unique_values_user=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in user_dict.items() ]))
# saving Unique values in a excel file for users dataset
Unique_values_user.to_excel('unique_values_users.xlsx')

'''
Analyzing only reservations completed 
'''



#Selecting only reservations completed
r_completed = bookings.loc[bookings['Estado de la reserva'] == 'COMPLETED']
#r_completed.drop(['Número de factura','Estado civil'],axis=1 ,inplace=True)

#counting the number of reservations per actual start date - time series
r_compl_start = r_completed.groupby("Inicio real de la reserva")["Kilometraje del viaje"].sum()
r_compl_start_day = r_compl_start.groupby(pd.Grouper(freq="M")).sum()

#counting the number of reservation per estimated start date - time series
#r_compl_start_e = r_completed.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
#r_compl_start_day_e = r_compl_start_e.groupby(pd.Grouper(freq="M")).sum()

#plot time series for reservation completed
r_compl_start_day.plot(label='Completed')
plt.title('No. of reservations by actual start date',fontsize=16)
plt.ylabel('kilometer')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
#plt.savefig('reservations_completed_by_startdate.pdf')
plt.show()

