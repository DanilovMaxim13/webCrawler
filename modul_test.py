import unittest
from Crawler import *
import os


class TestAllMethods(unittest.TestCase):
    """Тесты работающие без интернета"""
    def test_correct_link(self):
        url = 'https://stackoverflow.com'

        test_link_1 = "https://stackoverflow.com"
        test_link_2 = 'https://wikipedia.org'
        test_link_3 = '#'
        test_link_4 = '//#'
        correct_link_1 = Crawler.correct_link(url, test_link_1)
        correct_link_2 = Crawler.correct_link(url, test_link_2)
        correct_link_3 = Crawler.correct_link(url, test_link_3)
        correct_link_4 = Crawler.correct_link(url, test_link_4)
        self.assertEqual(correct_link_1, test_link_1)
        self.assertEqual(correct_link_2, test_link_2)
        self.assertEqual(correct_link_3, "https://stackoverflow.com/#")
        self.assertEqual(correct_link_4, "https://#")

    def test_save_content(self):
        url = 'test'
        path = os.getcwd()
        crawler_test = Crawler(url, path)

        path = os.path.join(path, '{}.html'.format('test'))
        crawler_test.save_page(url)
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_correct_enter(self):
        path1 = ''
        path2 = os.getcwd()

        self.assertEqual('eror', CorrectEnter.enter_correct_path(path1))
        self.assertEqual(path2, CorrectEnter.enter_correct_path(path2))

    def test_removes_bad_characters(self):
        url = 'https:///*|\\good:\"<>?'
        self.assertEqual('good', Crawler.removes_bad_characters(url))

    def test_get_links(self):
        url = 'test'
        crawler_test = Crawler(url, "")

        right_output = ['test/test_1',
                        'test/test_2']

        page = "<a href=\"test_1\">Link</a>" \
               " <a href=\"test_2\">Link</a>"
        new_links = crawler_test.get_links(page)
        self.assertEqual(new_links, right_output)

    """Тесты работающие только с интернетом"""

    def test_get_links2(self):
        url = 'https://vk.com'
        crawler_test = Crawler(url, "")

        right_output = ['https://vk.com//',
                        'https://vk.me/?act=dl',
                        'https://static.vk.com/restore',
                        'https://vk.com//join',
                        'https://vk.com//login?act=fb_sign',
                        'https://vk.com//settings?act=change_'
                        'regional&hash=a61011b4572266280a&lang_id=3',
                        'https://vk.com//settings?act=change_'
                        'regional&hash=a61011b4572266280a&lang_id=1',
                        'https://vk.com//settings?act=select_lang',
                        'https://vk.com//fv?to=%2F%3F_fm%3D1%26_fm2%3D1',
                        'https://vk.com//join?from=float']

        page = requests.get(url).text
        new_links = crawler_test.get_links(page)
        self.assertEqual(new_links, right_output)


if __name__ == '__main__':
    unittest.main()
