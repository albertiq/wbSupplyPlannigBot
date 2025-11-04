from settings import cfg


async def check_user_access(username: str) -> bool:
    return username in cfg.allowed_usernames
