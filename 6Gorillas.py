#Tenzinger Development Assessment

#Goal: Calculate the monthly traveling reimbursement for each employee
#      Return a csv with the employee information, the travelling reimbursement
#      And the paydate (first monday of the month)

#steps:
#How many days are there each month
#When is the first monday of the month
#Calculate the reimbursement
#Add reimbursement and date to existing dataframe
#export as csv
#make streamlit app so that HR doesn't need to know python

import streamlit as st
import pandas as pd
import numpy as np
from math import ceil


def important_days():
    #get amount of weekdays in each month (first two if statements)
    #also get first monday of the month (last if statement)
    counter = 0
    business_days = []
    pay_days = []

    year = pd.date_range(start = '2022-01-01', end = '2023-01-31', freq = 'D')

    for day_of_year in year:
        #weekdays = 1-5, saturday, sunday = 6,7
        if day_of_year.isoweekday() < 6:
            counter += 1

        if day_of_year.is_month_end:
            #print(f'business days in {i.month_name()}:', counter)
            business_days.append(counter)
            counter = 0

        if day_of_year.is_month_start:
            first_day = day_of_year.isoweekday()
            first_monday = 7 - first_day
            #plus one because the first day of the month needs to be added
            pay_days.append(day_of_year + pd.DateOffset(first_monday + 1))

    return business_days, pay_days

def reimbursement(employees, business_days):
    compensation = {'Bike' : 0.5,
                    'Bus'  : 0.25,
                    'Train': 0.25,
                    'Car'  : 0.10}

    travel_compensation = []
    for i in range(len(employees)):
        if employees['Transport'].iloc[i] == 'Bike' and (5 <= employees['Distance'].iloc[i] <= 10):
            current_compensation = 1
        else:
            current_compensation = compensation[employees['Transport'].iloc[i]]
        #money = cents per transport *     kilometers *         (workdays a week / 5 * business days a month)     * two-way trip
        money = current_compensation * employees['Distance'].iloc[i] * (ceil(employees['Workdays'].iloc[i]) / 5 * business_days)  * 2
        travel_compensation.append(money)

    return travel_compensation

def convert_df(df):
    return df.to_csv(index=None).encode('utf-8')

def main():
    #Get a list of business days and paydates a month
    business_days, pay_days = important_days()

    employees = pd.DataFrame({'Employee':  ['Paul', 'Martin', 'Jeroen', 'Tineke', 'Arnout', 'Matthijs', 'Rens'],
                              'Transport': ['Car', 'Bus', 'Bike', 'Bike', 'Train', 'Bike', 'Car'],
                              'Distance':  [60, 8, 9, 4, 23, 11, 12],
                              'Workdays':  [5, 4, 5, 3, 5, 4.5, 5] #assuming Matthijs works two half days means he'd still make 5 trips back and forth each week
                             })

    #simple streamlit app to make things pretty and easy for non-coders
    st.title('Tenzinger Development Assessment')
    st.write('An application to calculate how much travel compensation each employee should be getting depending on the vehicle they use, the distance they travel and the amount of days they work a week.')

    #sidebar with options for the month so that HR doesn't need to code
    with st.sidebar:
        months =  ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        current_month = st.radio('month', months)

    #converts month into index
    month_index = months.index(current_month)

    #calculates how much everyone should be getting
    travel_compensation = reimbursement(employees, business_days[month_index])

    #adds new rows to dataframe
    employees['Compensation'] = travel_compensation
    employees['Pay Date'] = pay_days[month_index + 1].date() # +1 because paydate is one month later

    #prints dataframe, but pretty with rounded numbers
    st.write(employees.style.format({'Workdays':'{:.1f}', 'Compensation':'{:.2f}'}))

    #convert and add download button for monthly csv's
    new_csv = convert_df(employees)
    st.download_button('Download csv', new_csv, current_month + '_travelpay.csv')


if __name__ == "__main__":
    main()
