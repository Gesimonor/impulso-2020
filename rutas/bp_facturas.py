from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from logica_facturas import listar_facturas

blueprint_facturas = Blueprint("bluep_facturas", __name__)

@blueprint_facturas.route("/facturas", methods=["GET"])
@login_required
def listar_facturas_route():
    facturas = listar_facturas()
    return render_template("facturas.html", usuario=current_user, facturas=facturas)

@blueprint_facturas.route("/facturas/crear-factura", methods=["POST"])
@login_required
def crear_factura_route():
    paciente_id = request.form.get("paciente_id")
    formula_id = request.form.get("formula_id")

    #numero_factura es un dato que debe tratarse como el id , debe ser consecutivo
    fecha = request.form.get("fecha")
    #estado = request.form.get("estado") pendiente calacular este dato con la base de abonos y detalles de compras

    #Tabla detalles_compras
    cantidad = request.form.getlist("cantidad[]")
    detalle = request.form.getlist("detalle[]")
    valor_unitario = request.form.getlist("valor_unitario[]")

    #tabla de abono
    pago = request.form.get("pago")
