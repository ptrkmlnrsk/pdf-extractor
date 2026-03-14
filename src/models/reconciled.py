from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Reconciled(Base):
    __tablename__ = "reconciled"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    amount_xlsx: Mapped[float]
    amount_pdf: Mapped[float]
    status: Mapped[str]
