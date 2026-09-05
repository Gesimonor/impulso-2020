# 📓 Cuaderno de Impulso 20/20

> Este archivo es dos cosas a la vez:
> 1. **Mi manual de instrucciones** (Claude lo lee solo, al empezar cada sesión).
> 2. **Tu cuaderno de repaso** — lo que has aprendido, el glosario y los tips.
>
> Léelo cuando quieras refrescar. Está escrito para ti, no para un robot.

---

## PARTE 0 — Instrucciones para Claude

**Cómo quiere trabajar Luz Stella:**

- ✋ **Explica ANTES de tocar.** Di qué vas a hacer y por qué, y espera el OK.
- 🐢 **Paso a paso.** Un cambio, pausa, explicación, seguimos. No diez archivos de golpe.
- 🎓 **Enseña, no solo resuelvas.** El objetivo es que ella entienda el código, no que aparezca solo.
- 🚫 **NUNCA borres ni "limpies" los comentarios del código.** Son sus apuntes de estudio.
  Están ahí a propósito. Si un comentario está desactualizado, díselo — no lo borres tú.
- 💬 **Español, y sin dar por sentado el vocabulario técnico.** Si usas una palabra rara,
  explícala en la misma frase.
- 🔍 **Justifica.** "Puse X porque si no pasa Y" vale más que el código en sí.

---

# PARTE 1 — Qué es este proyecto

**Impulso 20/20** es el sistema de una óptica. Tiene **dos programas distintos** que
comparten la misma carpeta (y esto confunde al principio, ojo):

| Programa | Archivo | Qué es | Tecnología |
|---|---|---|---|
| 🖥️ **El de escritorio** | `app.py` | Facturación: crea PDFs, manda WhatsApp, lee Google Sheets | Tkinter |
| 🌐 **El de la web** | `app_web.py` | Login + pacientes + fórmulas | Flask |

Ahora mismo estás construyendo **el de la web**. El de escritorio es el trabajo anterior,
que ya funciona.

## El mapa de la app web

```
app_web.py ............ El "director de orquesta". Arranca Flask, monta el login,
│                       y engancha los blueprints.
│
├── rutas/ ............ Las PUERTAS. Reciben lo que escribe el usuario en el navegador.
│   ├── bp_pacientes.py
│   └── bp_formulas.py
│
├── logica_*.py ....... El CEREBRO. Saben hablar con la base de datos. No saben nada de web.
│   ├── logica_usuario.py
│   ├── logica_paciente.py
│   └── logica_formulas.py
│
├── templates/ ........ La CARA. El HTML que ve la persona.
│   ├── base.html ..... el molde del que heredan todas
│   └── (las demás)
│
└── base-opticaprueba.db  La base de datos (SQLite: un archivo, no un servidor)
```

**La idea grande que ya aplicaste sin que nadie te lo dijera:** separar *rutas* de *lógica*.
Tú misma lo escribiste en `logica_paciente.py`:

> `logica_paciente.py → sabe de BASE DE DATOS`

Eso tiene nombre elegante: **separación de responsabilidades**. Cada archivo hace UNA cosa.
Es de las mejores decisiones del proyecto. 👏

---

# PARTE 2 — Lo que has aprendido (resumen)

### 🧱 Programación orientada a objetos
- Una **clase** es un molde de galletas; los **objetos** son las galletas.
  (Tu propia comparación, y es exacta.)
- `self` = "esta galleta en concreto". Tu metáfora del carrito del hotel funciona igual de bien.
- `__repr__` = cómo se ve el objeto cuando lo imprimes. Sirve muchísimo para depurar.

### 🗄️ Bases de datos con ORM
- **ORM** = escribes Python, y él escribe el SQL por ti.
- La clase `Paciente` **ES** la tabla `pacientes`. Mismo objeto, dos idiomas.
- El ciclo de vida siempre es el mismo: `abrir sesión → hacer algo → commit → close`.
- `commit()` es el "guardar de verdad". Sin él, no pasó nada.

### 🌐 Cómo funciona la web por dentro
- **GET** = "dame la página" (formulario vacío). **POST** = "toma estos datos" (formulario lleno).
- El **patrón POST → Redirect → GET**: lo descubriste tú sola y lo documentaste.
  Sin el redirect, apretar F5 crea el paciente dos veces. 💀
