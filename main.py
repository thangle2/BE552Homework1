import os
import sys
import math
from celloapi2 import CelloQuery, CelloResult
import json

    # standard read and write functions
def read_file(fname,chassis_name):
    with open('input/'+ fname, 'r') as file:
        content = file.read()
    data = json.loads(content)
    if fname == f'{chassis_name}.UCF.json':
       name, ymax, ymin, K, n = parse_UCF(data)
    elif fname == f'{chassis_name}.input.json':
        name, ymax, ymin = parse_input(data)
    file.close()
    return [name, ymax, ymin, K, n]

def write_output(fname, data):
    # open and write to .output JSON file
    with open(fname, 'w') as file:
        json.dump(data, file)
    file.close()

def parse_UCF(data):
    name = []
    ymax = []
    ymin = []
    K = []
    n = []
    alpha = []
    beta = []

    for i in range(len(data)):
        if data[i]["collections"] == 'models':
            name.append(data[i]['name'])
            if (data[i]["collections"] == 'parameters'):
                for j in range(len(data[i][name])):
                    if data[i][name][j]['name'] == 'ymax':
                        ymax.append(data[i][name][j]['value'])
                    elif data[i][name][j]['name'] == 'ymin':
                        ymin.append(data[i][name][j]['value'])
                    elif data[i][name][j]['name'] == 'K':
                        K.append(data[i][name][j]['value'])
                    elif data[i][name][j]['name'] == 'n':
                        n.append(data[i][name][j]['value'])
    print(ymax)
    return name, ymax, ymin, K, n, alpha, beta
def parse_input(data):
    # parse .input JSON and store parameters in corresponding lists
    name = []
    ymax = []
    ymin = []
    # alpha = []
    # beta = []

    for i in range(len(data)):
        if data[i]["collections"] == 'models':
            name.append(data[i]['name'])
            for j in range(len(data[i][name])):
                if data[i][name][j]['name'] == 'ymax':
                    ymax.append(data[i][name][j]['value'])
                elif data[i][name][j]['name'] == 'ymin':
                    ymin.append(data[i][name][j]['value'])
                # elif data[i][name][j]['name'] == 'alpha':
                #     alpha.append(data[i][name][j]['value'])
                # elif data[i][name][j]['name'] == 'beta':
                #     beta.append(data[i][name][j]['value'])

    # return name, ymax, ymin, alpha, beta
    return name, ymax,ymin



#all of the operatioans
def stretch(x, ymax, ymin):
    ymax_new = ymax*x
    ymin_new = ymin/x
    print('Stretch by a factor of ',x,'\n Y_max went from ',ymax,' to ',ymax_new,'\n Y_min went from ',ymin,' to',ymin_new)
    return ymax_new, ymin_new


def strongpromoter(x, ymax, ymin):
    ymax_new = ymax*x
    ymin_new = ymin*x
    print('Strong promoter by a factor of ',x,'\n Y_max went from ',ymax,' to ',ymax_new,'\n Y_min went from ',ymin,' to',ymin_new)
    return ymax_new, ymin_new
        
def weakpromotoer(x,ymax,ymin):
	ymax_new= ymax/x
	ymin_new= ymin/x
	print('Weak promoter by a factor of ',x,'\n Y_max went from ',ymax,' to ',ymax_new,'\n Y_min went from ',ymin,' to',ymin_new)
	return ymax_new, ymin_new

def increaseslope(n, x):
    n_new = n*x
    print('Increase slope by a factor of ',n,'\n N went from ',n,' to ',n_new)   
    return n_new

def decreaseslope(n,x):
	n_new = n/x
	print('Decrease slope by a factor of ',n,'\n N went from ',n,' to ',n_new)
	return n_new


def weakrbs(k, x):
    k_new = k/x
    print('Weak RBS by a factor of ',k,'\n k went from ',k,' to ',k_new)       
    return k_new

def strongrbs(k,x):
	k_new = k*x
	print('Strong RBS by a factor of ',k,'\n k went from ',k,' to ',k_new)
	return k_new
#calculating the score
def response(ymin, ymax, n, k, x):
    output = ymin + (ymax-ymin)/(1+(x/k) ^ n)
    return output

def score(ymin,ymax,n,k,x):
	on_min = response(ymin,ymax,n,k,x[0])
	off_max= response(ymin,ymax,n,k,x[1])
	final_score=math.log10(on_min/off_max)
	return final_score
  
def main():
  #in_dir=os.path.join(os.getcwd(), 'input')
  #out_dir=os.path.join(os.getcwd(), 'output')
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
  all_input=read_file(input_files,chassis)
  UCF= read_file(input_ucf,chassis)
  print(type(all_input))
  #operations='x'
  #while (operations != 'h'):
  	#operations= input('Choose an operation:\n (a) Stretch \n (b) Strong promoter \n (c) Weak Promoter \n (d) Increase Slope \n (e) Decrease Slope \n (f) Weak RBS \n (g) Strong RBS \n (h) Stop')
  	#match operations:
    		#case 'a':
        	#x= input('Input x: ')
            #stretch(x, ymax, ymin)
            
       		#case 'b':
        
        	#case 'c':
        
        	#case 'd':
        
        	#case 'e':
        
        	#case 'f':
        
        	#case 'g':
if __name__ == "__main__":
    main()