import time
import requests
import urllib.request
import os
import re
from bs4 import BeautifulSoup

def download(download_url):
    header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
            }

    r = requests.get(download_url, headers=header)
    r.encoding = 'utf-8'
    return r.text

def get_movie():
    url_douban = 'https://movie.douban.com/'
    html_douban = download(url_douban)
    soup = BeautifulSoup(html_douban)
    a = soup.find_all("li", class_="ui-slide-item")
    all_movie_dict = {}
    all_movie_list = []
    for i in a:
        c = i.find_all("li", class_="poster")
        if len(c):
            single_movie = {}
            # 获得电影名字
            title = i.get('data-title')
            all_movie_list.append(title)
            # 获得电影评分，空视为暂无评分
            score = i.get('data-rate')
            if score == "":
                score = "暂无评分"
            poster_url = c[0].a.img.get('src')
            detail_url = c[0].a.get('href')
            single_movie['poser_url'] = poster_url
            single_movie['detail_url'] = detail_url
            single_movie['score'] = score
            all_movie_dict[title] = single_movie
    return all_movie_list,all_movie_dict

if __name__ =='__main__':
    #豆瓣电影：'http://www.1905.com/vod/list/n_1_t_1/o3p1.html'
    all_movie_list,all_movie_dict = get_movie()
    print(all_movie_list)
    print(all_movie_dict)
        #(i)
