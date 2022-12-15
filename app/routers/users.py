from fastapi import APIRouter, Depends, HTTPException
from db.database import get_db
from sqlalchemy.orm import Session
from db import models
from security import get_apikey_header, get_current_user
from fastapi import status
import schemas

router = APIRouter(
  prefix='/api',
  tags=['users']
)


@router.get("/users/me", response_model=schemas.UserMeOut,
            summary="Показывает данные текущего пользователя",
            description="Маршрут получения информации о текущем пользователе.",
            response_description="Успешный ответ",
            status_code=status.HTTP_200_OK)
async def get_user_profile(current_user: str = Depends(get_current_user),
                           db: Session = Depends(get_db)) -> schemas.UserMeOut:
    """
    Маршрут получения информации о текущем пользователе.
    :param api_key:
    :param service: Сервис для обработки маршрута
    :return: Объект согласно схеме UserOut
    """
    return {"result": True, "user": current_user}


@router.post('/users/{id:int}/follow')
async def follow_user(id: int, current_user: schemas.UserFull = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    following = current_user.following
    if user in following:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you are following")
    current_user.following.append(user)
    db.add(current_user), db.commit()

    return {"result": True}


@router.delete('/users/{id:int}/follow', )
async def unfollow_user(id: int, current_user: schemas.UserFull = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    following = current_user.following
    if user not in following:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you are following")
    try:
        current_user.following.remove(user)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="you are not following")
    db.add(current_user), db.commit()

    return {"result": True}


@router.get('/users/{id:int}', response_model=schemas.UserMeOut)
async def get_any_users_profile(id: int, curren_user: schemas.UserFull = Depends(get_current_user),
                                db: Session = Depends(get_db)) -> schemas.UserMeOut:
    user = db.query(models.User).filter(models.User.id == id).first()
    return {"result": True, "user": user}
