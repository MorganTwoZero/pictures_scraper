from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from db.schemas import PostScheme
from settings import settings
from utils.crud.posts import save_to_db


TIMEZONE = settings.TIMEZONE

def lofter_save(db, r): 
    try:           
        soup = BeautifulSoup(r.text, 'html.parser')

        for item in soup.find_all(class_='m-mlist'):
            if item.find(class_='imgc') is not None:
                save_to_db(PostScheme(
                    author_link=item.find(class_='w-img ptag').a.attrs['href'],
                    author=item.find(class_='w-img ptag').a.attrs['title'],
                    author_profile_image=item.find(class_='w-img ptag').img.attrs['src'],
                    preview_link=item.find(class_='imgc').img.get('src')[:146],
                    created=datetime.utcfromtimestamp(
                        int(item.find(class_='isayc').attrs['data-time'][:-3])
                        ) + timedelta(hours=TIMEZONE),
                    post_link=item.find(class_='isayc').attrs['href'],
                    honkai=True,
                    ),
                db)
    except:
        print('Failed to get lofter')