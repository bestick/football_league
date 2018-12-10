# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import unittest

import time


class test_league(unittest.TestCase):

    def setUp(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(5)

    def login(self):
        # login
        pass

    def logout(self):
        pass

    def is_link_text_present(self):
        wd = self.wd
        try:
            wd.find_element_by_link_text('Показать больше матчей').click()
            return True
        except NoSuchElementException:
            return False


    def test_league(self):
        wd = self.wd
        self.open_page('https://www.myscore.com.ua/football/russia/premier-league-2017-2018')
        while self.is_link_text_present():
            time.sleep(2)

    def open_page(self, url):
        wd = self.wd
        wd.get(url)

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()



