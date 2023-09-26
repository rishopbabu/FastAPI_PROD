from fastapi import Depends, status, HTTPException, APIRouter  # to use fast api
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional  # to get the no of response as a list in get all post
from ..database import get_db
from .. import models, schemas, oauth2  # to use fast api methods import other methods

router = APIRouter(prefix="/posts", tags=["Posts"])

# CRUD Operations for Posts


# Get all posts
@router.get(
    "/get_all_posts",
    name="Get all posts",
    response_model=List[schemas.PostVoteResponse],
)  # here List[schemas.PostResponse] -> to get all posts in a list in get all posts
# @router.get("/get_all_posts", name="Get all posts")
def get_posts( # type: ignore
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 100,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print("posts", posts)

    return posts


# Get an individual post based on id
@router.get(
    "/get_post/{id}", name="Get posts by Id", response_model=schemas.PostVoteResponse
)
def get_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = (
        db.query(models.Post, func.count(models.Votes.post_id).label("votes"))
        .join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {id} was not found",
        )

    return post


# Post a single posts
@router.post(
    "/create_post",
    name="Post a posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(user_id=current_user.id, **post.model_dump()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Update a post
@router.put(
    "/update_post/{id}", name="Update posts by Id", response_model=schemas.PostResponse
)
def update_post(
    id: int,
    update_post: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with {id} does not found.",
        )

    if post.user_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform this action.",
        )

    post_query.update(update_post.model_dump(), synchronize_session=False) # type: ignore
    db.commit()

    return post_query.first()


# Delete a single post
@router.delete(
    "/delete_post/{id}", name="Delete posts by Id", status_code=status.HTTP_200_OK
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not found.",
        )

    if post.user_id != current_user.id: # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform this action.",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "Post with id {id} deleted successfully"}
