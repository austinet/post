import flickrapi
from urllib.request import urlretrieve
from PIL import Image

import os
from tqdm import tqdm

def _fetch(keyword, num_url):
    # Flickr api access key 
    flickr=flickrapi.FlickrAPI('c6a2c45591d4973ff525042472446ca2', '202ffe6f387ce29b', cache=True)

    # flickrapi.FlickrAPI.walk == flickr.photos.search
    photos = flickr.walk(text=keyword,
                         tag_mode='all',
                         extras='url_c',
                         per_page=100,
                         sort='relevance',
                         safe_search=3)

    urls = []
    for i, photo in enumerate(photos):
        url = photo.get('url_c')
        urls.append(url)
        
        # get n urls
        if i > num_url:
            break

    # print (urls)
    print('{} urls are fetched'.format(len(urls)))

    return urls

def _download(keyword, urls, num_url, resize):
    os.makedirs('./{}'.format(keyword), exist_ok=True)

    # Download image from the url and save it as 'n.jpg'
    if resize == True:
        for i in tqdm(range(len(urls))):
            try:
                urlretrieve(urls[i], './{}/{}.jpg'.format(keyword, i))

                image = Image.open('./{}/{}.jpg'.format(keyword, i)) 
                image = image.resize((256, 256), Image.ANTIALIAS)

                image.save('./{}/{}.jpg'.format(keyword, i))
            except: continue
    else:
        for i in tqdm(range(len(urls))):
            try:
                urlretrieve(urls[i], './{}/{}.jpg'.format(keyword, i))
                image.save('./{}/{}.jpg'.format(keyword, i))
            except: continue

def run(keyword, num_url, resize):
    urls = _fetch(keyword, num_url)
    _download(keyword, urls, num_url, resize)


run('gymnastics', 1000, resize=False)