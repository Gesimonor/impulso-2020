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
    total_pago

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<Paciente {self.nombre} {self.apellido} ({self.correo})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion




class Detalles_compras(Base):
    __tablename__ = "detalles_compras"

    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey("formula.id"), nullable=False)
    cantidad
    detalle
    valor_unidad
    valor_total

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
        return f"<Paciente {self.nombre} {self.apellido} ({self.correo})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion

    
    
