import streamlit as st
import streamlit_authenticator as stauth
import yaml

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
  guide_info="""
  # API Guide
  > ***Tips***
  > - If you start FastAPI on your own machine, default documentation url will be: `http://127.0.0.1:8000/docs`
  > - Also if you are using Linux/Unix system machine, you can use **Curl** to test our APIs.
  > - Software like **Postman** is also a good choice to test our APIs

  ## API 1: getRandomImages
  ### 1.1 Input Value
  ||Custom Number|
  |:-:|:-:|
  |Value Type|int|
  |Description|number of images user want to get(0<number<10)|
  |isOption|False|
  |Sample value|3|


  ### 1.2 Sample Request URL
  ```
  http://127.0.0.1:8000/api/get/random/?num=3
  ```


  ```
  curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/random/?num=3' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZWlodSIsImV4cCI6MTY1Njc3MTczMX0.s7RrxoRTOPEQitV_FUWc7PYW3eFZNy0vZzbFjtDIELs'
  ```

  ### 1.3 Sample Response
  > All return response will be in **Json** format
  > outside number key is the index number in the csv file, not the index of images
  
  ```json
  {
  "1": "0af3a80affb05a409c3348a3f3c4986e",
  "2": "0b80bcfce852e6cb449f3c4923dde0a2",
  "3": "0b8b0ab7f2446360d6ae632a2bdef033"
}
  ```

  ---
  ## API 2: fileNameandClassFilterRequest

  ### 2.1 Input Value
  ||class|filename|
  |:-:|:-:|:-:|
  |Value Type|str|str|
  |Description|aircraft class|image file name with max 32 length|
  |isOption|True|False|True|
  |Default value|User input required|""|
  |Sample value|V22|07baa6df06ca535cfa03b55ec741554d|

  ### 2.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/api/get/fileNameAndClass/?className=v22&filename=07baa6df06ca535cfa03b55ec741554d
  ```

  ```markdown
  curl -X 'GET' \
    'http://127.0.0.1:8000/api/get/fileNameAndClass/?className=v22&filename=07baa6df06ca535cfa03b55ec741554d' \
    -H 'accept: application/json'
  ```
  ### 2.3 Sample Response
  ```json
  {
    "18": {
      "filename": "07baa6df06ca535cfa03b55ec741554d",
      "width": "2048",
      "height": "1536",
      "class": "V22",
      "xmin": "337",
      "ymin": "166",
      "xmax": "1265",
      "ymax": "1340"
    }
  }
  ```

  ---
  ## API 3: imgSizeRangeFilterRequest
  ### 3.1 Input Value
  ||width|height|
  |:-:|:-:|:-:|
  |Value Type|int|int|
  |Description|image width range 0 ~ num|image height range 0 ~ num|
  |isOption|False|False|
  |Default value|User input required|User input required|
  |Sample value|700|700|
  

  ### 3.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/api/get/imgSizeRange/?width=550&height=500
  ```

  ```markdown
  curl -X 'GET' \
    'http://127.0.0.1:8000/api/get/imgSizeRange/?width=550&height=500' \
    -H 'accept: application/json'
  ```
  ### 3.3 Sample Response
  ```json
  {
    "69": {
      "filename": "0dc3f3e32533d1909ec496e32a3f916c",
      "width": "512",
      "height": "303",
      "class": "SR71",
      "xmin": "178",
      "ymin": "121",
      "xmax": "331",
      "ymax": "209"
    },
    "186": {
      "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
      "width": "512",
      "height": "341",
      "class": "Su57",
      "xmin": "28",
      "ymin": "162",
      "xmax": "236",
      "ymax": "282"
    },
    "187": {
      "filename": "2cf1ec46ef1a6534a784b25ce1d07978",
      "width": "512",
      "height": "341",
      "class": "Su57",
      "xmin": "115",
      "ymin": "43",
      "xmax": "483",
      "ymax": "172"
    }
  }
  ```
  ---
  ## API 4: aircraftPositionRangeFilterRequest
  ### 4.1 Input Value
  ||xmin|ymin|xmax|ymax|
  |:-:|:-:|:-:|:-:|:-:|
  |Value Type|int|int|int|int|
  |Description|aircraft position - xmin coordinate|aircraft position - ymin coordinate|aircraft position - xmax coordinate|aircraft position - ymax coordinate|
  |isOption|True|True|True|True|
  |Default value|0|0|0|0|
  |Sample value|300|300|500|500|

  ### 4.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/api/get/aircraftPositionRange/?xmin=300&ymin=300&xmax=500&ymax=500
  ```

  ```markdown
  curl -X 'GET' \
    'http://127.0.0.1:8000/api/get/aircraftPositionRange/?xmin=300&ymin=300&xmax=500&ymax=500' \
    -H 'accept: application/json'
  ```

  ### 4.3 Sample Response
  ```json
  {
    "129": {
      "filename": "1deecbebb637c7cfcb1ed6ef993243c1",
      "width": "1500",
      "height": "969",
      "class": "JAS39",
      "xmin": "327",
      "ymin": "308",
      "xmax": "420",
      "ymax": "374"
    }
  }
  ```
  ---
  ## API 5: aircraftNumandClass
  ### 5.1 Input Value
  ||class|Num|
  |:-:|:-:|:-:|
  |Value Type|str|int|
  |Description|aircraft class|how many aircrafts user wants to see in this image|
  |isOption|True|False|
  |Default value|User input required|""|
  |Sample value|F16|3|
  
  
  ### 5.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/api/get/aircraftNumandClass/?num=3&className=F16
  ```

  ```markdown
  curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/aircraftNumandClass/?num=3&className=F16'\
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZWlodSIsImV4cCI6MTY1Njc3MTczMX0.s7RrxoRTOPEQitV_FUWc7PYW3eFZNy0vZzbFjtDIELs'
  ```
  ### 5.3 Sample Response
  ```json

  {
  "97": {
    "filename": "2cc2da26e5c852e86339633fdffccbba",
    "class": "F16",
    "count": 3
  }
}
  
  ```
  ---
  ## API 6: displayImage
  ### 6.1 Input Value
  ||filename|
  |:-:|:-:|
  |Value Type|str|
  |Description|image filename|
  |isOption|False|
  |Default value|User input required|
  |Sample value|2cc2da26e5c852e86339633fdffccbba|

  ### 6.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/display/image/?imgName=2cc2da26e5c852e86339633fdffccbba
  ```

  ```markdown
  curl -X 'GET' \
  'http://127.0.0.1:8000/display/image/?imgName=2cc2da26e5c852e86339633fdffccbba' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZWlodSIsImV4cCI6MTY1Njc3MTczMX0.s7RrxoRTOPEQitV_FUWc7PYW3eFZNy0vZzbFjtDIELs'
  ```
  ### 6.3 Sample Response
  - return image

  ---
  ## API 7: displayboundingbox
  ### 7.1 Input Value
  ||filename|
  |:-:|:-:|
  |Value Type|str|
  |Description|image filename|
  |isOption|False|
  |Default value|User input required|
  |Sample value|2cc2da26e5c852e86339633fdffccbba|

  ### 7.2 Sample Request URL
  ```markdown
  http://127.0.0.1:8000/api/get/getboundingbox/?filename=2cc2da26e5c852e86339633fdffccbba
  ```

  ```markdown
  curl -X 'GET' \
  'http://127.0.0.1:8000/api/get/getboundingbox/?filename=2cc2da26e5c852e86339633fdffccbba' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJtZWlodSIsImV4cCI6MTY1Njc3MTczMX0.s7RrxoRTOPEQitV_FUWc7PYW3eFZNy0vZzbFjtDIELs'

  ```

  ### 7.3 Sample Response
  - return image

  """

  st.markdown(guide_info)


