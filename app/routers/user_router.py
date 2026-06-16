from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utils.security import hash_password
from app.config.database import get_db
from app.models.user import User
from app.schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserResponse
)
from app.schemas.user_schema import (
    LoginRequest,
    Token
)
from app.utils.security import (
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
        db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_data.first_name is not None:
        user.first_name = user_data.first_name

    if user_data.last_name is not None:
        user.last_name = user_data.last_name

    if user_data.email is not None:

        existing_email = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.email = user_data.email

    if user_data.password is not None:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)

    return user

@router.delete(
    "/{user_id}"
)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": f"User {user_id} deleted successfully"
    }


from fastapi.security import OAuth2PasswordRequestForm

@router.post(
    "/login",
    response_model=Token
)
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
            form_data.password,
            user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }