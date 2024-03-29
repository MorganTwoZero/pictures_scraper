from pathlib import Path

from pydantic import BaseSettings

env_location = Path("../.env").resolve()

class Settings(BaseSettings):
    SCARY_TAGS: list[str] = ['妊娠', '催眠', 'ヒカマニ', 'Hikakin_Mania', '巨大娘', 'COM3D2', 'mikumikudance', 'mmd', 'R18MMD', '崩坏3MMD', 'コイカツ', 'NTR', '動圖', 'R-18G', 'コイカツ!', 'うごイラ', '3D', 'koikatsu!', 'Koikatsu', 'Koikatsu!', '恋活', '3DCG', 'MMD', '王者荣耀', '斗破苍穹', 'koikatsu']
    SCARY_AUTHORS: list[str]= ['理香~', '碧梅秋暮君', 'Vulcax', 'hendienuns', '寂静之刃', 'Arise', 'Tomodachi', '梦醒幻实', 'AbilfloridaArts', '四奈乃', '云起', '極彩色', '阡陌菌', '千樺·エイミー・ザル', 'Trishnicajoy', 'PShiro', '黑虎阿符', 'BT1', 'BALD', 'Tay-X', 'Meigane', '过度解毒', '「雪」', '资源出口', '阿曼達·木子', 'MilkMan29', '興趣使然', '肉乎乎の布洛妮娅', '孤人GuRn', ' 哎呀_迷路了_迷路了__']

    # Global settings
    TIMEZONE: int = 2

    # Deployment settings
    SITE_URL: str = 'http://localhost:8080'

    # Credentials
    HEADER: str

    class Config:
        env_file = env_location
        env_file_encoding = 'utf-8'


settings = Settings()  # type: ignore
