from datetime import datetime, timedelta
import logging

from bs4 import BeautifulSoup

from db.schemas import PostScheme
from settings import settings


logger = logging.getLogger(__name__)

def parse(htmls):
    parsed = []

    for html in htmls:
        if html:
            soup = BeautifulSoup(html, 'html.parser')

            for item in soup.find_all(class_='m-mlist'):
                if 'data-type' in item.attrs and item.find(class_='imgc'):

                    if item.find(class_='totalnum'):
                        pic_num = int(item.find(class_='totalnum').string)
                    else:
                        pic_num = 1

                    parsed.append(
                        PostScheme(
                            author_link=item.find(class_='w-img ptag').a.attrs['href'],
                            author=item.find(class_='w-img ptag').a.attrs['title'],
                            author_profile_image=item.find(class_='w-img ptag').img.attrs['src'],
                            preview_link=item.find(class_='imgc').img.get('src')[:146],
                            created=datetime.utcfromtimestamp(
                                int(item.find(class_='isayc').attrs['data-time'][:-3])
                            ) + timedelta(hours=settings.TIMEZONE),
                            post_link=item.find(class_='isayc').attrs['href'],
                            images_number=pic_num
                        )
                    )

    logger.debug('Lofter updated')
    return parsed