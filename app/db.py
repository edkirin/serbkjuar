from typing import Optional

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.conf import AppConfig

Base = declarative_base()


class MachineModel(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True)
    external_id = Column(String)

    @classmethod
    def get_by_id(cls, session: Session, id: int) -> Optional["MachineModel"]:
        return session.query(cls).filter(cls.id == id).one_or_none()


def create_db_session(
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_name: str,
) -> Session:
    connection_url = (
        "postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}".format(
            db_user=db_user,
            db_password=db_password,
            db_host=db_host,
            db_port=db_port,
            db_name=db_name,
        )
    )

    engine = create_engine(connection_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
