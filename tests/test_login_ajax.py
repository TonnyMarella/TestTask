from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from dotenv import load_dotenv

from utils import scroll, ajax_app
from logger import set_file_logger

import pytest

import os

load_dotenv()

logger = set_file_logger("./logs/log_tests.log")


@pytest.mark.parametrize("email, password", [
    (os.getenv('EMAIL'), os.getenv('PASSWORD')),
    ('fake_email@gmail.com', 'fake_password'),
    (os.getenv('EMAIL'), 'fake_password'),
    ('fake_email@gmail.com', os.getenv('PASSWORD'))
])
def test_login_ajax(fixture_setup: webdriver.Remote, email: str, password: str) -> None:
    """
    Тест який входить в 'Ajax' і намагається увійти в аккаунт є тест з правильними данними і з неправильними
    """
    logger.info("Test 'Ajax' login starting....")
    driver = fixture_setup
    scroll.scroll_to_unlock(driver=driver)
    ajax_app.open_ajax(driver=driver)

    ajax_app.login_ajax(driver=driver, email_for_login=email, password_for_login=password)

    login = False
    logger.info("Test ajax 'Ajax', starting check if we logging")
    try:
        wait = WebDriverWait(driver, 5)
        add_hub = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.ajaxsystems:id/hubAdd')))
        if add_hub:
            login = True
    except TimeoutException:
        pass

    if email == os.getenv('EMAIL') and password == os.getenv('PASSWORD'):
        if not login:
            logger.error("Test 'Ajax' we are not login, with correct data, test failed!")
            pytest.fail("Test 'Ajax' we are not login, with correct data, test failed!")

        logger.info("Test 'Ajax' we are login, with correct data, test successful!")
        assert login is True
        ajax_app.logout_from_ajax(driver=driver)
    else:
        if login:
            logger.error("Test 'Ajax' we are login, with wrong data, test failed!")
            ajax_app.logout_from_ajax(driver=driver)
            pytest.fail("Test 'Ajax' we are login, with wrong data, test failed!")

        logger.info("Test 'Ajax' we are not login, with wrong data, test successful!")
        assert login is False
