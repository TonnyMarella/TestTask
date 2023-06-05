from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver


def get_number_of_screen(driver: webdriver.Remote) -> int:
    """
    Повертає кількість "робочих столів"
    """
    current_screen = driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.ScrollView')
    count_screen = int(current_screen.get_attribute('content-desc').split()[-1])
    return count_screen
