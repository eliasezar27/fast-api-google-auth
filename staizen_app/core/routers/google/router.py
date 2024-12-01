from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, RedirectResponse

# Import services outside the package
from core.models.database import Session, get_db
from core.schemas.request_schema import GenericUser
from core.schemas.response_schema import AccountResponse, GenericResponse
from core.dao.UserDAO import UserDAO
from core.auth.auth_handler import encode_jwt, mask_user_id
from core.constants.constant import MOCK_REDIRECT_LINK
from utils.logger import log_execution_time, logger

# Import services in the package
from .services.auth import init_flow

google_services = APIRouter(prefix='/google/auth', tags=["Google Services"])


@google_services.get(
    "/login",
    summary="Handles user login through google auth",
    response_model=GenericResponse
    )
@log_execution_time
async def login(request: Request):
    flow = init_flow()
    auth_url, _ = flow.authorization_url(prompt="consent")
    logger.info(f'----------- {auth_url}')
    return RedirectResponse(auth_url)


@google_services.get(
    "/mock_login",
    summary="Handles mocked user login through google auth",
    response_model=GenericResponse
    )
@log_execution_time
async def summary(request: Request):
    return RedirectResponse(MOCK_REDIRECT_LINK)


@google_services.post(
    "/register",
    summary="Handles user registration through google auth",
    response_model=AccountResponse
    )
@log_execution_time
async def register_user(request: Request, oauth_response: GenericUser, db: Session = Depends(get_db)):
    dao = UserDAO(db)
    existing_user = dao.get_user_by_email(oauth_response.email)
    if existing_user:
        message = 'User already registered'
        user = existing_user.name
        email = existing_user.email
    else:
        new_user = dao.create_user(GenericUser(name=oauth_response.name, email=oauth_response.email))
        message = 'User registered successfully'
        user = new_user.name
        email = new_user.email

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "code": 200,
            "message": message,
            "data": {
                "user": user,
                "email": email,
            }
        }
    )


@google_services.post(
    "/login_user",
    summary="Handles user login through google auth",
    response_model=GenericResponse
    )
@log_execution_time
async def login_user(request: Request, oauth_response: GenericUser, db: Session = Depends(get_db)):
    dao = UserDAO(db)
    existing_user = dao.get_user_by_email(oauth_response.email)
    if existing_user:
        success = True
        status_code = 200
        message = 'Welcome Back!'
    else:
        success = False
        status_code = 404
        message = f'User not found please register through {request.base_url}google/register'

    return JSONResponse(
        status_code=status_code,
        content={
            "success": success,
            "code": status_code,
            "message": message,
            "data": {}
        }
    )


@google_services.get(
    "/oauth2callback",
    summary="Oauth API callback functio",
    response_model=GenericResponse
    )
@log_execution_time
async def oauth2callback(request: Request, db: Session = Depends(get_db)):
    logger.info(f'Callback URL initiated {request.base_url}{request.url}')
    try:
        # Extract query parameters
        query_params = dict(request.query_params)

        if "code" not in query_params:
            return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "Authorization code missing",
                        "data": {}
                    }
                )

        flow = init_flow()
        flow.fetch_token(code=query_params["code"])

        # Get user info from Google
        session = flow.authorized_session()
        user_info = session.get("https://openidconnect.googleapis.com/v1/userinfo").json()

        if "sub" not in user_info:
            return JSONResponse(
                    status_code=400,
                    content={
                        "success": False,
                        "code": 400,
                        "message": "User info not retrieved",
                        "data": {}
                    }
                )

        # Check if user exists or register
        dao = UserDAO(db)
        email = user_info.get("email", "")
        name = user_info.get("name", "")
        user = dao.get_user_by_email(email)
        if not user:
            user = dao.create_user(GenericUser(name=name, email=email))

        user_id = user.id
        masked_user_id = mask_user_id(user_id)

        # Create JWT token
        jwt_token = encode_jwt({"sub": user_id, "email": email})

        # Return token and user info
        logger.info(f'User {user.name} [{user.email}] is authenticated')
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "code": 200,
                    "message": f"User successfully authenticated!",
                    "data": {
                        "access_token": jwt_token,
                        "token_type": "bearer",
                        "user_id": masked_user_id
                    }
                }
            )

    except Exception as e:
            logger.error(f'Error: {e}', exc_info=True)
            return JSONResponse(
                    status_code=500,
                    content={
                        "success": False,
                        "code": 500,
                        "message": f"Error {e}",
                        "data": {}
                    }
                )