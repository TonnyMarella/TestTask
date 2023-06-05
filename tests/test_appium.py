from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
import pytest
from dotenv import load_dotenv

from utils import scroll, count_screen, check_element
from logger import set_file_logger

import re
import os

load_dotenv()
logger = set_file_logger("./logs/log_tests.log")


@pytest.mark.parametrize("application", [
    'Тривога!',
    'Дія'
])
def test_find_application(fixture_setup: webdriver.Remote, application) -> None:
    """
    Тест для пошуку додатку додатків
    """
    logger.info(f"Test find '{application}' starting....")
    driver = fixture_setup
    scroll.scroll_to_unlock(driver=driver)
    number_of_screen = count_screen.get_number_of_screen(driver=driver)
    app = check_element.check_element_exists(driver=driver, number_of_screen=number_of_screen,
                                             accessibility_id=application)
    if not app:
        logger.error(f"Application '{application}' not found!")
        pytest.fail(f"Application '{application}' not found!")
    logger.info(f"Test find '{application}' completed successfully")
    assert True


def test_check_telegram_number(fixture_setup: webdriver.Remote) -> None:
    """
    Тест який шукає додаток "Telegram" заходить в нього відкріває наш профіль і перевіряє номер телефону
    """
    logger.info("Test check 'Telegram' number starting....")
    driver = fixture_setup
    scroll.scroll_to_unlock(driver=driver)
    number_of_screen = count_screen.get_number_of_screen(driver=driver)
    telegram = check_element.check_element_exists(driver=driver, number_of_screen=number_of_screen,
                                                  accessibility_id='Telegram')
    if not telegram:
        logger.error("Test check 'Telegram' number error")
        pytest.fail('Telegram not found!')
    telegram.click()

    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Відкрити меню навігації"]'))).click()
    logger.info("'Telegram' was opened")
    wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, 'androidx.recyclerview.widget.RecyclerView')))

    text_elements = wait.until(
        EC.presence_of_all_elements_located((AppiumBy.CLASS_NAME, 'android.widget.TextView')))
    phone = ''

    for i in text_elements:
        try:
            text = i.text
            if text.startswith("+"):
                phone = text
                logger.info("Number was found!")
                break
        except Exception:
            continue
    result = re.sub(r'\s+|[()]', '', phone)
    assert result == os.getenv('PHONE')
    if result == os.getenv('PHONE'):
        logger.info("Test check 'Telegram' number completed successfully ")
    else:
        logger.error("Test check 'Telegram' number was completed unsuccessfully")
