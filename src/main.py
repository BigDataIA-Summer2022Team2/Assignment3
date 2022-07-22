from fastapi import FastAPI, Query, Path, Request,HTTPException, Depends
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from numpy import equal
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import sys
import logging.config
from requests import request
from starlette.concurrency import iterate_in_threadpool
import os
import yaml
from fastapi.responses import Response
from datetime import datetime, timedelta
from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn
import streamlit_authenticator as stauth
from sys import argv
import boto3
import time
################################################################


from datetime import datetime
from pydantic import BaseModel
import pymysql
path = str(Path(Path(__file__).parent.absolute()))
sys.path.insert(0, path)

# import functions
from api_functions import returnHomePage, test_model




app = FastAPI()

global username
username = ""

############################# Auth - JWT #################################

if os.path.exists("key.txt"):
    os.remove("key.txt")
    os.system("openssl rand -hex 32 >> key.txt")
    f = open("key.txt", "r")
    key = f.read()
    
    f.close()
else:
    os.system("openssl rand -hex 32 >> key.txt")
    f = open("key.txt", "r")
    key = f.read()
    f.close()


######################################################## create `fastapi.yaml` and `trained_model.h5` ########################################################
"""
@date 7/21/2022
@author Cheng Wang
@Description: Create fastapi account and download trained model from AWS S3 using AWS S3 credentials
"""

