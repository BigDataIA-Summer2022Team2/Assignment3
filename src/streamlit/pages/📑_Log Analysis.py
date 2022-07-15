import streamlit as st
import streamlit_authenticator as stauth
import yaml
import datetime
import numpy as np
import pandas as pd
import pymysql
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import altair as alt
import seaborn as sns
import os

#st.session_state


with open('./streamlit_config.yaml') as file:
        config = yaml.safe_load(file)
        
authenticator = stauth.Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days']
)

#abs_path
#con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
#Todo
abs_path = os.path.dirname((os.path.abspath(__file__)))
print(abs_path)
yaml_path = abs_path + "/mysql.yaml"
print(os.path.exists(yaml_path))

with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)
#print(config)
db_host = config['credentials']['host']
db_user = config['credentials']['user']
db_password = config['credentials']['password']
db_database = config['credentials']['database']

con = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database, charset="utf8")
c = con.cursor()

with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
        
        options = st.multiselect(
            'What log info you want to get?',
            ['logId','requestUrl','userId', 'response', 'logTime', 'code_', 'username','level_','processTime'],
            ['logId','username','requestUrl','code_','level_','response'],key="log_output_selection")

        num_logs = st.number_input(label="Choose number of logs you want to see", min_value=0, max_value=40, step=5)
        isNumLogsButtonClick = st.button("OK")
        
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    st.markdown("# Log Analysis")
    #st.markdown("## Try it :smile:")
    if(isNumLogsButtonClick == True):
        if(num_logs != 0):
            sql = "SELECT "
            # sql_lmit = "LIMIT 10"
            for item in options:
                if(item == options[-1]):
                    sql = sql + "lt." + str(item)
                else:
                    if(item == "username"):
                        sql = sql + "ut."+str(item) + ", "
                    else:
                        sql = sql + "lt." + str(item) + ", "
                
            sql = sql + " FROM log_table lt INNER JOIN user_table ut ON lt.userId = ut.userId WHERE ut.username = '" + st.session_state.username + "' AND lt.requestURL LIKE '%qualityinspection%' LIMIT " + str(num_logs)
            #st.write(sql)
            c.execute(sql)
            result = c.fetchall()
            #st.write(result)
            df = pd.DataFrame(result, columns = options)
            st.table(df)
        else:
            list_keys = [],
            list_values = []
            df = pd.DataFrame(list_values,columns=list_keys)
            st.warning("You should give a number which is greater than 0!")
            st.table(df)
        
        
        # if("logTime" in options):
        #     log_start = st.sidebar.date_input("Log Sart from",datetime.date(2022, 6, 29),key="log_start",on_change=modify_start_date_to_default)
        #     log_end = st.sidebar.date_input("Log End",datetime.date(2022, 6, 29),key="log_end",on_change=modify_end_date_to_default)
            
            # Todo: start time -> end time log query (if have time)
            # time_start = st.time_input('Set an alarm for', datetime.time(0, 0),key="time_start")
            # time_end = st.time_input('Set an alarm for', datetime.time(0, 0),key="time_end")
    
            # st.write('Start time', time_start)
            # st.write('End time', time_end)
            
            # st.write('Log start from:', log_start)
            # st.write('Log start from:', log_end)
        
    
    if(st.session_state["username"] != "cheng" and st.session_state["username"] != "meihu" and st.session_state["username"] != "root" and st.session_state["username"] != "admin"):
        
    
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.requestUrl LIKE '%qualityinspection%'")
        count_current_user_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.requestUrl LIKE '%qualityinspection%' AND lt.response LIKE '%Ok%'")
        
        count_success_user_log = c.fetchall()[0][0]
        #st.write(count_success_user_log)
        #Creating the dataset
        keys = ["Ok","Defect","all"]
        #keys.append(st.session_state.username)
        values = [count_success_user_log,count_current_user_log-count_success_user_log,count_current_user_log]
        #values.append(count_current_user_log)

        fig = plt.figure(figsize = (6, 3))

        plt.bar(keys, values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of API functions calling")
        plt.title(st.session_state.username + "'s API Functions Call Bar Chart")
        st.pyplot(fig)
        
        ###########################################
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Ok', 'Defect'
        sizes = [count_success_user_log, count_current_user_log-count_success_user_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(st.session_state.username + "'s API functions Call Pie Chart")
        st.pyplot(fig1)
        
        ####################################################
        
        
    else:
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.requestUrl LIKE '%qualityinspection%'")
        count_current_user_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE ut.username ='" + st.session_state.username + "' AND lt.requestUrl LIKE '%qualityinspection%' AND lt.response LIKE '%Ok%'")
        
        count_success_user_log = c.fetchall()[0][0]
        #st.write(count_success_user_log)
        #Creating the dataset
        keys = ["Ok","Defect","all"]
        #keys.append(st.session_state.username)
        values = [count_success_user_log,count_current_user_log-count_success_user_log,count_current_user_log]
        #values.append(count_current_user_log)

        fig = plt.figure(figsize = (6, 3))

        plt.bar(keys, values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of API functions calling")
        plt.title(st.session_state.username + "'s Image Detection API Calls Bar Chart")
        st.pyplot(fig)
        
        ###########################################
        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = 'Ok', 'Defect'
        sizes = [count_success_user_log, count_current_user_log-count_success_user_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title(st.session_state.username + "'s Image Detection API Calls Pie Chart")
        st.pyplot(fig1)
        
        
        
        ########################################
        
        
        c.execute("SELECT ut.username, COUNT(*) FROM log_table lt INNER JOIN user_table ut ON lt.userId = ut.userId WHERE lt.requestURL LIKE '%qualityinspection%' GROUP BY ut.userId")   
        admin_result = c.fetchall()
        admin_keys = []
        admin_values = []
        for item in admin_result:
            admin_values.append(item[1])
            admin_keys.append(item[0])

        fig4 = plt.figure(figsize = (6, 3))

        plt.bar(admin_keys, admin_values)
        #plt.xlabel("Users")
        #plt.xlabel(st.session_state.username)
        plt.ylabel("Number of images Dectection")
        plt.title("Image Dectection API Function Call Bar Chart")
        st.pyplot(fig4)
        

        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE lt.requestUrl LIKE '%qualityinspection%'")
        count_current_log = c.fetchall()[0][0]
        
        c.execute("SELECT COUNT(*) FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId" + " WHERE lt.requestUrl LIKE '%qualityinspection%' AND lt.response LIKE '%Ok%'")
        count_success_log = c.fetchall()[0][0]
        labels = 'pass', 'fail'
        sizes = [count_success_log, count_current_log-count_success_log]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig5, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title("All Users Dectection Pass/Fail Pie Chart")
        st.pyplot(fig5)
        
        
        
        
        
        c.execute("SELECT count(lt.requestUrl),ut.username FROM log_table lt INNER JOIN user_table ut on lt.userId = ut.userId WHERE requestUrl LIKE '%qualityinspection%' GROUP BY ut.username")

        
        result = c.fetchall() 
        #st.write((result)) # ((18, 'cheng'), (2, 'meihu'), (2, 'admin'))
        api_call_num_list = []
        user_list = []
        
        for item in result:
            api_call_num_list.append(item[0])
            user_list.append(item[1])
        
        
        df3 = pd.DataFrame({
            'User': user_list,
            'api calls': api_call_num_list
        })

        df3 = df3.rename(columns={'User':'index'}).set_index('index')

        # #st.line_chart(df3)

        label1s = user_list
        size1s = api_call_num_list
        _length = len(user_list)
        explode1 = [0] *  len(user_list)

        fig6, ax2 = plt.subplots()
        ax2.pie(size1s, explode=explode1, labels=label1s, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax2.set_title("User's Image detect Data Analysis")
        st.pyplot(fig6)

        st.bar_chart(df3)
