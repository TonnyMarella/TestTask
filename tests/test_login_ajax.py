from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver

from utils import scroll, ajax_app
from logger import set_file_logger

import os

logger = set_file_logger("./logs/log_tests.log")


def test_successful_login_ajax(fixture_setup: webdriver.Remote) -> None:
    """
    Тест який входить в 'Ajax' успішно логіниться та перевіряє sidebar
    """
    logger.info("Test 'Ajax' starting....")
    driver = fixture_setup
    scroll.scroll_to_unlock(driver=driver)
    ajax_app.open_ajax(driver=driver)

    ajax_app.login_ajax(driver=driver, email_for_login=os.getenv('EMAIL'), password_for_login=os.getenv('PASSWORD'))

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, 'com.ajaxsystems:id/menuDrawer'))).click()

    sidebar_elements = {
        'addHub': 'Додати хаб',
        'settings': 'Налаштування застосунку',
        'help': 'Допомога',
        'logs': 'Повідомити про проблему',
        'camera': 'Відеоспостереження'
    }
    logger.info("Test ajax 'Ajax', start checking sidebar")
    for sidebar_id, sidebar_name in sidebar_elements.items():
        element = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, f'com.ajaxsystems:id/{sidebar_id}')))
        element_text = element.find_element(AppiumBy.CLASS_NAME, 'android.widget.TextView').text
        assert sidebar_name == element_text

    logger.info("Test 'Ajax' finished successful, start logout...")
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, 'com.ajaxsystems:id/settings'))).click()
    wait.until(EC.presence_of_element_located(
        (AppiumBy.ID, 'com.ajaxsystems:id/accountInfoLogoutNavigate'))).click()


def test_fail_login_ajax(fixture_setup: webdriver.Remote) -> None:
    """
    Тест який входить в 'Ajax' і намагається увійти в аккаунт з неправильними данними
    """
    logger.info("Test 'Ajax' starting....")
    driver = fixture_setup
    scroll.scroll_to_unlock(driver=driver)
    ajax_app.open_ajax(driver=driver)

    ajax_app.login_ajax(driver=driver, email_for_login='test@gmail.com', password_for_login='fakepasswod')

    login = False
    logger.info("Test ajax 'Ajax', starting check failed logging")
    try:
        wait = WebDriverWait(driver, 5)
        add_hub = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.ajaxsystems:id/hubAdd')))
        if add_hub:
            logger.info("Test 'Ajax' we are login, test failed")
            login = True
    except TimeoutException:
        pass
    assert login is False
    logger.info("Test ajax 'Ajax', we are not logged in, the test was successful")
