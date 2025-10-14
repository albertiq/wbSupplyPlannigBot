from settings import cfg


async def check_user_access(username: str) -> bool:
    """Проверяет, есть ли у пользователя доступ к настройкам"""
    return username in cfg.allowed_usernames
