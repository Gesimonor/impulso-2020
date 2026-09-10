from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infraestructura_db import Base, SessionLocal


class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer,ForeignKey("pacientes.id"), nullable=False)
    tipo_formula = Column(String(50), nullable=False, default="propia") #primera fecha de creacion de la formula, se puede cambiar pero es la fecha en que se creo la formula
    fecha_vencimiento = Column(DateTime, nullable=False)  # fecha de vencimiento de la formula no puede
    fecha = Column(DateTime, nullable=False, default=datetime.utcnow)
    prox_control = Column(DateTime, nullable=False)
    observaciones = Column(String(255), nullable=True)

    #Ojo Derecho
    od_esfera = Column(String(10), nullable=True)
    od_cilindro = Column(String(10), nullable=True)
    od_eje = Column(String(10), nullable=True)
    od_adicion = Column(String(10), nullable=True)
    od_alturabifocal = Column(String(10), nullable=True)
    od_distanciainterpupilar = Column(String(10), nullable=True)
    od_color = Column(String(10), nullable=True)

    #Ojo Izquierdo
    oi_esfera = Column(String(10), nullable=True)
    oi_cilindro = Column(String(10), nullable=True)
    oi_eje = Column(String(10), nullable=True)
    oi_adicion = Column(String(10), nullable=True)
    oi_alturabifocal = Column(String(10), nullable=True)
    oi_distanciainterpupilar = Column(String(10), nullable=True)
    oi_color = Column(String(10), nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.utcnow)  #

    def __repr__(self):
        return f"<Formula {self.id} para paciente {self.paciente_id}>"

def crear_formula(paciente_id, prox_control, fecha,fecha_vencimiento=None, observaciones=None,
                   od_esfera=None, od_cilindro=None, od_eje=None, od_adicion=None, od_alturabifocal=None,
                   od_distanciainterpupilar=None, od_color=None,
                   oi_esfera=None, oi_cilindro=None, oi_eje=None, oi_adicion=None, oi_alturabifocal=None,
                   oi_distanciainterpupilar=None, oi_color=None):
  with SessionLocal() as db:
    nueva_formula = Formula(
        fecha=fecha,
        paciente_id=paciente_id,
        fecha_vencimiento=fecha_vencimiento,
        prox_control=prox_control,
        observaciones=observaciones,
        od_esfera=od_esfera,
        od_cilindro=od_cilindro,
        od_eje=od_eje,
        od_adicion=od_adicion,
        od_alturabifocal=od_alturabifocal,
        od_distanciainterpupilar=od_distanciainterpupilar,
        od_color=od_color,
        oi_esfera=oi_esfera,
        oi_cilindro=oi_cilindro,
        oi_eje=oi_eje,
        oi_adicion=oi_adicion,
        oi_alturabifocal=oi_alturabifocal,
        oi_distanciainterpupilar=oi_distanciainterpupilar,
        oi_color=oi_color
    )
    db.add(nueva_formula)
    db.commit()
    db.refresh(nueva_formula)
    return nueva_formula

def consultar_formula_para_editar(id):
    with SessionLocal() as db:
        formulas = db.query(Formula).filter(Formula.id == id).first()
    return formulas

def eliminar_formula(formula_id):
    with SessionLocal() as db:
        formula = db.get(Formula, formula_id)
        if formula:
            db.delete(formula)
            db.commit()
            return True
        return False

def editar_formula(id, paciente_id, prox_control, fecha, fecha_vencimiento, observaciones,
                   od_esfera, od_cilindro, od_eje, od_adicion, od_alturabifocal, od_distanciainterpupilar, od_color,
                   oi_esfera, oi_cilindro, oi_eje, oi_adicion, oi_alturabifocal, oi_distanciainterpupilar, oi_color):
    with SessionLocal() as db:
        formula_db = db.query(Formula).filter(Formula.id == id).first()
        formula_db.paciente_id = paciente_id
        formula_db.prox_control = prox_control
        formula_db.fecha = fecha
        formula_db.fecha_vencimiento = fecha_vencimiento
        formula_db.observaciones = observaciones
        formula_db.od_esfera = od_esfera
        formula_db.od_cilindro = od_cilindro
        formula_db.od_eje = od_eje
        formula_db.od_adicion = od_adicion
        formula_db.od_alturabifocal = od_alturabifocal
        formula_db.od_distanciainterpupilar = od_distanciainterpupilar
        formula_db.od_color = od_color
        formula_db.oi_esfera = oi_esfera
        formula_db.oi_cilindro = oi_cilindro
        formula_db.oi_eje = oi_eje
        formula_db.oi_adicion = oi_adicion
        formula_db.oi_alturabifocal = oi_alturabifocal
        formula_db.oi_distanciainterpupilar = oi_distanciainterpupilar
        formula_db.oi_color = oi_color
        db.commit()
        db.refresh(formula_db)
        return formula_db

def listar_formulas():
    db = SessionLocal()
    ultimas_20formulas = db.query(Formula).order_by(Formula.fecha_creacion).limit(20).all()
    db.close()
    return ultimas_20formulas