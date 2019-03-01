# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
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
        import requests
        from bs4 import BeautifulSoup
        url = 'https://www.myscore.com.ua/match/8rkygV3B/#match-summary'
        # r = requests.get(url).text

        # div = soup.find('div', class_ = 'detailMS')
        # print('zzz :==', soup)
        wd = self.wd
        # we = self.we
        # zzz = {'Финал': [{'id': 'g_1_2iFXsPBF', 'tour': 'Финал', 'time': '20.05. 21:00', 'home': 'Анжи', 'away': 'Енисей ', 'score': '4 : 3', 'url': 'https://www.myscore.com.ua/match/2iFXsPBF/#match-summary'}, {'id': 'g_1_UDoUtqRL', 'tour': 'Финал', 'time': '20.05. 18:00', 'home': 'Тамбов', 'away': 'Амкар ', 'score': '0 : 1', 'url': 'https://www.myscore.com.ua/match/UDoUtqRL/#match-summary'}, {'id': 'g_1_O0GTr5d9', 'tour': 'Финал', 'time': '17.05. 17:30', 'home': 'Амкар', 'away': 'Тамбов', 'score': '2 : 0', 'url': 'https://www.myscore.com.ua/match/O0GTr5d9/#match-summary'}, {'id': 'g_1_UwHPqos3', 'tour': 'Финал', 'time': '17.05. 15:00', 'home': 'Енисей', 'away': 'Анжи', 'score': '3 : 0', 'url': 'https://www.myscore.com.ua/match/UwHPqos3/#match-summary'}]}
        # url = zzz['Финал'][0]['url']
        self.open_page(url)
        time.sleep(2)
        # r = wd.find_element_by_id('detailMS')
        r = wd.find_elements_by_id('summary-content')
        print('type(r)', type(r), 'len(r)', len(r))

        ttt = r[0].get_attribute('innerHTML')
        wd.close()
        # print('ttt:== ', ttt)
        #
        divs = BeautifulSoup(ttt, 'lxml').find_all('div')
        len_divs = len(divs)
        print( 'type(divs)', type(divs), 'len(divs)', len_divs, 'dir(divs)', dir(divs))
        name_class = divs[1].get('class')
        print('1:==', name_class)
        for ij in range(len_divs - 1, 0, -1):

            name_class = divs[ij].get('class')
            print(ij, name_class)
        cnt = 0
        for ij in range(len_divs - 1, 0, -1):
            name_class = divs[ij].get('class')
            if name_class == None:
                print(ij, 'ura!!!')
            elif type(name_class) == list and len(name_class) == 1:
                print(ij, 'list!!!')
            elif type(name_class) == list and len(name_class) > 1 and name_class[0][:18] == 'detailMS__incident':
                cnt = cnt + 1
                print(ij, name_class, cnt)
            else:
                print(ij, '=======Паршиво!!!')

        zzz = divs[66].get('class')
        print('type(zzz)', type(zzz), zzz, 'len(zzz)', len(zzz))



        #     try:
        #         name_class = divs[ij].get('class')
        #         print(name_class)
        #         if type(name_class) != list or name_class[0][:18] == 'detailMS__incident':
        #             del divs[ij]
        #     except:
        #         del divs[ij]
        # print('len(divs)', len(divs))

        # info = wd.find_elements_by_class_name('stage-12')

        # len_info = len(info)
        # print('len_info', len_info)
        # ttt = info[0].get_attribute('innerHTML')
        #
        # print('info: ==', info)

        # soup = BeautifulSoup(ttt, 'html.parser')
        # p1_away = soup.find('span', class_= 'p1_away')
        # p2_away = soup.find('span', class_= 'p2_away')
        # print('p1_away: ==', p1_away.text, 'p2_away: ==', p2_away.text)
        #
        # div = soup.find('div')
        # print('Type div:== ', 'div=', div)

        # kkk = ttt.find_elements_by_class_name('detailMS__incidentsHeader stage-12')
        #
        # print('kkk:==', kkk)
        # body_html = wd.find_element_by_xpath("/html/body")
        # body_html = wd.page_source
        # ddd = body_html.find_elements_by_class_name('detailMS')
        # print(ddd)

        # print('body_html <==', body_html)




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



