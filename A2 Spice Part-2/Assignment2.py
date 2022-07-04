'''
 Assignment 1 - EE2703
 Roll No: EE20B084
'''

import sys
import numpy as np

#this class used to store component data
class comp_data:
	fromnode = "0"  #first node value given in data
	tonode = "0"	#second node value given in data
	value = 0	#value for the component
	phase = 0	#phase in radians given for AC sources
	element= '0'	#type of element
	
	def __init__(self,name):
		self.name = name

if len(sys.argv) != 2:   #checking any input file given
	print('\nUsage: %s <inputfile>' % argv[0])
	exit()

with open(sys.argv[1]) as f:
	comp_lines = f.readlines()
	
	freq = 0;  	#by default assuming source is DC
	node_tbl = {}	#used to assign a number as key value to nodes used in circuit file
	comp_ls = []	#used to store list of all class of component data
	current_tbl = {}#used to assign currents of voltage sources
	i = 0		
	k = 0		#used to count voltage sources and inductors(if DC)
	
	for comp_line in comp_lines[::-1]:
			data = comp_line.split('#')[0].split()
		
			#for resistance, inductance, capacitance
			if(len(data) == 4):
				comp = comp_data(data[0])
				comp.fromnode = data[1]
				comp.tonode = data[2]
				comp.value = float(data[3])
				comp.element = data[0][0]
				
				if data[0][0] == 'L':
					if freq != 0:
						comp.value = complex(0,2*np.pi*freq*float(data[3]))
					else:  #In DC, L is given then we will make it as Voltage source with zero voltage at steady state
						k+=1
						comp.element = "VS"
						comp.value = 0
				if data[0][0] == 'C' and freq != 0:
					comp.value = complex(0,-1/(2*np.pi*freq*float(data[3])))
				
				comp_ls.append(comp)
				
			#for DC Sources	
			if(len(data) == 5):
				comp = comp_data(data[0])
				comp.fromnode = data[1]
				comp.tonode = data[2]
				comp.value = float(data[4])
				if data[0][0] == 'V': comp.element = 'VS';k+=1; current_tbl[data[0]] = k
				else: comp.element = 'CS'
				comp_ls.append(comp)
				
			#for AC sources
			if(len(data) == 6):
				comp = comp_data(data[0])
				comp.fromnode = data[1]
				comp.tonode = data[2]
				real = np.cos(float(data[5]))
				img = np.sin(float(data[5]))
				comp.value = (float(data[4])/2)*(complex(real,img))
				comp.phase = float(data[5])
				if data[0][0] == 'V': comp.element = 'VS'; k+=1; current_tbl[data[0]] = k
				else: comp.element = 'CS'
				comp_ls.append(comp)
			
			#for frequency
			if (len(data) == 3):
				freq = float(data[2])
				
			if(len(data)>3):
				if data[1] not in node_tbl.keys() :
					node_tbl[data[1]] = i
					i+=1
				if data[2] not in node_tbl.keys():
					node_tbl[data[2]] = i
					i+=1
					
	node_ls = list(node_tbl.keys())	
	current_ls = list(current_tbl.keys())	
	gnd = node_tbl['GND']	
	p = k-1		
	n = len(node_tbl)		
	M = np.zeros((k+n)*(k+n)).reshape((k+n,k+n))
	M = np.array(M,dtype=complex)
	b = np.zeros(k+n).reshape((k+n,1))
	b = np.array(b,dtype=complex)
	
	for x in comp_ls:	#as per MNA method used in circuit analysis, forming matrices 
		if x.element == 'R' or freq != 0 :
			if x.element != "VS" and x.element != 'CS':
				M[node_tbl[x.fromnode]][node_tbl[x.fromnode]] += (1/x.value)
				M[node_tbl[x.fromnode]][node_tbl[x.tonode]] -= (1/x.value)
				M[node_tbl[x.tonode]][node_tbl[x.tonode]] += (1/x.value)
				M[node_tbl[x.tonode]][node_tbl[x.fromnode]] -= (1/x.value)
		
		if x.element == 'VS':
			current_tbl[x.name] = k; k-=1
			M[node_tbl[x.fromnode]][n+k] -= 1
			M[n+k][node_tbl[x.fromnode]] -= 1
			M[node_tbl[x.tonode]][n+k] += 1
			M[n+k][node_tbl[x.tonode]] += 1
			b[n+k] = x.value
			
		if x.element == 'CS':
			b[node_tbl[x.fromnode]] += x.value
			b[node_tbl[x.tonode]] -= x.value
		
	M[gnd] = 0; M[gnd][gnd] = 1;b[gnd] = 0	#including an equation that Vgnd = 0, which makes matrices several changes
	
	print("Matrix M:\n",M)
	print("Matrix b:\n",b)	

	try:
		x = np.linalg.solve(M,b)
	except Exception:
		print('The matrix M cannot be inverted as it is singular. Please provide a valid circuit definition'); exit()
			
	i = 0
	while(i<=n+p):
		if(i<n): print("Voltage at node ", node_ls[i], "is ", x[i])		
		else:    print("Currents through ", current_ls[i-n], 'is ', x[i])
		i+=1 
	
	#Voltage convention : From node of the voltage source is at a lower potential  
	#Current covention: direction of current is to From node of voltage source
	#voltages of nodes are printed as per node_tbl obtained
