from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infraestructura_db import Base, SessionLocal

class Formula(Base):
    __tablename__ = "formula"

    id = Column(Integer, primary_key=True),
    paciente_id = Column(Integer,ForeignKey("pacientes.id"), nullable=False)
    formula_id = Column(Integer,ForeignKey("formula.id"), nullable=False)

    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    forma_pago = Column(String, nullabñe=False)
    total_pago = Column(int, nullable=True) #Columna calculada por los datos de detalles_compra
    estado = Column(String, nullable=False)#Abonada, Cancelada, Sin monto

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<Formula {self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion




class Detalles_compras(Base):
    __tablename__ = "detalles_compras"

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey("formula.id"), nullable=False)
    cantidad = Column(int, nullable=True)
    detalle = Column(String, nullable=False)
    valor_unidad = Column(int, nullable=True)
    valor_total = Column(int, nullable=True)

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<{self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion


class abonos(Base):
    __tablename__ = "abonos"

    id = Column(Integer, nullable=True)
    factura_id = Column(Integer, ForeignKey("factura.id"), nullable=False)

    pago = Column(int, nullable=True)
    deuda = Column(int, nullable=True) #Columna calculada por los pagos y el total de la deuda.
    forma_pago = Column(String, nullable=True)

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
            return f"<{self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion
    
