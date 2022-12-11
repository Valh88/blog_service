from fastapi import APIRouter, Depends
from db.database import get_db
from sqlalchemy.orm import Session
from db.models import User
from security import get_apikey_header
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
async def get_user_profile(api_key: str = Depends(get_apikey_header),
                           db: Session = Depends(get_db)) -> schemas.UserMeOut:
    """
    Маршрут получения информации о текущем пользователе.
    :param api_key:
    :param service: Сервис для обработки маршрута
    :return: Объект согласно схеме UserOut
    """

    # user = await User.get_user_by_token(db, api_key)

    user = db.query(User).filter(User.id == 2).first()
    user_model = schemas.UserFull(id=user.id, name=user.name, followers=user.followers, followoing=user.following)
    return {"result": True, "user": user_model}
