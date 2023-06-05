import pytest

from .count_screen import get_number_of_screen
from .check_element import check_element_exists
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver

from logger import set_file_logger

logger = set_file_logger("./logs/log_tests.log")


def open_ajax(driver: webdriver.Remote) -> None:
    """
    Функція яка шукає 'Gspace', в ньому знаходить 'Ajax' і відкриває його
    """
    try:
        number_of_screen = get_number_of_screen(driver=driver)
        gspace = check_element_exists(driver=driver, number_of_screen=number_of_screen,
                                      accessibility_id='Gspace')
        if not gspace:
            logger.error("Test ajax 'Gspace' not found!")
            pytest.fail('Gspace not found!')
        gspace.click()
        wait = WebDriverWait(driver, 30)
        ajax = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.'
                             'FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
                             'androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/'
                             'android.widget.LinearLayout/android.widget.RelativeLayout[2]/'
                             'android.widget.GridView/android.widget.LinearLayout[2]')))
        ajax.click()
        logger.info("Test ajax 'Ajax' opened")
    except Exception as e:
        pytest.fail(f"Test 'Ajax' some problem with open 'Ajax', error: \n {e}")


def login_ajax(driver: webdriver.Remote, email_for_login: str, password_for_login: str) -> None:
    """
    Функція отримує данні для входу і виконує вхід в аккаунт 'Ajax'
    """
    try:
        logger.info("Test ajax 'Ajax', start logging")
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, 'com.ajaxsystems:id/compose_view'))).click()
        wait = WebDriverWait(driver, 10)
        email = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, 'com.ajaxsystems:id/compose_view')))
        email.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText').clear().send_keys(email_for_login)
        password = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, 'com.ajaxsystems:id/authLoginPassword')))
        password.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText').clear().send_keys(password_for_login)

        enter = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, 'com.ajaxsystems:id/bottomContent')))
        enter.find_element(AppiumBy.CLASS_NAME, 'android.view.View').click()
    except Exception as e:
        pytest.fail(f"Test 'Ajax' some problem with logging, error: \n {e}")
