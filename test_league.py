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

    def is_link_text_present(self, text=None):
        wd = self.wd
        try:
            wd.find_element_by_link_text(text).click()
            return True
        except NoSuchElementException:
            return False

    def test_league(self):
        wd = self.wd
        self.open_page('https://www.myscore.com.ua/football/russia/premier-league-2017-2018')
        while self.is_link_text_present('Показать больше матчей'):
            time.sleep(2)

        zzz = wd.find_element_by_class_name('soccer').find_element_by_tag_name('tbody').find_element_by_tag_name('tr')

        if zzz.find_element_by_class_name('event_round'):
            self.save_f(zzz.text)
        else:
            


        # class ="event_round" > < td colspan="6" > Финал < / td > < / tr >
        # zzz = zzz.find_element_by_tag_name('tr')

    def save_f(self, text):
        handle = open("output.txt", "w")
        handle.write(text)
        handle.close()



    def open_page(self, url):
        wd = self.wd
        wd.get(url)

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()



