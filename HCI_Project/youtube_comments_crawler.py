from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time


def youtube_crawler(url):
    print("start youtube comments crawler at url ", url)

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver  = webdriver.Chrome(executable_path='/home/jeongwu/HCI/HCI_Project/chrome_driver_83/chromedriver', chrome_options=chrome_options)
    driver.implicitly_wait(3)

    #url = 'https://www.youtube.com/watch?v=xKf0soeFJtY'
    #url = 'https://youtu.be/sKr9MM_04DI'
    driver.get(url)

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True: 
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
        
    html_source = driver.page_source

    driver.close()

    soup = BeautifulSoup(html_source, 'lxml')

    youtube_user_IDs = soup.select('div#header-author > a > span')

    youtube_comments = soup.select('yt-formatted-string#content-text')

    str_youtube_userIDs = []
    str_youtube_comments = []

    for i in range(len(youtube_user_IDs)):
        str_tmp = str(youtube_user_IDs[i].text)
        # print(str_tmp)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        #str_tmp = str_tmp.replace(' ','')
        str_youtube_userIDs.append(str_tmp)
        
        str_tmp = str(youtube_comments[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        #str_tmp = str_tmp.replace(' ', '')
        
        str_youtube_comments.append(str_tmp)

    '''
    for i in range(len(str_youtube_userIDs)):
        print(str_youtube_userIDs[i], str_youtube_comments[i])
    '''

    pd_data = {"id":str_youtube_userIDs, "document":str_youtube_comments}

    youtube_pd = pd.DataFrame(pd_data)
    youtube_pd = youtube_pd[['id', 'document']]

    youtube_pd.to_csv("./output/comments.csv", encoding="utf-8-sig")

    print("youtube comments crawler ended")