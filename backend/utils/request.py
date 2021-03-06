import ast
import asyncio
from typing import Iterable, Sequence
from itertools import zip_longest
import logging

import httpx

from settings import settings
from db.schemas import RequestResults, UserWithTwitter


logger = logging.getLogger(__name__)

PIXIV_URL = 'https://www.pixiv.net/touch/ajax/search/illusts?include_meta=1&type=illust_and_ugoira&word=崩坏3rd OR 崩壊3rd OR 崩坏3 OR 崩壞3rd OR honkaiimpact3rd OR 붕괴3 OR 붕괴3rd OR 崩坏学园 OR 崩壊学園 OR 崩坏 OR 崩坏三 OR リタ・ロスヴァイセ OR 琪亚娜 OR 符华 OR フカ OR 希儿&s_mode=s_tag_full&lang=en'
TWITTER_SEARCH_URL ='https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%23%E7%AC%A6%E5%8D%8E%20OR%20%23%E5%B4%A9%E5%9D%8F3%20OR%20%23%E3%83%95%E3%82%AB%20OR%20%23%E5%B4%A9%E5%9D%8F3rd%20OR%20%23%E5%B4%A9%E5%A3%9E3rd%20OR%20%23%EB%B6%95%EA%B4%B43rd%20OR%20%23Honkaiimpact3rd%20OR%20%23%E5%B4%A9%E5%A3%8A3rd%20min_faves%3A2&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CreplyvotingDownvotePerspective%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo'
TWITTER_HOME_URL = 'https://api.twitter.com/1.1/statuses/home_timeline.json?tweet_mode=extended&exclude_replies=1&include_rts=0&count=200'
MIHOYO_URL = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=4&gids=1&is_good=false&is_hot=false&page_size=20&sort_type=2'
LOFTER_URL = 'https://www.lofter.com/tag/'
LOFTER_TAGS = '崩坏3 符华 琪亚娜 丽塔 崩坏三 崩坏3rd 雷电芽衣'
PIXIV_HEADER: dict[str, str] = ast.literal_eval(settings.PIXIV_HEADER)
TWITTER_HEADER: dict[str, str] = ast.literal_eval(settings.TWITTER_HEADER)
TWITTER_LIKE_URL = 'https://api.twitter.com/1.1/favorites/create.json?id='

urls = [PIXIV_URL, TWITTER_SEARCH_URL, MIHOYO_URL]
headers = [PIXIV_HEADER, TWITTER_HEADER]

for tag in LOFTER_TAGS.split(' '):
    url = LOFTER_URL + tag
    urls.append(url)

async def _get(
    client: httpx.AsyncClient, 
    url: str, 
    header = None,
    ) -> httpx.Response:
    try:
        response = await client.get(url, headers=header, timeout=20)
    except httpx.TimeoutException:
        '''Return empty response so that user wouldn't 
        get other user's response in request_homeline_many_users
        if some request fails'''
        response = httpx.Response(status_code=400, text='Request timeout')
        logger.exception(
            f'Request timeout, url={url}, header={header}'
            )
    return response

async def request_honkai() -> RequestResults:

    client = httpx.AsyncClient()

    tasks = []
    for url, header in zip_longest(urls, headers, fillvalue=''):
        tasks.append(asyncio.ensure_future(_get(client, url, header)))

    responses: tuple[httpx.Response] = await asyncio.gather(*tasks)
    await client.aclose()

    results = results_to_sources(responses)

    return results

async def request_homeline(
    users: Iterable[UserWithTwitter]
    ) -> Iterable[tuple[UserWithTwitter, httpx.Response]]:
    
    client = httpx.AsyncClient()

    tasks = []
    for user in users:
        tasks.append(
            asyncio.ensure_future(
                _get(
                    client, 
                    TWITTER_HOME_URL, 
                    ast.literal_eval(user.twitter_header)
                    )
                )
            )

    responses: tuple[httpx.Response] = await asyncio.gather(*tasks)
    await client.aclose()

    return [i for i in zip(users, responses)]

def results_to_sources(
    results_list: Sequence[httpx.Response]) -> RequestResults:

    results = RequestResults(
        pixiv = results_list[0].json()['body']['illusts'],
        twitter_honkai = list(results_list[1].json(
            )['globalObjects']['tweets'].values()),
        bbs_mihoyo = results_list[2].json()['data']['list'],
        lofter = [result.text for result in results_list[3:]],
    )
    
    return results

async def pixiv_proxy(url) -> httpx.Response:

    header=PIXIV_HEADER
    header.update({'Referer': 'https://www.pixiv.net/'})
    client = httpx.AsyncClient()

    response = await _get(client, url, header)
    await client.aclose()

    return response

async def like_request(
    post_id: int, 
    user: UserWithTwitter,
    ) -> httpx.Response:

    client = httpx.AsyncClient()
    url = TWITTER_LIKE_URL + str(post_id)
    header = ast.literal_eval(user.twitter_header)

    response = await client.post(url, headers=header, timeout=20)
    await client.aclose()

    return response