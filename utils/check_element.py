from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException
from appium import webdriver

from typing import Union

from .scroll import scroll_to_next_screen


def check_element_exists(driver: webdriver.Remote, number_of_screen: int, accessibility_id: str) -> \
        Union[bool, webdriver.WebElement]:
    """
    Функція проходить по робочому столу і шукає додаток якій нам потрібен
    """
    element = False
    for i in range(0, number_of_screen):
        try:
            element = driver.find_element(AppiumBy.ACCESSIBILITY_ID, accessibility_id)
            break
        except NoSuchElementException:
            scroll_to_next_screen(driver=driver)
            continue
    return element
