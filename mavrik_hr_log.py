import streamlit as st
import pandas as pd
import numpy as np
import pickle
st. set_page_config(layout="wide") 

st.title(""" How It Works 	:grey_question:""")
st.caption("""
To get started, simply:
- Create a new file name (example: week 2 payroll)
- Input the employee's first and last name in section 1
- Enter the number of hours worked by the employee during the first week
- Input the number of hours worked by the employee during the second week
- Click the "add to my database" button
- Experience the convenience of automatic overtime and regular hours calculation in your database.

""")
#Start a new pickle file to save information given by user
db_name = st.text_input(":file_folder: Create a new file name (example: week 2 payroll)", help="Do not use \ or / when naming a folder as it won't work")
st.write("✅ Your file is saved as:", db_name,".csv")
st.title("Data table")

class EmployeeData:
    def __init__(self):
        try:
            with open(db_name+'.pkl', 'rb') as f: #try opening a file name
                self.df = pickle.load(f) #load that file
        except FileNotFoundError: #if file is not on the machine
            self.df = pd.DataFrame(columns=['Name', 'Week 1', 'Week 2', 'Regular', 'Overtime']) #create a new dataframe with name, week1, week2, regular n ot columns
            
    def regular_overtime(self,hours): #function categorizes hours into regular and overtime hours
        """ computes the no. of regular hours vs the no. of hours spent over time"""
        reg = 0
        ot= 0

        if hours <= 40: #if employee worked less than or equal to 40 hours 
            reg = hours #then take the user's input as regular hours
            ot = 0 #no overtime in this case
        else:
            reg = 40 #if otherwise, which means that user worked more than 40 hours
            ot = hours - 40 #70-40, would be 20 hours of overtime
        return (reg, ot) #returns a tuple where first index is the regular time and second index is the overtime variable
    
    def add_to_df(self, name, week1, week2): #adding user input to the main table
        regular_hours = self.regular_overtime(week1)[0] + self.regular_overtime(week2)[0] #adding users input from week1 and week 2 user entries
        overtime_hours = self.regular_overtime(week1)[1] + self.regular_overtime(week2)[1] #adding overtime to week 1 and week 2 columns
        self.df = self.df.append({'Name': name, 'Week 1': float(week1), 'Week 2': float(week2), 'Regular': float(regular_hours), 'Overtime': float(overtime_hours)}, ignore_index=True) #append all this information to the df
        with open(db_name+'.pkl', 'wb') as f: #now open a new pickle file using the database name
            pickle.dump(self.df, f) #save that pickle file
        return self.df #return the dataframe

    def create_aggrid(f): #turn the dataframe into an aggrid dataframe to allow user to edit information in the table itself
        Agrid_output = AgGrid(f, editable=True, theme="streamlit", height=300)
        return Agrid_output #return the dataframe

    def employee_df(file_name = 'Book1.csv'):
        df = pd.read_csv(r'Book1.csv')['Full name'].to_frame() #retrives the names of all employees provided by matt
        return df #list of all employees working with mavrick
    
    def add_employee(self, first_name, last_name):
        """ adds a new employee to the main employee list"""
        dataf = EmployeeData.employee_df() #reads the employee information csv file
        dataf = dataf.append(pd.Series({"Full name": last_name + "," + " " + first_name}), ignore_index=True)
        return dataf

    def remove_employee(self, selection):
        df = EmployeeData.employee_df()
        df = df.apply(lambda x: x.str.strip())
        mask = ~df['Full name'].isin(selection)
        df = df[mask]
        df = df.to_csv("Book1.csv")

# ----------------------------------------------------------------------------------start of application --------------------------------------------------------------------------
employee_data = EmployeeData() #initialize the employee data class
employee_names = employee_data.employee_df() #list of employee names

#add new employee to the selection list
with st.sidebar:
    st.sidebar.image("logo_transparent.png")

        
    with st.form(key='my_form'):
        st.subheader("Section 1: Add employee hours")
        options = st.multiselect(":female-office-worker: Employee Name ", employee_names) #select names of employees from the list
        first_week_hours = st.number_input(":calendar: Week one (1) hours worked", step=0.01, min_value=0.0, help="50") #hours worked by employee in first week
        second_week_hours = st.number_input(":calendar: Week two (2) hours worked", step=0.01, min_value=0.0, help="60") #hours worked by employee in second week
        submit_button = st.form_submit_button(label=':➕Submit')
        if submit_button:
            for name in options:
                employeeName = name
                employee_data.add_to_df(employeeName, first_week_hours, second_week_hours)
    
    with st.form(key="employee_addition_form"):
        st.subheader("This section is for adding new employees to your list")
        fst_name = st.text_input("First name")
        lst_name = st.text_input("Last name")
        submit_button = st.form_submit_button(label=":➕ Add new employee")
    if submit_button:
        employee_data.add_employee( fst_name, lst_name).to_csv("Book1.csv")
        st.experimental_rerun()

    with st.form(key="removing employees"):
        st.subheader("This section is for removing employees")
        selection = st.multiselect("Select Employees to be removed ", employee_names)
        submit_button = st.form_submit_button(label=":➖ Remove selected employees")
        if submit_button:
            employee_data.remove_employee(selection)
            st.experimental_rerun()
    
st.dataframe(employee_data.df.style.format({'Week 1': '{:,.1f}', 'Week 2': '{:,.1f}', 'Regular': '{:,.1f}', 'Overtime':'{:,.1f}'}), width=1000)
@st.cache
def convert_df(df):
    df = df.sort_values(by="Name", ascending=True)
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(employee_data.df)

st.download_button(
    label=":arrow_down: Download Data to an Excel File",
    data=csv,
    file_name=db_name+'.csv',
    mime='text/csv',
)

col1, col2 = st.columns(2)

col1.metric(label="Total Regular hours", value=employee_data.df['Regular'].sum(), delta="hours")
col2.metric(label="Total Overtime hours", value=employee_data.df['Overtime'].sum(), delta="hours")

