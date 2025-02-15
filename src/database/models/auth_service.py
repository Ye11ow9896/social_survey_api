from datetime import date

from .base import Base, str_16, create_comment
from src.lib.utils import utc_now, today
from sqlalchemy.orm import Mapped, mapped_column


class AuthService(Base):
    __tablename__ = "auth_service"
    __table_args__ = create_comment(
        "Таблица для хранения подключенных сервисов к API"
    )

    service_name: Mapped[str_16] = mapped_column(
        comment="Название сервиса для получения доступа к API"
    )
    hash_password: Mapped[str_16] = mapped_column(comment="Хэш пароля сервиса")
    hash_password_updated_at: Mapped[date] = mapped_column(
        default=today,
        onupdate=utc_now,
        comment="Дата обновления пароля. На будущее, когда будет функцинал обновления пароля. Например раз в 3 месяца",
    )
