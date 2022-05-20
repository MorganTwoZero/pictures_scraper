from pathlib import Path

from pydantic import BaseSettings


env_location = Path("../.env").resolve()

class Settings(BaseSettings):
    LOFTER_TAGS: str = '崩坏3 符华 琪亚娜 丽塔 崩坏三 崩坏3rd 雷电芽衣'
    SCARY_TAGS: str = '催眠 ヒカマニ Hikakin_Mania 巨大娘 COM3D2 mikumikudance mmd R18MMD 崩坏3MMD コイカツ NTR 動圖 R-18G コイカツ! うごイラ 3D koikatsu! Koikatsu 恋活 3DCG MMD 王者荣耀 斗破苍穹 koikatsu'
    SCARY_AUTHORS: str= 'Arise Tomodachi 梦醒幻实 AbilfloridaArts 四奈乃 云起 極彩色 阡陌菌 千樺·エイミー・ザル Trishnicajoy PShiro 黑虎阿符 BT1 BALD Tay-X Meigane 过度解毒 「雪」 资源出口 阿曼達·木子 MilkMan29 興趣使然'
    PIXIV_URL: str = 'https://www.pixiv.net/touch/ajax/search/illusts?include_meta=1&type=illust_and_ugoira&word=崩坏3rd OR 崩壊3rd OR 崩坏3 OR 崩壞3rd OR honkaiimpact3rd OR 붕괴3 OR 붕괴3rd OR 崩坏学园 OR 崩壊学園 OR 崩坏 OR 崩坏三 OR リタ・ロスヴァイセ OR 琪亚娜 OR 符华 OR フカ OR 希儿&s_mode=s_tag_full&lang=en'
    TWITTER_SEARCH_URL: str ='https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q=%23%E7%AC%A6%E5%8D%8E%20OR%20%23%E5%B4%A9%E5%9D%8F3%20OR%20%23%E3%83%95%E3%82%AB%20OR%20%23%E5%B4%A9%E5%9D%8F3rd%20OR%20%23%E5%B4%A9%E5%A3%9E3rd%20OR%20%23%EB%B6%95%EA%B4%B43rd%20OR%20%23Honkaiimpact3rd%20OR%20%23%E5%B4%A9%E5%A3%8A3rd%20min_faves%3A2&tweet_search_mode=live&count=20&query_source=typed_query&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CreplyvotingDownvotePerspective%2CvoiceInfo%2Cenrichments%2CsuperFollowMetadata%2CunmentionInfo'
    TWITTER_HOME_URL: str = 'https://api.twitter.com/1.1/statuses/home_timeline.json?tweet_mode=extended&exclude_replies=1&include_rts=0&count=200'

    # Global settings
    TIMEZONE: int = 2
    UPDATE_TIMEOUT: int = 20

    # Deployment settings
    FRONTEND_URL: str

    # Credentials
    PIXIV_HEADER: str
    TWITTER_HEADER: str

    # Security settings
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = env_location
        env_file_encoding = 'utf-8'


settings = Settings()  # type: ignore