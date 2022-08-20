import json
from telnetlib import DO
import pandas as pd
import copy


## Actual program
def recursive(d1, d2):
    d = {}
    for key, value in d1.items():
        if key in d2:
            if ((type(d1[key]) is dict) and type(d2[key]) is dict):
                d[key] = recursive(d1[key], d2[key])
            if (type(value) is not dict):
                if (d1[key] == d2[key]):
                    d[key] = value #blindly copy value eg string
                else:
                    d[key] = [d1[key], d2[key]] #append conflicts into a list
        else:
            d[key] = value #blindly copy the entire value

    for key, value in d2.items():
        if key not in d1:
            d[key] = value
    return d

def recursive_2(d1, d2, dOut):
    # no return
    for key, value in d1.items():
        if key in d2:
            if ((type(d1[key]) is dict) and type(d2[key]) is dict):
                dOut[key]={}
                recursive_2(d1[key], d2[key], dOut[key])
            if (type(value) is not dict):    
                if (d1[key] == d2[key]):
                    dOut[key] = value #blindly copy value eg string
                else:
                    dOut[key] = [d1[key], d2[key]]
        else:
            dOut[key]= value
    for key, value in d2.items():
        if key not in d1:
            dOut[key] = d2[key]


## A small test case
source ={
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "username": {
                    "type": "string",
                    "maxLength": 30,
                    "minLength": 2
                }
            }     
}
d ={}
destination ={
            "properties": {
                "user_id": {
                    "type": "string"
                },
                "username": {
                    "type": "string"
                }
            }
}
## try running it!
recursive_2(source, destination,d)
print(d)


## Test it on actual json files
def merge_JsonFiles(filename):
    result = list()

    with open(filename[0], 'r') as infile1:
        with open(filename[1], 'r') as infile2:
            data1 = json.load(infile1)
            data2 = json.load(infile2)
            data3 = recursive(data1, data2)
    
    print(data3)
                

    with open('MergeJsonDemo.json', 'w') as output_file:
        json.dump(data3, output_file, indent=4)

# files=['../account-service/docs/swagger.json','../payment-service/docs/swagger.json']

# merge_JsonFiles(files)
