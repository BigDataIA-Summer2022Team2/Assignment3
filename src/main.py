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

########################################################
result={}
if len(argv) == 1:
    os.system("echo 'You need input your username, full_name, email, password!!!'")
else:
    print("Your argvs are:\t", argv)
    print("Length of argv is:\t", len(argv),"\n\n\n")
    username = argv[1]
    result[username] = {}
    result[username]['username'] = argv[1]
    list_passwd = []
    list_passwd.append(argv[2])
    list_hashed_res = stauth.Hasher(list_passwd).generate()
    result[username]['hashed_password'] = list_hashed_res[0]
    
    print("username:\t\t\t", argv[1])
    print("plain password:\t\t\t", argv[2])
    print("hashed password:\t\t", list_hashed_res[0])

    if len(argv) == 3:
        result[username]['full_name'] = argv[1]
        result[username]['email'] = ""
        print("full name:\t\t\t", argv[1])
        print("email:\t\t\t\t", "")

    elif(len(argv) == 4):
        result[username]['full_name'] = argv[3]
        result[username]['email'] = ""
        print("full name:\t\t\t", argv[3])
        print("email:\t\t\t\t", "")

    elif(len(argv) == 5):
        result[username]['full_name'] = argv[3]
        result[username]['email'] = argv[4]
        print("full name:\t\t\t", argv[3])
        print("email:\t\t\t\t", argv[4])

    result[username]['disabled'] = False
    print('account disabled:\t\t', result[username]['disabled'])

    with open('fastapi.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(data=result, stream=file, allow_unicode=True)
        print("Successfully create `fastapi.yaml` file!")
         
    abs_path = os.path.dirname((os.path.abspath(__file__)))
    yaml_path = abs_path + "/fastapi.yaml"
    
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
        if username in config.keys():
            user_dict = config[username]
            print(user_dict)
#########################################################











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
