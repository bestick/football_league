# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.firefox.webelement import FirefoxWebElement
# from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import unittest
import time


class test_league(unittest.TestCase):

    def setUp(self):
        self.wd = WebDriver()
        # self.we = FirefoxWebElement()
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

        # zzcc = wd.find_element_by_class_name('fs-table tournament-page')
        # lll = zzcc.get_attribute('innerHTML')
        # print('len zzcc:', len(zzcc))


        tables = wd.find_elements_by_class_name('soccer')
        # lll = tables[0].get_attribute('innerHTML')
        print('len tables:', len(tables))

        season = []
        for ij in range(1,len(tables)):
            tbody = tables[ij].find_element_by_tag_name('tbody')
            # lll = tbody.get_attribute('innerHTML')
            # print('xxxx======', lll)
            season.append(self.tour_data(tbody))
        print(season[0])
        print(season[1])


    def test_match(self):

        wd = self.wd
        # we = self.we
        zzz = {'Финал': [{'id': 'g_1_2iFXsPBF', 'tour': 'Финал', 'time': '20.05. 21:00', 'home': 'Анжи', 'away': 'Енисей ', 'score': '4 : 3', 'url': 'https://www.myscore.com.ua/match/2iFXsPBF/#match-summary'}, {'id': 'g_1_UDoUtqRL', 'tour': 'Финал', 'time': '20.05. 18:00', 'home': 'Тамбов', 'away': 'Амкар ', 'score': '0 : 1', 'url': 'https://www.myscore.com.ua/match/UDoUtqRL/#match-summary'}, {'id': 'g_1_O0GTr5d9', 'tour': 'Финал', 'time': '17.05. 17:30', 'home': 'Амкар', 'away': 'Тамбов', 'score': '2 : 0', 'url': 'https://www.myscore.com.ua/match/O0GTr5d9/#match-summary'}, {'id': 'g_1_UwHPqos3', 'tour': 'Финал', 'time': '17.05. 15:00', 'home': 'Енисей', 'away': 'Анжи', 'score': '3 : 0', 'url': 'https://www.myscore.com.ua/match/UwHPqos3/#match-summary'}]}
        url = zzz['Финал'][1]['url']
        self.open_page(url)
        time.sleep(2)
        info = wd.find_elements_by_class_name('detailMS')
        # info = wd.find_elements_by_tag_name('div')
        len_info = len(info)
        ttt = info[0].get_attribute('innerHTML')
        print('len_info', len_info)
        print('info: ==',  info)
        print('ttt: ==',  ttt)

        # print('kkk:==', kkk)


    def tour_data(self, tbody):
        tours = {}
        tr_s = tbody.find_elements_by_tag_name('tr')
        for ij in range(len(tr_s)):
            class_name = tr_s[ij].get_attribute('class')

            if class_name[-14:] == 'stage-finished':
                if round_name not in tours:
                    tours[round_name] = []
                tours[round_name].append(self.match_data(tr_s[ij], round_name))
            elif class_name == 'event_round':
                round_name = tr_s[ij].text

                print(' ')
                print('-----------------------')
                print('event_round:== ', round_name)
            else:
                print('Паршивая ситуация')

        return tours

    def match_data(self, tr, name):

        print('')
        print('===========')
        print('Имя класса tr:', tr.get_attribute('class'))
        print('Тур:', name)
        id = tr.get_attribute('id')
        print('id матча:', id)
        td_s = tr.find_elements_by_tag_name('td')
        start_time = td_s[1].text
        home = td_s[2].find_element_by_tag_name('span').text
        away = td_s[3].find_element_by_tag_name('span').text
        score = td_s[4].text
        url = 'https://www.myscore.com.ua/match/' + id[4:] + '/#match-summary'

        internals = {}
        internals['id'] = id
        internals['tour'] = name
        internals['time'] = start_time
        internals['home'] = home
        internals['away'] = away
        internals['score'] = score
        internals['url'] = url
        # match = {id: internals}

        print('Начало в:', start_time)
        print('Team home:', home)
        print('Team away:', away)
        print('Счет:', score)
        # https: // www.myscore.com.ua / match / 0jHHqppJ /  # match-summary
        print('Url на матч:', url)
        # if id[4:] == '0jHHqppJ':
        #     self.open_page('https://www.myscore.com.ua/football/russia/premier-league-2016-2017')
        # return match
        return internals


    def open_page(self, url):
        wd = self.wd
        wd.get(url)

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()



