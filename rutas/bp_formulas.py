from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from logica_formulas import crear_formula, consultar_formulas_por_paciente, editar_formula, eliminar_formula
from  datetime import datetime



blueprint_formulas = Blueprint("bluep_formulas", __name__) #le decimos que es un blueprint y que se llama formulas, el __name__ es para decirle a Flask que este archivo es el que tiene las rutas de formulas

@blueprint_formulas.route("/formulas", methods=["GET", "POST"]) #Get es para traer la pagina y POST es para enviar los datos del formulario
@login_required