- Los **puertos** y el rango `127.x.x.x`. Ese comentario tuyo en `app_web.py` es
  mejor que muchos tutoriales.

### 🔐 Seguridad
- Las contraseñas **nunca** se guardan tal cual. Se guarda el **hash**.
- Un hash va en una sola dirección: puedes verificar, pero no puedes revertir.
- Por eso la columna se llama `contrasena_hash` y no `contrasena`. El nombre importa.
- La `secret_key` firma las cookies. Sin ella, cualquiera se hace pasar por admin.

### 🎨 Plantillas
- `base.html` es el molde; las demás hacen `{% extends %}` y solo rellenan los huecos (`block`).
- Cambias el menú en un sitio → cambia en toda la app. Eso es **DRY**
  (*Don't Repeat Yourself* — no te repitas).

### 🧩 Blueprints
- Cuando `app_web.py` empezó a crecer, lo partiste en blueprints.
  Es exactamente el momento correcto para hacerlo.

### 🐛 Errores de los que aprendiste
- El de las rutas relativas: por eso ahora usas `Path(__file__).parent`.
  Así el `.db` se busca **al lado del archivo**, no donde esté parada la terminal.
- Que el formulario diga `name="email"` y la columna se llame `correo` **no es un error** —
  son dos mundos distintos. Solo hay que leer el nombre correcto en cada lado.

---

# PARTE 3 — 📖 Glosario de palabras raras

## Python general

| Palabra | Qué significa en cristiano |
|---|---|
| **clase** | Un molde. `class Paciente` = el molde de los pacientes. |
| **objeto / instancia** | La galleta que sale del molde. Un paciente concreto. |
| **atributo** | Un dato del objeto. `paciente.nombre`. |
| **método** | Una función que vive dentro de una clase. |
| **`self`** | "yo mismo, este objeto en particular". |
| **`__init__`** | El constructor. Se ejecuta al nacer el objeto. |
| **`__repr__`** | Cómo se imprime el objeto. |
| **dunder** | Nombre de cariño para `__loquesea__` (*double underscore*). |
| **`__name__`** | Cómo se llama el archivo que corre. Vale `"__main__"` si lo ejecutas directamente. |
| **`if __name__ == "__main__"`** | "Solo haz esto si me estás EJECUTANDO, no si me estás importando". |
| **decorador** | El `@algo` pegadito encima de una función. Le añade poderes sin tocarla por dentro. Tu explicación ("meter una función en otra función") es correcta. |
| **`*args`** | "acepta todos los argumentos sueltos que vengan". |
| **`**kwargs`** | "acepta todos los argumentos con nombre". Un diccionario. Lo usas en `editar_formula`. |
| **`with` (context manager)** | "abre esto, y ciérramelo tú solito aunque explote todo". Más seguro que `abrir/cerrar` a mano. |
| **`None`** | "no hay nada aquí". OJO: no es `0` ni `""`, es la ausencia. |
| **booleano** | `True` o `False`. Nada más. |
| **`hasattr` / `setattr`** | "¿tiene este atributo?" / "ponle este atributo". |
| **`strptime`** | *string parse time* → convierte texto `"2024-05-10"` en fecha de verdad. |
| **`strftime`** | Al revés: fecha → texto. (La `p` es *parse*, la `f` es *format*.) |
| **`Path`** | Forma moderna y segura de manejar rutas de carpetas. |

## Bases de datos / SQLAlchemy

| Palabra | Qué significa |
|---|---|
| **SQLite** | Base de datos que es *un solo archivo*. Sin servidor. Perfecta para empezar. |
| **ORM** | *Object Relational Mapping*. El traductor Python ↔ SQL. |
| **SQLAlchemy** | El ORM que usas. |
| **`engine`** | El cable que conecta con la base. Se crea una vez. |
| **`session`** | La conversación con la base. Se abre, se usa, se cierra. |
| **`sessionmaker`** | La fábrica de sesiones. `SessionLocal()` crea una nueva. |
| **`Base` / `DeclarativeBase`** | El molde padre del que heredan todas tus tablas. |
| **`metadata.create_all()`** | "crea las tablas si no existen". Si existen, no hace nada. |
| **`commit()`** | GUARDAR DE VERDAD. Sin esto, nada se escribe. |
| **`refresh()`** | "vuelve a leer de la base" — sirve para traer el `id` recién asignado. |
| **`query().filter().first()`** | SELECT ... WHERE ... y dame el primero (un objeto). |
| **`.all()`** | Dame todos (una lista). |
| **`.limit(20)`** | Máximo 20. |
| **`order_by()`** | Ordenar. |
| **`primary_key`** | La columna que identifica de forma única. Tu `id`. |
| **`ForeignKey`** | "esta columna apunta a la fila de otra tabla". `paciente_id → pacientes.id`. |
| **`nullable=False`** | Obligatorio, no puede quedar vacío. |
| **`unique=True`** | No se puede repetir. |
| **`__tablename__`** | El nombre real de la tabla en la base. |

## Flask / Web

| Palabra | Qué significa |
|---|---|
| **Flask** | El framework que convierte tu Python en una página web. |
| **framework** | Un esqueleto ya hecho: tú rellenas, él se encarga del resto. |
| **ruta / route** | Una dirección de la web. `/pacientes`. |
| **`@app.route()`** | Decorador que dice "cuando alguien entre a esta URL, ejecuta esta función". |
| **GET** | "muéstrame la página". |
| **POST** | "toma estos datos del formulario". |
| **`request`** | La caja con TODO lo que mandó el navegador. |
| **`request.form.get("x")`** | Sacar el campo `x` del formulario. |
| **`request.args`** | Lo que va en la URL después del `?`. |
| **`redirect`** | "vete a otra página". |
| **`url_for("nombre_funcion")`** | Construye la URL a partir del NOMBRE de la función. Mejor que escribir `/pacientes` a mano: si cambias la URL, esto se actualiza solo. |
| **`render_template`** | "toma este HTML, rellénalo con estos datos, y mándaselo". |
| **`flash`** | Mensajito de una sola vez ("Paciente creado ✅"). |
| **Blueprint** | Un paquete de rutas que vive en su propio archivo. Para no tener un `app_web.py` de 2000 líneas. |
| **`register_blueprint`** | Enchufar ese paquete a la app. |
| **Jinja2** | El lenguaje de las plantillas: `{{ variable }}` y `{% instrucción %}`. |
| **`{% extends %}`** | "heredo el molde de base.html". |
| **`{% block %}`** | Un hueco rellenable del molde. |
| **`debug=True`** | Modo desarrollo: se reinicia solo y muestra los errores. ⚠️ NUNCA en producción. |
| **localhost / 127.0.0.1** | Tu propio computador. Nadie más lo ve. |
| **puerto** | La "puerta" del computador. Flask usa la 5000. |

## Seguridad / Login

| Palabra | Qué significa |
|---|---|
| **hash** | Huella digital de la contraseña. Solo va hacia adelante, no se puede revertir. |
| **`generate_password_hash`** | Crear la huella. |
| **`check_password_hash`** | Comparar la huella guardada con lo que escribió el usuario. |
| **cookie** | Papelito que el navegador guarda para recordar quién eres. |
| **`secret_key`** | La llave que FIRMA las cookies para que nadie las falsifique. |
| **sesión (de login)** | El "estás dentro" que dura hasta que cierras. |
| **Flask-Login** | La extensión que gestiona todo eso. |
| **`LoginManager`** | El portero de la discoteca. |
| **`UserMixin`** | Un kit de piezas ya hechas (`is_authenticated`, `get_id`...) que Flask-Login exige. Heredas de él y ya las tienes. |
| **`@login_required`** | "para entrar aquí hay que estar logueado". |
| **`current_user`** | El usuario que está navegando ahora mismo. |
| **`user_loader`** | La función que, dado un id de la cookie, va a la base y trae el usuario. Se ejecuta en CADA petición. |
| **`login_user` / `logout_user`** | Abrir y cerrar sesión. |
| **texto plano** | La contraseña sin cifrar. Lo que NUNCA se guarda. |

## Del `app.py` de escritorio

| Palabra | Qué significa |
|---|---|
| **Tkinter** | La librería de ventanas de Python (botones, cajas de texto...). |
| **GUI** | *Graphical User Interface*. La interfaz con ventanitas. |
| **`ttk`** | Los widgets "bonitos" de Tkinter. |
| **widget** | Cualquier cachito de la interfaz: un botón, una etiqueta, una caja. |
| **`messagebox`** | Las ventanitas de aviso. |
| **ReportLab** | La librería para generar PDFs. |
| **`canvas`** | El "lienzo" del PDF sobre el que dibujas. |
| **`landscape` / `A4`** | Horizontal / tamaño de hoja. |
| **pandas** | Librería para manejar tablas de datos. |
| **DataFrame** | Una tabla en memoria (como una hoja de Excel dentro de Python). |
| **gspread** | Para leer y escribir Google Sheets. |
| **OAuth / credenciales de servicio** | La forma en que Google verifica que tu programa tiene permiso. |
| **`subprocess`** | Ejecutar otro programa desde Python (abrir el PDF). |
| **`threading`** | Hacer dos cosas a la vez para que la ventana no se congele. |
| **`os` / `sys`** | Hablar con el sistema operativo. |
| **`tempfile`** | Archivos temporales que se borran solos. |
| **`alias` (`import x as y`)** | Ponerle apodo a una librería para escribir menos. |

## Git / GitHub

| Palabra | Qué significa |
|---|---|
| **repositorio (repo)** | La carpeta del proyecto con todo su historial. |
| **commit** | Una foto guardada del proyecto en un momento dado. |
| **push** | Subir tus commits a GitHub. |
| **pull / fetch** | Bajarte lo que hay en GitHub. |
| **rama (branch)** | Una línea de trabajo paralela. Puedes experimentar sin romper lo bueno. |
| **`main`** | La rama principal, la "buena". |
| **merge** | Juntar una rama con otra. |
| **`.gitignore`** | La lista de archivos que git debe IGNORAR. |
| **clonar** | Bajarse el repo completo por primera vez. |

---

# PARTE 4 — 💡 Tips de buenas prácticas

## Lo que ya haces bien (no lo cambies)

1. ✅ **Separar rutas de lógica.** Es la decisión más importante del proyecto.
2. ✅ **Comentar todo.** En serio, ignora a quien diga que "el código limpio no necesita comentarios".
   Tú estás **aprendiendo**, y estos comentarios son tu memoria externa. Valen oro.
3. ✅ **Nombres en español y descriptivos.** `buscar_por_id_editar` se entiende sola.
4. ✅ **Hashear contraseñas.** Mucha gente con años de experiencia sigue sin hacerlo.
5. ✅ **`Path(__file__).parent`** en vez de rutas absolutas.
6. ✅ **`url_for()`** en vez de escribir URLs a mano.
7. ✅ **El patrón POST → Redirect → GET.**

## Lo siguiente que vale la pena aprender

### 1. 🔴 Crea un `.gitignore` — esto es lo más urgente

Ahora mismo estás subiendo a GitHub:
- `usuarios.db` y `base-opticaprueba.db` → **con los hashes de las contraseñas dentro**
- Toda la carpeta `__pycache__/` → archivos basura que Python regenera solo

Un `.gitignore` con esto lo arregla:

```
__pycache__/
*.pyc
*.db
*.json
.vscode/
```

> ⚠️ Ojo: en `app.py` hay un `bbd-optica-liza-vision-...json` (credenciales de Google).
> Ese archivo **jamás** debe llegar a GitHub. Si alguna vez lo subes, hay que
> **revocar la clave en Google**, no basta con borrarlo del repo — el historial lo recuerda.

### 2. 🔑 La `secret_key` no debe estar escrita en el código

En `app_web.py` está literal: `"cambia-esto-por-una-clave-secreta-real"`.
Lo correcto es leerla de una **variable de entorno**:

```python
import os
app.secret_key = os.environ.get("SECRET_KEY", "clave-de-desarrollo")
```

Así la clave real vive fuera del código y nunca se sube.

### 3. ⚠️ Valida antes de tocar

Este patrón se repite mucho en `logica_paciente.py`:

```python
paciente = db.query(...).first()
paciente.nombre = nombre        # ← si no existe, aquí revienta
```

Si el paciente no existe, `first()` devuelve `None`, y `None.nombre` explota.
La costumbre buena es preguntar siempre primero:

```python
if paciente is None:
    return None
```

(En `logica_usuario.py` ya lo haces 👏 — solo falta llevarlo a pacientes y fórmulas.)

### 4. 📅 `datetime.utcnow` está quedando obsoleto

En Python 3.12+ avisa. El reemplazo:

```python
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

### 5. 🧭 Ordenar al revés para traer "los últimos"

Ojo con esto, que es sutil:

```python
db.query(Paciente).order_by(Paciente.fecha_creacion).limit(20).all()
```

Ordena de **más viejo a más nuevo** y coge los 20 primeros → te trae los **20 MÁS ANTIGUOS**,
aunque la variable se llame `ultimos_20pacientes`. Para los más recientes hace falta
`.desc()`:

```python
order_by(Paciente.fecha_creacion.desc())
```

### 6. 🔁 Una sola `Base` para todo el proyecto

Cada `logica_*.py` crea su propia `class Base(DeclarativeBase)`. Funciona por ahora,
pero son tres bases separadas que no se conocen entre sí. Cuando quieras usar
`relationship()` (para hacer `paciente.formulas` y que te dé todas sus fórmulas),
vas a necesitar que compartan la misma `Base`.

Solución típica: un archivo `base.py` con la `Base`, y que los tres la importen.

### 7. 🧪 Prueba antes de dar por bueno

Antes de decir "ya está", ejecútalo. Especialmente después de tocar rutas — hay errores
que solo aparecen al hacer clic.

### 8. 📝 Escribe un `README.md` de verdad

El tuyo tiene una línea. Uno útil responde: qué es esto, cómo se instala, cómo se arranca.
Tu yo del futuro te lo va a agradecer.

> Detalle: el README dice `pip install -r requirements.txt` pero tu archivo se llama
> `requerimientos.txt`. Y le faltan librerías del `app.py` (reportlab, pandas, gspread...).

### 9. 🌿 Una rama por cosa nueva

En vez de trabajar siempre en `main`:

```bash
git checkout -b agregar-buscador-pacientes
```

Si sale mal, borras la rama y `main` sigue intacto. Es una red de seguridad gratis.

### 10. 💬 Commits que se entiendan

Tus commits actuales dicen `Act`, `Act`, `ACt`. Dentro de tres meses no vas a saber
qué era cada uno. Prueba con:

```
Agregar edición de pacientes
Corregir ruta de la base de datos
```

Regla simple: **completa la frase "Este commit va a ___"**.

---

# PARTE 5 — 🐛 Cosas que encontré leyendo (para que las revises tú)

> No he tocado nada. Son pistas para que investigues cuando quieras.

| Dónde | Qué pasa |
|---|---|
| `rutas/bp_pacientes.py:64` y `:71` | `url_for("bluep_pacientes.pacientes")` — pero esa función no existe, se llama `crear_paciente_route`. Al editar o eliminar un paciente esto debería dar error. |
| `rutas/bp_formulas.py:47` | Llamas `editar_formula(id=id, ...)`, pero la función espera `formula_id`. El `id` se cuela dentro de los `**kwargs` y el argumento obligatorio queda sin llenar. |
| `rutas/bp_formulas.py` | `prox_control` se manda como texto, sin `strptime`, pero la columna es `DateTime`. Compara con cómo sí conviertes `fecha`. |
| `logica_formulas.py:47` | `Base.metadata.create_all(engine)` está comentado. Si la tabla `formulas` no existiera, no se crearía. |
| `logica_paciente.py` | `consultar_paciente` devuelve un objeto si buscas por documento, pero una **lista** si buscas por nombre. Quien la use no sabrá qué le llega. |
| `logica_paciente.py:87` | Tu propio comentario: *"Pendiente validar que el documento no exista ya"*. Sigue pendiente 🙂 |
| `app.py` | Importa `msvcrt`, que **solo existe en Windows**. En Mac o Linux no arrancaría. |

---

## 🚀 Chuleta de arranque

```bash
# Instalar dependencias
pip install -r requerimientos.txt

# Arrancar la web
python app_web.py
# → http://127.0.0.1:5000

# Arrancar el de escritorio (solo Windows)
python app.py

# Ver qué hay en la base
python practica.py
```

---

*Cuaderno creado el 5 de septiembre de 2026. Se puede editar, ampliar y tachar. Es tuyo.*
