import http.client
import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from selenium.webdriver.remote.command import Command
import yaml
import socket
import allure
from attrdict import AttrDict
import random

TEST_CONFIG = None
chrome_options = Options()


def save_screenshot(context):
    allure.attach(context.driver.browser.get_screenshot_as_png(),
                  name='screenshot',
                  attachment_type=allure.attachment_type.PNG)


def get_test_config():
    global TEST_CONFIG
    if TEST_CONFIG is None:
        raise AssertionError("Attempting to access config before loaded")
    return TEST_CONFIG


def set_test_config(test_data):
    global TEST_CONFIG
    TEST_CONFIG = test_data


def start_testing(context):
    """
    Initialise variable
    :param context:
    :return:
    """

    """
        Create all the globally available context values.
        These values are always available even after the completion of a scenario has reset the context.
        Having one complete list makes it easier to explain to a new test developer
    """

    context.gi_for_reporting = list()
    context.report_for_features = list()
    context.report_for_scenarios = list()
    context.pages = AttrDict
    context.driver = AttrDict


def setup_python_path():
    # -- NEEDED-FOR: formatter.user_defined.feature
    import os
    PYTHONPATH = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = "." + os.pathsep + PYTHONPATH


def load_config_file_yaml(file_name):
    if os.path.exists(file_name) is False:
        AssertionError("Config file '{}' not found".format(file_name))
    with open(file_name) as setting:
        yaml_data = AttrDict(yaml.safe_load(setting))
    return yaml_data


def get_browser_status(context):
    try:
        context.driver.browser.execute(Command.STATUS)
        return True
    except (socket.error, http.client.CannotSendRequest, AttributeError):
        return False


def init_web_pages(context, browser="chrome"):
    if get_browser_status(context) is False:
        launch_browser(context, browser=browser)


def get_data_for_first_test():
    context_env = get_test_config()
    data = context_env['first_test']
    return data


def launch_browser(context, browser):
    if browser == "chrome":
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--headless')
        path_to_repo = os.getcwd()
        system = platform.system()

        if system == "Darwin":
            system_folder = "mac64"
        else:
            system_folder = "linux"
            chrome_options.add_argument('--headless')
        context.driver.browser = webdriver.Chrome(
            executable_path=path_to_repo + '/webdriver/' + system_folder + '/chromedriver',
            chrome_options=chrome_options)

    #DOCKER
    # desiredCapabilities = {
    #     "browserName": "chrome",
    #     "version": "83.0",
    #     "enableVNC": True,
    #     "enableVideo": False
    # }
    # chromeOptionsRemote = webdriver.ChromeOptions()
    # chromeOptionsRemote.add_argument('--window-size=1920,1080')
    # chromeOptionsRemote.add_argument('--start-maximized')
    # chromeOptionsRemote.add_argument('--enableVNC')
    # chromeOptionsRemote.add_argument("--disable-session-crashed-bubble")
    # context.driver.browser = webdriver.Remote(options=chromeOptionsRemote, command_executor='http://localhost'
    #                                                                                         ':4444/wd/hub',
    #                                           desired_capabilities=desiredCapabilities)
