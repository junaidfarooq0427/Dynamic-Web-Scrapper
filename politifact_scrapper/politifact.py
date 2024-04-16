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


url = 'https://www.politifact.com'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Images
images = soup.find_all('img')
image_data = [{'src': get_image_source(img), 'alt': img.get(
    'alt', '')} for img in images if get_image_source(img)]

# Text
text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div']
text_data = [tag.text for tag in soup.find_all(text_tags)]
text_data = list(set(text_data))
text_data = [text for text in text_data if text.strip()]

# Videos
video_data = extract_videos(soup)

df_images = pd.DataFrame(image_data)
df_images.to_csv('images_data.csv', index=False)

df_text = pd.DataFrame(text_data, columns=['text'])
df_text.to_csv('text_data.csv', index=False)

df_videos = pd.DataFrame(video_data, columns=['video_src'])
df_videos.to_csv('videos_data.csv', index=False)

print("Completed data scraping and saving results in texts, videos, and images.")


#The provided Python code was created for web scraping and data handling tasks. It utilizes the BeautifulSoup library (https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for parsing HTML, pandas (https://pandas.pydata.org/docs/) for data manipulation, and requests (https://docs.python-requests.org/en/latest/) for making HTTP requests. The code was written with the assistance of the GPT-3 language model developed by OpenAI.
