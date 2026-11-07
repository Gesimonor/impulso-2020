from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infraestructura_db import Base, SessionLocal
from sqlalchemy.orm import relationship, joinedload

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True)
    numero_factura = Column(Integer, nullable=False) #obligatorio
    paciente_id = Column(Integer,ForeignKey("pacientes.id"), nullable=False) #obligatorio
    formula_id = Column(Integer,ForeignKey("formulas.id"), nullable=True) #Opcional

    fecha = Column(DateTime, nullable=False, default=datetime.utcnow) #Obligatorio
    estado = Column(String, nullable=False)#Abonada, Cancelada, Sin monto

    #Columnas foraneas
    paciente = relationship("Paciente")
    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<Factura {self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion

class Detalles_compras(Base):
    __tablename__ = "detalles_compras"

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    cantidad = Column(Integer, nullable=True)
    detalle = Column(String, nullable=False)
    valor_unidad = Column(Integer, nullable=True)

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<{self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion


class Abonos(Base):
    __tablename__ = "abonos"

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)

    pago = Column(Integer, nullable=True)
    forma_pago = Column(String, nullable=True)

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
            return f"<{self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion
    


def listar_facturas():
    with SessionLocal() as db:
        facturas = db.query(Factura)\
                     .options(joinedload(Factura.paciente))\
                     .order_by(Factura.fecha).limit(20).all()
    return facturas