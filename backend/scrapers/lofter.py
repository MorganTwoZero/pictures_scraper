import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from db.read_create import save_to_db
from db.schemas import PostCreate

TIMEZONE = int(os.environ['TIMEZONE'])

SEARCH_URL_TEMPLATE = 'https://www.lofter.com/tag/'
LOFTER_TAGS = os.environ['LOFTER_TAGS'].split()


def lofter_save():
    for tag in LOFTER_TAGS:
        try:
            r = requests.get(url=SEARCH_URL_TEMPLATE + tag)    
            soup = BeautifulSoup(r.text, 'html.parser')

            for item in soup.find_all(class_='m-mlist'):
                if item.find(class_='imgc') is not None:
                    save_to_db(PostCreate(
                        author_link=item.find(class_='w-img ptag').a.attrs['href'],
                        author=item.find(class_='w-img ptag').a.attrs['title'],
                        author_profile_image=item.find(class_='w-img ptag').img.attrs['src'],
                        preview_link=item.find(class_='imgc').img.get('src')[:146],
                        created=datetime.utcfromtimestamp(int(item.find(class_='isayc').attrs['data-time'][:-3])) + timedelta(hours=TIMEZONE),
                        post_link=item.find(class_='isayc').attrs['href'],
                        source='lofter',
                        )
                    )
        except Exception:
            print('Failed to get ' + SEARCH_URL_TEMPLATE + tag)