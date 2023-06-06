from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver

from utils import scroll, ajax_app
from logger import set_file_logger

import os

logger = set_file_logger("./logs/log_tests.log")


def test_ajax_sidebar(fixture_setup: webdriver.Remote) -> None:
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
    logger.info("Test 'Ajax', start checking sidebar")
    for sidebar_id, sidebar_name in sidebar_elements.items():
        element = wait.until(EC.presence_of_element_located(
            (AppiumBy.ID, f'com.ajaxsystems:id/{sidebar_id}')))
        element_text = element.find_element(AppiumBy.CLASS_NAME, 'android.widget.TextView').text
        assert sidebar_name == element_text
    ajax_app.logout_from_ajax(driver=driver, in_sidebar=True)
