# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

# Указываем полный путь к geckodriver.exe на вашем ПК.
# driver = webdriver.Firefox('e:\\1\\geckodriver.exe')
# driver.get("http://www.google.com")
import unittest

class test_league(unittest.TestCase):

    def setUp(self):
        self.wd = WebDriver()
        self.wd.implicitly_wait(5)

    def login(self):
        # login
        pass

    def logout(self):
        pass

    def test_test_league(self):
        wd = self.wd
        wd.get('https://www.myscore.com.ua')
        # self.login(self)

    def open_page(self):
        # open home page or league page
        pass

    def tearDown(self):
        self.wd.quit()


if __name__ == '__main__':
    unittest.main()



