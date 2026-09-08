from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

CARPETA_PROYECTO = Path(__file__).parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "base-opticaprueba.db"

engine = create_engine(f"sqlite:///{RUTA_BASE_DATOS}", echo=False)

class Base(DeclarativeBase):
    pass

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine) #Esta es la variale para ahcer uso de la tabla de usuarios