import os
import threading
from posixpath import dirname
import requests
from urllib import parse, robotparser
from bs4 import BeautifulSoup
import re
import time


class CorrectEnter:
    @staticmethod
    def enter_correct_path(path):
        if not os.path.exists(path):
            print("Invalid path, please try again")
            return 'eror'
        return path


class Crawler:
    all_links = []
    all_links_save = []
    all_links_page = {}
    save_queue = {}
    robot = robotparser.RobotFileParser()

    def __init__(self, start_url, save_path):
        if start_url != 'test':
            self.save_path = save_path
            self.domain = parse.urljoin(start_url, '/')
            self.start_dir = dirname(start_url)
            if self.domain.startswith(start_url):
                self.start_dir = self.domain

            page = requests.get(start_url).text
            self.save_queue[start_url] = page
            self.all_links_page[start_url] = page
            self.all_links_save = [start_url]
            self.all_links = [start_url]

            self.main_thread = threading.Thread(target=self.main_work,
                                                kwargs={'links': [start_url]})
            self.save_thread = threading.Thread(target=self.save_page_division)

            self.robot.set_url(self.domain + "robots.txt")
            self.robot.read()
        else:
            self.save_path = save_path
            self.domain = 'test'
            self.start_dir = 'test'

            page = "<a href=\"test_1.\">Link</a>" \
                   " <a href=\"test_2\">Link</a>"
            self.save_queue[start_url] = page
            self.all_links_page[start_url] = page
            self.all_links_save = [start_url]
            self.all_links = [start_url]

            self.main_thread = threading.Thread(target=self.main_work,
                                                kwargs={'links': [start_url]})
            self.save_thread = threading.Thread(target=self.save_page_division)

    def division_by_threads(self):
        self.main_thread.start()
        self.save_thread.start()
        self.main_thread.join()
        self.save_thread.join()

    def main_work(self, links):
        for link in links:
            new_links = self.get_links(self.all_links_page[link])
            if len(new_links) != 0:
                self.main_work(new_links)

    def get_links(self, page):
        links = []
        soup = BeautifulSoup(page, 'html.parser')
        for link in soup.findAll('a', href=True):
            link = link['href']
            link = self.correct_link(self.start_dir, link)
            if link not in self.all_links:
                if self.domain != 'test':
                    if self.allow_robots(link):
                        self.all_links.append(link)
                        self.all_links_save.append(link)

                        page = requests.get(link).text
                        self.save_queue[link] = page
                        self.all_links_page[link] = page
                        links.append(link)
                else:
                    links.append(link)
        return links

    def allow_robots(self, link):
        return self.robot.can_fetch("*", link)

    @staticmethod
    def correct_link(url, link):
        if not link.startswith('http'):
            if link.startswith(r'//'):
                return 'https:' + link
            if not link.startswith(r'/'):
                url = url + r'/'
            return url + link
        return link

    def save_page_division(self):
        while self.main_thread.isAlive() or len(self.all_links_save) > 0:
            for link in self.all_links_save:
                self.all_links_save.remove(link)
                while threading.activeCount() > 100:
                    time.sleep(1)
                th = threading.Thread(target=self.save_page,
                                      kwargs={'link': link})
                th.start()
        while len(self.save_queue) > 0:
            pass

    def save_page(self, link):
        while link not in self.save_queue:
            time.sleep(1)
        name = self.removes_bad_characters(link)
        file = open(os.path.join(self.save_path, '{}.html'.format(name)),
                    'w', encoding='utf-8')
        file.write(self.save_queue[link])
        file.close()
        print('Полностью скачалась страница ', link)
        del self.save_queue[link]

    @staticmethod
    def removes_bad_characters(link):
        name = link.replace("https://", "")
        return re.sub('[^a-zA-Z0-9]', '', name)
