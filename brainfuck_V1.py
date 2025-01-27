'''
	Brainfuck Interpreter using Pre-Rendering
	August 24, 2017
'''

''' ---------- FUNCTIONS ---------- '''

def script_reader(file_name):
# Reads a .txt script file and removes any whitespace from it
	
	try:
		with open(file_name, "r") as raw_file:
			extracted = raw_file.read()
	except FileNotFoundError:
		raise Exception("The file does not exist")
		
	return "".join(extracted.split())
	
def pointer_inc(pointer, memory_map):
# Implements the > function	
	
	pointer += 1
	
	if len(memory_map) <= pointer + 1:
		memory_map.append(0)
		
	if pointer >= 30000:
		raise Exception("The memory pointer has overflowed over 30000")
		
	return pointer, memory_map
	
def pointer_dec(pointer):
# Implements the < function
	
	pointer -= 1
	
	if pointer < 0:
		raise Exception("The memory pointer has underflowed")
	
	return pointer
	
def byte_inc(pointed_byte):
# Implements the + function	

	pointed_byte = 0 if pointed_byte == 255 else pointed_byte + 1
		
	return pointed_byte

def byte_dec(pointed_byte):
# Implements the - function	

	pointed_byte = 255 if pointed_byte == 0 else pointed_byte - 1
	
	return pointed_byte

def print_ascii(pointed_byte):
# Implements the . function
	
	print(chr(pointed_byte), end = "", flush = True)
	
def usr_input():
# Implements the , function	
	
	try:
		ascii_input = ord(input("Enter a valid ASCII character:\n> "))
	except:
		raise Exception("This is not a valid ASCII character")

	return ascii_input

def loop_start(ins_pointer, script, pointed_byte):
# Implements the [ function	

	loop_token = 1
	while loop_token > 0 and pointed_byte == 0:
		ins_pointer += 1
		
		if script[ins_pointer] == "[":
			loop_token += 1
		if script[ins_pointer] == "]":
			loop_token -= 1
		
	return ins_pointer

# Implements the ] function	
def loop_end(ins_pointer, script, pointed_byte):
		
	loop_token = 1
	while loop_token > 0 and pointed_byte != 0:
		ins_pointer -= 1
		
		if script[ins_pointer] == "]":
			loop_token += 1
		if script[ins_pointer] == "[":
			loop_token -= 1
				
	return ins_pointer
	
''' ---------- MAIN PROGRAM ---------- '''

# Executes the interpreter if called as a main program
if __name__ == "__main__":
	
	script = script_reader(input("Enter the script file name:\n> "))
	memory_map = [0]
	pointer = 0
	ins_pointer = 0
	
	while ins_pointer < len(script):
		
		if script[ins_pointer] == ">":
			pointer, memory_map = pointer_inc(pointer, memory_map)
			
		if script[ins_pointer] == "<":
			pointer = pointer_dec(pointer)
			
		if script[ins_pointer] == "+":
			memory_map[pointer] = byte_inc(memory_map[pointer])
			
		if script[ins_pointer] == "-":
			memory_map[pointer] = byte_dec(memory_map[pointer])
			
		if script[ins_pointer] == ".":
			print_ascii(memory_map[pointer])
			
		if script[ins_pointer] == ",":
			memory_map[pointer] = usr_input()
			
		if script[ins_pointer] == "[":
			ins_pointer = loop_start(ins_pointer, script, memory_map[pointer])
		
		if script[ins_pointer] == "]":
			ins_pointer = loop_end(ins_pointer, script, memory_map[pointer])	
	
		ins_pointer += 1
	input("The program has ended. Press any key to exit.\n")
