from datetime import datetime
from zoneinfo import ZoneInfo

from settings import cfg


def get_local_time() -> datetime:
    return datetime.now(ZoneInfo(cfg.timezone))
