import sys

Circuit = ".circuit\n"
End = ".end\n"

def reverse_tokens(Cktlines):

	for Cktline in Cktlines[::-1]:
		tokens = Cktline.split('#')[0].split()
		
		# R, L, C, Independent Sources
		if(len(tokens) == 4):
			ElementType = tokens[0]
			node1 = tokens[1]
			node2 = tokens[2]
			Value = tokens[3]
			print(Value,'',node2,'',node1,'',ElementType)
			
		# CCxS
		elif(len(tokens) == 5):
			ElementType = tokens[0]
			node1 = tokens[1]
			node2 = tokens[2]
			Voltage = tokens[3]
			Value = tokens[4]
			print(Value,'',Voltage,'',node2,'',node1,'',ElementType)
			
		# VCxS
		elif(len(tokens) == 6):
			ElementType = tokens[0]
			node1 = tokens[1]
			node2 = tokens[2]
			node3 = tokens[3]
			node4 = tokens[4]
			Value = tokens[5]
			print(Value,'',node4,'',node3,'',node2,'',node1,'',ElementType)
			
		else:
			print(Cktline)
	
	return
			


if len(sys.argv) != 2 :
	print('\nUsage: %s <inputfile>' % argv[0])
	exit()
	
try:
	with open(sys.argv[1]) as f:
		lines = f.readlines()
		
		start = lines.index(Circuit)
		end = lines.index(End)
		reverse_tokens(lines[start+1:end])
        
except IOError:
    print('Invalid file')
    exit()
