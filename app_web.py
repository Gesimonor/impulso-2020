"""
Versión del login conectada directamente a tu tabla usuarios.db
(la misma que creaste desde el notebook), usando las funciones ya
hechas en logica_usuario.py.

Correr con:  python app_simple.py
Abrir en el navegador:  http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user,
)

from logica_usuario import Usuario, SessionLocal, buscar_por_correo, verificar_contrasena

app = Flask(__name__) # Esta variable le indica a Flask como se llama el archivo y donde buscar los archivos y OJO siempre los html con Flask deben llamarsen templates osea la carpeta porque si no FLask no sabe donde buscar los htmkl
app.secret_key = "cambia-esto-por-una-clave-secreta-real" # y esto es super iportante, resulta que las Cookies de una web guardan los datos miimos para identificarte como ID, rol y correo por ejemplo, si no esta cifrado un hacker tendria axeceso a eso y no lo queremos
#ESTO ES CONFIGURACION DE SEGURIDAD QUE VALIDA QUE SIEMPRE SE LOGUEN Y SI NO PUES NO PUEDES ENTRAR A LA APP
login_manager = LoginManager() #es el gestor de los usuario, Flask por si solo no sabe de usuarios y pide ayuda a LoginManager para hacer como esa duanas en la mpagina web
login_manager.init_app(app) #este instala a LoginManager dentro de la pagina web    
login_manager.login_view = "login" #esta es super importante, si alguien intenta entrar sin estar logeado esta linia dice que automaticamente valla a login.html
login_manager.login_message = "Inicia sesión para continuar." # y este es un mensajito para recordarle que debe hacer login para usar la app


class UsuarioSesion(UserMixin):
""" OJO leer porque esto explica el porque de UserMixin, es un requisieto importante para UsuarioSession pueda ser el puente estre Flask y la BD
Flask-Login exige:      UserMixin responde:
¿esta autenticado?      is_authenticated() : Pregunta si inició sesión correctamente:
¿cuenta activa?         is_active() : UserMixin responde True por defecto — asume que todas las cuentas están activas. (pero si quisieras bloquearlas agregariamos una columna de activo Si o No)
¿es anónimo?            is_anonymous() : Un usuario anónimo es alguien que no inició sesión — solo está navegando o que ya inicio y no mustra "Inciio sesion" si no "Bienenido Luz Stella"
¿cuál es su id?         get_id() : el Id de la base y se usa para muchas cosas :)
"""
    def __init__(self, datos_usuario: Usuario):#Aqui SQLalchemy le entrega a Flask un usuario y de la clase Usuario que ya sabesmos que hablamos de la misma tabla, usuario es un nombre ejempl, no debe ser el mismo si no quieres
        self.id = datos_usuario.id
        self.nombre = datos_usuario.nombre
        self.apellido = datos_usuario.apellido
        self.correo = datos_usuario.correo
        self.rol = datos_usuario.rol
        


@login_manager.user_loader
def cargar_usuario(user_id):
    db = SessionLocal()
    usuario = db.get(Usuario, int(user_id))
    db.close()
    return UsuarioSesion(usuario) if usuario else None


@app.route("/")
def inicio():
    return redirect(url_for("dashboard") if current_user.is_authenticated else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # OJO: el formulario manda el campo con name="email" (así está
        # en tu login.html), pero en tu tabla la columna se llama
        # "correo" — son cosas distintas y está bien que se llamen
        # diferente, solo hay que leer el nombre correcto de cada lado.
        correo_escrito = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Ya no escribimos la consulta aquí — usamos las funciones que
        # ya probamos en logica_usuario.py.
        if verificar_contrasena(correo_escrito, password):
            usuario = buscar_por_correo(correo_escrito)
            login_user(UsuarioSesion(usuario))
            return redirect(url_for("dashboard"))

        flash("Correo o contraseña incorrectos.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard_simple.html", usuario=current_user)


if __name__ == "__main__":
    app.run(debug=True)