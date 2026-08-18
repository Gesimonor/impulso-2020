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

app = Flask(__name__)
app.secret_key = "cambia-esto-por-una-clave-secreta-real"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Inicia sesión para continuar."


class UsuarioSesion(UserMixin):
    """Envoltorio que necesita Flask-Login para manejar la sesión.
    No cambia nada de tu tabla, solo la hace compatible."""
    def __init__(self, usuario: Usuario):
        self.id = usuario.id
        self.nombre = usuario.nombre
        self.apellido = usuario.apellido
        self.correo = usuario.correo
        self.rol = usuario.rol


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