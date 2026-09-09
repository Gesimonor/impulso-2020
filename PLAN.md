# 🗺️ Plan de Impulso 20/20

> Mapa del proyecto en tres niveles: **módulos** → **vistas** → **tareas**.
> Las casillas `- [ ]` se marcan cambiando el espacio por una `x`. GitHub las pinta solas.
>
> Estado leído del código en el commit `72b6926` (7 de septiembre de 2026).

---

# NIVEL 1 — Mapa de módulos

| Módulo | Qué hace | Estado |
|---|---|---|
| 👤 **Usuarios** | Login, roles y gestión de quién entra a la app | 🟡 **En curso** — el login funciona, pero no hay pantalla para administrar usuarios |
| 🧑‍🤝‍🧑 **Pacientes** | Ficha de cada persona: datos de contacto y documento | 🟡 **En curso** — se crean y se listan; editar y eliminar tienen fallos |
| 💊 **Fórmulas** | La receta óptica: graduación de cada ojo, controles y vencimiento | 🟡 **En curso** — se crean y se listan; editar no funciona |
| 🧾 **Facturas** | Facturación, abonos y PDF para el cliente | 🟠 **Existe, pero fuera de la web** — vive en `app.py` (escritorio, Tkinter) y funciona; en la web es solo un enlace muerto |
| 📅 **Citas** | Agenda de consultas y recordatorios | 🔴 **No empezado** — solo el enlace muerto en el menú |
| 📊 **Reportes** | Ventas, pacientes atendidos, controles vencidos | 🔴 **No empezado** — ni siquiera está en el menú |

### Leyenda
- 🟢 **Hecho** — funciona y está probado
- 🟡 **En curso** — se puede usar, pero le falta o tiene fallos
- 🟠 **Parcial** — existe en otro lado, falta traerlo
- 🔴 **No empezado**

### El elefante en la sala 🐘

**Facturas ya está construido, pero en el programa equivocado.**

`app.py` es una app de escritorio (Tkinter) que factura, calcula abonos, genera el PDF,
lo manda por WhatsApp y guarda en Google Sheets. Funciona. Pero es un mundo aparte del
`app_web.py`, con su propia forma de guardar datos.

En algún momento hay que decidir: **¿se migra a la web, o conviven?**
No hay que decidirlo hoy, pero conviene tenerlo presente — es el trabajo más grande que queda.

---

# NIVEL 2 — Las vistas de cada módulo

## 👤 Usuarios

### Vista: Login `/login` ✅ funciona
- **Muestra:** logo, correo, contraseña
- **Campos:** `email` (obligatorio), `password` (obligatorio)
- **Acciones:** Ingresar
- **Validaciones:** el correo debe existir; la contraseña se compara contra el hash
- **Pendiente:** mensaje de error más claro, "olvidé mi contraseña", límite de intentos

### Vista: Panel principal `/applayout` 🟡 vacía
- **Muestra:** "Bienvenida, {nombre}" y una tarjeta con texto de relleno
- **Pendiente:** poner algo útil — citas de hoy, controles vencidos, últimos pacientes

### Vista: Lista de usuarios ❌ no existe
> Las funciones ya están escritas en `logica_usuario.py` (`crear_usuario`, `listar_usuarios`,
> `actualizar_usuario`, `cambiar_contrasena`, `eliminar_usuario`), pero **ninguna ruta las usa**.
> Hoy los usuarios solo se crean a mano desde la consola.
- **Debería mostrar:** nombre, correo, rol, fecha de creación
- **Acciones:** crear, editar, cambiar contraseña, eliminar
- **Validaciones:** correo único, contraseña mínima, no borrarse a una misma
- **Ojo:** esta pantalla solo debería verla el rol `admin`

---

## 🧑‍🤝‍🧑 Pacientes

