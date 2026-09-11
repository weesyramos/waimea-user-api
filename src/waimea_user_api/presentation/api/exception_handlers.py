from fastapi import Request
from fastapi.responses import JSONResponse

from waimea_user_api.application.exceptions import UserAlreadyExistsError


async def user_already_exists_handler(
    request: Request,
    exc: UserAlreadyExistsError,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )