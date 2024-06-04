from functools import wraps

from core.db.session import session


def unit_of_work(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    return wrapper