### Vista: Lista de pacientes `/pacientes` 🟡
- **Muestra:** nombre, apellido, documento, celular, correo, fecha de nacimiento, dirección
- **Acciones:** agregar (abre modal), editar (va a otra página), eliminar (con confirmación)
- **Pendiente:** buscador por documento o nombre
- **Pendiente:** paginación — hoy solo muestra 20
- **🐛 Bug:** trae los **20 más antiguos**, no los más recientes (falta `.desc()` en el `order_by`)

### Vista: Crear paciente (modal) 🟡
- **Campos, todos obligatorios:** nombre, apellido, documento, celular, correo, fecha de nacimiento, dirección
- **Acciones:** Guardar, Cancelar
- **Validaciones que hay:** las del navegador (`required`, formato de correo)
- **Pendiente:** validar **documento duplicado** — hoy la app revienta con un error feo si se repite
- **Pendiente:** validar que el celular sean solo números
- **Pendiente:** validar que la fecha de nacimiento no sea futura

### Vista: Editar paciente `/pacientes/editar/<id>` 🐛
- **Campos:** los mismos, precargados con los datos actuales
- **Acciones:** Guardar cambios
- **🐛 Bug:** al guardar falla — `url_for("bluep_pacientes.pacientes")` apunta a una función
  que no existe (se llama `crear_paciente_route`)
- **Pendiente:** si el paciente no existe, hoy la app se cae en vez de avisar

### Vista: Eliminar paciente 🐛
- **Acciones:** botón con confirmación
- **🐛 Bug:** mismo `url_for` roto que en editar
- **A pensar:** ¿borrar de verdad, o marcarlo como inactivo? Si un paciente tiene fórmulas,
  borrarlo deja esas fórmulas huérfanas

---

## 💊 Fórmulas

### Vista: Lista de fórmulas `/formulas` 🟡
- **Muestra:** ID del paciente, fecha de receta, vencimiento, próximo control, observaciones
- **Acciones:** agregar (modal), editar, eliminar
- **Pendiente:** mostrar el **nombre** del paciente, no su ID — hoy sale "7" en vez de "María Gómez"
- **Pendiente:** buscador y filtro por paciente
- **Pendiente:** ver las fórmulas de un paciente desde su ficha
- **🐛 Bug:** mismo problema del `order_by` — trae las 20 más antiguas

### Vista: Crear fórmula (modal) 🟡
- **Campos generales:** `paciente_id` (obligatorio), fecha (obligatoria), fecha de vencimiento (opcional), próximo control (menú: 3 / 6 / 12 / 24 meses), observaciones
- **Por cada ojo (OD y OI):** esfera, cilindro, eje, adición, altura bifocal, distancia interpupilar, color
- **Acciones:** Guardar, Cancelar
- **✅ Ya hecho:** el próximo control se calcula solo, sumando meses con `relativedelta`
- **Pendiente:** elegir el paciente por **nombre o documento**, no escribiendo su ID a mano
- **Pendiente:** validar que el `paciente_id` exista de verdad
- **Pendiente:** validar el formato de la graduación (esfera y cilindro con decimales, eje entre 0 y 180)
- **Pendiente:** sugerir el vencimiento automáticamente (suele ser un año)

### Vista: Editar fórmula `/formulas/editar/<id>` ❌ no funciona
- **🐛 Bug 1:** se llama `editar_formula(id=id, ...)` pero la función espera `formula_id`
- **🐛 Bug 2:** `prox_control` se manda sin convertir. Desde el cambio del menú desplegable,
  el formulario envía `"6"` (meses) y se intenta guardar en una columna de fecha
- **🐛 Bug 3:** `consultar_formulas_por_paciente(id)` busca por paciente, no por fórmula.
  Para editar UNA fórmula hace falta buscarla por SU id
- **Pendiente:** no existe la plantilla `editar_formula.html`

### Vista: Imprimir fórmula ❌ no existe
- **Pendiente:** PDF de la receta para entregar al paciente
- 💡 En `app.py` ya hay código que genera PDFs con ReportLab. Se puede reaprovechar

---

