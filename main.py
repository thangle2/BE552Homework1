import os
import sys
import math
from celloapi2 import CelloQuery, CelloResult
import json

#-------- Reading and writing the files
def read_file(fname,chassis_name):
    K=[]
    n=[]
    with open('input/' + fname, 'r') as file:
        content = file.read()
    data = json.loads(content)
    name, ymax, ymin, K, n = parse(data)
    file.close()
    return name, ymax, ymin, K, n

def write_output(fname, data):
    # open and write to .output JSON file
    with open(fname, 'w') as file:
        json.dump(data, file)
    file.close()
#------- Parsing through the Json files
def parse(data):
    name = []
    ymax = []
    ymin = []
    K = []
    n = []

    for i in range(len(data)):
        if data[i]["collection"] == 'models':
            name.append(data[i]['name'])
            for j in range(len(data[i]['parameters'])):
                if data[i]['parameters'][j]['name'] == 'ymax':
                    ymax.append(data[i]['parameters'][j]['value'])
                elif data[i]['parameters'][j]['name'] == 'ymin':
                    ymin.append(data[i]['parameters'][j]['value'])
                elif data[i]['parameters'][j]['name'] == 'K':
                    K.append(data[i]['parameters'][j]['value'])
                elif data[i]['parameters'][j]['name'] == 'n':
                    n.append(data[i]['parameters'][j]['value'])
    return name, ymax, ymin, K, n



#----------all of the necessary operations
def stretch(x, ymax, ymin):
    for i in range(len(ymax)):
        ymax[i]=ymax[i]*x
        print('Stretch by a factor of ',x,'\n Y_max went to',ymax[i])
    for i in range(len(ymin)):
        ymin[i]=ymin[i]/x
        print('Stretch by a factor of ',x,'\n Y_minwent to',ymin[i])
    return ymax, ymin


def strongpromoter(x, ymax, ymin):
    for i in range(len(ymax)):
        ymax[i]=ymax[i]*x
        print('Strong promoter by a factor of ',x,'\n Y_max went to',ymax[i])
    for i in range(len(ymin)):
        ymin[i]=ymin[i]*x
        print('Strong promoter by a factor of ',x,'\n Y_minwent to',ymin[i])
    return ymax, ymin
        
def weakpromoter(x,ymax,ymin):
    for i in range(len(ymax)):
        ymax[i]=ymax[i]/x
        print('Weak promoter by a factor of ',x,'\n Y_max went to',ymax[i])
    for i in range(len(ymin)):
        ymin[i]=ymin[i]/x
        print('Weak promoter by a factor of ',x,'\n Y_minwent to',ymin[i])
    return ymax, ymin

def increaseslope(n, x):
    for i in range(len(n)):
        n[i]=n[i]*x
        print('Increase Slope by a factor of ',x,'\n n went to',n[i])
    return n

def decreaseslope(n,x):
    for i in range(len(n)):
        n[i]=n[i]/x
        print('Decrease Slope by a factor of ',x,'\n n went to',n[i])
    return n


def weakrbs(k, x):
    for i in range(len(k)):
        k[i]=k[i]/x
        print('Weak RBS by a factor of ',x,'\n b went to',k[i])
    return k

def strongrbs(k,x):
    for i in range(len(k)):
        k[i]=k[i]*x
        print('Strong RBS by a factor of ',x,'\n n went to',k[i])
    return k
#----------------calculating the score
def response(ymin, ymax, n, k, x):
    output = ymin + (ymax-ymin)/(1+(x/k) ^ n)
    return output

def score(ymin,ymax,n,k,x):
    truthtable = [0]*2
    for i in range(0, 1):
        truthtable[i] = response(ymin, ymax, n, k, x[i])

    on_min = truthtable[0]
    off_max= truthtable[1]
    final_score=math.log10(on_min/off_max)
    return final_score
  
def main():
  in_dir=os.path.join(os.getcwd(), 'input')
  out_dir=os.path.join(os.getcwd(), 'output')
  chassis=input('Enter chassis name: ')
  input_ucf= f'{chassis}.UCF.json'
  input_files=f'{chassis}.input.json'
  output_files=f'{chassis}.output.json'
  v_file = 'and.v'
  options = 'options.csv'
  q = CelloQuery(
        input_directory=in_dir,
        output_directory=out_dir,
        verilog_file=v_file,
        compiler_options=options,
        input_ucf=input_ucf,
        input_sensors=input_files,
        output_device=output_files,
    )
  name1, ymax1, ymin1, K1, n1=read_file(input_files,chassis)
  name2, ymax2, ymin2, K2, n2= read_file(input_ucf,chassis)
  name=name1+name2
  ymax=ymax1+ymax2
  ymin=ymin1+ymin2
  K=K1+K2
  n=n1+n2
  operations='x'
  xfinal=[]
  while (operations != 'h'):
    operations= input('Choose an operation:\n (a) Stretch \n (b) Strong promoter \n (c) Weak Promoter \n (d) Increase Slope \n (e) Decrease Slope \n (f) Weak RBS \n (g) Strong RBS \n (h) Stop\n')
    if (operations=='a'):
        x=input('Input x: ')
        ymax,ymin=stretch(float(x), ymax, ymin)
        xfinal.append(float(x))
    elif(operations=='b'):
        x=input('Input x: ')
        ymax,ymin=strongpromoter(float(x),ymax,ymin)
        xfinal.append(float(x))
    elif(operations=='c'): 
        x=input('Input x: ')
        ymax,ymin=weakpromoter(float(x),ymax,ymin)
        xfinal.append(float(x))
    elif(operations=='d'): 
        x=input('Input x: ')
        n=increaseslope(n,float(x))
        xfinal.append(float(x))
    elif(operations=='e'): 
        x=input('Input x: ')
        n=decreaseslope(n,float(x))
        xfinal.append(float(x))
    elif(operations=='f'): 
        x=input('Input x: ')
        K=weakrbs(K,float(x))
        xfinal.append(float(x))
    elif(operations=='g'):
        x=input('Input x: ')
        K=strongrbs(K,float(x)) 
        xfinal.append(float(x)) 
  print(xfinal)
  print("Output of our score: ", score(ymin,ymax,n,K,xfinal));
  q.get_results()
  res = CelloResult(results_dir=out_dir)
  print("Output of sequence score: ",res.circuit_score)   

if __name__ == "__main__":
    main()
