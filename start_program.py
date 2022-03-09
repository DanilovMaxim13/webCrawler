from Crawler import *
import argparse


def start_crawler(save_path, urls):
    save_path = CorrectEnter.enter_correct_path(save_path)
    if save_path != 'eror':
        for link in urls:
            print('Началось скачивание работа с введенным URL:', link)
            craw = Crawler(link, save_path)
            craw.division_by_threads()
        print('Программа завершила свое выполнение. '
              'Скачанные страницы, находятся по адресу:', save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str,
                        help='What is the path?')
    parser.add_argument('--urls', type=str, nargs='+',
                        help='What is the urls?')
    args = parser.parse_args()
    start_crawler(args.path, args.urls)
