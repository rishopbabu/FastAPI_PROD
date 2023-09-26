from fastapi import Depends, status, HTTPException, APIRouter  # to use fast api
from sqlalchemy.orm import Session
from ..database import get_db
from .. import (
    models,
    schemas,
    utils,
    oauth2,
)  # to use fast api methods import other methods
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# Create a new users account or Rejister a new user
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreateUserResponse,
)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # check if the registered user already exist or not
    existing_user_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    existing_user_phone = db.query(models.Users).filter(models.Users.phone == user.phone).first()

    if existing_user_email and existing_user_phone:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User with email: {user.email} and phone number: {user.phone} already exists',
        )
    elif existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User with email: {user.email} already exists',
        )
    elif existing_user_phone:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'User with phone number: {user.phone} already exists'
        )

    # hash the user password - user.password
    hashed_pwd = utils.hash_password(
        user.password
    )  # getting the password from user input and store in a variable
    user.password = hashed_pwd  # set the user.password a hashed password

    # create a new user
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Get all users
@router.get(
    "/get_all_users",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.GetUserResponse],
)
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    users = db.query(models.Users).all()

    return users


# Get all users based on Id
@router.get(
    "/get_user/{id}", name="Get users by Id", response_model=schemas.GetUserResponse
)
def get_users(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    users = db.query(models.Users).filter(models.Users.id == id).first()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} does not exists",
        )

    return users
