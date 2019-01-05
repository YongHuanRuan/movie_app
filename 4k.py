import time
import requests
import urllib.request
import os
import re
import json
import urllib.request
import http.cookiejar
from bs4 import BeautifulSoup

def download(download_url):
    header = {
        "X-Requested-With":'XMLHttpRequest',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0"
            }
    r = requests.get(download_url, headers=header)
    a= json.loads(r.text)
    return a
def get_movie(search_content):
    # 4k屋在线电影
    host_url = 'http://www.kkkkmao.com'
    search_url = 'http://www.kkkkmao.com/index.php?s=vod-search-wd-' + urllib.request.quote(
        search_content) + '-1-ajax'  # 'http://www.kkkkmao.com/index.php?s=vod-search-wd-'+urllib.request.quote(search_content)
    search_html = download(search_url)
    ajaxtxt = search_html['data']['ajaxtxt']
    soup = BeautifulSoup(ajaxtxt)
    # 标题 list
    title_list = []
    for i in soup.find_all('div', class_='play-txt'):
        title = ''.join(i.h5.a.strings)
        title_list.append(title)
    # 播放url list和海报post_url  list
    play_url_list = []
    post_url_list = []
    for i in soup.find_all('a', class_='play-img'):
        # 播放地址url
        href = i.get("href")
        play_url = host_url + href
        play_url_list.append(play_url)
        # 海报url
        post_url = i.img.get('src')
        post_url_list.append(post_url)
    # 主演 list
    actors_list = []
    for i in soup.find_all('p', class_='actor'):
        actors = ""
        for k in [j.string for j in i.find_all('a')]:
            if k:
                actors = actors + " " + k
        actors_list.append(actors)
    # 剧情 list
    plot_list = []
    for i in soup.find_all('p', class_='plot'):
        plot = "".join([j.string for j in i.strings])
        plot_list.append(plot)
    # print(soup.prettify())
    all_movie_dict = {}
    for i, j in enumerate(title_list):
        single_movie_dict = {}
        single_movie_dict['post_img'] = post_url_list[i]
        single_movie_dict['play_url'] = play_url_list[i]
        single_movie_dict['plot_txt'] = plot_list[i]
        single_movie_dict['actors'] = actors_list[i]
        all_movie_dict[j] = single_movie_dict
    return all_movie_dict


if __name__ =='__main__':
    search_content = input()
    all_movie_dict = get_movie(search_content)
    print(all_movie_dict)
