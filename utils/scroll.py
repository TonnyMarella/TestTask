from appium import webdriver


def scroll_to_unlock(driver: webdriver.Remote) -> None:
    """
    Свайпає з низу у верх для роблокування телефону
    """
    screen_size = driver.get_window_size()
    start_x = int(screen_size["width"] / 2)
    start_y = int(screen_size["height"] * 0.8)
    end_x = int(screen_size["width"] / 2)
    end_y = int(screen_size["height"] * 0.2)
    driver.swipe(start_x, start_y, end_x, end_y)


def scroll_to_next_screen(driver: webdriver.Remote) -> None:
    """
    Свайпає з ліва вправо для переміщення між "робочими столами"
    """
    screen_size = driver.get_window_size()
    start_x = screen_size['width'] * 0.8
    end_x = screen_size['width'] * 0.2
    y = screen_size['height'] * 0.5
    driver.swipe(start_x, y, end_x, y)
