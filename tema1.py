# global variables
q0_glo = 0
alpha = 'A'
sigma_glo = []
for i in range(0, 26):
		sigma_glo.append(alpha) 
		alpha = chr(ord(alpha) + 1)
sigma_glo.append('#')

# class Turing Machine
class Turing_Machine:
	def __init__(self, states, sigma, delta, q0, final_states):
		self.states = states
		self.sigma = sigma
		self.delta = delta
		self.q0 = q0
		self.final_states = final_states
	
# read function
def readTM(codificare_MT_string):
	nr_of_state = int(codificare_MT_string[0])
	states = []
	# add first state
	states.append(q0_glo)
	# add other states
	for i in range(1, nr_of_state):
		states.append(i)
	# there is final state	
	if(codificare_MT_string[1] != '-'):	
		final_states = [int(x) for x in codificare_MT_string[1].split(' ')]
	else:
		# there is no final state	
		final_states = '-';	
	# creating delta matrix	
	transitions = [[0 for x in range(5)]for y in range(len(codificare_MT_string) - 2)]
	# complete the matirx
	for i in range(2, len(codificare_MT_string)):
		transitions[i - 2] = [x for x in codificare_MT_string[i].split(' ')]
	# create an object
	TM = Turing_Machine(states, sigma_glo, transitions, q0_glo, final_states)
	return TM

# step function
def step(TM, config):
	config = config.split(",")
	# assign u, q and v
	u = config[0][1:len(config[0])]
	q = config[1]
	v = config[2][0:len(config[2]) - 1]
	config_1 = ()
	found = 0
	for i in range(0, len(TM.delta)):
		# if we find the state
		if TM.delta[i][0] == q:
			# if we find the current symbol
			if TM.delta[i][1] == v[0]:
				found = 1
				# right move
				if TM.delta[i][4] == 'R':
					q_1 = TM.delta[i][2] 
					u_1 = u + TM.delta[i][3]
					v_1 = v[1:len(v)]
					# left move
				if TM.delta[i][4] == 'L':
					q_1 = TM.delta[i][2]
					u_1 = u[0:len(u) - 1]
					v_1 = u[len(u) - 1] + TM.delta[i][3] + v[1 : len(v)] 
					# halt - don't move
				if TM.delta[i][4] == 'H':
					u_1 = u
					q_1 = TM.delta[i][2]
					v_1 = TM.delta[i][3] + v[1 : len(v)]
				if u_1 == '':
					u_1 = '#'
				if v_1 == '':
					v_1 = '#'		
				config_1 = (u_1, q_1,v_1)
	if found == 0:
		return 0								
	return config_1	

# accept function					
def accept(TM, word):
	curr_state = q0_glo
	word_index = 0
	if len(TM.final_states) == 1:
		if(TM.final_states[0] == '-'):
			return False
	while(1):
		found = 0
		for j in range(0, len(TM.delta)):
			# if we find the state and the current symbol
			if int(TM.delta[j][0]) == curr_state:
				if TM.delta[j][1] == word[word_index]:
					found = 1
					# change the current state	
					curr_state = int(TM.delta[j][2])
					# modify the word
					word = word[:word_index] + TM.delta[j][3] + word[word_index + 1 :]
					for k in range(0, len(TM.final_states)):
						# if current state is final return True
						if curr_state == int(TM.final_states[k]):
							return True	
						# left move
					if TM.delta[j][4] == 'L':
						word_index = word_index - 1
						if word_index >= len(word):
							word = "#" + word
							# right move
					if TM.delta[j][4] == 'R':
						word_index = word_index + 1
						if word_index >= len(word):
							word = word + "#"
							# halt
					if TM.delta[j][4] == 'H':
						word_index = word_index
		if found == 0:
			return False
# k_accept- same as "accept" function
# plus we count the number of steps
# we have done, and if they are less
# than or equal to k, function returns True 						
def k_accept(TM,word):
	word = word.split(",")
	k = word[1]
	word = word[0]
	curr_state = q0_glo
	word_index = 0
	steps = 0
	if len(TM.final_states) == 1:
		if(TM.final_states[0]) == '-':
			return False
	while (1):
		found = 0
		for j in range(0, len(TM.delta)):
			if int(TM.delta[j][0]) == curr_state:
				if TM.delta[j][1] == word[word_index]:
					steps = steps + 1
					if steps > int(k):
						return False
					found = 1
					curr_state = int(TM.delta[j][2])
					word = word[:word_index] + TM.delta[j][3] + word[word_index + 1 :]
					for m in range(0, len(TM.final_states)):
						# if current state is final
						# and number of steps is less or equal to k
						# return True
						if curr_state == int(TM.final_states[m]):
							if steps <= int(k):
								return True	
					if TM.delta[j][4] == 'L':
						word_index = word_index - 1
						if word_index >= len(word):
							word = "#" + word
					if TM.delta[j][4] == 'R':
						word_index = word_index + 1
						if word_index >= len(word):
							word = word + "#"
					if TM.delta[j][4] == 'H':
						word_index = word_index
		if found == 0:
			return False

codificare_MT_string = []	
# read the task name
task = input()
# read the input for the task
line_2 = input()
line_2_array = [x for x in line_2.split(' ')]
try:
	while True:
		line_3 = input()
		codificare_MT_string.append(line_3)
except EOFError as error:
	pass			
TM = readTM(codificare_MT_string)

if(task == 'step'):
	for i in range(0, len(line_2_array)):
		config_1 = step(TM, line_2_array[i])
		if config_1 == 0:
			print("False", end = " ")
		else:
			print("("+config_1[0]+","+str(config_1[1])+","+config_1[2]+")", end = " ")
if(task == 'accept'):
	for i in range(0, len(line_2_array)):
		res = accept(TM, line_2_array[i])		
		print(res, end = " ")
if(task == 'k_accept'):
	for i in range(0, len(line_2_array)):
		res = k_accept(TM,line_2_array[i])
		print(res, end = " ")