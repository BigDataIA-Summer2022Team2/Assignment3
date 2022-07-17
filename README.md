# DAMG 7245 Big-Data-Systems-Intelligence-Analytics-Labs-Summer-2022

> Assignment 3 - Transfer Learning
> 
> Team 2
> 
> Cheng Wang NUID: 001280107
> 
> Meihu Qin NUID: 002190486


## 1. Intro

- We build a Transfer-Learning project in Assignment 3
- [Dataset](https://www.kaggle.com/datasets/ravirajsinh45/real-life-industrial-dataset-of-casting-product)
- Model: `Insepection_v3`

## 2. Setup

- It is different from previous two assignments, we don't need to use `AWS S3 credentials`, we train our model on our machine and deploy it online
- There are ***three things*** needs to be done before you test our assignment!
  ```python
  cd Assignment3/
  pip install requirements.txt
  ```
- Then you need to config your localhost db config and put it into the path we set up.
- Also you need to config your streamlit config

## 3. What is in this repo?
1. api functions
   ```markdown
   Path: Assignment3/src/api_functions/
   ```
   
2. FastAPI: **main.py**
  - default port: `127.0.0.1:8000`
   ```markdown
   Path: /src/
   <!--start FastAPI unicorn server -->
   uvicorn main:app --reload  
   ```

3. Streamlit: **Home.py**
  - default port: `127.0.0.1:8501`
  
  ```markdown
   Path: /src/strreamlit/Home.py
   <!--start Streamlit server -->
   streamlit run Home.py 
   ```
  
  - If you didn't create your own `streamlit config yaml file`, you will not login into our streamlit app successfully!
  - Due to technicial issue, we set our username and password are the same for ask token from FastAPI in our Home.page, you can change it if you want.

4. log
   ```markdown
   Path: /src/log/
   ```
   
   - no log file inside because I used `.gitignore` to ignore it but it will auto-generate when you run FastAPI.


5. requirements.txt: All Python modules we need in this assignment
  - We highly recommend to use virtual evvironment
  - `python -m venv .venv`
  - Create a `.gitignore` file and add `.venv/*` into it
  - open script file which is inside the .`venv` folder and run following command
  - then you will get a nice and clean programming environment
    ```markdown
    Path: /assignment_1/
    
    pip install requirements.txt 
    ```

## 4. API Functions

> Use `uvicorn main:app --reload` to start FastAPI uvicorn server
> 
> go to : `http://127.0.0.1/8000/`, this is home page
> 
> click `docs` button and you will jump to API documentation

### JWT Auth
- We create auth which needs user to login
- You can create your own user and hashed password in your local database
- Then our function will auto-read these info and check whether you are correct user or not
- If you didn't login and test out API function(s), you will get response **401 : Not authenticated**

### API Qualityinspection

- We create simple api function to test our trained model
- People who use our api could input one image file and get response back which includes ***probability*** and ***status***


## 5. Attestation 
- ***WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK***
- ***Contribution: Cheng Wang: 50% Meihu Qin: 50%***
