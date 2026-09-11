from fastapi import APIRouter, Depends, status

from waimea_user_api.application.use_cases.create_user import (
    CreateUserData,
    CreateUserResult,
    CreateUserUseCase,
)
from waimea_user_api.presentation.api.dependencies import get_create_user_use_case
from waimea_user_api.presentation.api.users.schemas import (
    CreateUserRequest,
    CreateUserResponse,
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> CreateUserResponse:
    result: CreateUserResult = await use_case.execute(
        CreateUserData(
            name=request.name,
            email=request.email,
            role_id=request.role_id,
            password=request.password,
        )
    )

    return CreateUserResponse(
        id=result.user.id,
        name=result.user.name,
        email=result.user.email,
        role_id=result.user.role_id,
        generated_password=result.generated_password,
    )