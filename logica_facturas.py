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
    detalles_compras_id = Column(Integer, ForeignKey("detalles_compras.id"), nullable=True) #Opcional
    abonos_id = Column(Integer, ForeignKey("abonos.id"), nullable=True) 

    fecha = Column(DateTime, nullable=False, default=datetime.utcnow) #Obligatorio
    fecha_vencimiento = Column( DateTime, nullable=True, default=datetime)
    estado = Column(String, nullable=False)#Abonada, Cancelada, Sin monto
    forma_pago = Column(String, nullable=False)
    observacion = Column(String, nullable=False)

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
    medio_pago = Column(String, nullable=True)

    def __repr__(self):#Este __repr__ es una variable especial que se encarga de ejecutarse cuando llamas al objeto creado con el molde es bueno para mirar que creaste o que se creo
            return f"<{self.id})>"#el self es un espacio de memoria temporal para almacenar lo que contiene el objeto y posterior ponerlo en la varibale correspodiente es como el carrito que lleva las maletas de la recepion a la habitacion
    


def listar_facturas():
    with SessionLocal() as db:
        facturas = db.query(Factura)\
                     .options(joinedload(Factura.paciente))\
                     .order_by(Factura.fecha).limit(20).all()
    return facturas


def crear_factura(paciente_id, formula_id, fecha, observacion, cantidad, detalle, valor_unitario, pago, forma_pago):
    with SessionLocal() as db:
        nueva_factura = Factura(
            numero_factura = db.query(Factura).count() + 1,  # Generar un número de factura consecutivo
            paciente_id=paciente_id, #datos que traigo del html porque ya existen 
            formula_id=formula_id,  #datos que traigo del html porque ya existen 
            
            fecha=fecha,
            fecha_vencimiento=None,  # Puedes ajustar esto según tus necesidades
            estado="Sin monto",  # Estado inicial de la factura
            forma_pago=forma_pago,
            observacion=observacion)
        
        db.add(nueva_factura)
        db.flush() #usamos este porque commit no se ejecuta hasta que se cierre la sesion y necesitamos el id de la factura para crear los detalles de compras
        
        crear_detalles_compras(nueva_factura.id, cantidad, detalle, valor_unitario)
    return nueva_factura

def crear_detalles_compras(factura_id, cantidad, detalle, valor_unitario):
    with SessionLocal() as db:
        nuevo_detalle = Detalles_compras(
            factura_id=factura_id,
            cantidad=cantidad,
            detalle=detalle,
            valor_unidad=valor_unitario
        )
        db.add(nuevo_detalle)
        db.commit()
    return nuevo_detalle