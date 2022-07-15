import streamlit as st
import streamlit_authenticator as stauth
import yaml
import requests
import json
import io
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
def getFastAPIResponse(url,data):
    
    token_str = 'bearer ' + st.session_state["token"]
    headers = {'accept': 'application/json','authorization': str(token_str)}
    response = requests.get(url=url,params=data,headers=headers)

    return response






############################################# API Functions Calling #############################################
def function1():
    st.markdown("# Check 🎈")
    st.sidebar.markdown("# Function 1 🎈")
    #randNum = st.sidebar.number_input("Pick a number for random images [1,9]",1,9,step=1)
    isClick = st.sidebar.button("OK")
    
        
    uploaded_files = st.file_uploader(label="Image File Upload",type=['png', 'jpg', 'jpeg', 'svg'], accept_multiple_files = True, key="image")
    
    
    for i in range(0,len(uploaded_files)):
        filename = uploaded_files[i].name
        filetype = uploaded_files[i].type
        filesize = uploaded_files[i].size
        filedata = uploaded_files[i].read()
        
        
        st.write(filename)
        st.write(filetype)
        st.write(filesize)
        st.write(type(filedata))
        
        
        
        
        #header = {"Content-Type" : "multipart/form-data"}
        file = {
            "filename" : filename,
            'file': filedata,
            "Content-Type" : "application/octet-stream",
            "Content-Disposition": "form-data"
        }
        url = 'http://127.0.0.1:8000/qualityinspection/'

        # encode_data = encode_multipart_formdata(data)
        # data = encode_data[0]
        headers = {
            "Accept": "image/jpeg"
        }
        response = requests.post(url=url, headers = headers, files=file)
        
        st.write(response)
    
    
    # url = 'http://127.0.0.1:8000/qualityinspection/'
    # files = {'attach': ('p5.png', open('../p5.png', 'rb'))}

        #url = 'http://127.0.0.1:8000/api/get/random/'
        #data = {'num' : randNum}
        #response = getFastAPIResponse(url,data)
    
        #st.write(response.content[0])
        if(response.content[0]  == 123): # json style
            st.write(1)
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
                st.json(res_j)
                # with st.expander("Image file list",expanded=True):
                #     st.json(res_j)
                # with st.expander("Full images file info",expanded=False):
                #     for i in range(randNum):
                #         filename = str(res_j.get(str(i+1)))
                #         print(filename)
                #         data1 = {"filename":filename}
                #         url1 = 'http://127.0.0.1:8000/api/get/fileNameAndClass'
                #         response1 = getFastAPIResponse(url1,data1).json()
                #         st.json(response1)
                    #Todo display images
            
        elif(response.content[0] == 255): # image style
            st.write(2)
        #     st.success("You did it! :heart:")
        #     img_data = Image.open(io.BytesIO(response.content))
        #     st.image(img_data)
            
        # else:
        #     st.error("Seomthing went wrong! Please contact us for help!")

    

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
    "Function 1": function1,
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