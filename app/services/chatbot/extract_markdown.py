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