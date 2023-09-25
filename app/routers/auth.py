from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(database.get_db),
):
    # user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first() # get the user email and check
    user = (
        db.query(models.Users)
        .filter(models.Users.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    user_details = {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "created_at": user.created_at,
    }

    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )  # create a token

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_details": user_details,
    }  # return a token
