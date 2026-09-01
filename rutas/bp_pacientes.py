from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from logica_paciente import crear_paciente, listar_pacientes, consultar_paciente, editar_paciente, eliminar_paciente, buscar_por_id_editar
from  datetime import datetime

blueprint_pacientes = Blueprint("bluep_pacientes", __name__) #le decimos que es un blueprint y que se llama pacientes, el __name__ es para decirle a Flask que este archivo es el que tiene las rutas de pacientes

@blueprint_pacientes.route("/pacientes", methods=["GET", "POST"]) #Get es para traer la pagina y POST es para enviar los datos del formulario
@login_required
#request es un objeto de Flask que contiene toda la información de la petición que llegó
def crear_paciente_route():
    """ 
    Request es un objeto de Flask que contiene toda la información de la petición que llegó.
        request.method      → "GET" o "POST"
        request.form        → los datos del formulario
        request.form.get("nombre")  → el valor del campo "nombre"
        request.url         → la URL completa
        request.args        → parámetros de la URL (?buscar=juan)
    """
    if request.method == "POST":
        crear_paciente(
            documento=request.form.get("documento"),
            nombre=request.form.get("nombre"),
            apellido=request.form.get("apellido"),
            celular=request.form.get("celular"),
            correo=request.form.get("correo"),
            fecha_nacimiento=datetime.strptime(request.form.get("fecha_nacimiento"), "%Y-%m-%d"), #Esto convierte el texto en una fecha legible para la logicas
            direccion=request.form.get("direccion")
        )
        flash("Paciente creado exitosamente") #flash es una funcion de Flask que sirve para mostrar mensajes en la pagina web, en este caso se muestra un mensaje de exito cuando se crea un paciente    
        return redirect(url_for("bluep_pacientes.pacientes")) #1 va en blueprint_pacientes porque es el nombre del blueprint y 2 va en pacientes porque es el nombre de la funcion que tenemos arriba
    """Sin redirect:
        Usuario llena formulario → POST → paciente creado
        Usuario presiona F5 (recargar)
        → el navegador pregunta "¿reenviar el formulario?"
        → ¡crea el paciente dos veces! 💀

        Con redirect:
        Usuario llena formulario → POST → paciente creado
        → redirect a /pacientes → GET limpio
        Usuario presiona F5
        → solo recarga la página, no reenvía el formulario 
    """

    pacientes = listar_pacientes()
    return render_template("pacientes.html", usuario=current_user, pacientes=pacientes)


@blueprint_pacientes.route("/pacientes/editar/<int:id>", methods=["GET", "POST"])
@login_required 
def editar_paciente_route(id):
    paciente = buscar_por_id_editar(id)
    if request.method == "POST":
        editar_paciente(
            id=id,
            documento=request.form.get("documento"),
            nombre=request.form.get("nombre"),
            apellido=request.form.get("apellido"),
            celular=request.form.get("celular"),
            correo=request.form.get("correo"),
            fecha_nacimiento=datetime.strptime(request.form.get("fecha_nacimiento"), "%Y-%m-%d"),
            direccion=request.form.get("direccion")
        )
        flash("Paciente editado exitosamente")
        return redirect(url_for("bluep_pacientes.pacientes"))
    return render_template("editar_paciente.html", usuario=current_user, paciente=paciente)

@blueprint_pacientes.route("/pacientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_paciente_route(id):
    eliminar_paciente(id)
    flash("Paciente eliminado exitosamente")
    return redirect(url_for("bluep_pacientes.pacientes"))
