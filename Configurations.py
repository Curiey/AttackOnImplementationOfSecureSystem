import string
import logging as log
from datetime import datetime


password = ""

# FILE
result_path = "./results"

# LOG
use_logger = False
write_to_console = False
log_level = log.INFO
session = None
running_folder_format = datetime.now().strftime("%m-%d-%Y---%H-%M-%S")

# PASSWORD
max_password_size_attempt = 3
attempts = 5
current_attempt = 0
default_password_size = 32
default_character = "-"

# ALPHA
default_alpha = 0.05
number_alpha = 0.05
letter_alpha = 0.05

letters_lower = list(string.ascii_lowercase)
letter_upper = list(string.ascii_uppercase)
numbers = list(string.digits)

characters = letters_lower

# TREAD POOL EXECUTOR
use_thread_pool = True
max_of_threads = 1  # plus one is for 0 size

# sleep time before sending a request to the server
sleep_time = 0

# T-test
alpha = 0.05

# configuration Dictionary
configuration_level_setup_dict = {
    1: {
        "max_password_size_attempt": 3,
        "attempts": 3,
        "use_thread_pool": False,
        "max_of_threads": 1
    },
    2: {
        "max_password_size_attempt": 3,
        "attempts": 3,
        "use_thread_pool": False,
        "max_of_threads": 1
    },
    3: {
        "max_password_size_attempt": 5,
        "attempts": 7,
        "use_thread_pool": False,
        "max_of_threads": 10
    },
    4: {
        "max_password_size_attempt": 5,
        "attempts": 10,
        "use_thread_pool": False,
        "max_of_threads": 10
    },
    5: {
        "max_password_size_attempt": 3,
        "attempts": 5,
        "use_thread_pool": False,
        "max_of_threads": 10
    },
    6: {
        "max_password_size_attempt": 3,
        "attempts": 5,
        "use_thread_pool": False,
        "max_of_threads": 10
    }
}