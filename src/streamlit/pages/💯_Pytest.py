import streamlit as st
import streamlit_authenticator as stauth
import streamlit.components.v1 as cp
import pickle
import os
import yaml

#st.session_state

with open('./streamlit_config.yaml') as file:
        config = yaml.safe_load(file)
        
authenticator = stauth.Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days']
)

with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
    
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    abs_path = os.path.dirname((os.path.abspath(__file__)))
    pytest_report = abs_path + "/pytest_report.html"
    
    with open(pytest_report, "rt") as f:
        f_data = f.read()
        cp.html(f_data,height=3000,width=1000)


