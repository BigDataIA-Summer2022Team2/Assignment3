import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
import pandas as pd
import numpy as np
import time
import base64
from PIL import Image
import os
import requests
import pymysql

#st.session_state # check golbal variables status


if 'token' not in st.session_state:
    st.session_state.token = ''
###############################################################
def homepage():
    #st.sidebar.markdown("# Military Aircraft Detection Dataset version 7 🎈")    
    st.header("Military Aircraft Detection version 7 🎈")
    st.image(showHomePageImgCover())
    markdown_info = """
    ## About Dataset
    - [Kaggle Dataset Link](https://www.kaggle.com/datasets/a2015003713/militaryaircraftdetectiondataset/)
    > - bounding box in PASCAL VOC format (xmin, ymin, xmax, ymax)
    > - 40 aircraft types
    > (A10, A400M, AG600, AV8B, B1, B2, B52 Be200, C130, C17, C5, E2, EF2000, F117, F14, F15, F16, F18, F22, F35, F4, J20, JAS39, MQ9, Mig31, Mirage2000, RQ4, Rafale, SR71(may contain A12), Su34, Su57, Tornado, Tu160, Tu95(may contain Tu142), U2, US2, V22, Vulcan, XB70, YF23)

    ## Team 2
    - [Github Repo](https://github.com/BigDataIA-Summer2022Team2/Assignment2)
    - Cheng Wang
        - NUID: 001280107
        - email: wang.cheng3@northeastern.edu
    - Meihu Qin
        - NUID: 002190486
        - email: qin.mei@northeastern.edu
    """

    st.markdown(markdown_info)
    
# display home page img cover
def showHomePageImgCover():
    file_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
    img_path = file_path + "/0041e69431bf872309d1aff628b6494f.jpg"

    open_img = Image.open(img_path)
    img_data = np.asarray(open_img)
    return img_data


########################################################################

with open('./streamlit_config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


name, authentication_status, username = authenticator.login('Login','main')


if st.session_state["authentication_status"]:
    #st.sidebar.header(f'Welcome *{st.session_state["name"]}*')
    #st.balloons() # Issue: when refresh page, balloons() function will be called again
    homepage()
    
    
elif st.session_state["authentication_status"] == False:
    st.error('Username or Password is incorrect')
    st.session_state.token = ''
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
    st.session_state.token = ''
    
with st.sidebar:
    if(st.session_state.authentication_status == True):
        
        headers = {'accept': 'application/json','Content-Type': 'application/x-www-form-urlencoded',}
        url = 'http://127.0.0.1:8000/token'
        
        data = {'grant_type':'','username': str(username),"password": str(username),'scope':'','client_id':'','client_secret':''}
            
        #res = requests.post(url=url,params=data,headers=headers)
        
        if(st.session_state.token == ''):
            res = requests.post(url=url,data=data,headers=headers)
            token = res.json()["access_token"]
            st.session_state["token"] = token
        st.info('User: ***%s***' % st.session_state.username)

        authenticator.logout('Logout')
    



    

# if authentication_status:
#     authenticator.logout('Logout', 'main')
#     st.write(f'Welcome *{name}*')
#     st.title('Some content')
# elif authentication_status == False:
#     st.error('Username or Password is incorrect')
# elif authentication_status == None:
#     st.warning('Please enter your username and password')




# if authentication_status:
#     try:
#         if authenticator.reset_password(username, 'Reset password'):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)

# try:
#     if authenticator.register_user('Register user', preauthorization=False):
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)

# try:
#     username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
#     if username_forgot_pw:
#         st.success('New password sent securely')
#         # Random password to be transferred to user securely
#     elif username_forgot_pw == False:
#         st.error('Username not found')
# except Exception as e:
#     st.error(e)

# try:
#     username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
#     if username_forgot_username:
#         st.success('Username sent securely')
#         # Username to be transferred to user securely
#     elif username_forgot_username == False:
#         st.error('Email not found')
# except Exception as e:
#     st.error(e)

# if authentication_status:
#     try:
#         if authenticator.update_user_details(username, 'Update user details'):
#             st.success('Entries updated successfully')
#     except Exception as e:
#         st.error(e)

# with open('../config.yaml', 'w') as file:
#     yaml.dump(config, file, default_flow_style=False)
