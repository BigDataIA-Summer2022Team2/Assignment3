# DAMG 7245 Big-Data-Systems-Intelligence-Analytics-Labs-Summer-2022

> Team 2
> 
> Cheng Wang NUID: 001280107
> 
> Meihu Qin NUID: 002190486

<!-- Todo: Change this README file for Assignemnt 2 -->

## 1. Intro

- Assignment 1 is a very easy way to understand what a real-life python project looks like
- create

## 2. Setup

- If S3 credential is filaed, you can create your own AWS S3 bucket and store all required info into `/assignment_1/credentials/` json file
- Under Assignment 1 folder, you will see a `requirements.txt` file, it contains all Python packages that we installed on our machine.  Use fllowing commands in your terminal to install all required packages
  ```python
  cd /assignment_1/
  pip install requirements.txt
  ```

## 3. What is in ths repo?

1. pandas profling
   ```markdown
   Path: /assignment_1/notebooks/pandas_profiling
   ```
2. great expectations
   ```markdown
   Path: /assignment_1/great_expectations
   ```
3. pillow
   ```markdown
   Path: /assignment_1/src/metadata.py
   ```
4. model card
   ```markdown
   Path: /assignment_1/notebooks/model_card/
   ```
5. AWS S3 bucket connector
   ```markdown
   Path: /assignment_1/notebooks/AWS_S3/
   ```
6. api functions
   ```markdown
   Path: /assignment_1/api_functions/
   ```
7. main.py
   ```markdown
   Path: /assignment_1/src/
   <!--start FastAPI unicorn server -->
   uvicorn main:app --reload 
   ```
8. index.html/result.html
   ```markdown
   Path: /assignment_1/src/
   ```
9. log
   ```markdown
   Path: /assignment_1/logs/
   ```
   - no log file inside because I used `.gitignore` to ignore it but you can generate one if you want
10. pytest
    ```markdown
    Path: /assignment_1/
    ```

- pytest confguration py file
- pytest data test py file

11. requirements.txt
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

- We create some simple api functions to test
- People who use our api could input some values and get some correct result to see

1. infoFilter
   - image filname
   - image width
   - image height
   - image aircraft class name
   - aircraft position in this image
     - xmin
     - ymin
     - xmax
     - ymax
   - retuen all correct json responses
2. aircraftClassAndFilenameRequest
   - image aircraft class name
   - image filname
   - retuen all correct json responses
3. imgSzieRangeRequest
   - image width
   - image height
   - retuen all correct json responses
4. aircraftPositionRequest
   - aircraft position in this image
   - xmin
   - ymin
   - xmax
   - ymax

- retuen all satisfied responses

5. getAllImgInfo
   - no input value
   - retuen all images info
6. numAndClassFiteredInfoRequest
   - get selected number aircrafts in one image
   - just equal to input number
   - ignore lager number of aircrafts
   - option: aircraft class name
     - e.g. 4,"F16"
     - 1 image contains 4 F16 aircrafts
7. getNumRandomImage
   - input num and return num images

8. getPandasCsvOutputHtmlPage
   - no input
   - it is a html page to show our pandas profiling image info output

9. getPandasImageOutputHtmlPage
   - no input
   - a html page to show our pandas profling csv info output

10. displayImageInHTML
    - no input
    - a html page to show 5 random images

11. getModelCardHtmlOutput
    - no input
    - a html page to show model card html output

## 5. Html output display

- `http://127.0.0.1/8000/pandas/html/csv` csv info pandas profiling html
- `http://127.0.0.1/8000/pandas/html/image` Image info pandas profiling html
- `http://127.0.0.1/8000/modelcard/html/` model card nfo pandas profiling html
- `http://127.0.0.1/8000/display/image` random display 5 images on web page

## 6. Attestation 
- WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
- Contribution: Cheng Wang: 50% Meihu Qin: 50%
