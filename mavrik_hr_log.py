import streamlit as st
import pandas as pd
import numpy as np
import pickle
from st_aggrid import AgGrid

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.markdown(""" ### How It Works 	:grey_question:""")
st.caption("""Unleash the power of automation with our cutting-edge employee hours worked tracking app.Effortlessly log and aggregate employee data, including 
weekly hours and overtime worked, in a streamlined and dynamic manner. Say goodbye to tedious manual data entry and hello to increased efficiency and organization. :grinning:""")

st.caption("""
1. Type in the first and last name of the employee
2. Type in the number of hours worked by the employee during the first week
3. Type in the number of hours worked by the employee during the second week
4. Click the "add to my database" button
5. Watch the database automatically tally up the overtime and regular hours worked

""")
db_name = st.text_input(":file_folder: Create a new database name (example: 1-15-2023 to 1-20-2023) ")
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

# Function to switch name format
# def switch_name_format(name):
#     last_name, first_name = name.split(', ')
#     return f"{first_name} {last_name}"

def create_aggrid(f):
    Agrid_output = AgGrid(f, editable=True, theme="streamlit", height=300)
    return Agrid_output


###### start of application --------------------------------------------------------------------------
with st.sidebar:
    st.sidebar.image("Maverick Concierge Blue Logo-01.jpg")
    st.title("Mavrick's time tracking app")
    
    list = pd.read_csv(r"Book1.csv")['Full name']
    # employee_names = list.apply(switch_name_format)
    employee_names = list
    options = st.multiselect(":female-office-worker: Employee Name ", employee_names)
    firstWeek = st.number_input(":calendar: Week one (1) hours worked", step=0.01, min_value=0.0, help="50")
    secondWeek = st.number_input(":calendar: Week two (2) hours worked", step=0.01, min_value=0.0, help="60")

    if st.button(":cd: Add to my database"):
        for name in options:
            employeeName = name
            employee_data.add_to_df(employeeName, firstWeek, secondWeek)
    
# st.dataframe(employee_data.df, width=1000)
edited_df = create_aggrid(employee_data.df)

@st.cache
def convert_df(df):
    df = df.sort_values(by="Name", ascending=True)
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(employee_data.df)

st.download_button(
    label=":point_down: Download Data to an Excel File",
    data=csv,
    file_name=db_name+'.csv',
    mime='text/csv',
)

col1, col2 = st.columns(2)

col1.metric(label="Total Regular hours", value=employee_data.df['Regular'].sum(), delta="hours")
col2.metric(label="Total Overtime hours", value=employee_data.df['Overtime'].sum(), delta="hours")
