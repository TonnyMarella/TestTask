from appium import webdriver
from typing import Union

from logger import set_file_logger
from dotenv import load_dotenv

import pytest
import subprocess

import os

load_dotenv()

logger = set_file_logger("./logs/log_tests.log")


@pytest.fixture(scope='function')
def fixture_setup(fixture_find_udid: str) -> webdriver:
    """
    Фікстура яка створює підключення до телефону за допомогою Appium, для кожного тесту створюється нове підключення,
    після виконання тесту телефон блокується і виходимо з підключення
    """
    if not fixture_find_udid:
        logger.error("udid not found")
        pytest.skip('udid not found')

    desired_caps = {
        "platformName": os.getenv('PLATFORM_NAME'),
        "appium:platformVersion": os.getenv('PLATFORM_VERSION'),
        "appium:deviceName": os.getenv('DEVICE_NAME'),
        "appium:appPackage": os.getenv('APP_PACKAGE'),
        "appium:appActivity": os.getenv('APP_ACTIVITY'),
        "appium:automationName": os.getenv('AUTOMATION_NAME'),
        "appium:udid": fixture_find_udid
    }

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    driver.implicitly_wait(10)
    logger.info("Driver created")
    yield driver
    driver.lock()
    driver.quit()
    logger.info("Driver closed")


@pytest.fixture(scope='session')
def fixture_find_udid() -> Union[bool, str]:
    """
    Фікстура яка шукає udid телефону через subprocess
    """
    adb_command = ['adb', 'devices']
    udid = None
    process = subprocess.Popen(adb_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()

    if process.returncode == 0:
        for line in output.strip().split('\n'):
            if 'List of devices attached' not in line and line.strip() != '':
                device_info = line.strip().split('\t')
                if 'device' in device_info:
                    return device_info[0]
    return False
