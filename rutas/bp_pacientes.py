from flask import Blueprint
# ← importas Blueprint de Flask

blueprint_pacientes = Blueprint("pacientes", __name__)
# ← creas el plano llamado "pacientes"

@blueprint_pacientes.route("/pacientes")
# ← decorador que dice "cuando visiten /pacientes
#    ejecuta la función de abajo"

def pacientes():
    return "Hola desde pacientes"
# ← la función que se ejecuta