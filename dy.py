import time

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'https://www.duoyi.com'
}


def urls_crawler(url):
    """
    爬虫入口，主要爬取操作
    """
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.encoding = 'utf-8'
        r = r.text
        file = open('html.txt', 'a')
        file.write(r + '\n')
        file = open('news.txt', 'a')
        news_list = BeautifulSoup(r, 'lxml').find('div', class_="newsList").find('ul').find_all('a')
        # 获取最新消息
        for news in news_list:
            file.write("%s %s%s \n" % (news.contents[0], url, news['href']))

        file = open('games.txt', 'a')
        # 推荐游戏
        recommend_games = BeautifulSoup(r, 'lxml').find('div', class_="recommendCon clfix").find('ul').find_all('li')
        for game in recommend_games:
            game_info = game.find('div', class_="proInfoCon")
            game_name = game_info.find('dt').find('a').string
            game_url = 'https://%s' % (game_info.find('dt').find('a')['href'][2:-1])
            file.write("%s\n%s\n" % (game_name, game_url))
            game_img = game.find('img', class_="lazy_img")['relsrc'][2:]
            save_pic(game_img, game_name)
            for dd in game_info.find('dl').find_all('dd'):
                for a in dd.find_all('a'):
                    file.write('%s\n' % a.string)
            file.write('\n')

    except Exception as e:
        print(e)


def save_pic(pic_src, pic_name):
    """
    保存图片到本地
    """
    try:
        time.sleep(0.10)
        img = requests.get('http://' + pic_src, headers=HEADERS, timeout=10)
        img_name = "{}.jpg".format(pic_name)
        with open(img_name, 'ab') as f:
            f.write(img.content)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        urls_crawler('https://www.duoyi.com')
    except Exception as ex:
        print(ex)
        time.sleep(30)
        urls_crawler('https://www.duoyi.com')
    print("That is all!")
