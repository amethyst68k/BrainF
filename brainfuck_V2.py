'''
	Brainfuck Interpreter with Pre-Rendering
	August 26, 2017
'''

from datetime import datetime

''' ---------- PRE-RENDERING FUNCTIONS ---------- '''

# Pre-renders the target address of a loop start [
def loop_prerender(script, ins_pointer):
	
	parenthesis_token = 1
	
	while parenthesis_token > 0:
		ins_pointer += 1
		
		# Uses a parenthesis token system to associate parenthesis pairs
		try:
			if script[ins_pointer] == "[":
				parenthesis_token += 1
			if script[ins_pointer] == "]":
				parenthesis_token -= 1
		
		# Raises an exception when square brackets are unbalanced
		except IndexError:
			raise Exception("UNBALANCED BRACKETS")
			
	return ins_pointer

# Pre-renders the total sum of a group of incrementations + / decrementations -
def add_prerender(script, ins_pointer):
	
	final_add = 0
	
	while 1:
		
		# Adds up the final value of incrementation/decrementation
		try:
			if script[ins_pointer] == "+":
				final_add += 1
			elif script[ins_pointer] == "-":
				final_add -= 1	
			elif script[ins_pointer] in "><[].,":
				break
		
		# Handles the case where the function reaches the end of the program
		except IndexError:
			break
		
		ins_pointer += 1
		
	# NOTE: Decrements the instruction pointer to cancel the last loop cycle
	return ins_pointer - 1, final_add

# Pre-renders the total sum of a group of pointer incrementations > / decrementations <
def pointer_prerender(script, ins_pointer):
	
	final_add = 0
	
	while 1:
		
		# Adds up the final value of pointer incrementation/decrementation
		try:
			if script[ins_pointer] == ">":
				final_add += 1
			elif script[ins_pointer] == "<":
				final_add -= 1
			elif script[ins_pointer] in "+-[].,":
				break
		
		# Handles the case where the function reaches the end of the program
		except IndexError:
			break
			
		ins_pointer += 1
	
	# NOTE: Decrements the instruction pointer to cancel the last loop cycle	
	return ins_pointer - 1, final_add

''' ---------- PRE-RENDERING ---------- '''	

# Loads the script file from current directory
file_name = input("Enter the script file name:\n> ")
with open(file_name, "r") as raw_file: 
	script = "".join(raw_file.read())

# Starts a timer
timer_start = datetime.now()

# Initialises various dictionaries used to store pre-rendering data
loop_start_dict = {}
loop_end_dict = {}
inc_dict = {}
bypass_dict = {}
point_dict = {}

ins_pointer = 0

# Pre-rendering loop
while ins_pointer < len(script):
	
	# Pre-renders the loop addresses
	if script[ins_pointer] == "[":
		loop_target = loop_prerender(script, ins_pointer)
		loop_start_dict[ins_pointer] = loop_target
		loop_end_dict[loop_target] = ins_pointer

	# Pre-renders the incrementation/decrementation values and the bypass addresses
	if script[ins_pointer] in "+-":
		new_ins_pointer, inc_dict[ins_pointer] = add_prerender(script, ins_pointer)
		bypass_dict[ins_pointer] = new_ins_pointer
		ins_pointer = new_ins_pointer
		
	# Pre-renders the instruction pointer incrementation/decrementation values and the bypass addresses
	if script[ins_pointer] in "><":
		new_ins_pointer, point_dict[ins_pointer] = pointer_prerender(script, ins_pointer)
		bypass_dict[ins_pointer] = new_ins_pointer
		ins_pointer = new_ins_pointer
		
	ins_pointer += 1

''' ---------- PROGRAM EXECUTION ---------- '''

# Initialises the memory map, memory pointer and instruction pointer
memory_map = [0]
pointer = 0
ins_pointer = 0

# Executes the program until the end of instructions
while ins_pointer < len(script):
	
	# Increments >/Decrements < the memory pointer
	if script[ins_pointer] in "><": 
		pointer += point_dict[ins_pointer]
		ins_pointer = bypass_dict[ins_pointer]
		
		# Creates a new memory byte if the memory pointer points to a new memory address
		while pointer > len(memory_map) - 1:
			memory_map.append(0)
		
		# Handles the case where the memory pointer overflows to 30000 or more	
		if len(memory_map) > 30000:
			raise Exception("POINTER OVERFLOWED ABOVE 30000")
		
		# Handles the case where the memory pointer underflows
		if pointer < 0:
			raise Exception("POINTER UNDERFLOWED BELOW 0")
	
	# Increments +/Decrements -	a byte
	if script[ins_pointer] in "+-":
		memory_map[pointer] += inc_dict[ins_pointer]
		
		# Simulates unsigned 8 bit overflow
		while memory_map[pointer] > 255:
			memory_map[pointer] -= 256
		while memory_map[pointer] < 0:
			memory_map[pointer] += 256
		
		ins_pointer = bypass_dict[ins_pointer]
	
	# Prints an ASCII character from byte .		
	if script[ins_pointer] == ".":
		print(chr(memory_map[pointer]), end = "", flush = True)
	
	# Asks the user for an ASCII character as an input byte ,
	if script[ins_pointer] == ",":
		ascii_input = ord(input("\nEnter a valid ASCII character: "))
	
	# [ Jumps to loop end if byte is equal to 0
	if script[ins_pointer] == "[" and memory_map[pointer] == 0:
		ins_pointer = loop_start_dict[ins_pointer]
	
	# ] Jumps to loop start if byte is not equal to 0
	if script[ins_pointer] == "]" and memory_map[pointer] != 0:
		ins_pointer = loop_end_dict[ins_pointer]
		
	ins_pointer += 1

# Prints the total execution time and waits for the user's input to close the interpreter
input("\nExecution time: {}. Press any key to exit.\n".format(datetime.now() - timer_start))