## 🧾 Facturas

### Estado actual: existe en escritorio, no en la web
Lo que `app.py` ya hace y funciona:
- Crear factura con consecutivo automático
- Calcular totales y saldos
- Registrar abonos e historial
- Generar el PDF
- Enviarlo por WhatsApp
- Guardar en Google Sheets

### Vistas que harían falta en la web
- **Lista de facturas** — número, paciente, fecha, total, saldo, estado
- **Crear factura** — paciente, ítems, cantidades, precios, abono inicial
- **Detalle de factura** — con historial de abonos y botón de PDF
- **Registrar abono** — monto, fecha, forma de pago

> ⚠️ Antes de programar nada aquí hay que decidir **dónde viven las facturas**:
> ¿en `base-opticaprueba.db` como todo lo demás, o siguen en Google Sheets?

---

## 📅 Citas — no empezado

### Vistas que harían falta
- **Agenda / calendario** — vista por día o semana
- **Agendar cita** — paciente, fecha, hora, motivo, profesional
- **Detalle de cita** — con estado: agendada, atendida, cancelada, no asistió

### Ideas
- Recordatorio por WhatsApp el día anterior (ya hay código de WhatsApp en `app.py`)
- Enlazar la cita con la fórmula que salga de ella
- Avisar cuando a un paciente le toque control, según `prox_control`

---

## 📊 Reportes — no empezado

### Ideas de reportes útiles para la óptica
- Pacientes atendidos por mes
- **Controles vencidos** — a quién hay que llamar (el dato ya existe en `prox_control`)
- Fórmulas por vencer en los próximos 30 días
- Ventas del mes y cartera pendiente
- Exportar a Excel

> 💡 De todos estos, el de **controles vencidos** es el que más plata trae y el más fácil:
> es una consulta filtrando por fecha.

---

# NIVEL 3 — Checklist

## 🔴 Urgente (antes de seguir agregando cosas)

- [ ] Crear `.gitignore` (`__pycache__/`, `*.pyc`, `*.db`, `*.json`, `.vscode/`)
- [ ] Sacar del repo los `.db` y los `.pyc` ya subidos
- [ ] Mover la `secret_key` a una variable de entorno
- [ ] Verificar que el `.json` de credenciales de Google **nunca** llegó a GitHub

## 🐛 Bugs conocidos

- [ ] `bp_pacientes.py:64` — `url_for` apunta a `pacientes`, debe ser `crear_paciente_route`
- [ ] `bp_pacientes.py:71` — mismo problema al eliminar
- [ ] `bp_formulas.py:46` — `editar_formula(id=...)` debe ser `formula_id=...`
- [ ] `bp_formulas.py:48` — `prox_control` sin convertir de meses a fecha al editar
- [ ] `bp_formulas.py:44` — usa `consultar_formulas_por_paciente`, debería buscar por id de fórmula
- [ ] `listar_pacientes()` — falta `.desc()`, trae los más antiguos
- [ ] `listar_formulas()` — mismo problema
- [ ] `logica_usuario.py` — quitar los imports que ya no se usan (`Path`, `create_engine`, `sessionmaker`)

## 👤 Usuarios

- [x] Modelo `Usuario` con contraseña hasheada
- [x] Login funcionando
- [x] Cerrar sesión
- [x] Proteger las rutas con `@login_required`
- [x] Funciones CRUD en `logica_usuario.py`
- [ ] Pantalla de administración de usuarios
- [ ] Rutas para crear, editar y eliminar usuarios
- [ ] Que solo el rol `admin` pueda entrar ahí
- [ ] Cambiar la propia contraseña
- [ ] Mensaje de error claro al fallar el login

## 🧑‍🤝‍🧑 Pacientes

