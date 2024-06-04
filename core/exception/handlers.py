from fastapi import Request
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse


async def generic_db_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Violation Error, Request was not processed"},
    )
