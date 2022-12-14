from fastapi import APIRouter, Depends, HTTPException, status
import schemas
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from security import get_current_user
from settings import logger

router = APIRouter(prefix="/api", tags=["tweets"])


@router.get("/tweets", response_model=schemas.TweetResult)
@logger.catch
async def all_tweets(
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> schemas.TweetResult:
    tweets = db.query(models.Tweet).order_by(models.Tweet.created_at.desc()).all()
    return {
        "result": True,
        "tweets": [
            schemas.TweetsOut(
                id=tweet.id,
                content=tweet.content,
                author=tweet.author,
                likes=[{"user_id": user.id, "name": user.name} for user in tweet.likes],
                attachments=tweet.get_list_path(),
            )
            for tweet in tweets
        ],
    }


@router.post("/tweets")
@logger.catch
async def create_tweet(
    tweet: schemas.TweetAdd,
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pictures = (
        db.query(models.Picture)
        .filter(models.Picture.id.in_(tweet.tweet_media_ids))
        .all()
    )
    tweet = models.Tweet(content=tweet.tweet_data, author_id=current_user.id)
    [tweet.attachments.append(pick) for pick in pictures]
    db.add(tweet), db.commit()
    return {"result": True, "tweet_id": tweet.id}


@router.delete("/tweets/{id:int}")
@logger.catch
async def delete_tweet(
    id: int,
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if tweet.author == current_user:
        db.delete(tweet), db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tweet not found and delete only yours tweet",
        )
    return {"result": True}


@router.post("/tweets/{id:int}/likes")
@logger.catch
async def like_tweet(
    id: int,
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = db.query(models.Tweet).filter(models.Tweet.id == id).first()
    if tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="tweet not found"
        )
    tweet.likes.append(current_user)
    db.add(tweet), db.commit()
    return {"result": True}


@router.delete("/tweets/{id:int}/likes")
@logger.catch
async def delete_like_tweet(
    id: int,
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tweet = (
        db.query(models.Tweet)
        .filter(models.Tweet.id == id and models.Tweet.author == current_user)
        .first()
    )
    if tweet is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="tweet not found"
        )
    try:
        tweet.likes.remove(current_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="like not found"
        )
    db.add(tweet), db.commit()
    return {"result": True}


@router.delete("/tweets/{id:int}/follow")
@logger.catch
async def unfollow_user(
    id: int,
    current_user: schemas.UserFull = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    following = current_user.following
    if user not in following:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="you are following"
        )
    try:
        current_user.following.remove(user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="you are not following"
        )
    db.add(current_user), db.commit()
    return {"result": True}