- [x] Modelo `Paciente`
- [x] Crear paciente
- [x] Listar pacientes
- [x] Formulario de edición (la pantalla)
- [ ] Que guardar los cambios funcione (bug del `url_for`)
- [ ] Que eliminar funcione (mismo bug)
- [ ] Validar documento duplicado
- [ ] Validar que el celular sean solo números
- [ ] Validar que la fecha de nacimiento no sea futura
- [ ] Buscador por documento o nombre
- [ ] Paginación
- [ ] Ordenar por más reciente
- [ ] Avisar bonito cuando el paciente no existe
- [ ] Ficha del paciente con sus fórmulas

## 💊 Fórmulas

- [x] Modelo `Formula` con OD y OI
- [x] Relación con paciente (`ForeignKey`)
- [x] Crear fórmula
- [x] Listar fórmulas
- [x] Próximo control calculado automáticamente
- [ ] Que editar funcione (los tres bugs)
- [ ] Plantilla `editar_formula.html`
- [ ] Mostrar el nombre del paciente en vez del ID
- [ ] Elegir paciente por nombre o documento
- [ ] Validar que el paciente exista
- [ ] Validar formato de la graduación
- [ ] Sugerir fecha de vencimiento
- [ ] Generar PDF de la receta
- [ ] Ver el historial de fórmulas de un paciente

## 🧾 Facturas

- [x] Facturación completa en escritorio (`app.py`)
- [ ] Decidir: ¿migrar a la web o mantener las dos?
- [ ] Decidir dónde se guardan (SQLite o Google Sheets)
- [ ] Modelo `Factura` y `DetalleFactura`
- [ ] Modelo `Abono`
- [ ] Lista de facturas
- [ ] Crear factura
- [ ] Detalle con historial de abonos
- [ ] Registrar abono
- [ ] Generar PDF
- [ ] Consecutivo automático

## 📅 Citas

- [ ] Modelo `Cita`
- [ ] Vista de agenda
- [ ] Agendar cita
- [ ] Editar y cancelar
- [ ] Estados: agendada / atendida / cancelada / no asistió
- [ ] Enlazar con la fórmula resultante
- [ ] Recordatorio por WhatsApp

## 📊 Reportes

- [ ] Agregar "Reportes" al menú
- [ ] Controles vencidos (a quién llamar) ⭐ el más útil
- [ ] Fórmulas por vencer en 30 días
- [ ] Pacientes atendidos por mes
- [ ] Ventas del mes
- [ ] Cartera pendiente
- [ ] Exportar a Excel

## 🏗️ Del proyecto en general

- [x] Separar rutas de lógica
- [x] Blueprints
- [x] Plantilla base con herencia
- [x] Una sola `Base` en `infraestructura_db.py`
- [ ] `README.md` de verdad
- [ ] Arreglar el nombre: el README dice `requirements.txt`, el archivo es `requerimientos.txt`
- [ ] Completar `requerimientos.txt` con lo que usa `app.py`
- [ ] Cambiar `datetime.utcnow` por `datetime.now(timezone.utc)`
- [ ] Página 404 y 500 bonitas
- [ ] Primeras pruebas automáticas
- [ ] Que la app se vea bien en celular

---

# 🎯 Por dónde seguir

Un orden sugerido, de lo que más rinde a lo que menos:

1. **El `.gitignore`** — cinco líneas, quita basura y protege datos
2. **Los bugs de editar y eliminar** — son de una línea cada uno y desbloquean funciones enteras
3. **El buscador de pacientes** — con 200 pacientes, una lista de 20 no sirve
4. **Elegir paciente por nombre en fórmulas** — escribir el ID a mano es pedir errores
5. **El reporte de controles vencidos** — es una sola consulta y sirve para llamar clientes
6. **Citas** — módulo nuevo completo
7. **Facturas en la web** — lo más grande, lo último

> Regla: **una rama por cosa**. `git checkout -b arreglar-editar-paciente`.
> Si sale mal, borras la rama y `main` sigue sano.

---

*Actualizado el 9 de septiembre de 2026, sobre el commit `72b6926`.*
*Es un documento vivo: márcalo, táchalo y cámbialo según avances.*
