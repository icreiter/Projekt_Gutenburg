
# Command
import os

# import regex package
import re

# import requests package
import requests as req

# import BeartifulSoup
from bs4 import BeautifulSoup as bs

# make directory path and folder "project_gutenberg"
folderPath = 'project_gutenberg'
def mkdir():
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

# Data arrey for scraping
listData = []

# get book ID & title

def bookInfo():

    url = 'https://www.gutenberg.org/browse/languages/zh'

    res = req.get(url)
    soup = bs(res.text, 'lxml')

    ebook_links = soup.select(
        'div.pgdbbylanguage li.pgdbetext a[href^="/ebooks/"]'
    )

    for link in ebook_links:
        parent_text = link.parent.get_text()
        a_text = link.get_text()

        # to get chinese book ID and title
        if "(Chinese)" in parent_text and re.search(r'[\u4e00-\u9fa5]', a_text):
            id = link['href'].split('/')[2]
            title = ''.join(re.findall(r'[\u4e00-\u9fa5]', a_text))

            listData.append((id, title))


    # print ID & title result
    for id, title in listData:
        print(f"({id}, {title}),")

def download():

    for id, title in listData:
        url = f'https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt'
        try:
            res = req.get(url)

            if res.status_code == 200:
                content = res.text
                contCh = re.sub(r'[^\u4e00-\u9fa5\u3000-\u303F\uff00-\uffef]', '', content)

                # Save file
                file_path = os.path.join(folderPath, f'{title}.txt')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(contCh)
            
                print(f'已存 {title}.txt')

            else:
                print(f"無法下載 {title}")
        
        except Exception as e:
            print("下載{title}時發生錯誤: {e}")

mkdir()
bookInfo()
download()

