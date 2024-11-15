import logging

test_case_logger = logging.getLogger('test_case_logger')
test_case_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('test_cases.log', mode='a')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

test_case_logger.addHandler(file_handler)
