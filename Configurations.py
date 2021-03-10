
# FILE
result_path = "./results"

# LOG
write_to_console = True

# PASSWORD
default_password_size = 16

attempts = 100

letters_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'w', 'y', 'z']
letter_upper = [c.upper() for c in letters_lower]
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
signs = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '\\', '|', "{", "}", ";", ":", "<", ">", "?"]

characters = letters_lower + letter_upper

number_of_threads = 16