import logging as log
import string
from threading import Lock

mutex = Lock()

password = ""

# FILE
result_path = "./results"

# LOG
use_logger = True
write_to_console = True
log_level = log.INFO

# PASSWORD
password_size_attempt = 3
attempts = 1
default_password_size = 32
default_character = "-"

letters_lower = list(string.ascii_lowercase)
letter_upper = list(string.ascii_uppercase)
numbers = list(string.digits)
signs = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '\\', '|', "{", "}", ";", ":", "<", ">", "?", "'"]

characters = letters_lower

# TREAD POOL EXECUTOR
use_thread_pool = False
max_of_threads = 1  # plus one is for 0 size

# sleep time before sending a request to the server
# sleep_time = 0.1
sleep_time = 0

# T-test
alpha = 0.05
