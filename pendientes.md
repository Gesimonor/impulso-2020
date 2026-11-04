# Impulso 20/20 — Mapa de pendientes

Última actualización: 3 de noviembre de 2026

---

## 🔴 Bugs que rompen hoy

| Dónde | Qué pasa |
|---|---|
| `editar_formula.html` | Botón **Cancelar** apunta a `crear_formula_route`, que ahora solo acepta POST → error 405. Debe ir a `listar_formulas_route` |
| `ver_formula.html` | Botón **Volver**, mismo problema |
| `editar_paciente.html` | Botón **Cancelar** apunta a `crear_paciente_route` (solo POST) → mismo error |
| `ver_paciente.html` | Botón **Ver** de la tabla de fórmulas apunta a `crear_formula_route`; debe ser `ver_formula_route` |
| `ver_paciente.html` | `</div>` y `</form>` cruzados en el bloque de Eliminar |
| `formulas.html` y `facturas.html` | `{{ today }}` — la plantilla lo espera pero ningún blueprint lo pasa; el campo de fecha sale vacío |
| `editar_formula.html` | El campo de paciente sigue siendo un input de número editable; debería ser el campo doble (visible + oculto) |

---

## 💰 Módulo de Facturas (en construcción)

**Lo que ya existe:** los tres modelos (`facturas`, `detalles_compras`, `abonos`), la relación con paciente vía `relationship` + `joinedload`, `bp_facturas` con la ruta de listar, `facturas.html` con la tabla, el modal, el buscador de paciente y las filas dinámicas.

**Lo que falta:**

### Backend
- [ ] Ruta de **crear factura** (POST) — leer las filas con `request.form.getlist("cantidad[]")`
- [ ] **Recalcular los totales en el servidor** — nunca confiar en el número que manda el navegador
- [ ] Funciones de lógica: `crear_factura`, crear detalles, crear abono
- [ ] **Validar que venga paciente** — el `required` en un `type="hidden"` los navegadores lo ignoran
- [ ] `numero_factura` — decidir quién genera el consecutivo (ligado a los rangos DIAN)
- [ ] `paciente_id` a `nullable=True` si las microventas pueden no tener paciente
- [ ] Función para calcular el total de una factura (suma de sus detalles)
- [ ] Función para calcular el saldo (total − suma de abonos)

### Frontend
- [ ] Columna **Total** en la lista (hoy muestra `#`)
- [ ] Formato de miles con punto: filtro `| pesos` en Jinja + `toLocaleString("es-CO")` en JS
- [ ] Quitarle el `name="total"` al campo — es solo visual, Flask lo recalcula
- [ ] **Bloquear el campo de paciente al elegir** + botón ✕ que deshaga la selección
- [ ] Ver factura / editar / eliminar
- [ ] Pantalla de abonos (registrar uno nuevo, ver historial)
- [ ] Generar el PDF (reutilizar el conocimiento de ReportLab de `app.py`)

---

## 💊 Módulo de Fórmulas

- [ ] **Profesional que prescribe** + usar `tipo_formula` (propia / EPS)
  - Propia → `optometra_id` (FK a usuarios, filtrando por rol)
  - EPS → nombre y registro profesional como texto
  - Agregar `registro_profesional` a la tabla `usuarios`
- [ ] **Bloquear la edición** de una fórmula que ya tiene factura asociada
- [ ] Guardar **quién creó** la fórmula (`usuario_id`)
- [ ] Selects para los campos de color (hoy son texto libre)

---

## 🧑‍🤝‍🧑 Módulo de Pacientes

- [ ] **Borrado lógico** — columna `activo` en vez de `db.delete()`. Las historias clínicas tienen plazos de conservación y hoy quedan fórmulas huérfanas
- [ ] No permitir eliminar un paciente que tenga fórmulas o facturas
- [ ] Mensaje distinto cuando una búsqueda no encuentra nada (hoy dice "no hay pacientes registrados", que confunde)
- [ ] **Flash con categorías** — verde para éxito, rojo para error. Hoy todos salen verdes

---

## 🏗️ Arquitectura y limpieza

- [ ] Unificar `.tabla-pacientes` y `.tabla` en `base.html` — hoy son dos clases con el mismo estilo
- [ ] Sacar el **buscador de paciente** a un fragmento reutilizable (`{% include %}`) — ya está copiado dos veces y en Citas serían tres
- [ ] Imports **explícitos** de los modelos en `app_web.py`, para que el `create_all` no dependa de la cadena de blueprints
- [ ] Borrar `consultar_paciente` de `logica_paciente.py` — código muerto que nadie llama
- [ ] Quitar imports sobrantes en `logica_usuario.py` (`create_engine`, `DeclarativeBase`, `sessionmaker`, `Path`)
- [ ] `cargar_usuario` en `app_web.py` sigue con el estilo viejo sin `with`
- [ ] **Alembic** (migraciones) — antes de instalar en la primera óptica. Hoy agregar una columna obliga a borrar el `.db`

---

## 🔒 Seguridad

