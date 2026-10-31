from flask import Blueprint, render_template
from flask_login import login_required, current_user
from logica_facturas import listar_facturas

blueprint_facturas = Blueprint("bluep_facturas", __name__)

@blueprint_facturas.route("/facturas", methods=["GET"])
@login_required
def listar_facturas_route():
    facturas = listar_facturas()
    return render_template("facturas.html", usuario=current_user, facturas=facturas)