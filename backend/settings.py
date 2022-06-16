from pathlib import Path

from pydantic import BaseSettings

env_location = Path("../.env").resolve()

class Settings(BaseSettings):
    SCARY_TAGS: str = '妊娠 催眠 ヒカマニ Hikakin_Mania 巨大娘 COM3D2 mikumikudance mmd R18MMD 崩坏3MMD コイカツ NTR 動圖 R-18G コイカツ! うごイラ 3D koikatsu! Koikatsu 恋活 3DCG MMD 王者荣耀 斗破苍穹 koikatsu'
    SCARY_AUTHORS: str= '寂静之刃 Arise Tomodachi 梦醒幻实 AbilfloridaArts 四奈乃 云起 極彩色 阡陌菌 千樺·エイミー・ザル Trishnicajoy PShiro 黑虎阿符 BT1 BALD Tay-X Meigane 过度解毒 「雪」 资源出口 阿曼達·木子 MilkMan29 興趣使然'

    # Global settings
    TIMEZONE: int = 2
    UPDATE_TIMEOUT: int = 20

    # Deployment settings
    FRONTEND_URL: str = 'http://localhost:8080'

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