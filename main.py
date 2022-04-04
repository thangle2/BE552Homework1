import os
import sys
import math
from itertools import combinations
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
    if(len(K)==0):
        for i in range(len(name)):
            K.append(0)
    if(len(n)==0):
        for i in range(len(name)):
            n.append(0)

    return name, ymax, ymin, K, n



#----------all of the necessary operations
def stretch(x, ymax, ymin,tempymax,tempymin):
    for i in range(len(ymax)):
        if((ymax[i]==tempymax) and (ymin[i]==tempymin)):
                ymax[i]=ymax[i]*x
                ymin[i]=ymin[i]/x
                print('Stretch by a factor of ',x,' Y_max went to',ymax[i],' from ',tempymax)
                print('Stretch by a factor of ',x,' Y_minwent to',ymin[i],' from ',tempymin)
    return ymax, ymin


def strongpromoter(x, ymax, ymin,tempymax,tempymin):
    for i in range(len(ymax)):
        if((ymax[i]==tempymax) and (ymin[i]==tempymin)):
            ymax[i]=ymax[i]*x
            ymin[i]=ymin[i]*x
            print('Strong promoter by a factor of ',x,'\n Y_max went to',ymax[i],' from ',tempymax)
            print('Strong promoter by a factor of ',x,'\n Y_minwent to',ymin[i],' from ',tempymin)
    return ymax, ymin
        
def weakpromoter(x,ymax,ymin,tempymax,tempymin):
    for i in range(len(ymax)):
        if((ymax[i]==tempymax) and (ymin[i]==tempymin)):
            ymax[i]=ymax[i]/x
            ymin[i]=ymin[i]/x
            print('Weak promoter by a factor of ',x,'\n Y_max went to',ymax[i],' from ',tempymax)
            print('Weak promoter by a factor of ',x,'\n Y_minwent to',ymin[i],' from ',tempymin)
    return ymax, ymin

def increaseslope(n, x,tempn):
    for i in range(len(n)):
        if(tempn==n[i]):
            n[i]=n[i]*x
            print('Increase Slope by a factor of ',x,'\n n went to',n[i],' from ',tempn)
    return n

def decreaseslope(n,x):
    for i in range(len(n)):
        if(tempn==n[i]):
            n[i]=n[i]/x
            print('Decrease Slope by a factor of ',x,'\n n went to',n[i],' from ',tempn)
    return n


def weakrbs(k, x,tempk):
    for i in range(len(k)):
        if(tempk==k[i]):
            k[i]=k[i]/x
            print('Weak RBS by a factor of ',x,'\n b went to',k[i],' from ',tempk)
    return k

def strongrbs(k,x):
    for i in range(len(k)):
        if(tempk==k[i]):
            k[i]=k[i]*x
            print('Strong RBS by a factor of ',x,'\n b went to',k[i],' from ',tempymax)
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
#---------------- gettinng the stat given the name of the sensor or gate
def getstat(input,name,ymax,ymin,k,n):
    for i in range(len(name)):
        if (name[i]==input):
            return ymax[i],ymin[i],k[i],n[i]
    print('Not Found!')
#--------update the json files
def update(input_files,name,ymax,ymin,k,n):
    with open('input/' + input_files, "r") as jsonFile:
        data = json.load(jsonFile)
    for x in range(len(name)):
        nametime=name[x]
        tempymax,tempymin,tempk,tempn=getstat(nametime,name,ymax,ymin,k,n)
        for i in range(len(data)):
            if data[i]["collection"] == 'models':
                if(data[i]['name']==name[x]):
                    for j in range(len(data[i]['parameters'])):
                        if data[i]['parameters'][j]['name'] == 'ymax':
                            data[i]['parameters'][j]['value']=tempymax
                        elif data[i]['parameters'][j]['name'] == 'ymin':
                            data[i]['parameters'][j]['value']=tempymin
                        elif data[i]['parameters'][j]['name'] == 'K':
                            data[i]['parameters'][j]['value']=tempk
                        elif data[i]['parameters'][j]['name'] == 'n':
                            data[i]['parameters'][j]['value']=tempn
    with open('input/' + input_files, "w") as jsonFile:
        json.dump(data, jsonFile)





