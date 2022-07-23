import streamlit as st
import numpy as np
import yaml
import streamlit_authenticator as stauth


def degTags():
    tab1, tab2, tab3, tab4, tab5= st.tabs(["DAG detail", "Runtime Duration", "Calendar", "DAG Runs", "Log details"])


    with tab1:
        st.subheader("DAG detail")
        st.image("./pages/pic1.png")
        
        
    with tab2:
        st.subheader("Runtime Duration")
        st.image("./pages/pic2.png")

    with tab3:
        st.subheader("Calendar")
        st.image("./pages/pic3.png")

    with tab4:
        st.subheader("DAG Runs")
        st.image("./pages/pic5.png")

    with tab5:
        st.subheader("Log details")
        st.image("./pages/pic4.png")

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
    degTags()