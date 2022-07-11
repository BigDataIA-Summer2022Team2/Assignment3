import os
import json
from json import load
from boto3 import client
import boto3
# @Description: take class name and file name as input, return information of files that meet those two requirements
# @Author: Cheng Wang
# @UpdateDate: 6/12/2022
"""
    Type the class name and file name you want to search.
"""    
def getFileNameClassNameFilteredResult(className:str,filename:str):
    try:
        key = 'csv/combined.csv'
        abs_path = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
        #csv_path = abs_path+"/credentials/aws_s3_credentials.json"
        csv_path = abs_path+"/credentials/aws_s3_credentials.json"
        credentials = json.load(open(csv_path))
        s3_resource = boto3.client(
            service_name=credentials['service_name'],
            region_name=credentials['region_name'],
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'])


        bucket = credentials['aws_s3_bucket_name']

        obj = s3_resource.get_object(Bucket = bucket , Key = key)
        body_str = obj['Body'].read().decode()

        csv_header_value_list = body_str.split() # split body into 1 list (contain csv headers and values) header=str->  csv_header_value_list[0]        value=string
        inner_index_num = csv_header_value_list[0].split(',')   # header 0-7 [0] file_name
        index_no = 0
        result={}

        # filename="4a042db1cef213a1ed865422e6355f76"
        # className=""

        for i in range(len(csv_header_value_list)):
            if(i > 0):
                index_no += 1 #?   +1 record(key+value)
                            
                header_list = csv_header_value_list[0].split(',') # split key(header) list
                        
                csv_header_value_list[i] = csv_header_value_list[i].split(',') #  slipt value list ','

                
                if(filename == '' or filename == csv_header_value_list[i][0]):
                    if(className == '' or className == csv_header_value_list[i][3]):
                        result[str(index_no)] = {}
                        for j in range(len(inner_index_num)): #? 8 elements
                            result[str((index_no))][header_list[j]] = csv_header_value_list[i][j] # i = 0      |      j = 0 - 7  
        if result == {}:
            result['response'] = {'error':'No data Found'}
        return result
    except:
        print("There are some error in this function, please check your input format") 

