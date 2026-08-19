"""
logica_usuario.py

Todo lo relacionado con usuarios, en un solo lugar:
  - Conexión a la base de datos
  - El modelo Usuario (el "traductor" entre Python y usuarios.db)
  - Las funciones para crear, consultar, modificar y eliminar usuarios

Tanto el notebook como la app de Flask importan de aquí, para no repetir
la misma lógica en dos lugares distintos.
"""

from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash


# ===========================================================================
# CONEXIÓN Y MODELO
# ===========================================================================

# Path(__file__) es la ruta de ESTE archivo (logica_usuario.py).
# .parent es la carpeta que lo contiene, sin importar desde dónde se
# ejecute el programa. Así, "usuarios.db" siempre se busca al lado de
# este archivo — ya no depende de la carpeta desde donde arranques la
# terminal (que era justo la causa del problema que tenías).
CARPETA_PROYECTO = Path(__file__).parent
RUTA_BASE_DATOS = CARPETA_PROYECTO / "usuarios.db"

engine = create_engine(f"sqlite:///{RUTA_BASE_DATOS}", echo=False)


class Base(DeclarativeBase):
    pass


class Usuario(Base): #Las clases son moldes y estos moldes dan objetos como los moldes de las galletas 
    __tablename__ = "usuarios" #la variable __tablename__ lo que hace es que le indica a usuarios que es una tabla, y que los datos que le va a entregar a delante son los nombres de las columnas

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)
    correo = Column(String(150), nullable=False, unique=True)
    contrasena_hash = Column(String(255), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):  #Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<Usuario {self.nombre} {self.apellido} ({self.rol})>" #el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion



# Crea la tabla si no existe. Si ya existe (como en tu caso), no hace nada.
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine) #Esta es la variale para ahcer uso de la tabla de usuarios

"""
with SessionLocal() as session: #esta funcion imprimira todo lo que contiene la base de datos BORRAR CUANDO NO  SE NECESITE
    usuarios = session.query(Usuario).all()
    for usuario in usuarios:
        print(usuario)  # ← __repr__ de cada uno
"""
# ===========================================================================
# FUNCIONES DE LÓGICA (crear, consultar, modificar, eliminar)
# ===========================================================================
# Cada función abre su propia sesión y la cierra al terminar — así quien
# use estas funciones (el notebook, o una ruta de Flask) no tiene que
# preocuparse de manejar la sesión manualmente cada vez.

def crear_usuario(nombre, apellido, rol, correo, contrasena_texto_plano):
    db = SessionLocal()
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        rol=rol,
        correo=correo,
        contrasena_hash=generate_password_hash(contrasena_texto_plano),
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)  # trae el id ya asignado antes de cerrar
    db.close()
    return nuevo_usuario


def listar_usuarios():
    db = SessionLocal()
    todos = db.query(Usuario).all()
    db.close()
    return todos


def buscar_por_correo(correo):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    db.close()
    return usuario


def verificar_contrasena(correo, contrasena_escrita):
    usuario = buscar_por_correo(correo)
    if usuario is None:
        return False
    return check_password_hash(usuario.contrasena_hash, contrasena_escrita)


def actualizar_usuario(correo, nuevo_nombre=None, nuevo_apellido=None, nuevo_rol=None):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        db.close()
        return None

    if nuevo_nombre:
        usuario.nombre = nuevo_nombre
    if nuevo_apellido:
        usuario.apellido = nuevo_apellido
    if nuevo_rol:
        usuario.rol = nuevo_rol

    db.commit()
    db.close()
    return usuario


def cambiar_contrasena(correo, nueva_contrasena_texto_plano):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        db.close()
        return False

    usuario.contrasena_hash = generate_password_hash(nueva_contrasena_texto_plano)
    db.commit()
    db.close()
    return True


def eliminar_usuario(correo):
    db = SessionLocal()
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if usuario is None:
        db.close()
        return False

    db.delete(usuario)
    db.commit()
    db.close()
    return True