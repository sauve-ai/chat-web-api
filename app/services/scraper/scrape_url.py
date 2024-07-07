import requests
from bs4 import BeautifulSoup
import re
import pdb
# from app.services.chatbot.extract_markdown import get_content, process_urls

import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import html2text

async def scrape_website(session, url):
    async with session.get(url) as response:
        return await response.text()

def convert_html_to_markdown(html):
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    markdown = converter.handle(html)
    return markdown

def convert_to_absolute_url(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    for img_tag in soup.find_all('img'):
        if img_tag.get('src'):
            src = img_tag.get('src')
            if src.startswith(('http://', 'https://')):
                continue
            absolute_url = urljoin(base_url, src)
            img_tag['src'] = absolute_url
        elif img_tag.get('data-src'):
            src = img_tag.get('data-src')
            if src.startswith(('http://', 'https://')):
                continue
            absolute_url = urljoin(base_url, src)
            img_tag['data-src'] = absolute_url

    for link_tag in soup.find_all('a'):
        href = link_tag.get('href')
        if href.startswith(('http://', 'https://')):
                continue
        absolute_url = urljoin(base_url, href)
        link_tag['href'] = absolute_url

    updated_html = str(soup)
    return updated_html

async def get_content(session, url):
    html = await scrape_website(session, url)
    # updated_html = convert_to_absolute_url(html, url)
    markdown = convert_html_to_markdown(html)
    return markdown

async def get_page_contents_markdown(url_list):
    async with aiohttp.ClientSession() as session:
        tasks = [get_content(session, url) for url in url_list]
        pages = []
        for link, task in zip(url_list, asyncio.as_completed(tasks)):
            try:
                print(f"Processing link: {link}")
                filtered_text = await task
                cleaned_text = remove_whitespace(filtered_text)
                pages.append({
                    "text": cleaned_text,
                    "source": link
                }) 
            except Exception as e:
                print(f"Error processing {link}: {e}")
        return pages

def remove_whitespace(text):
    return ' '.join(text.split())

# This function can be called from FastAPI
async def process_urls(url_list):
    return await get_page_contents_markdown(url_list)



class ScrapeWebPage:
    """Scrapes the Web page and processes it as required.
    """
    def __init__(self, url) -> None:
        self.url =url
    
    @staticmethod
    def extract_base_url(url:str)->str:
        """Extracts the base url from a long url."""
        pattern = r'^.+?[^\/:](?=[?\/]|$)'
        match = re.match(pattern, url)
        if match:
            return match.group(0)
        else: 
            raise Exception("Invalid URL.")
        
    def get_url(self):
        base_url = ScrapeWebPage.extract_base_url(self.url)
        print(f"BASE URL:{base_url}")

        headers = {
                "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
            } 
        reqs = requests.get(self.url,  headers=headers, allow_redirects=True, timeout=None)
        soup = BeautifulSoup(reqs.text, "html.parser")
        # print(soup)
        urls = []
        for link in soup.find_all("a"):
            urls.append(link.get("href"))
        if self.url not in urls:
            urls.append(self.url)
        elif base_url not in urls:
            urls.append(base_url)
        urls = list(set(urls))
        urls = list(filter(None, urls))
        print(urls)
        return urls, base_url
    
    def process_urls(self, url_list:list, base_url:str)->list:
        """Processes unnecessary urls in the list and adds the base url if required. 

        Args:
            url_list (list): List of urls to process.

        Returns:
            list: List of processed urls.
        """
        new_url_list = [url for url in url_list if "#" not in url]
        # processed_list = [url for url in new_url_list if url.startswith(self.url)]
        for index, item in enumerate(new_url_list):
            if item.startswith("/"):
                new_url_list[index] = f"{self.url.rstrip('/')}{item}"
        new_url_list = [url for url in new_url_list if base_url in url]
        return new_url_list

    # @staticmethod    
    # async def get_page_contents_markdown(url_list:list):
    #     pages=[]
    #     for link in url_list:
    #         try:
    #             print(f"Processing link: {link}")
    #             filtered_text = await process_urls(link)
    #             cleaned_text = ScrapeWebPage.remove_whitespace(filtered_text)
    #             pages.append({
    #                 "text": cleaned_text,
    #                 "source": link
    #             }) 
    #         except Exception as e:
    #             print("Invalid URL: ", link)
    #     return pages
    
    def get_page_contents(self, url_list:list):
        pages=[]
        for link in url_list:
            try:
                print(f"Processing link: {link}")
                request = requests.get(link)
                scraped_data = BeautifulSoup(request.text, "html.parser")
                filtered_text = scraped_data.text
                cleaned_text = ScrapeWebPage.remove_whitespace(filtered_text)
                pages.append({
                    "text": cleaned_text,
                    "source": link
                }) 
            except Exception as e:
                print("Invalid URL: ", link)
        return pages
    
    @staticmethod
    def remove_whitespace(text:str):
        pattern = r"\s+"
        s = re.sub(pattern, " ", text)
        return s

# from fastapi import FastAPI
# app = FastAPI()

# @app.get("/main")
# async def url():
#     tai_scraper = ScrapeWebPage("https://www.setopati.com/")
#     url_list, base_url = tai_scraper.get_url()
#     processed_url = tai_scraper.process_urls(url_list=url_list, base_url=base_url)
#     print("LENGHT", len(url_list))
#     print(processed_url)
#     print(url_list)
#     content = await get_page_contents_markdown(url_list = processed_url)
#     return content

# with requests.session() as s:
#     for i in range(0,3):
#         res = s.get("https://tai.com.np")
#         print(res.text)4
