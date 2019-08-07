"""
Global setting of VN Trader.
"""

from logging import CRITICAL

from .utility import load_json

SETTINGS = {
    "font.family": "Arial",
    "font.size": 12,

    "log.active": True,
    "log.level": CRITICAL,
    "log.console": True,
    "log.file": True,

    "sinaqq.interval": 30,
    "hedge.etf": "sh510050",
    "hedge.qqcode": "10001888",
    "hedge.etfsize": 12000,
    "hedge.qqcodesize": 2,
    "hedge.exe_price":3.0,
    "hedge.remain":18,
    "hedge.v": 0.02,
    "hedge.start":-40.0,
    "hedge.stop":40.0,
    "database.driver": "mysql",  # see database.Driver
    "database.database": "stock",  # for sqlite, use this as filepath
    "database.host": "192.168.52.128",
    "database.port": 3306,
    "database.user": "root",
    "database.password": "root",
}

# Load global setting from json file.
SETTING_FILENAME = "vt_setting.json"
SETTINGS.update(load_json(SETTING_FILENAME))


def get_settings(prefix: str = ""):
    prefix_length = len(prefix)
    return {k[prefix_length:]: v for k, v in SETTINGS.items() if k.startswith(prefix)}
