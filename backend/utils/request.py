import asyncio
import logging

from httpx import AsyncClient, Response, TimeoutException, ConnectError

from db.schemas import RequestResults


logger = logging.getLogger(__name__)

PIXIV_URL = 'https://www.pixiv.net/touch/ajax/search/illusts?include_meta=1&type=illust_and_ugoira&word=崩坏3rd OR 崩壊3rd OR 崩坏3 OR 崩壞3rd OR honkaiimpact3rd OR 붕괴3 OR 붕괴3rd OR 崩坏学园 OR 崩壊学園 OR 崩坏 OR 崩坏三 OR リタ・ロスヴァイセ OR 琪亚娜 OR 符华 OR フカ OR 希儿&s_mode=s_tag_full&lang=en'
TWITTER_SEARCH_URL ='https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%23%E7%AC%A6%E5%8D%8E%20OR%20%23%E5%B4%A9%E5%9D%8F3%20OR%20%23%E3%83%95%E3%82%AB%20OR%20%23%E5%B4%A9%E5%9D%8F3rd%20OR%20%23%E5%B4%A9%E5%A3%9E3rd%20OR%20%23%EB%B6%95%EA%B4%B43rd%20OR%20%23Honkaiimpact3rd%20OR%20%23%E5%B4%A9%E5%A3%8A3rd%20min_faves%3A2&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CreplyvotingDownvotePerspective%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo'
TWITTER_HOME_URL = 'https://api.twitter.com/1.1/statuses/home_timeline.json?tweet_mode=extended&exclude_replies=1&include_rts=0&count=200'
MIHOYO_URL = 'https://bbs-api.mihoyo.com/post/wapi/getForumPostList?forum_id=4&gids=1&is_good=false&is_hot=false&page_size=20&sort_type=2'
LOFTER_URL = 'https://www.lofter.com/tag/'
LOFTER_TAGS = '崩坏3 符华 琪亚娜 丽塔 崩坏三 崩坏3rd 雷电芽衣'
TWITTER_LIKE_URL = 'https://api.twitter.com/1.1/favorites/create.json?id='
BCY_URL = "https://bcy.net/apiv3/common/circleFeed?circle_id=109315&since=0&sort_type=2&grid_type=10"

urls = [PIXIV_URL, TWITTER_SEARCH_URL, MIHOYO_URL, BCY_URL, TWITTER_HOME_URL]
for tag in LOFTER_TAGS.split(' '):
    url = LOFTER_URL + tag
    urls.append(url)

async def make_request(
    client: AsyncClient, 
    url: str
    ) -> Response | None:
    try:
        response = await client.get(url)
        return response
    except (TimeoutException, ConnectError):
        logger.warning(
            f'Request timeout, URL: {url[:100]}'
            )

async def request_honkai(client: AsyncClient) -> RequestResults:
    tasks = []
    for url in urls:
        tasks.append(asyncio.ensure_future(make_request(client, url)))
    responses = await asyncio.gather(*tasks)

    results = results_to_sources(responses)
    return results

def results_to_sources(results_list: list[Response]) -> RequestResults:

    results = RequestResults(
        pixiv = results_list[0].json()['body']['illusts'],
        twitter_honkai = list(results_list[1].json(
            )['globalObjects']['tweets'].values()),
        bbs_mihoyo = results_list[2].json()['data']['list'],
        bcy = results_list[3].json()['data']['items'],
        myfeed = results_list[4].json(),
        lofter = [result.text for result in results_list[5:]],
    )    
    return results

async def pixiv_proxy(url, client: AsyncClient) -> Response | None:
    return await make_request(client, url)

async def like_request(
    post_id: int,
    client: AsyncClient
    ) -> Response:
    url = TWITTER_LIKE_URL + str(post_id)
    return await client.post(url)