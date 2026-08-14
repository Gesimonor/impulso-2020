"""
Base de datos de usuarios con SQLAlchemy.
Campos: Nombre, Apellido, Rol, Correo, Contraseña (encriptada), Fecha de creación.

Dividido en procesos:
  PROCESO 1 — Conexión a la base de datos
  PROCESO 2 — Definición de la tabla
  PROCESO 3 — Apertura de la sesión de trabajo
  PROCESO 4 — Crear usuarios
  PROCESO 5 — Consultar usuarios
  PROCESO 6 — Modificar usuarios
  PROCESO 7 — Eliminar usuarios
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash


# ===========================================================================
# PROCESO 1 — Conexión a la base de datos
# ===========================================================================

# create_engine() abre el archivo de base de datos. Si "usuarios.db" no
# existe todavía, lo crea automáticamente. Si ya existe, lo abre tal cual.
# "sqlite:///" es el prefijo que le dice a SQLAlchemy qué motor usar
# (en este caso SQLite); el nombre después de eso es el archivo.
engine = create_engine("sqlite:///usuarios_sqlalchemy.db", echo=False)

# declarative_base() crea una "clase base" de la cual van a heredar
# todas las tablas que definas. Es lo que conecta tus clases de Python
# con tablas reales de la base de datos.
Base = declarative_base()


# ===========================================================================
# PROCESO 2 — Definición de la tabla
# ===========================================================================

class Usuario(Base):
    # Nombre real de la tabla dentro del archivo de base de datos.
    __tablename__ = "usuarios"

    # Columna id: número único que identifica cada fila.
    # primary_key=True significa que es el identificador principal de la
    # tabla, y SQLAlchemy lo va aumentando solo (1, 2, 3...) en cada
    # usuario nuevo, sin que tengas que asignarlo tú.
    id = Column(Integer, primary_key=True)

    # Columnas de texto normales. nullable=False significa que el campo
    # es obligatorio: no se puede guardar un usuario sin nombre.
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    rol = Column(String(50), nullable=False)

    # unique=True impide que se repita el mismo correo en dos usuarios
    # distintos. Si lo intentas, SQLAlchemy lanza un error automáticamente.
    correo = Column(String(150), nullable=False, unique=True)

    # Aquí se guarda la contraseña ya encriptada (nunca la original).
    contrasena_hash = Column(String(255), nullable=False)

    # default=datetime.utcnow significa que, si no se especifica una
    # fecha al crear el usuario, se pone la fecha y hora actuales
    # automáticamente.
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        # Define cómo se ve un usuario cuando lo imprimes en consola.
        # Solo es para que sea más fácil leer los resultados; no afecta
        # el funcionamiento de la base de datos.
        return f"<Usuario {self.nombre} {self.apellido} ({self.rol})>"


# Esta línea revisa la clase Usuario de arriba y crea la tabla real en
# el archivo de base de datos. Si la tabla ya existe, no hace nada
# (es seguro correr esta línea muchas veces).
Base.metadata.create_all(engine)


# ===========================================================================
# PROCESO 3 — Apertura de la sesión de trabajo
# ===========================================================================

# sessionmaker crea una "fábrica" de sesiones conectada a tu base de
# datos (engine). Una sesión es tu canal de trabajo: por ahí es que
# vas a crear, consultar, modificar y borrar usuarios.
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()


# ===========================================================================
# PROCESO 4 — Crear usuarios
# ===========================================================================

def crear_usuario(nombre, apellido, rol, correo, contrasena_texto_plano):
    # generate_password_hash() convierte la contraseña en un texto
    # cifrado e irreversible. Ni mirando la base de datos se puede
    # saber cuál era la contraseña original — solo se puede comparar
    # (ver verificar_contrasena más abajo).
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        rol=rol,
        correo=correo,
        contrasena_hash=generate_password_hash(contrasena_texto_plano),
        # fecha_creacion no se escribe a mano: el default del modelo
        # ya se encarga de ponerla automáticamente.
    )

    # add() marca el objeto como "listo para guardar".
    db.add(nuevo_usuario)
    # commit() es el que de verdad escribe el cambio en el archivo.
    # Antes de esta línea, el usuario todavía no existe en el archivo.
    db.commit()

    print(f"Usuario creado: {nuevo_usuario}")
    return nuevo_usuario


# ===========================================================================
# PROCESO 5 — Consultar usuarios
# ===========================================================================

def listar_usuarios():
    # db.query(Usuario) arma una consulta sobre la tabla de usuarios.
    # .all() trae TODAS las filas que existan.
    todos = db.query(Usuario).all()
    for u in todos:
        print(u)
    return todos


def buscar_por_correo(correo):
    # .filter(...) agrega la condición "donde el correo sea igual a...".
    # .first() trae solo el primer resultado que cumpla la condición,
    # o None si no encuentra ninguno.
    return db.query(Usuario).filter(Usuario.correo == correo).first()


def verificar_contrasena(correo, contrasena_escrita):
    usuario = buscar_por_correo(correo)
    if usuario is None:
        # Ese correo no existe en la base de datos.
        return False

    # check_password_hash toma la contraseña que se acaba de escribir,
    # la encripta con la misma fórmula, y compara si coincide con el
    # hash guardado. Nunca "desencripta" nada, solo compara.
    return check_password_hash(usuario.contrasena_hash, contrasena_escrita)


# ===========================================================================
# PROCESO 6 — Modificar usuarios
# ===========================================================================

def actualizar_usuario(correo, nuevo_nombre=None, nuevo_apellido=None, nuevo_rol=None):
    usuario = buscar_por_correo(correo)
    if usuario is None:
        print("No existe ese usuario.")
        return

    # Se cambia el atributo directamente, como si fuera una variable
    # normal de Python. Solo se actualizan los campos que sí se pasaron
    # (los que quedan en None no se tocan).
    if nuevo_nombre:
        usuario.nombre = nuevo_nombre
    if nuevo_apellido:
        usuario.apellido = nuevo_apellido
    if nuevo_rol:
        usuario.rol = nuevo_rol

    # Aquí es cuando SQLAlchemy detecta qué cambió y lo guarda de verdad.
    db.commit()
    print(f"Usuario {correo} actualizado.")


def cambiar_contrasena(correo, nueva_contrasena_texto_plano):
    usuario = buscar_por_correo(correo)
    if usuario is None:
        print("No existe ese usuario.")
        return

    usuario.contrasena_hash = generate_password_hash(nueva_contrasena_texto_plano)
    db.commit()
    print(f"Contraseña actualizada para {correo}.")


# ===========================================================================
# PROCESO 7 — Eliminar usuarios
# ===========================================================================

def eliminar_usuario(correo):
    usuario = buscar_por_correo(correo)
    if usuario is None:
        print("No existe ese usuario.")
        return

    # delete() marca el objeto para ser borrado.
    db.delete(usuario)
    # commit() ejecuta el borrado real en el archivo.
    db.commit()
    print(f"Usuario {correo} eliminado.")


# ===========================================================================
# Prueba de todos los procesos
# ===========================================================================

if __name__ == "__main__":
    crear_usuario("Ana", "Gómez", "optometra", "ana@visionclara.com", "clave123")

    print(verificar_contrasena("ana@visionclara.com", "clave123"))      # True
    print(verificar_contrasena("ana@visionclara.com", "clave-mala"))    # False

    print("\n--- Antes de actualizar ---")
    listar_usuarios()

    actualizar_usuario("ana@visionclara.com", nuevo_apellido="Gómez Rodríguez")
    cambiar_contrasena("ana@visionclara.com", "clave-nueva-456")

    print("\n--- Después de actualizar ---")
    listar_usuarios()

    db.close()
