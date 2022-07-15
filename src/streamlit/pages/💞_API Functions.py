import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
import json
import io
import pandas as pd
import numpy as np
from io import BytesIO
import time
import os
from PIL import Image
from urllib3 import encode_multipart_formdata
st.set_page_config(page_title="API Functions",page_icon=":heart:")

#st.session_state # check global variables status


############################### SET st.session_state function on_change variables ###############################



############################### SET st.session_state function on_change variables ###############################





# get response from FastAPI
def getFastAPIResponse(url,filename,filedata):
    
    token_str = 'bearer ' + st.session_state["token"]
    headers = {'Accept': '*/*','authorization': str(token_str)}
    file = {
                "filename" : filename,
                'file': filedata,
                "Content-Type" : "application/octet-stream",
                "Content-Disposition": "form-data"
            }
    
    response = requests.post(url=url, headers = headers, files=file)

    return response






############################################# API Functions Calling #############################################
def function1():
    st.markdown("# Casting Product Image Data for Quality Inspection 🎈")
    #randNum = st.sidebar.number_input("Pick a number for random images [1,9]",1,9,step=1)    
        
    uploaded_files = st.sidebar.file_uploader(label="Image File Upload",type=['png', 'jpg', 'jpeg', 'svg'], accept_multiple_files = True, key="image")
    isClick = st.sidebar.button("OK")
    if isClick:
        for i in range(len(uploaded_files)-1,-1,-1):
            res_dict={}
            filename = uploaded_files[i].name
            filetype = uploaded_files[i].type
            filesize = uploaded_files[i].size
            filedata = uploaded_files[i].read()
        
            
            url = 'http://127.0.0.1:8000/qualityinspection/'
            response = getFastAPIResponse(url,filename,filedata)
            
            if(response.content[0] == 123): # json style

                res_j = response.json()
                if "detail" in res_j.keys():
                    if res_j["detail"] == "Could not validate credentials":
                        st.warning("You should login again!")
                        st.session_state.authentication_status = None
                        time.sleep(2)
                        st.experimental_rerun()
                    elif res_j["detail"] == "Item not found":
                        st.error("There is no target image file! Please try again or click hint to try our sample!")
                    else:
                        st.error("New error which is not handled. Please contact us ASAP!")
                else:
                    st.success("You did it! :heart:")
                    res_dict[filename] = {}
                    res_dict[filename]["filetype"] = filetype
                    res_dict[filename]["status"] = res_j["status"]
                    res_dict[filename]["probability"] = res_j["probability"]
                    
                    st.image(filedata,width=256)
                    st.table(res_dict)
                    
                    
                    
                
            elif(response.content[0] == 255): # image style
                st.error("Return response is in image format! Something went wrong! Please contact us for help!")
                
            else:
                st.error("Seomthing went wrong! Please contact us for help!")

    

############################################# API Functions Calling #############################################




with open('./streamlit_config.yaml') as file:
        config = yaml.safe_load(file)
        
authenticator = stauth.Authenticate(
config['credentials'],
config['cookie']['name'],
config['cookie']['key'],
config['cookie']['expiry_days']
)

func_num = {
    "Quality inspection": function1,
}



with st.sidebar:
    if(st.session_state.authentication_status == True):
        st.info("User: ***%s***" % st.session_state.username)
        authenticator.logout('Logout')
    
if(st.session_state.authentication_status == None or st.session_state.authentication_status == False):
    st.header("Please go to ***Home Page and login***!")
    st.session_state.token = ''

if(st.session_state.authentication_status == True):
    selected_func = st.sidebar.selectbox("Select a function!", func_num.keys(),disabled=False)
    func_num[selected_func]()