result={}
s3_credentials = {}
try:
    if os.path.exists("fastapi.yaml") and os.path.exists("trained_model.h5"):
        print("\n\033[0;35;40m `fastapi.yaml` and  `trained_model.h5` file exists!\033[0m\n\n\n")
        time.sleep(1)
    
    elif os.path.exists("fastapi.yaml") and not os.path.exists("trained_model.h5"):
        # 5 params
        if len(argv) == 6:
            s3_credentials["service_name"] = argv[1]
            s3_credentials["region_name"] = argv[2]
            s3_credentials["aws_access_key_id"] = argv[3]
            s3_credentials["aws_secret_access_key"] = argv[4]
            s3_credentials["aws_s3_bucket_name"] = argv[5]

            s3_resource = boto3.client(
                service_name=s3_credentials['service_name'],
                region_name=s3_credentials['region_name'],
                aws_access_key_id=s3_credentials['aws_access_key_id'],
                aws_secret_access_key=s3_credentials['aws_secret_access_key'])

            bucket = s3_credentials['aws_s3_bucket_name']

            key = 'model/trained_model.h5'

            s3_resource.download_file(bucket,key,Filename="trained_model.h5")
            if os.path.exists("trained_model.h5"):
                print("\n\033[0;32;40mSuccessfully create `trained_model.h5` file!\033[0m\n")
                # raise ValueError("\033[0;33;40mYou need input AWS S3 credentials: service_name, region_name, aws_access_key_id, aws_secret_access_key, aws_s3_bucket_name!\033[0m")
            
            
            print("service name:\t\t\t\033[1;36;40m",s3_credentials["service_name"],"\033[0m")
            print("region name:\t\t\t\033[1;36;40m",s3_credentials["region_name"],"\033[0m")
            print("aws access key id:\t\t\033[1;36;40m",s3_credentials["aws_access_key_id"],"\033[0m")
            print("aws secret access key:\t\t\033[1;36;40m",s3_credentials["aws_secret_access_key"],"\033[0m")
            print("aws s3 bucket name:\t\t\033[1;36;40m",s3_credentials["aws_s3_bucket_name"],"\033[0m\n")
        
        else:
            raise IOError("\033[0;33;40mWe have a strict check here in order to confirm you have correct AWS S3 credentials!\nFormat:\n1. service_name\n2. region_name\n3. aws_access_key_id\n4. aws_secret_access_key\n5. aws_s3_bucket_name\033[0m")
            
        
    elif os.path.exists("trained_model.h5") and not os.path.exists("fastapi.yaml"):
        # at least 2 params
        # at most 4 params
        # status = false 

        if(len(argv) < 3):
            print("\n\033[0;31;40mError: No fastapi.yaml file!\033[0m")
            raise IOError("\033[0;33;40mAt least you need input your username and password!\033[0m")
        
        username = argv[1]
        result[username] = {}
        result[username]['username'] = argv[1]
        list_passwd = []
        list_passwd.append(argv[2])
        list_hashed_res = stauth.Hasher(list_passwd).generate()
        result[username]['hashed_password'] = list_hashed_res[0]

        if len(argv) == 3:
            result[username]['full_name'] = argv[1]
            result[username]['email'] = ""

        elif(len(argv) == 4):
            result[username]['full_name'] = argv[3]
            result[username]['email'] = ""
           
        elif(len(argv) == 5):
            result[username]['full_name'] = argv[3]
            result[username]['email'] = argv[4]
        elif(len(argv > 5)):
            print("\033[0;33;40mWe only accept at most 4 params here!\nFormat:\n1. username\n2. password\n3. full_name\n4. email\n\033[0m")
            
        result[username]['disabled'] = False
        with open('fastapi.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(data=result, stream=file, allow_unicode=True)
                
        if os.path.exists("fastapi.yaml"):
            print("\n\033[0;32;40mSuccessfully create `fastapi.yaml` file!\033[0m\n")
        else:
            raise FileExistsError("\n\033[0;31;40mCreate fastapi.yaml file failed!\033[0m\n")
        
        print("username:\t\t\t\033[1;36;40m", result[username]['username'],"\033[0m")
        print("plain password:\t\t\t\033[1;36;40m", argv[2],"\033[0m")
        print("hashed password:\t\t\033[1;36;40m", result[username]['hashed_password'],"\033[0m")
        print("full name:\t\t\t\033[1;36;40m", result[username]['full_name'],"\033[0m")
        print("email:\t\t\t\t\033[1;36;40m", result[username]['email'],"\033[0m")
        print('account disabled:\t\t\033[1;36;40m', result[username]['disabled'],"\033[0m") 
        
    elif not os.path.exists("trained_model.h5") and not os.path.exists("fastapi.yaml"):
        if(len(argv) != 10):
            raise IOError("\n\033[0;33;40mPlease input info correctly! \n Format:\n1. username\n2. password\n3. full name\n4. email\n5. service_name\n6. region_name\n7. aws_access_key_id\n8. aws_secret_access_key\n9. aws_s3_bucket_name\033[0m\n")
        else:
            
            username = argv[1]
            result[username] = {}
            result[username]['username'] = argv[1]
            list_passwd = []
            list_passwd.append(argv[2])
            list_hashed_res = stauth.Hasher(list_passwd).generate()
            result[username]['hashed_password'] = list_hashed_res[0]
            result[username]['full_name'] = argv[3]
            result[username]['email'] = argv[4]
            result[username]['disabled'] = False
            
            
            with open('fastapi.yaml', 'w', encoding='utf-8') as file:
                yaml.dump(data=result, stream=file, allow_unicode=True)
                
            if os.path.exists("fastapi.yaml"):
                print("\n\033[0;32;40mSuccessfully create `fastapi.yaml` file!\033[0m\n")
            else:
                raise FileExistsError("\n\033[0;31;40mCreate fastapi.yaml file failed!\033[0m\n")
            
            print("username:\t\t\t\033[1;36;40m", result[username]['username'],"\033[0m")
            print("plain password:\t\t\t\033[1;36;40m", argv[2],"\033[0m")
            print("hashed password:\t\t\033[1;36;40m", result[username]['hashed_password'],"\033[0m")
            print("full name:\t\t\t\033[1;36;40m", result[username]['full_name'],"\033[0m")
            print("email:\t\t\t\t\033[1;36;40m", result[username]['email'],"\033[0m")
            print('account disabled:\t\t\033[1;36;40m', result[username]['disabled'],"\033[0m")
    
            
            s3_credentials["service_name"] = argv[5]
            s3_credentials["region_name"] = argv[6]
            s3_credentials["aws_access_key_id"] = argv[7]
            s3_credentials["aws_secret_access_key"] = argv[8]
            s3_credentials["aws_s3_bucket_name"] = argv[9]

            print("===========================================================================")        
            print("service name:\t\t\t\033[1;36;40m",s3_credentials["service_name"],"\033[0m")
            print("region name:\t\t\t\033[1;36;40m",s3_credentials["region_name"],"\033[0m")
            print("aws access key id:\t\t\033[1;36;40m",s3_credentials["aws_access_key_id"],"\033[0m")
            print("aws secret access key:\t\t\033[1;36;40m",s3_credentials["aws_secret_access_key"],"\033[0m")
            print("aws s3 bucket name:\t\t\033[1;36;40m",s3_credentials["aws_s3_bucket_name"],"\033[0m\n")

            s3_resource = boto3.client(
                service_name=s3_credentials['service_name'],
                region_name=s3_credentials['region_name'],
                aws_access_key_id=s3_credentials['aws_access_key_id'],
                aws_secret_access_key=s3_credentials['aws_secret_access_key'])

            bucket = s3_credentials['aws_s3_bucket_name']

            key = 'model/trained_model.h5'

            s3_resource.download_file(bucket,key,Filename="trained_model.h5")
            if os.path.exists("trained_model.h5"):
                print("\n\033[0;32;40mSuccessfully create `trained_model.h5` file!\033[0m\n")
             
    else:
        raise Exception("\n\033[0;31;40mSomething went wrong when we are trying to create config file for you! Please contact us for help!\033[0m\n")
    
except Exception as err:
    print("\n\033[0;31;40mException: ",err,"\033[0m\n")
    
    if os.path.exists("key.txt"):
        os.remove("key.txt")
        print("\n\033[0;34;40m=== Remove key.txt file ===\033[0m\n")
    if os.path.exists("fastapi.yaml"):
        #os.remove("fastapi.yaml")
        #print("\033[0;34;40m=== Remove fastapi.yaml file ===\033[0m\n")
        print("\033[0;34;40m=== In production env, we wanna keep fastapi config until you delete the whole container or you need to delete it manually! ===\033[0m\n")
        
    if os.path.exists("trained_model.h5"):
        #os.remove("trained_model.h5")
        #print("\033[0;34;40m=== Remove trained_model.h5 file ===\033[0m\n")
        print("\033[0;34;40m=== In order to reduce our bills in AWS S3. Once you download the trained model, we will keep it until you delete the whole container or you need to delete it manually! ===\033[0m\n")
        
    print("\033[0;33;40mSystem will exit in 3 seconds~\n\033[0m")
    time.sleep(3)
    sys.exit(1)
else:
    print("\033[0;32;40mHave Fun :D \033[0m\n\n")
    print("You can copy your input info if you cannot remember...\n\nAfter 5 seconds, I will clear terminal and let you try our project!")
    time.sleep(5)
    os.system("clear")   
    
######################################################## create `fastapi.yaml` and `trained_model.h5` ########################################################
SECRET_KEY = key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 30 mins expire

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    abs_path = os.path.dirname((os.path.abspath(__file__)))
    yaml_path = abs_path + "/fastapi.yaml"
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)

    # user_dict = config[username]
    return UserInDB(**config[username])



