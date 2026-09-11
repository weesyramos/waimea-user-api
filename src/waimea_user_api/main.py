from fastapi import FastAPI

from waimea_user_api.application.exceptions import UserAlreadyExistsError
from waimea_user_api.presentation.api.exception_handlers import (
    user_already_exists_handler,
)
from waimea_user_api.presentation.api.users.controller import router as users_router


app = FastAPI()


app.add_exception_handler(
    UserAlreadyExistsError,
    user_already_exists_handler,
)

app.include_router(users_router)