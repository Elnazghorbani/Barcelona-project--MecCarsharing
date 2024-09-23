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
r_compl_start = r_completed.groupby("Inicio real de la reserva")["Número de reserva corto"].count()
r_compl_start_day = r_compl_start.groupby(pd.Grouper(freq="M")).sum()

#counting the number of reservation per estimated start date - time series
#r_compl_start_e = r_completed.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
#r_compl_start_day_e = r_compl_start_e.groupby(pd.Grouper(freq="M")).sum()

#plot time series for reservation completed
r_compl_start_day.plot(label='Completed')
plt.title('No. of reservations by actual start date',fontsize=16)
plt.ylabel('No. of reservations')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
#plt.savefig('reservations_completed_by_startdate.pdf')
plt.show()


'''
Extracting unique values for reservations completed 
'''

#getting the unique values for each column in bookings dataset for reservations completed
r_compl_info =[]
for column in r_completed:
     value = r_completed[column].unique()
     r_compl_info.append(value)

# A dictionary with the column name and the unique values per column for bookings dataset for reservations completed
keys_list = list(r_completed.columns)
values_list = r_compl_info
zip_iterator = zip(keys_list, values_list)
a_dictionary = dict(zip_iterator)
#print(a_dictionary)

#Unique values to a dataframe for bookings dataset for reservations completed
Unique_values=pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in a_dictionary.items() ]))
# saving Unique values in a excel file for bookings dataset
Unique_values.to_excel('unique_values_bookings_completed.xlsx')


'''
Time series plot for types of reservations by estimated start date
'''
# bookings canceled
r_compl_start_e = r_completed.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
r_compl_starte_day = r_compl_start_e.groupby(pd.Grouper(freq="M")).sum()

# bookings canceled
r_canceled = bookings.loc[bookings['Estado de la reserva'] == 'CANCELED']
#counting the number of reservations per actual start date - time series
r_canc_start = r_canceled.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
r_canc_start_day = r_canc_start.groupby(pd.Grouper(freq="M")).sum()
# bookings in progress
r_progress = bookings.loc[bookings['Estado de la reserva'] == 'IN_PROGRESS']
#counting the number of reservations per actual start date - time series
r_prog_start = r_progress.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
r_prog_start_day = r_prog_start.groupby(pd.Grouper(freq="M")).sum()
# bookings scheduled
r_scheduled = bookings.loc[bookings['Estado de la reserva'] == 'SCHEDULED']
#counting the number of reservations per actual start date - time series
r_sched_start = r_scheduled.groupby("Inicio estimado de la reserva")["Número de reserva corto"].count()
r_sched_start_day = r_sched_start.groupby(pd.Grouper(freq="M")).sum()

#plot time series for each type of reservation
r_compl_starte_day.plot(label='Completed')
r_canc_start_day.plot(label='Canceled')
r_prog_start_day.plot(label='In Progress')
r_sched_start_day.plot(label='Scheduled')
plt.title('No. of reservations by status and estimated start date',fontsize=16)
plt.ylabel('No. of reservations')
plt.xlabel('Date')
plt.legend()
plt.tight_layout()
#plt.savefig('reservations_by_status_&_estimated_start_date.pdf')
plt.show()

'''
Analysis of the location of completed bookings
'''
# counting number of reservations completed by start point (it is not possible to see all names)
r_compl_by_startpoint = r_completed.groupby("Sitio de inicio")["Número de reserva corto"].count()
r_compl_by_startpoint.describe() #to generate statistics
r_compl_by_startpoint=r_compl_by_startpoint.sort_values()
r_compl_by_startpoint.plot.barh()
plt.title('No. of reservations by start point', fontsize=16)
plt.ylabel('Star point')
plt.xlabel('No. of reservations')
plt.yticks(fontsize=5, rotation=45)
plt.tight_layout()
plt.legend()
#plt.savefig('reservations completed by start point.pdf')
plt.show()

#TOP 20 starting points

top_20_startpoint = r_compl_by_startpoint.sort_values(ascending=0)[:20]
top_20_startpoint.plot.barh()
plt.title('Top 20 starting points', fontsize=16)
plt.ylabel('Starting point')
plt.xlabel('No. of reservations')
plt.yticks(fontsize=5, rotation=45)
plt.tight_layout()
#plt.savefig('Top 20 starting points.pdf')
plt.show()

#TOP 20 end points

r_compl_by_endpoint = r_completed.groupby("Sitio final")["Número de reserva corto"].count()
r_compl_by_endpoint.describe() #to generate statistics
top_20_endpoint = r_compl_by_endpoint.sort_values(ascending=0)[:20]
top_20_endpoint.plot.barh()
plt.title('Top 20 end points', fontsize=16)
plt.ylabel('End point')
plt.xlabel('No. of reservations')
plt.yticks(fontsize=5, rotation=45)
plt.tight_layout()
plt.savefig('Top 20 end points.pdf')
plt.show()
