from functools import wraps

from core.db import session


class UnitOfWork(object):
    def __call__(self, func):
        @wraps(func)
        async def _uow(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

            return result

        return _uow()
