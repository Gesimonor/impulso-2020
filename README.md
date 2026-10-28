# pip install -r requirements.txt
#py -m pip install flask

{{ url_for('bluep_pacientes.ver_paciente_route', id=paciente.id) }}

Cosas por hacer

🔴 Rompen
ver_paciente.html — </div> y </form> al revés
ver_paciente.html — botón Ver de fórmulas apunta a crear_formula_route
editar_formula.html — Cancelar apunta a ruta POST → error 405
ver_formula.html — Volver, mismo problema
editar_paciente.html — Cancelar, mismo problema
🟡 No funcionan
El {{ today }} en dos plantillas, nadie lo pasa
El <select> de pacientes sin la variable pacientes
editar_formula.html — campo de paciente editable
Botones Cita y Factura apuntando a fórmulas
🟢 Cosméticos
Comentarios desactualizados en base.html
TODO ya cumplidos
El <form> vacío en pacientes.html

Los 4, 5 y 6 son el mismo error y se arreglan igual: cambiar el url_for a la ruta de listar.