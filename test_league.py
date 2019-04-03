# -*- coding: utf-8 -*-
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import json
import os.path as op
from datetime import datetime


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
        url = 'https://www.myscore.com.ua/football/russia/premier-league-2016-2017'
        season = self.get_season(url)
        file = 'e:/5/rfpl 2016_17_ru.json'
        self.save_json(file, season[1])

        # for ik in range(len(season)):
        #     for key in season[ik]:
        #         w_tour = season[ik][key]
        #         for idx in range(len(w_tour)):
        #             w_fh, w_sh = self.test_match(w_tour[idx]['id'])
        #             season[ik][key][idx]['fh'], season[ik][key][idx]['sh'] = w_fh, w_sh
        #         print(season[ik])
        #
        #
        # with open('season_1.json', 'w', encoding='utf-8') as fh:  # открываем файл на запись
        #     fh.write(json.dumps(season[1], ensure_ascii=False))  # преобразовываем словарь data в unicode-строку и записываем в файл

    def get_season(self, url):
        wd = self.wd
        self.open_page(url, 2)
        # self.open_page('https://www.myscore.com.ua/football/russia/premier-league-2017-2018', 2)
        # self.open_page('https://www.myscore.com.ua/football/england/premier-league-2017-2018/', 2)
        while self.is_link_text_present('Показать больше матчей'):
            time.sleep(3)
        tables = wd.find_elements_by_class_name('soccer')
        # print('len tables:', len(tables))
        season = []
        for ij in range(1, len(tables)):
            tbody = tables[ij].find_element_by_tag_name('tbody')
            season.append(self.tour_data(tbody))
        return season

    def test_match(self, id = 'jkcJ3GaI'):
        # import requests
        from bs4 import BeautifulSoup

        fh, sh, is_fh  = [], [], True
        wd = self.wd
        # self.open_page('https://www.myscore.com.ua/match/veVP9R8C/#match-summary', 2)
        url = 'https://www.myscore.com.ua/match/' + id + '/#match-summary'
        self.open_page(url , 2)
        # self.open_page('https://www.myscore.com.ua/match/z7poAt22/#match-summary', 2)

        r = wd.find_element_by_id('summary-content').get_attribute('innerHTML')
        # wd.close()

        ##########################
        divs = BeautifulSoup(r, 'lxml').div.contents
        print('type(divs)', type(divs), 'len(divs)', len(divs))

        for ij in range(len(divs)):
            roow = self.parse_row(divs[ij])
            # print(ij, roow)

            stage = roow[0]['stage']
            if stage == '':
                if is_fh:
                    fh.append(roow[1])
                else:
                    sh.append(roow[1])

            else:
                is_fh = False if stage == '2-й тайм' else True
                if is_fh:
                    fh.append(roow[1])
                else:
                    sh.append(roow[1])
        print(fh)
        print(sh)
        return fh, sh

    def test_fill_season(self, file = 'e:/5/rfpl 2016_17_ru.json'):
        file, maxi = 'e:/5/rfpl 2016_17_ru.json', 32
        if op.isfile(file):
            season = self.open_json(file)
            now = datetime.now()
            suffi = '_' + now.strftime("%Y%m%d_%H%M") + '.json'
            self.save_json(file.replace('.json', suffi), season)
            id_list = self.select_id(season, maxi)
            print(id_list)
            for idx in range(len(id_list)):
                w_fh, w_sh = self.test_match(id_list[idx])
                season[ik][key][idx]['fh'], season[ik][key][idx]['sh'] = w_fh, w_sh

            #############################################################################################

        else:
            print('==================')

    def parse_row(self, line):
        row, inners = [], dict()
        tmp = line.get('class')
        if tmp[0] == 'detailMS__incidentRow' and tmp[1] != '--empty':
            row.append({'stage': ''})
            row.append(self.get_inners(line, tmp[1]))

        elif tmp[0] == 'detailMS__incidentsHeader':
            stage = line.div.text
            score = (line.contents)[1].find_all('span')
            score_h = score[0].text.replace('\n', '')
            score_a = score[1].text.replace('\n', '')

            row.append({'stage': stage})
            row.append({'score_h': score_h, 'score_a': score_a})
        elif tmp[0] == 'detailMS__incidentRow' and tmp[1] == '--empty':
            inners['empty odd'] = ''
            row.append({'stage': ''})
            row.append(inners)
        else:
            print('!!!  Вне ЗОНЫ ВЕРХНЕГО УРОВНЯ   !!!!!!!!!!!!!')

        return row

    def get_inners(self, line, team):
        inners = dict()
        event = ((line.contents)[1].get('class'))[1]
        inners['team'] = (team.split('--'))[1]
        inners['time_box'] = line.div.text
        inners['event'] = event
        if event in ['y-card', 'yr-card', 'r-card']:
            try:
                inners['participant'] = line.find('a').text
            except AttributeError:
                inners['participant'] = self.find_sp(line, "participant-name", False)
        elif event == 'soccer-ball':
            inners['participant'] = self.find_sp(line, "participant-name", False)
            inners['assist'] = self.find_sp(line, "assist note-name")
            inners['subincident'] = self.find_sp(line, "subincident-name")
        elif event == 'substitution-in':
            inners['substitution-in'] = self.find_sp(line, "substitution-in-name", False)
            inners['substitution-out'] = (self.find_sp(line, "substitution-out-name", False)).replace('\xa0', '')
        elif event in ['soccer-ball-own', 'penalty-missed']:
            inners['note'] = self.find_sp(line, "note-name")
            inners['participant'] = line.find('a').text
        else:
            print('!!!  Вне ЗОНЫ !!!!!!!!!!!!!')
        return inners

    def find_sp(self, line, name, isHooks = True):
        tmp = line.find('span', class_= name)
        return '' if tmp == None else tmp.text[1:-1] if isHooks else tmp.text

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

        id = tr.get_attribute('id')[4:]
        print('id матча:', id)
        td_s = tr.find_elements_by_tag_name('td')
        start_time = td_s[1].text
        home = td_s[2].find_element_by_tag_name('span').text
        away = td_s[3].find_element_by_tag_name('span').text
        score = td_s[4].text

        return {'id': id, 'tour': name, 'time': start_time, 'home': home, 'away': away, 'score': score.replace(' : ', ':')}

    def select_id(self, season, maxi):
        ij = 0
        id_list = []
        for key in season:
            for idx in range(len(season[key])):
                id_tour = season[key][idx]
                if 'fh' not in id_tour:
                    id_list.append(id_tour['id'])
                    ij = ij + 1
                if ij == maxi:
                    return id_list
        return id_list

    def open_page(self, url, pause=1):
        wd = self.wd
        wd.get(url)
        time.sleep(pause)

    def open_json(self, file):
        with open(file, 'r', encoding='utf-8') as fh:     # открываем файл на чтение
            return json.load(fh)                                                        # загружаем из файла данные в словарь data

    def save_json(self, name, data):
        with open(name, 'w', encoding='utf-8') as fh:               # открываем файл на запись
            fh.write(json.dumps(data, ensure_ascii=False))          # преобразовываем словарь data в unicode-строку и записываем в файл

    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()