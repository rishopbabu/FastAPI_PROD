from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr # to create models
from pydantic.types import conint #this is for vote increment & decrement

# Base model for Users
# This BaseModel always returns as Dictonary
class CreateUser(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str

class CreateUserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True

class GetUserResponse(CreateUserResponse):
    pass

# User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id: Optional[int] = None

# Base model for Posts
# This BaseModel always returns as Dictonary
class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

# only for backwards compatibility to send the desired content to the users
class PostResponse(PostBase): # it usees the postbase class fields automatically
    id: int
    created_at: datetime
    user_id: int
    user_detail: GetUserResponse
    
    class Config:
        from_attributes = True

class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int
    
    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int # want to give the post id
    dir: conint(le=1) # only lessthan or equal to one