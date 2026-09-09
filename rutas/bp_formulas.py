from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from logica_formulas import crear_formula, consultar_formula_para_editar, editar_formula, eliminar_formula, listar_formulas
from  datetime import datetime
from dateutil.relativedelta import relativedelta

blueprint_formulas = Blueprint("bluep_formulas", __name__) #le decimos que es un blueprint y que se llama formulas, el __name__ es para decirle a Flask que este archivo es el que tiene las rutas de formulas

@blueprint_formulas.route("/formulas", methods=["GET", "POST"]) #Get es para traer la pagina y POST es para enviar los datos del formulario
@login_required
def crear_formula_route(): #Crea y precarga la lista de las formulas 
    if request.method == "POST":
        prox_control_int= int(request.form.get("prox_control"))
        prox_control_date = (datetime.strptime(request.form.get("fecha"), "%Y-%m-%d")) + relativedelta(months=prox_control_int)
        crear_formula(request.form.get("paciente_id"),
                      prox_control=prox_control_date,
                      fecha = datetime.strptime(request.form.get("fecha"), "%Y-%m-%d"),
                      fecha_vencimiento=datetime.strptime(request.form.get("fecha_vencimiento"), "%Y-%m-%d") if request.form.get("fecha_vencimiento") else None, #que si el campo fecha_vencimiento no esta vacio, si no esta vacio lo convierte a datetime, si esta vacio lo deja en None
                      observaciones=request.form.get("observaciones"),
                      od_esfera=request.form.get("od_esfera"),
                      od_cilindro=request.form.get("od_cilindro"),
                      od_eje=request.form.get("od_eje"),
                      od_adicion=request.form.get("od_adicion"),
                      od_alturabifocal=request.form.get("od_alturabifocal"),
                      od_distanciainterpupilar=request.form.get("od_distanciainterpupilar"),
                      od_color=request.form.get("od_color"),
                      oi_esfera=request.form.get("oi_esfera"),
                      oi_cilindro=request.form.get("oi_cilindro"),
                      oi_eje=request.form.get("oi_eje"),
                      oi_adicion=request.form.get("oi_adicion"),
                      oi_alturabifocal=request.form.get("oi_alturabifocal"),
                      oi_distanciainterpupilar=request.form.get("oi_distanciainterpupilar"),
                      oi_color=request.form.get("oi_color")
        )
        flash("Fórmula creada exitosamente")
        return redirect(url_for("bluep_formulas.crear_formula_route"))
    formulas = listar_formulas()
    return render_template("formulas.html", usuario=current_user, formulas=formulas)

@blueprint_formulas.route("/formulas/editar/<int:id>", methods=["GET", "POST"]) 
@login_required
def editar_formula_route(id): #EDita y prellena los campos 
    formula = consultar_formula_para_editar(id)
    return render_template("editar_formula.html",  usuario=current_user,formula=formula) #GET y se usa  usuario=current_user porque en la base.html tenemos un Bienvenido <usuario ese el nombre y debe llenar ese hueco con susuario

@blueprint_formulas.route("/formulas/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_formula_route(id):
    eliminar_formula(id)
    flash("Fórmula eliminada exitosamente")
    return redirect(url_for("bluep_formulas.crear_formula_route"))

        