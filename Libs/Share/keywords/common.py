import re
import statistics
from datetime import datetime
from typing import List, Dict, Any
import time
import os
import platform
from pathlib import Path
from datetime import datetime
from SeleniumLibrary.base import keyword, LibraryComponent
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from os.path import join
from dotenv import load_dotenv
from dotenv import dotenv_values
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


class Common(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def load_env(self):
        current_path = self.get_core_path()
        dotenv_path = join(current_path, '.env')
        load_dotenv(dotenv_path)
        config = dotenv_values(dotenv_path)
        env_name = []
        result = {}
        for i in config.keys():
            env_name.append(i)
        list(map(lambda name: result.update({name.lower(): os.environ.get(name)}), env_name))
        return result

    @keyword
    def get_core_path(self):
        current_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.dirname(os.path.dirname(os.path.join("..", current_path)))

    @keyword
    def get_current_os(self):
        return platform.system()

    @keyword
    def enable_download_in_headless_chrome(self, driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = (
            "POST", '/session/' + str(driver.session_id) + '/chromium/send_command')
        print("session_id:", str(driver.session_id))
        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

    @keyword
    def start_browser(self):
        if BuiltIn().get_variable_value('${BROWSER}').lower() == 'chrome':
            driver = self.handle_chrome_browser()
        else:
            driver = self.handle_firefox_browser()
        driver.maximize_window()
        driver.get(BuiltIn().get_variable_value('${BASE_URL}').lower())
        self.debug('Opened browser with session id %s.' % driver.session_id)
        ad_domains = [
            "*doubleclick.net/*",
            "*googlesyndication.com/*",
            "*googleads.g.doubleclick.net/*",
            "*adservice.google.com/*",
            "*adservice.google.*/*",
            "*amazon-adsystem.com/*",
            "*ads.pubmatic.com/*",
            "*adnxs.com/*",
            "*taboola.com/*",
            "*outbrain.com/*",
            "*scorecardresearch.com/*"
        ]

        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ad_domains})
        return self.ctx.register_driver(driver, alias=None)

    def handle_chrome_browser(self):
        curr_path = self.get_core_path()
        # chrome_download_location = BuiltIn().get_variable_value('DOWNLOAD_DIR')
        windows_chrome_driver_path = curr_path + str(Path('/Drivers/chromedriver.exe'))
        linux_chrome_driver_path = curr_path + str(Path('/Drivers/chromedriver'))
        options = ChromeOptions()
        if BuiltIn().get_variable_value('${HEADLESS}').lower() == 'true':
            options.add_argument("headless")
        else:
            options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--blink-settings=imagesEnabled=false")
        prefs = {
            "profile.default_content_setting_values.notifications": 1,
            "profile.managed_default_content_settings.images": 2,
            "profile.managed_default_content_settings.javascript": 1,
            "profile.managed_default_content_settings.ads": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.managed_default_content_settings.autoplay": 2,
        }
        options.add_experimental_option("prefs", prefs)
        if self.get_current_os().lower() == 'windows':
            driver = webdriver.Chrome(options=options,
                                      executable_path=windows_chrome_driver_path)
        else:
            driver = webdriver.Chrome(options=options, executable_path=linux_chrome_driver_path)
        # if BuiltIn().get_variable_value('HEADLESS').lower() == 'true':
        #     self.enable_download_in_headless_chrome(driver, chrome_download_location)
        return driver

    def handle_firefox_browser(self):
        curr_path = self.get_core_path()
        # firefox_download_location = BuiltIn().get_variable_value('DOWNLOAD_DIR')
        windows_firefox_driver_path = curr_path + str(Path('/Drivers/geckodriver.exe'))
        linux_firefox_driver_path = curr_path + str(Path('/Drivers/geckodriver'))
        options = FirefoxOptions()
        if BuiltIn().get_variable_value('${HEADLESS}').lower() == 'true':
            options.headless = True
        else:
            options.headless = False
        options.set_preference('pdfjs.previousHandler.alwaysAskBeforeHandling', False)
        options.set_preference('browser.download.folderList', 2)
        # options.set_preference('browser.download.dir', firefox_download_location)
        options.set_preference('browser.download.panel.shown', False)
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/csv," + "text/csv," +
                               "application/x-msexcel,application/excel," +
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document," +
                               "application/x-excel,application/vnd.ms-excel" +
                               "application / xml")
        if self.get_current_os().lower() == 'windows':
            driver = webdriver.Firefox(capabilities=None, options=options,
                                       executable_path=windows_firefox_driver_path)

        else:
            driver = webdriver.Firefox(capabilities=None, options=options,
                                       executable_path=linux_firefox_driver_path)
        return driver

    @keyword
    def wait_until_element_is_visible(self, locator, default_timeout=None):
        global_timeout = float(BuiltIn().get_variable_value('${TIMEOUT}'))
        if default_timeout is not None:
            expected_timeout = time.time() + float(default_timeout)
        else:
            expected_timeout = time.time() + global_timeout
        while True:
            if time.time() > expected_timeout:
                mess = f"Element {locator} not visible after {expected_timeout} second"
                raise AssertionError(mess)
            if self.is_visible(locator) is not None:
                return True

    @keyword
    def wait_until_element_is_enabled(self, locator, default_timeout=None):
        global_timeout = float(BuiltIn().get_variable_value('${TIMEOUT}'))
        if default_timeout is not None:
            expected_timeout = time.time() + float(default_timeout)
        else:
            expected_timeout = time.time() + global_timeout
        while True:
            if time.time() > expected_timeout:
                mess = f"Element {locator} not enabled after {expected_timeout} second"
                raise AssertionError(mess)
            if self.is_element_enabled(locator):
                return True

    @keyword
    def is_element_visible_in_time(self, locator, default_timeout=None):
        global_timeout = float(BuiltIn().get_variable_value('${TIMEOUT}'))
        if default_timeout is not None:
            expected_timeout = time.time() + float(default_timeout)
        else:
            expected_timeout = time.time() + global_timeout
        while True:
            if time.time() > expected_timeout:
                return False
            if self.is_visible(locator):
                return True

    @keyword
    def select_dropdown_list_value(self, locator, text):
        dropdown_list = self.find_element(locator)
        options = dropdown_list.find_elements(by=By.TAG_NAME, value='option')
        for option in options:
            if option.get_attribute('textContent').lower().strip() == text.lower():
                return option.click()
        message = f"{text} not found"
        raise AssertionError(message)

    @keyword
    def wait_cards_ready(self, locator, timeout=30):
        driver = self.ctx.driver
        cards = driver.find_elements(By.CSS_SELECTOR, locator)
        if not cards:
            raise AssertionError("No wrapper cards found")
        for idx, card in enumerate(cards):
            WebDriverWait(driver, timeout).until(
                lambda d, c=card: c.value_of_css_property("opacity") == "1"
            )
            WebDriverWait(driver, timeout).until(
                lambda d, c=card: c.value_of_css_property("transform") in ["none", "matrix(1, 0, 0, 1, 0, 0)"]
            )
            self._wait_for_stable_height(card, timeout)

    def _wait_for_stable_height(self, element, timeout=10):
        start = time.time()
        last_height = None

        while time.time() - start < timeout:
            height = element.size["height"]
            if height == last_height:
                return True
            last_height = height
            time.sleep(0.20)

        raise Exception("Card height still changing → animation not complete")

    @keyword
    def extract_temperature_value(self, temp_string):
        match = re.search(r'(-?\d+)', temp_string)
        if match:
            return float(match.group(1))
        raise ValueError(f"Could not extract temperature from: {temp_string}")

    @keyword
    def convert_fahrenheit_to_celsius(self, fahrenheit):
        celsius = (float(fahrenheit) - 32) * 5 / 9
        return round(celsius, 1)

    @keyword
    def create_weather_report_file(self, weather_data):
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        file_path = str(Path(self.get_core_path() + "/Generated_Report"))
        file = file_path + f"/auto_weather_report_{timestamp}.txt"
        with open(file, 'w') as f:
            f.write(f"Weather Report Generated: {timestamp}\n")
            f.write("=" * 50 + "\n\n")
            for i, day in enumerate(weather_data, 1):
                f.write(f"Day {i}: {day.get('day_value', 'N/A')}\n")
                f.write(f"  Temperature (Fahrenheit): {day.get('temperature', 'N/A')}\n")
                # Add Celsius conversion if available
                if 'temperature_celsius' in day:
                    f.write(f"  Temperature (Celsius): {day['temperature_celsius']}\n")
                f.write(f"  Weather Description: {day.get('weather_description', 'N/A')}\n")
                f.write(f"  Real Feel: {day.get('real_feel', 'N/A')}\n")
                f.write(f"  Humidity: {day.get('humidity', 'N/A')}\n")
                f.write("-" * 30 + "\n")
            # Add summary
            f.write(f"\nSummary:\n")
            f.write(f"Total Days: {len(weather_data)}\n")

    @keyword
    def create_weather_summary(self, weather_data):
        if not weather_data:
            return "No weather data available"
        total_days = len(weather_data)
        conditions = {}
        for day in weather_data:
            condition = day.get('weather_description', 'Unknown')
            conditions[condition] = conditions.get(condition, 0) + 1
        most_common = max(conditions.items(), key=lambda x: x[1])
        summary = f"Analyzed {total_days} days. "
        summary += f"Most common condition: {most_common[0]} ({most_common[1]} days)"
        return summary
