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
        self.ids = []

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
            time.sleep(1)

        # zzcc = wd.find_element_by_id('fs - results')
        tables = wd.find_elements_by_class_name('soccer')
        print('len tables:', len(tables))

        for ij in range(1,len(tables)):
            tbody = tables[ij].find_element_by_tag_name('tbody')
            # lll = tbody.get_attribute('innerHTML')
            # print('xxxx======', lll)

            self.tour_data(tbody)

        # self.open_page('https://www.myscore.com.ua/match/UDoUtqRL/#match-summary')
        # time.sleep(3)

    def tour_data(self, tbody):
        tr_s = tbody.find_elements_by_tag_name('tr')
        for ij in range(len(tr_s)):
            class_name = tr_s[ij].get_attribute('class')

            if class_name[-14:] == 'stage-finished':
                self.match_data(tr_s[ij])
            elif class_name == 'event_round':
                print(' ')
                print('-----------------------')
                print('event_round')
            else:
                print('Паршивая ситуация')

    def match_data(self, tr):
        print('')
        print('===========')
        print('Имя класса tr:', tr.get_attribute('class'))
        id = tr.get_attribute('id')
        print('id матча:', id)
        td_s = tr.find_elements_by_tag_name('td')

        print('Начало в:', td_s[1].text)
        print('Team home:', td_s[2].find_element_by_tag_name('span').text)
        print('Team away:', td_s[3].find_element_by_tag_name('span').text)
        print('Счет: ', td_s[4].text)
        print('Url на матч: ', id[4:])

    def open_page(self, url):
        wd = self.wd
        wd.get(url)

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()