**Ahora (baratas y evitan rehacer):**
- [ ] `secret_key` real, generada con `secrets.token_hex(32)`, guardada en un `.env`
- [ ] **`.gitignore`** con `__pycache__/`, `*.pyc`, `*.db`, `.vscode/`, `.env`
- [ ] **Sacar la base de datos de GitHub** — hoy tiene datos de pacientes publicados. El `.gitignore` no saca lo que ya subió
- [ ] **Roles** (admin / recepcionista / optómetra) — la columna existe pero nadie la usa

**Antes de producción:**
- [ ] HTTPS
- [ ] `debug=False`
- [ ] Respaldos automáticos
- [ ] Sesiones que expiren
- [ ] `pip-audit` y versiones fijas en `requerimientos.txt`
- [ ] Agregar `python-dateutil` a `requerimientos.txt` (ya se usa y no está)

---

## 📋 Módulos que no existen

- **Citas** — fecha, paciente, profesional, estado
- **Inventario** — productos, stock, descuento automático al facturar
- **Microventas** — ventas pequeñas (tornillo, pañito, líquido). Decidido: misma tabla `facturas`, sin paciente ni fórmula
- **Mantenimiento de equipos** — hojas de vida, cronograma, alertas. Probablemente requisito de habilitación
- **Datos de la óptica** — tabla de configuración (NIT, dirección, logo, firma). Hoy no existe; en el sistema viejo estaban quemados en el código

---

## 🚀 Producto / futuro

- Recordatorios automáticos de próximo control (el dato ya está en `prox_control`)
- Recordatorio de cumpleaños (`fecha_nacimiento` ya existe)
- Casilla de **autorización de tratamiento de datos** en el formulario de paciente — necesaria para cualquier mensaje comercial (Ley 1581)
- Factura electrónica vía **Factus** (ver notas abajo)
- Multi-tenencia — decisión aplazada hasta tener clientes reales
- Dos tipos de óptica: con optómetra (presta servicios de salud) vs. solo despacho. Funcionalidad y precio distintos

---

## 🔎 Investigación pendiente

### Normativa
- [ ] Buscar la **norma nacional** (Ministerio de Salud) de habilitación de ópticas y de RIPS — la fuente primaria, antes de ir a la Secretaría
- [ ] **Derecho de petición** a la Secretaría Distrital de Salud de Bogotá, citando la norma:
  - ¿Las ópticas deben reportar RIPS? ¿Y las que solo despachan fórmulas externas?
  - ¿Qué documentación exigen en una visita de inspección?
  - ¿Se aceptan registros digitales o los piden impresos? ¿Con qué requisitos (trazabilidad, firma)?
  - ¿Qué exigen sobre mantenimiento de equipos?
  - ¿Qué identificación del profesional debe llevar una fórmula? ¿Registro profesional obligatorio?
  - ¿Hay que conservar la fórmula de origen al despachar una externa?
- [ ] Documento soporte para microventas — preguntar a un contador, no a la Secretaría

### Factus (factura electrónica)
- [ ] **Pedir credenciales de sandbox** — es gratis y no compromete a nada
- [ ] Armar la tabla comparativa: campos que pide Factus vs. campos que tengo
  - Agrupar por: cliente / óptica / venta / administración DIAN / respuesta de la DIAN
- [ ] Campos que habrá que guardar de la respuesta: CUFE, estado DIAN, fecha de validación
- [ ] Calcular volumen para pedir cotización (ej.: 5 ópticas × 200 facturas/mes = 12.000/año)
- [ ] Decidir: ¿el costo lo paga la óptica o va incluido en la mensualidad?

**Lo que ya se sabe de Factus:**
- El modelo de aliado/casa de software sí existe; se crea una cuenta por cada cliente con su NIT
- Las facturas salen a nombre de cada óptica, no del aliado ni de Factus
- Sandbox gratuito, sin pago hasta pasar a producción
- Activación: 3 días hábiles. Requiere Cámara de Comercio (< 30 días), cédula del rep. legal, RUT y rango de numeración DIAN
- Dos modalidades: paquete por NIT (certificado incluido) o bolsa dividida (certificado aparte, $130.000/año por NIT)
- Token vence cada 60 min; rate limit de 80 peticiones/min por NIT; no tienen webhooks
- Validar una factura tarda ~2,5 segundos → hay que mostrar algo en la interfaz mientras tanto
- **RIPS:** ellos generan el XML de factura; la parte de RIPS la hace uno

---

## ✅ Decisiones ya tomadas (para no volver a discutirlas)

- **Los datos calculados no se guardan.** Total, saldo y valor por línea se calculan al momento. Guardar hechos, calcular conclusiones
- **Precios en `Integer`** (pesos enteros), nunca `Float`
- **El `valor_unitario` sí se guarda** — es un hecho histórico, no un cálculo
- **Abonos en tabla aparte**, no duplicando la factura como en el sistema viejo
- **Detalles de compra en tabla aparte**, sin límite de 4 líneas (el PDF se adapta)
- **La factura apunta a la fórmula con `formula_id`**, no copia la graduación. Para que no mienta, se bloquea la edición de fórmulas ya facturadas
- **Una sola base de datos** para todo; multi-tenencia se decide después
- **Buscar = GET, modificar = POST.** El término de búsqueda va en la URL
- **Formatear es la última capa** — el número vive como entero en todas partes y solo se convierte a texto al pintarlo
- **Lo que el usuario ve ≠ lo que viaja a Flask** — nombre visible, id oculto