def main():
    #--------inputing all files
    in_dir=os.path.join(os.getcwd(), 'input')
    out_dir=os.path.join(os.getcwd(), 'output')
    chassis=input('Enter chassis name: ')
    input_ucf= f'{chassis}.UCF.json'
    input_files=f'{chassis}.input.json'
    output_files=f'{chassis}.output.json'
    v_file = 'and.v'
    options = 'options.csv'
    name1, ymax1, ymin1, K1, n1=read_file(input_files,chassis)
    name2, ymax2, ymin2, K2, n2= read_file(input_ucf,chassis)
    user_choice='x'
    while(user_choice !='c'):
        user_choice= input('What do you want to do:\n (a) Do an operation on gate or sensor\n (b) Check a sensor or a gate\n (c) Check result\n')
        if(user_choice=='a'):
            operations='x'
            while (operations != 'h'):
                operations= input('Choose an operation:\n (a) Stretch \n (b) Strong promoter \n (c) Weak Promoter \n (d) Increase Slope \n (e) Decrease Slope \n (f) Weak RBS \n (g) Strong RBS \n (h) Stop\n')
                if(operations=='h'):
                    break
                gate_sensor= input('Gate or Sensors: \n (a) Gate \b (b) Sensor\n')
                if(gate_sensor=='a'):
                    name=name2
                    ymax=ymax2
                    ymin=ymin2
                    k=K2
                    n=n2
                    print('--------------')
                    for i in range(len(name2)):
                        print(i,'-',name2[i],'\n')
                elif(gate_sensor=='b'):
                    name=name1
                    ymax=ymax1
                    ymin=ymin1
                    k=K1
                    n=n1
                    print('--------------')
                    for i in range(len(name1)):
                        print(i,'-',name1[i],'\n')
                nametime_index=input('Choose a name (type the number)\n')
                nametime=name[int(nametime_index)]
                tempymax,tempymin,tempk,tempn=getstat(nametime,name,ymax,ymin,k,n) 
                if (operations=='a'):
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Stretch ',nametime,' by ',x)
                    print('--------------')
                    ymax,ymin=stretch(float(x), ymax, ymin,tempymax,tempymin)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='b'):
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Strong promoter ',nametime,' by ',x)
                    print('--------------')
                    ymax,ymin=strongpromoter(float(x),ymax,ymin,tempymax,tempymin)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='c'): 
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Weak promoter ',nametime,' by ',x)
                    print('--------------')
                    ymax,ymin=weakpromoter(float(x),ymax,ymin,tempymax,tempymin)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='d'): 
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Increase Slope ',nametime,' by ',x)
                    print('--------------')
                    n=increaseslope(n,float(x),tempn)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='e'): 
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Decrease Slope ',nametime,' by ',x)
                    print('--------------')
                    n=decreaseslope(n,float(x),tempn)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='f'): 
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Weak RBS ',nametime,' by ',x)
                    print('--------------')
                    K=weakrbs(k,float(x),tempk)
                    print('--------------')
                    print('\n\n\n')
                elif(operations=='g'):
                    x=input('Input x: ')
                    print('\n\n\n')
                    print('--------------')
                    print('Strong RBS ',nametime,' by ',x)
                    print('--------------')
                    K=strongrbs(k,float(x),tempk)
                    print('--------------')
                    print('\n\n\n')
                if(gate_sensor=='a'):
                    name2=name
                    ymax2=ymax
                    ymin2=ymin
                    K2=k
                    n2=n
                if(gate_sensor=='a'):
                    name1=name
                    ymax1=ymax
                    ymin1=ymin
                    K1=k
                    n1=n
        elif(user_choice=='b'):
            gate_sensor= input('Gate or Sensors: \n (a) Gate \b (b) Sensor\n')
            nametime_index='y'
            while(nametime_index!='x'):
                if(gate_sensor=='a'):
                    name=name2
                    ymax=ymax2
                    ymin=ymin2
                    k=K2
                    n=n2
                    print('--------------')
                    for i in range(len(name2)):
                        print(i,'-',name2[i],'\n')
                    print('(b) Change to Sensor')
                    print('(x) stop\n')
                elif(gate_sensor=='b'):
                    name=name1
                    ymax=ymax1
                    ymin=ymin1
                    k=K1
                    n=n1
                    print('--------------')
                    for i in range(len(name1)):
                        print(i,'-',name1[i],'\n')
                    print('(b) Change to Gate')
                    print('(x) stop\n')
                nametime_index=input('Choose a name (type the number or variable)\n')
                if(nametime_index=='x'):
                    break
                elif(nametime_index=='b'):
                    if(gate_sensor=='a'):
                        gate_sensor='b'
                    elif(gate_sensor=='b'):
                        gate_sensor='a'
                else:

                    nametime=name[int(nametime_index)]
                    tempymax,tempymin,tempk,tempn=getstat(nametime,name,ymax,ymin,k,n)
                    print('\n\n\n')
                    print('--------------')
                    print(nametime,' statistic:\n','Ymax: ',tempymax,'\n Ymin: ',tempymin,'\n K: ',tempk,'\n n:',tempn)
                    print('--------------')
                    print('\n\n\n')
    update(input_files,name1,ymax1,ymin1,K1,n1)
    update(input_ucf,name2,ymax2,ymin2,K2,n2)
    q = CelloQuery(
        input_directory=in_dir,
        output_directory=out_dir,
        verilog_file=v_file,
        compiler_options=options,
        input_ucf=input_ucf,
        input_sensors=input_files,
        output_device=output_files,
    )
    best_score = 0
    best_gates = None
    best_input_signals = None
    signal_input = 2
    signals = q.get_input_signals()
    print('--------------')
    signal_pairing = list(combinations(signals, signal_input))
    for signal_set in signal_pairing:
        signal_set = list(signal_set)
        q.set_input_signals(signal_set)
        q.get_results()
        try:
            res = CelloResult(results_dir=out_dir)
            if res.circuit_score > best_score:
                best_score = res.circuit_score
                best_chassis = chassis
                best_input_signals = signal_set
        except:
            pass
        q.reset_input_signals()
    print('--------------')
    print(f'Best Score: {best_score}')
    print(f'Best Input Signals: {best_input_signals}')  

if __name__ == "__main__":
    main()
