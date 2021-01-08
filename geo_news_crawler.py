# Geo News Latest News Web Scraper
# 25 Aug

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as Soup

url = "https://www.geo.tv/latest-news"

folder_path = "D:/geo/"
index_file_path = folder_path + "/index.txt"


hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
req = Request(url,headers=hdr)

website_response = urlopen(req)
source_code = website_response.read()

main_soup = Soup(source_code, 'html.parser')
first_row_div = main_soup.find('div', class_='row')
news_div = first_row_div.div

news_items = news_div.find_all('a', class_='open-section')

visited_links = open(index_file_path).readlines()

"""
cleaned_visited_links = []
for link in visited_links:
    cleaned_visited_links.append(link.strip())
"""
cleaned_visited_links = [link.strip() for link in visited_links]

for news in news_items:
    href = news.get('href')
    if(href not in cleaned_visited_links):
        title = news.text.strip()
        req = Request(href, headers=hdr)
        website_response = urlopen(req)

        source_code = website_response.read()

        soup = Soup(source_code, 'html.parser')

        file_name = soup.title.text

        cleaned_file_name = str()
        for char in file_name:
            if(char.isdigit() or char.isalpha() or char.isspace()):
                cleaned_file_name += char

        news_story_file = folder_path + cleaned_file_name + ".txt"

        paragraphs = soup.find_all('p')
        story_text = str()
        for p in paragraphs:
            story_text += p.text.strip() +"\n"

        file = open(news_story_file, 'w', encoding = 'utf-8')
        file.write(story_text)
        file.flush()
        file.close()

        file = open(index_file_path, 'a+', encoding='utf-8')
        file.write(href+"\n")
        file.close()

        print(news_story_file)
    else:
        print("Duplicate:", href)