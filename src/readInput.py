from sys import argv
import os
import yaml
import streamlit_authenticator as stauth


if "__main__"==__name__:

    # username = "admin"

    result={}
    

    
    if len(argv) == 1:
        os.system("echo 'You need input your username, full_name, email, password!!!'")
    else:
        username = argv[1]
        result[username] = {}
        result[username]['username'] = argv[1]
        list_passwd = []
        list_passwd.append(argv[2])
        print("Create a list to store passwd:\t", list_passwd)
        list_hashed_res = stauth.Hasher(list_passwd).generate()
        print("Here is list of passwd hashed:\t", list_hashed_res)
        result[username]['hashed_password'] = list_hashed_res[0]
        print("After hashed password:\t", result[username]['hashed_password'])
        if len(argv) == 3:
            result[username]['full_name'] = argv[1]
            result[username]['email'] = ""
        elif(len(argv) == 4):
            result[username]['full_name'] = argv[3]
            result[username]['email'] = ""
        elif(len(argv) == 5):
            result[username]['full_name'] = argv[3]
            result[username]['email'] = argv[4]
        
        result[username]['disabled'] = False
    
        with open('fastapi.yaml', 'w', encoding='utf-8') as file:
            yaml.dump(data=result, stream=file, allow_unicode=True)
        
        abs_path = os.path.dirname((os.path.abspath(__file__)))
        yaml_path = abs_path + "/fastapi.yaml"
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
            if username in config.keys():
                user_dict = config[username]
                print(user_dict)
