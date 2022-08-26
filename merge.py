import json
from telnetlib import DO
import pandas as pd
import copy
import argparse

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
# recursive_2(source, destination,d)
# print(d)


## Test it on actual json files
def merge_JsonFiles(inFileList, outFileName):
    result = list()

    with open(inFileList[0], 'r') as infile1:
        with open(inFileList[1], 'r') as infile2:
            data1 = json.load(infile1)
            data2 = json.load(infile2)
            data3 = recursive(data1, data2)
    
    # print(data3)
                

    with open(outFileName, 'w') as output_file:
        json.dump(data3, output_file, indent=4)

# files=['../account-service/docs/swagger.json','../payment-service/docs/swagger.json']

# merge_JsonFiles(files)

# Create the parser
parser = argparse.ArgumentParser()
# Add an argument
parser.add_argument('--input', type=str, required=True)
parser.add_argument('--output', type=str, required=True)
# Parse the argument
args = parser.parse_args()

in_str = args.input
in_list = in_str.split(",")
in1 = in_list[0]
in2 = in_list[1]
print(in1,in2)
out_str = args.output
print(out_str)

merge_JsonFiles(in_list, out_str)


# Appendix
# merge Any x, Any y
# x : Empty
#     return y
# x : Key k, Value v
#     y : Empty
#         return x
#     y : Key k, Value w
#         return ???
#     y : Key l, Value w
#         return
# x : Array [x1...xn], y: Array [y1...yn]
#     return Array[x_1'...x_n']
#     where x_i' = merge ( x_1, y[k] )


# def fib(x):
#     if x == 2:
#         return 1
#     if x == 1:
#         return 1
#     reuturn fib(x-1)+fib(x-2)