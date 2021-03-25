import logging as log
from threading import Lock

mutex = Lock()

password = ""

# FILE
result_path = "./results"

# LOG
write_to_console = True
log_level = log.INFO

# PASSWORD
attempts = 2
default_password_size = 16
default_character = "-"

letters_lower = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
letter_upper = [c.upper() for c in letters_lower]
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
signs = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '\\', '|', "{", "}", ";", ":", "<", ">", "?", "'"]

characters = letters_lower

# TREAD POOL EXECUTOR
use_thread_pool = True
max_of_threads = 2  # plus one is for 0 size

# sleep time before sending a request to the server
sleep_time = 0
