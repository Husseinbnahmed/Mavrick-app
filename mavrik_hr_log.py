import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.markdown(""" ### How It Works 	:grey_question:""")
st.caption("""Unleash the power of automation with our cutting-edge employee hours worked tracking app.Effortlessly log and aggregate employee data, including 
weekly hours and overtime worked, in a streamlined and dynamic manner. Say goodbye to tedious manual data entry and hello to increased efficiency and organization. :grinning:""")

st.caption("""
1. Enter the employee's first and last name.
2. Input the hours worked by the employee during the first week.
3. Input the hours worked by the employee during the second week.
4. Click the "add to database" button
5. Observe the database automatically calculate the total overtime and regular hours worked.

""")
db_name = st.text_input(":file_folder: Create a new database name (example: week 20 ) ")
class EmployeeData:
    def __init__(self):
        try:
            with open(db_name+'.pkl', 'rb') as f:
                self.df = pickle.load(f)
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['Name', 'Week 1', 'Week 2', 'Regular', 'Overtime'])
            
    def regular_overtime(self,hours):
        """ computes the no. of regular hours vs the no. of hours spent over time"""
        reg = 0
        ot= 0

        if hours <= 40:
            reg = hours
            ot = 0 
        else:
            reg = 40
            ot = hours - 40
        return (reg, ot)
    
    def add_to_df(self, name, week1, week2):
        regular_hours = self.regular_overtime(week1)[0] + self.regular_overtime(week2)[0]
        overtime_hours = self.regular_overtime(week1)[1] + self.regular_overtime(week2)[1]
        self.df = self.df.append({'Name': name, 'Week 1': int(week1), 'Week 2': int(week2), 'Regular': int(regular_hours), 'Overtime': float(overtime_hours)}, ignore_index=True)
        with open(db_name+'.pkl', 'wb') as f:
            pickle.dump(self.df, f)
        return self.df
    
employee_data = EmployeeData()






###### start of application --------------------------------------------------------------------------
with st.sidebar:
    st.sidebar.image("Maverick Concierge Blue Logo-01.jpg")
    st.title("TimeMaverick")
    

    employee_names = ['Diana Farghaly', 'Hussein Mohamed', 'Matt Morcos', 'Mark Morocs']
    options = st.multiselect(":female-office-worker: Employee Name ", employee_names)
    firstWeek = st.number_input(":calendar: Week one (1) hours worked", step=0.01, min_value=0.0, help="50")
    secondWeek = st.number_input(":calendar: Week two (2) hours worked", step=0.01, min_value=0.0, help="60")

    if st.button(":cd: Add to my database"):
        for name in options:
            employeeName = name
            employee_data.add_to_df(employeeName, firstWeek, secondWeek)
    
st.dataframe(employee_data.df, width=1000)


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(employee_data.df)

st.download_button(
    label=":point_down: Download Data to an Excel File",
    data=csv,
    file_name=db_name+'.csv',
    mime='text/csv',
)
