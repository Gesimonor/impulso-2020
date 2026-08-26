
from logica_paciente import Paciente, SessionLocal

with SessionLocal() as session: #esta funcion imprimira todo lo que contiene la base de datos BORRAR CUANDO NO  SE NECESITE
    usuarios = session.query(Paciente).with_entities(   
        Paciente.id,
        Paciente.nombre,
        Paciente.apellido,
        Paciente.celular,
        Paciente.correo,    
        Paciente.fecha_nacimiento,
        Paciente.direccion,
        Paciente.fecha_creacion,
    ).all()
    for usuario in usuarios:
       # todo_usuario = session.query(Paciente).filter(Paciente.id == usuario.id).first()
        print(usuario)  # ← __repr__ de cada uno
