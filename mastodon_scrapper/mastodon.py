import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_image_source(img):
    if img.get('src'):
        return img['src']
    elif img.get('data-src'):
        return img['data-src']
    return None


def extract_videos(soup):
    videos = []
    for video in soup.find_all('video'):
        if video.get('src'):
            videos.append(video['src'])
        for source in video.find_all('source'):
            if source.get('src'):
                videos.append(source['src'])
    for iframe in soup.find_all('iframe'):
        if iframe.get('src'):
            videos.append(iframe['src'])
    return videos


def extract_links(soup):
    links = []
    for link in soup.find_all('a'):
        url = link.get('href')
        text = link.text.strip()
        if url: 
            links.append({'url': url, 'text': text})
    return links


url = 'https://mastodon.social/explore'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Images
image_data = [{'src': get_image_source(img), 'alt': img.get(
    'alt', '')} for img in soup.find_all('img') if get_image_source(img)]

# Text
text_data = [tag.text for tag in soup.find_all(
    ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']) if tag.text.strip()]

# Videos
video_data = extract_videos(soup)

# Links
link_data = extract_links(soup)

# Saving data to CSV
pd.DataFrame(image_data).to_csv('images_data.csv', index=False)
pd.DataFrame(text_data, columns=['text']).to_csv('text_data.csv', index=False)
pd.DataFrame(video_data, columns=['video_src']).to_csv(
    'videos_data.csv', index=False)
pd.DataFrame(link_data).to_csv('links_data.csv', index=False)

print("Completed data scraping and saving results in texts, videos, and images.")

#The provided Python code was created for web scraping and data handling tasks. It utilizes the BeautifulSoup library (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for parsing HTML, pandas (https://pandas.pydata.org/docs/) for data manipulation, and requests (https://docs.python-requests.org/en/latest/) for making HTTP requests. The code was written with the assistance of the GPT-3 language model developed by OpenAI.
