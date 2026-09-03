"""
Versión del login conectada directamente a tu tabla usuarios.db
(la misma que creaste desde el notebook), usando las funciones ya
hechas en logica_usuario.py.

Correr con:  python app_simple.py
Abrir en el navegador:  http://127.0.0.1:5000
Info de puertos importante
0 - 1023    → reservados del sistema, no tocar 
1024 - 65535 → libres para usar 

Info de IP 
El rango 127.x.x.x está reservado para localhost:

127.0.0.1  → el más usado
127.0.0.2  → también es localhost
127.0.0.3  → también es localhost
...hasta 127.255.255.255

http://localhost/      → mismo que 127.0.0.1
http://127.0.0.1/      → mismo que localhost
"""
from rutas.bp_pacientes import blueprint_pacientes    #Esto trae he ,importa y trae la carpeta de ruta
from rutas.bp_formulas import blueprint_formulas    #Esto trae he ,importa y trae la carpeta de ruta
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user,
)

from logica_usuario import Usuario, SessionLocal, buscar_por_correo, verificar_contrasena

app = Flask(__name__) # Esta variable le indica a Flask como se llama el archivo y donde buscar los archivos y OJO siempre los html con Flask deben llamarsen templates osea la carpeta porque si no FLask no sabe donde buscar los htmkl
app.secret_key = "cambia-esto-por-una-clave-secreta-real" # y esto es super iportante, resulta que las Cookies de una web guardan los datos miimos para identificarte como ID, rol y correo por ejemplo, si no esta cifrado un hacker tendria axeceso a eso y no lo queremos


# Blueprint
app.register_blueprint(blueprint_pacientes)#Esta es la que trae el blueprint de pacientes
app.register_blueprint(blueprint_formulas) #Esta es la que trae el blueprint de formulas


#ESTO ES CONFIGURACION DE SEGURIDAD QUE VALIDA QUE SIEMPRE SE LOGUEN Y SI NO PUES NO PUEDES ENTRAR A LA APP

login_manager = LoginManager() #es el gestor de los usuario, Flask por si solo no sabe de usuarios y pide ayuda a LoginManager para hacer como esa duanas en la mpagina web
login_manager.init_app(app) #este instala a LoginManager dentro de la pagina web    
login_manager.login_view = "login" #esta es super importante, si alguien intenta entrar sin estar logeado esta linia dice que automaticamente valla a login.html
login_manager.login_message = "Inicia sesión para continuar." # y este es un mensajito para recordarle que debe hacer login para usar la app


class UsuarioSesion(UserMixin):
    """ 
    OJO leer porque esto explica el porque de UserMixin, es un requisieto importante para UsuarioSession pueda ser el puente estre Flask y la BD
    Flask-Login exige:      UserMixin responde:
    ¿esta autenticado?      is_authenticated() : Pregunta si inició sesión correctamente:
    ¿cuenta activa?         is_active() : UserMixin responde True por defecto — asume que todas las cuentas están activas. (pero si quisieras bloquearlas agregariamos una columna de activo Si o No)
    ¿es anónimo?            is_anonymous() : Un usuario anónimo es alguien que no inició sesión — solo está navegando o que ya inicio y no mustra "Inciio sesion" si no "Bienenido Luz Stella"
    ¿cuál es su id?         get_id() : el Id de la base y se usa para muchas cosas :)
    """
    def __init__(self, datos_usuario: Usuario):#Aqui SQLalchemy le entrega a Flask un usuario y de la clase Usuario que ya sabesmos que hablamos de la misma tabla, usuario es un nombre ejempl, no debe ser el mismo si no quieres
        self.id = datos_usuario.id
        self.nombre = datos_usuario.nombre
        self.correo = datos_usuario.correo
        self.rol = datos_usuario.rol
        
#LA DE VALIDACION DEL LOGIN
#Ojo importante esta porque valida que el usuario sigue en loguin, si hace un movimiento dentro de la app valida que el siga en login y aparte que exista en la base
@login_manager.user_loader #Esta vaina es un Decorador, para que sirve para meter una funcion a otra funcion. EN este caso vamos a usar la funcion de cargar_usuario para la c@login_manager.user_loader , y se coloca asi pegadita con un @
def cargar_usuario(user_id):
    db = SessionLocal()
    usuario = db.get(Usuario, int(user_id)) #esto es esto db.query(Usuario).filter(Usuario.id == user_id).first() solo que como buena practica se usa Get
    db.close()
    return UsuarioSesion(usuario) if usuario else None



#LA DEL INICIO
@app.route("/") #este ami / es el http://127.0.0.1:5000 es la pagina de inicio si no quisieras es se puede por ejemplo @app.route("/login")
def inicio():
    #Aqui lo que quiere decir es ¿Estas en login? SI: Ve a app-layout NO: Ve a el lgoin 
    return redirect(url_for("applayout") if current_user.is_authenticated else url_for("login"))

"""
GET  → la página con los input vacíos 
POST → los input llenos enviados al servidor 
"""
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("applayout"))

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
            return redirect(url_for("base"))

        flash("Correo o contraseña incorrectos.") #Este si la validacion no funciona
        return redirect(url_for("login"))
    #Y este es el estado del GET
    return render_template("login.html")



#Cerrar Sesion
@app.route("/logout")
@login_required
def logout():
    logout_user() #Este miguito borra de las cookies el ID y cierra sesion
    return redirect(url_for("applayout"))

#Es la página principal después del login
@app.route("/applayout")
@login_required
def applayout():
    return render_template("app-layout.html", usuario=current_user)


#Esto corre el servicio
if __name__ == "__main__": # el if valida que  que lo estan corriendo a el y no que estan usando de el
    app.run(debug=True)