def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    global username
    username = current_user.username
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    global username
    username = user.username
    # global accesstoken
    # accesstoken = access_token
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

############################# Auth - JWT #################################


# Home page
@app.get("/", response_class=HTMLResponse)
async def home():
    response = returnHomePage.getHomePage()
    return response


############################# API Functions #################################

@app.post("/qualityinspection/")
async def qualityinspection(file: bytes = File(), current_user: User = Depends(get_current_active_user)):
    """
        Cheking the quality by uploading your image file.
        """                      
    if not file:
        return {"message": "No upload file sent"}
    else:
        # content = file.read()
        # for file in files:
        #     count = 1
        #print(file)
        response = test_model.qualityinspection(file)
        

    return response


# @Description: input basemodel
# @Author: Cheng Wang
# @UpdateDate: 6/13/2022
class csvInfo(BaseModel):
    #description: Union[str, None] = None
    #price: float
    #tax: Union[float, None] = None
    fileName : str=None
    width : int=None
    height : int=None
    className : str # 飞机种类的 class 为 python 内置关键字 需要转换
    xmin : int=None
    ymin : int=None
    xmax : int=None
    ymax : int=None
    base64 : str=None
    RGB : dict=None
    valid_width : int=None
    valid_height : int=None
    fileSize : str=None
    aircraft_more_than_1 : bool=None
    aircraft_num : int=None
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)    
