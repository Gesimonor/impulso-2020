#Agregar el limpiar del entry_saldo_anterior y los otros
#Ajustar el estado de los abonos


import threading
import time

import tkinter as tk #AS es para darle un Alias a la biblioteca, y Tkinter es la interfaz grafiza de GUI
from tkinter import messagebox, ttk, simpledialog, Toplevel, Listbox #si quiesiera ponere alias quedaria asi "import messagebox as mb, ttk as t"
import os #Esta cosa sirve para trabajar con el sistema operatico, en este caso Rutas
import subprocess #y esta la esta usando para abrir el pdf una vez creado, pues que esta bien pero debo desabilitarla cuando este creado
from datetime import datetime #esta cosa me trae la fecha actual
from reportlab.lib.pagesizes import landscape, A4 #Tamano , orientacion de la hoja "landscape" esta es para que sea horizontal
from reportlab.pdfgen import canvas as pdf_canvas # type: ignore #es el lienzo sobre el que puedes dibujar texto, imagenes y formas en el PDF.
from reportlab.lib import colors #Colores
from reportlab.platypus import Table, TableStyle #"Table" para agregar tablas y "TableStyle" par darle estilo a tabla
from reportlab.lib.colors import Color
import pandas as pd
import psutil
from openpyxl import load_workbook

import pywhatkit as kit

import sys
import os
import msvcrt
import tempfile
from pdf2image import convert_from_path

import gspread #funcionamineot inline con sheets
from oauth2client.service_account import ServiceAccountCredentials


def obtener_sheet(nombre_hoja):
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        ruta_json = recurso_path("bbd-optica-liza-vision-ca29c72be601.json")
        #ruta_json = r"C:\Users\luzes\Claro drive\Cositas Varias\IMPULSO 360°\Optica Liza Vision\Sede 2 - Villa Claaudia\Factura Online\bbd-optica-liza-vision-ca29c72be601.json"
        creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, scope)    
        client = gspread.authorize(creds)
        hoja = client.open_by_key("1tNk_wdkAg5txQj2cUHeUAswX46aEWqKWPfu9jJMwmEE").worksheet(nombre_hoja)
        
        #print("✅ Conexión exitosa con la hoja:", nombre_hoja)
        return hoja
    except Exception as e:
        messagebox.showerror("Error de conexión", f"No se pudo conectar con la hoja '{nombre_hoja}':\n{e}")
        #print("❌ Error al conectar con la hoja:", nombre_hoja, "\n", e)
        return None


def obtener_dataframe_desde_sheets(nombre_hoja_interna="Facturas"):
    try:
        # Autenticación
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
        ]
        ruta_json = recurso_path("bbd-optica-liza-vision-ca29c72be601.json")
        #ruta_json = r"C:\Users\luzes\Claro drive\Cositas Varias\IMPULSO 360°\Optica Liza Vision\Sede 2 - Villa Claaudia\Factura Online\bbd-optica-liza-vision-ca29c72be601.json"

        creds = ServiceAccountCredentials.from_json_keyfile_name(ruta_json, scope)
        client = gspread.authorize(creds)

        # Abrir hoja y hoja interna (worksheet)
        sheet = client.open_by_key("1tNk_wdkAg5txQj2cUHeUAswX46aEWqKWPfu9jJMwmEE")
        worksheet = sheet.worksheet(nombre_hoja_interna)

        # Obtener los datos (incluye encabezados)
        data = worksheet.get_all_records()

        # Convertir a DataFrame
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la hoja: {e}")
        return pd.DataFrame()

if getattr(sys, 'frozen', False):
    # Cuando está empacado como .exe con PyInstaller
    base_path = sys._MEIPASS
else:
    # Cuando se ejecuta como script normal
    base_path = os.path.dirname(__file__)

poppler_path = os.path.join(base_path, "poppler-24.08.0", "Library", "bin")

def recurso_path(rel_path):
    try:
        # Cuando se ejecuta como un archivo .exe
        base_path = sys._MEIPASS
    except Exception:
        # Cuando se ejecuta como un script normal de Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, rel_path)

ruta_logo = recurso_path("Logo con eslogan.jpg")
#ruta_logo = r"C:\Users\luzes\Claro drive\Cositas Varias\IMPULSO 360°\Optica Liza Vision\Sede 2 - Villa Claaudia\Factura Online\Logo con eslogan.jpg"
ruta_firma = recurso_path("Firma sin fondo.png")
#ruta_firma = r"C:\Users\luzes\Claro drive\Cositas Varias\IMPULSO 360°\Optica Liza Vision\Sede 2 - Villa Claaudia\Factura Online\Firma sin fondo.png"

#Variables
FECHA_ACTUAL = datetime.now().strftime("%Y-%m-%d") 
FECHA = datetime.now()

# Obtiene la carpeta "Documentos" del usuario actual
directorio_usuario = os.path.expanduser("~")
carpeta_facturas = os.path.join(directorio_usuario, "Documentos", "Facturas")
carpeta_imagenes = os.path.join(carpeta_facturas, "Imagenes Facturas")
carpeta_pdfs = os.path.join(carpeta_facturas, "PDF Facturas")



#++++++++++++++++++++FUNCIONES DE GUI++++++++++++++++++++++++++++++++
#Funciones de interfaz GUI  

# Validaciones de entradas
def limitar_caracteres(texto): #26
    return len(texto) <= 26
def validar_numeros(numeros):# Función de validación: Solo permite números

    return numeros.isdigit() or numeros == ""  # Permite solo números y vacío
def validar_texto(texto):# Función de validación: Solo permite letras

    return texto.replace(" ", "").isalpha() or texto == "" # Permite solo texto y espacios

def obtener_valor_limpio(var):# Función para mostrar el número formateado con puntos

    try:
        return int(var.get().replace('.', '').replace(',', ''))
    except ValueError:
        return 0   
def formatear_gui(entry_var):#Esta es la validacion para ver el punto de miles
    texto = entry_var.get().replace('.', '').replace(',', '')
    if texto.isdigit():
        formateado = "{:,}".format(int(texto)).replace(",", ".")
        entry_var.set(formateado)

def limpiar_campos():
    campos = [
        entry_cliente, entry_documento, entry_direccion, entry_celular, entry_formadepago, 
        entry_total, entry_abono, entry_saldo, 
        entry_saldo_anterior, entry_nuevo_abono,entry_saldo_anterior,entry_nuevo_abono
    ]

    for campo in campos:
        campo.config(state="normal")
        campo.delete(0, tk.END)
        if campo in [entry_total, entry_saldo_anterior]:
            campo.config(state="readonly")

    # Si también tienes los productos:
    for item in entries_compras:
        item["Cantidad"].delete(0, tk.END)
        item["Detalle"].delete(0, tk.END)
        item["Valor Unidad"].delete(0, tk.END)

        item["Valor Total"].config(state="normal")
        item["Valor Total"].delete(0, tk.END)
        item["Valor Total"].config(state="readonly")
        # Listas de los campos de Ojo Derecho (OD) y Ojo Izquierdo (OI)
    campos_od = [
        "Esfera Derecho", "Cilindro Derecho", "Eje Derecho", "Adición Derecho",
        "Alt Bif Derecho", "Dist P. Derecho", "Color Derecho"
    ]

    campos_oi = [
        "Esfera Izquierdo", "Cilindro Izquierdo", "Eje Izquierdo", "Adición Izquierdo",
        "Alt Bif Izquierdo", "Dist P. Izquierdo", "Color Izquierdo"
    ]

    # Limpiar los campos de Ojo Derecho (OD)
    for campo in campos_od:
        entries_tabla[campo].delete(0, tk.END)

    # Limpiar los campos de Ojo Izquierdo (OI)
    for campo in campos_oi:
        entries_tabla[campo].delete(0, tk.END)


def limpiar_entrada():
    entrada_busqueda_num_factura.delete(0, tk.END) 
def limpiar_valor(valor, predeterminado=""):
    """Limpia valores como 'NaN', None o numéricos inválidos."""
    if valor is None:
        return predeterminado
    try:
        if str(valor).strip().lower() == "nan":
            return predeterminado
        return str(valor)
    except (ValueError, TypeError):
        return predeterminado
    
#Funciones para el manejo de los totales
def actualizar_total(entry_cant, entry_valorunidad, entry_valortotal):#Hace las multiplicaiones
    try:
        cantidad = int(float(entry_cant.get()))
    except ValueError:
        cantidad = 0

    try:
        valor_unidad = int(float(entry_valorunidad.get()))

    except ValueError:
        valor_unidad = 0

    total = cantidad * valor_unidad

    # Desbloquear temporalmente el Entry para modificarlo
    entry_valortotal.config(state="normal")
    entry_valortotal.delete(0, tk.END)
    entry_valortotal.insert(0, f"{total}")
    entry_valortotal.config(state="readonly") 
def calcular_total_y_saldo(*args):
    try:
        total = 0
        for fila in entries_compras:
            valor = fila["Valor Total"].get()
            total += int(float(valor)) if valor else 0

        entry_total.config(state="normal")
        entry_total.delete(0, tk.END)
        entry_total.insert(0, str(total))
        entry_total.config(state="readonly")
        
        total_mirar = entry_total.get()
        total_ajustado = int(float(total_mirar))
        abono = obtener_valor_limpio(var_abono)
        saldo = total_ajustado - abono
        saldo_formateado = "{:,}".format(saldo).replace(",", ".")

        # Actualizamos el campo de saldo
        entry_saldo.config(state="normal")
        entry_saldo.delete(0, tk.END)
        entry_saldo.insert(0, saldo_formateado)
        entry_saldo.config(state="readonly")

        entry_saldo_anterior.config(state="normal")
        entry_saldo_anterior.delete(0, tk.END)
        entry_saldo_anterior.insert(0, saldo_formateado)
        entry_saldo_anterior.config(state="readonly")
        
    except ValueError:
        pass  # Puedes poner un mensaje de error si quieres
def resta_de_abono_nuevo():
    global saldo_anterior_original
    try:
        nuevo_abono = int(entry_nuevo_abono.get() or 0)
    except ValueError:
        nuevo_abono = 0

    nuevo_saldo = saldo_anterior_original - nuevo_abono

    entry_saldo_anterior.configure(state="normal")
    entry_saldo_anterior.delete(0, tk.END)
    entry_saldo_anterior.insert(0, nuevo_saldo)
    entry_saldo_anterior.configure(state="readonly")

#Funciones del metodo de abono
def buscar_facturas_por_documento(documento_cliente):
    try:
        df = obtener_dataframe_desde_sheets(nombre_hoja_interna="Facturas")
        resultados = df[df["Documento"].astype(str) == str(documento_cliente)]
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo buscar por documento: {e}")
        return pd.DataFrame()
def seleccionar_factura_por_documento():#2
    documento = entrada_busqueda.get()
    if not documento:
        messagebox.showwarning("Campo vacío", "Por favor ingrese un número de documento")
        return

    resultados = buscar_facturas_por_documento(documento)

    if resultados.empty:
        messagebox.showinfo("Sin resultados", "No se encontraron facturas para este documento")
        return

    ventana = Toplevel()
    ventana.title("Seleccione una factura")

    listbox = Listbox(ventana, width=120)
    listbox.pack(padx=10, pady=10)

    for index, row in resultados.iterrows():
        resumen = f"Factura N° {row['Numero Factura']} | Cliente: {row['Cliente']} | Fecha: {row['Fecha']} | Total: {row['Total']} | Saldo: {row['Saldo']}"
        listbox.insert(tk.END, resumen)

    def cargar_factura_seleccionada():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una factura")
            return

        fila = resultados.iloc[seleccion[0]]
        factura_seleccionada = fila["Numero Factura"]
        print(factura_seleccionada)
        ventana.destroy()
        visualizar_historial_abonos(factura_seleccionada)
        print(f"factura seleccionada del sistema de abono {factura_seleccionada}")

    tk.Button(ventana, text="Buscar factura", command=cargar_factura_seleccionada).pack(pady=10)
def visualizar_historial_abonos(numero_factura_abono): #3
    resultados = buscar_facturas_abonadas(numero_factura_abono)
    print(f"Este es el número de factura a buscar en abono: {numero_factura_abono}")
    if resultados.empty:
        messagebox.showinfo("Sin resultados", f"No se encontraron registros para la factura N° {numero_factura_abono}")
        return

    ventana = Toplevel()
    ventana.title(f"Historial de abonos - Factura N° {numero_factura_abono}")

    listbox = Listbox(ventana, width=100)
    listbox.pack(padx=10, pady=10)

    for index, row in resultados.iterrows():
        resumen = f"Fecha: {row['Fecha']} | Total: {row['Total']} | Abono: {row['Abono']} | Saldo: {row['Saldo']}"
        listbox.insert(tk.END, resumen)

    def cargar_seleccion():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una versión")
            return

        fila = resultados.iloc[seleccion[0]]
        print(fila)
        global numero_factura_abono
        numero_factura_abono = fila["Numero Factura"]
        precargar_datos_en_gui(fila)
        ventana.destroy()

    boton = tk.Button(ventana, text="Cargar esta factura", command=cargar_seleccion)
    boton.pack(pady=10)
def buscar_facturas_abonadas(numero_factura_abono):
    try:
        # Obtener DataFrame desde la hoja "Abonadas" en el archivo "BBD"
        df = obtener_dataframe_desde_sheets(nombre_hoja_interna="Abonadas")
        
        # Filtrar por número de factura
        resultados = df[df["Numero Factura"].astype(str) == str(numero_factura_abono)]
        return resultados
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo buscar la factura: {e}")
        return pd.DataFrame()
saldo_anterior_original = 0
def precargar_datos_en_gui(fila):
    # Precargar datos generales
    entry_cliente.delete(0, tk.END)
    entry_cliente.insert(0, limpiar_valor(fila.get("Cliente", "")))

    entry_documento.delete(0, tk.END)
    entry_documento.insert(0, fila.get("Documento"))

    entry_direccion.delete(0, tk.END)
    entry_direccion.insert(0, limpiar_valor(fila.get("Direccion", "")))

    entry_celular.delete(0, tk.END)
    entry_celular.insert(0, limpiar_valor(fila.get("Celular")))

    entry_formadepago.delete(0, tk.END)
    entry_formadepago.insert(0, limpiar_valor(fila.get("Forma de pago", "")))

    # Detalles de productos
    for i in range(1, 4):
        cantidad_entry = entries_compras[i-1]["Cantidad"]
        detalle_entry = entries_compras[i-1]["Detalle"]
        valor_unidad_entry = entries_compras[i-1]["Valor Unidad"]
        valor_total_entry = entries_compras[i-1]["Valor Total"]

        cantidad_entry.delete(0, tk.END)
        cantidad_entry.insert(0, fila.get(f"Cantidad{i}", ""))

        detalle_entry.delete(0, tk.END)
        detalle_entry.insert(0, limpiar_valor(fila.get(f"Detalle{i}", "")))

        valor_unidad_entry.delete(0, tk.END)
        valor_unidad_entry.insert(0, fila.get(f"Valor Unidad{i}", ""))

        valor_total_entry.config(state="normal")
        valor_total_entry.delete(0, tk.END)
        valor_total_entry.insert(0, fila.get(f"Valor Total{i}", ""))
        valor_total_entry.config(state="readonly")

    # Abonos y saldo
    saldo = int(float(fila.get("Saldo", 0)))
    abono = int(float(fila.get("Abono", 0)))
    total = int(float(fila.get("Total", 0)))

    entry_saldo.config(state="normal")
    entry_saldo.delete(0, tk.END)
    entry_saldo.insert(0, str(saldo))
    entry_saldo.config(state="readonly")

    entry_abono.config(state="normal")
    entry_abono.delete(0, tk.END)
    entry_abono.insert(0, str(abono))

    entry_total.config(state="normal")
    entry_total.delete(0, tk.END)
    entry_total.insert(0, str(total))
    entry_total.config(state="readonly")

    global saldo_anterior_original
    saldo_anterior_original = saldo

    entry_saldo_anterior.config(state="normal")
    entry_saldo_anterior.delete(0, tk.END)
    entry_saldo_anterior.insert(0, str(saldo))
    entry_saldo_anterior.config(state="readonly")

    var_abono.set(f"{abono:,}".replace(",", "."))

    campos_ojo = [
    "Esfera", "Cilindro", "Eje", "Adición", "Alt Bif", "Dist P.", "Color"
    ]
    for lado in ["Derecho", "Izquierdo"]:
        for campo in campos_ojo:
            key = f"{campo} {lado}"
            entrada = entries_tabla[key]
            entrada.delete(0, tk.END)
            entrada.insert(0, limpiar_valor(fila.get(key, "")))
#Funciones de meotod de modificion

def buscar_factura_para_modificar():
    numero = entrada_busqueda_num_factura.get()
    if not numero:
        messagebox.showwarning("Campo vacío", "Por favor ingresa un número de factura.")
        return

    try:
        # Cargar la hoja "Facturas" desde Google Sheets
        df = obtener_dataframe_desde_sheets(nombre_hoja_interna="Facturas")
    except Exception as e:
        messagebox.showerror("Error al leer el archivo", f"Ocurrió un error:\n{e}")
        return

    # Asegurarse de comparar correctamente el número
    #print("Columnas reales en df:", df.columns.tolist())
    resultados = df[df["Numero Factura"].astype(str).str.strip() == numero.strip()]
    #print(resultados)


    if resultados.empty:
        messagebox.showinfo("Sin resultados", f"No se encontró la factura N° {numero}")
        return

    fila = resultados.iloc[-1]  # Toma la última si hay duplicados
    precargar_datos_en_gui(fila)


#Funciones de PDF
def guardar_factura_en_facturas(datos, estado_factura):
    try:
        hoja_facturas = obtener_sheet("Facturas")
        numero_factura = int(datos["Numero Factura"])
        #print(f"este es el de df 1 {type(numero_factura)}")
        #numero_factura = str(numero_factura)
        #print(f"este es el de df 2 {type(numero_factura)}")
        lista_datos = list(datos.values())
        # Obtener todos los registros actuales
        registros = hoja_facturas.get_all_records()
        fila_a_modificar = None

        # Buscar si ya existe la factura para modificarla
        for i, fila in enumerate(registros):
            if str(fila["Numero Factura"]) == str(numero_factura):
                fila_a_modificar = i + 2  # +2 porque get_all_records omite encabezado y Sheets es 1-indexado
                break

        if fila_a_modificar:
            # Actualizar fila existente
            hoja_facturas.update(f"A{fila_a_modificar}", [lista_datos])
            messagebox.showinfo("Modificada", f"Factura {numero_factura} modificada con éxito.")
        else:
            # Insertar nueva factura al final
            hoja_facturas.append_row(lista_datos)
            messagebox.showinfo("Guardada", f"Factura {numero_factura} guardada con éxito.")

        # Guardar también en hojas especiales según estado
        if estado_factura == "Abonando":
            hoja_abonadas = obtener_sheet("Abonadas")
            hoja_abonadas.append_row(lista_datos)

        elif estado_factura == "Cancelada":
            hoja_canceladas = obtener_sheet("Canceladas")
            hoja_canceladas.append_row(lista_datos)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar la factura en Google Sheets:\n{e}")

def obtener_consecutivo():
    try:
        hoja = obtener_sheet("Facturas")
        # Obtener solo la columna 'Numero Factura' para mayor eficiencia
        numeros_factura = hoja.col_values(1)[1:] # [1:] para omitir el encabezado
        print(numero_factura)
        
        # Filtrar valores vacíos y convertirlos a enteros
        numeros_validos = [int(n) for n in numeros_factura if n.isdigit()]

        if not numeros_validos:
            return 1  # Si no hay facturas, empieza en 1
        
        max_numero = max(numeros_validos)
        return max_numero + 1
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener el consecutivo: {e}")
        return 1
def generar_factura(numero_factura=None):#CREO EL PDF

    saldo_total = entry_saldo.get().replace(".", "").strip()
    saldo_anterior = int(entry_saldo_anterior.get().replace(".", "").strip())

    if saldo_total.isdigit():
        saldo_total = int(saldo_total)
    else:
        saldo_total = 0  # Asume 0 si está vacío o mal escrito
    global estado_factura
    estado_factura = "Cancelada" if saldo_total == 0 or saldo_anterior == 0 else "Abonando"

    entrada = entrada_busqueda_num_factura.get().strip()
    es_nueva = numero_factura is None
    es_modificacion = entrada != ""

    if es_nueva:
        numero_factura = obtener_consecutivo()
    elif es_modificacion:
        numero_factura = entrada
    else:
        numero_factura
    
    numero_factura = int(numero_factura)
    print(type(numero_factura))
    print(numero_factura)


    datos = { 
        "Numero Factura":f"{numero_factura:02}",
        "Cliente": entry_cliente.get().strip().title(), #Primera letra mayuscuala
        "Documento": int(entry_documento.get() or 0), #entrada numero , validar numeros
        "Direccion": entry_direccion.get(), #entrada texto
        "Celular": int(entry_celular.get() or 0), #entrada numero , validar numeros
        "Forma de pago": entry_formadepago.get(), #entrada numeros
        "Fecha": FECHA_ACTUAL, #ESTATICA
        #Cuadro de detalles de la venta
        "Cantidad1": int(float(entries_compras[0]["Cantidad"].get() or 0)),
        "Detalle1": entries_compras[0]["Detalle"].get().strip().capitalize(),
        "Valor Unidad1": int(entries_compras[0]["Valor Unidad"].get() or 0),
        "Valor Total1":entries_compras[0]["Valor Total"].get() or 0,

        "Cantidad2": int(float(entries_compras[1]["Cantidad"].get() or 0)),
        "Detalle2": entries_compras[1]["Detalle"].get().strip().capitalize(),
        "Valor Unidad2": int(entries_compras[1]["Valor Unidad"].get() or 0),
        "Valor Total2": entries_compras[1]["Valor Total"].get() or 0,

        "Cantidad3": int(float(entries_compras[2]["Cantidad"].get() or 0)),
        "Detalle3": entries_compras[2]["Detalle"].get().strip().capitalize(),
        "Valor Unidad3": int(entries_compras[2]["Valor Unidad"].get() or 0),
        "Valor Total3": entries_compras[2]["Valor Total"].get() or 0,

        "Cantidad4": int(float(entries_compras[3]["Cantidad"].get() or 0)),
        "Detalle4": entries_compras[3]["Detalle"].get().strip().capitalize(),
        "Valor Unidad4": int(entries_compras[3]["Valor Unidad"].get() or 0),
        "Valor Total4": entries_compras[3]["Valor Total"].get() or 0,
        #Totales
        "Abono":int(var_abono.get().replace(".", "")) if es_nueva or es_modificacion else  int(entry_nuevo_abono.get().strip().replace(".", "")),
        "Saldo":int(entry_saldo.get().strip().replace(".", "")) if es_nueva or es_modificacion  else int(entry_saldo_anterior.get().strip().replace(".", "")),
        "Total":int(float(entry_total.get() or "0")),
        "Observaciones": entries_obs.get("1.0", "end").strip(), #Primera letra mayuscuala,
        "Esfera Derecho": entries_tabla["Esfera Derecho"].get(),
        "Cilindro Derecho": f"-{entries_tabla["Cilindro Derecho"].get()}",
        "Eje Derecho": entries_tabla["Eje Derecho"].get(),
        "Adición Derecho": entries_tabla["Adición Derecho"].get(),
        "Alt Bif Derecho": entries_tabla["Alt Bif Derecho"].get(),
        "Dist P. Derecho": entries_tabla["Dist P. Derecho"].get(),
        "Color Derecho": entries_tabla["Color Derecho"].get(),
        "Esfera Izquierdo": entries_tabla["Esfera Izquierdo"].get(),
        "Cilindro Izquierdo": f"-{entries_tabla["Cilindro Izquierdo"].get()}",
        "Eje Izquierdo": entries_tabla["Eje Izquierdo"].get(),
        "Adición Izquierdo": entries_tabla["Adición Izquierdo"].get(),
        "Alt Bif Izquierdo": entries_tabla["Alt Bif Izquierdo"].get(),
        "Dist P. Izquierdo": entries_tabla["Dist P. Izquierdo"].get(),
        "Color Izquierdo": entries_tabla["Color Izquierdo"].get(),
        }
    
    datos_especificos = {
        "Dueño":"Elizabeth Montaño Rodriguez",
        "nit":"53 890 573 - 9",
        "Direccion":"Cra 69 #17-42 Sur Villa Claudia",
        "Direccion_dividida1":"Cra 69 #17-42 Sur Villa Claudia",
        #"Direccion_dividida2":"Sibate",
        "telefono_empresa":"313 354 3143",
        "Correo":"lizavisionoptica@gmail.com"
    }

    # Medidas de un cuarto de hoja carta en puntos (1 pulgada = 72 puntos)
    width, height = (612, 396)  # Ancho x Alto, horizontal

    ruta_carpeta = r"C:\Facturas"
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

        # Ruta base del archivo
    nombre_base = f"Factura_{datos['Cliente']}_{datos['Documento']}_{datos['Numero Factura']}"
    ruta_pdf = os.path.join(carpeta_pdfs, f"{nombre_base}.pdf")

    contador = 1
    while os.path.exists(ruta_pdf):
        ruta_pdf = os.path.join(carpeta_pdfs, f"{nombre_base}({contador}).pdf")
        contador += 1

    # Crear el canvas con el tamaño personalizado
    c = pdf_canvas.Canvas(ruta_pdf, pagesize=(width, height))

    #PDF

    # Borde para hoja tamaño 307 x 396
    c.setStrokeColor(colors.HexColor("#0E2C5D"))  # Color del borde (azul oscuro)
    c.setLineWidth(2)  # Grosor del borde
    margen = 15  # Distancia del borde al borde del papel

    # Dibuja el rectángulo
    c.rect(margen, margen, width - 2*margen, height - 2*margen)

    #AQUI EMPIEZA EL PDF

    #Logo
        #Logo
    c.drawImage(ruta_logo,50, 320, width=85, height=40, mask='auto')
    #Encabezado con la fuente personalizada


    c.setFont("Helvetica",18)
    c.setFillColor(colors.HexColor("#0E2C5D"))
    c.drawString(150,  340, "Óptica Liza Vision")

    #Datos especificos
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.HexColor("#070707"))
    c.drawString(150, height - 70,f"{datos_especificos['Dueño']}")
    c.drawString(150, height - 80,f"Nit: {datos_especificos['nit']}")

    c.drawString(width/2+1, height - 53,f"Telefono: {datos_especificos['telefono_empresa']}")
    c.drawString(width/2+1, height - 63,f"Direccion: {datos_especificos['Direccion_dividida1']}")
    c.drawString(width/2+1, height - 73,f"Correo: {datos_especificos['Correo']}")

            # Numero de factura
    c.setFillColor(colors.HexColor("#E21616"))
    c.setFont("Helvetica-Bold", 11)
    c.drawString(430, 310, f"FACTURA DE VENTA N° {datos['Numero Factura']}") 

    #Fecha
    c.setFillColor(colors.HexColor("#070707"))
    c.setFont("Helvetica", 10) #ya quedo
    c.drawString(480, 300, f"Fecha: {datos["Fecha"]}")
    
        # Tabla de datos del cliente
    datos_tabla1 = [[f"Señor@: {datos["Cliente"]}"], 
                [f"Documento: {datos["Documento"]}"]]
    
    datos_tabla2 = [[f"Direccion: {datos["Direccion"]}"],
                   [f"Celular: {datos["Celular"]}"],
                [f"Forma de pago: {datos["Forma de pago"]}"]]
    tabla1 = Table(datos_tabla1, colWidths=[(265)], rowHeights=[14]*len(datos_tabla1))
    tabla2 = Table(datos_tabla2, colWidths=[(265)], rowHeights=[14]*len(datos_tabla2))

    tabla1.setStyle(TableStyle([
        
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#000000")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), 
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    tabla2.setStyle(TableStyle([
        
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#000000")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), 
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    tabla1.wrapOn(c, width, height)
    tabla1.drawOn(c, 40, 262)
    tabla2.wrapOn(c, width, height)
    tabla2.drawOn(c, width/2, 248)    

    

        # Tabla de precios
    datos_tabla = [["Cant", "Detalle", "V. Uni", "V. Total"]]

    for i in range(1, 5):  # Cambié el rango a (1, 4) para cubrir los 3 productos
        cantidad = datos[f"Cantidad{i}"]
        valor_uni = datos[f"Valor Unidad{i}"]
        detalle = datos[f"Detalle{i}"]
        valor_total = datos[f"Valor Total{i}"]

        # Si cantidad o valor unidad son 0, se muestra como ""
        fila = [
            "" if cantidad == 0 else cantidad,
            detalle,
            "" if valor_uni == 0 else valor_uni,
            valor_total
        ]
        
        # Agregar la fila a la tabla en cada iteración
        datos_tabla.append(fila)

    # Generar tabla solo si hay datos
    if len(datos_tabla) > 1:
        tabla = Table(datos_tabla, colWidths=[30, 360, 70, 70], rowHeights=[14] * len(datos_tabla))
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#04214E")),  # Fondo azul oscuro para encabezado
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),                 # Texto blanco para encabezado
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ])) 
        tabla.wrapOn(c, width, height)
        tabla.drawOn(c, 40, 173)

            # Tabla de de abono y de saldo y total
    datos_tabla = [
        ["Abono", f"${datos['Abono']:,}".replace(",", ".")],
        ["Saldo", f"${datos['Saldo']:,}".replace(",", ".")],
        ["Total", f"${datos['Total']:,}".replace(",", ".")]]

    tabla = Table(datos_tabla, colWidths=[40,70], rowHeights=[14]*len(datos_tabla))
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#04214E")),  # Fondo azul oscuro para encabezado
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 460, 120)


        #Obs
    # Establecer la fuente en cursiva
    c.setFont("Times-Italic", 10)  # Cambia 10 por el tamaño que quieras

    # Dibujar el texto de observaciones
    c.drawString(45, 120, f"Observaciones: {datos['Observaciones']}")

    # Regresar a la fuente normal para el resto del documento
    c.setFont("Times-Roman", 10)


        #Cuadros de firma
    datos_tabla = [["\nAceptada", "\nFirma Electronica Autorizada"]]
    tabla = Table(datos_tabla, colWidths=[265,265], rowHeights=[40]*len(datos_tabla)) 
    tabla.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Oblique"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    
    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 40, 75)

        #CC y firma

    c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.70))  # Gris claro con 15% opacidad
    c.setFont("Helvetica", 10) #ya quedo
    c.drawString(45, 90, "CC:_____________________________________")
    c.drawString(45, 100,"Firma:___________________________________")

    c.setFillColor(colors.HexColor("#070707"))
            # Tabla de receta
    datos_tabla = [["Ojo", "Esfera", "Cilindro", "Eje", "Adición","Alt Bif","Dist P.","Color"],
                ["O.D", datos['Esfera Derecho'], datos['Cilindro Derecho'], datos['Eje Derecho'], datos['Adición Derecho'],datos['Alt Bif Derecho'],datos['Dist P. Derecho'],datos['Color Derecho']],
                ["O.I", datos['Esfera Izquierdo'], datos['Cilindro Izquierdo'], datos['Eje Izquierdo'], datos['Adición Izquierdo'],datos['Alt Bif Izquierdo'],datos['Dist P. Izquierdo'],datos['Color Izquierdo']]]

    tabla = Table(datos_tabla, colWidths=[26,72,72,72,72,72,72,72], rowHeights=[13]*len(datos_tabla)) #rowHeights=[40, 50, 50])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#04214E")),  # Fondo azul oscuro para encabezado
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    tabla.wrapOn(c, width, height)
    tabla.drawOn(c, 40, 28)

    #La firma de la optica
    c.drawImage(ruta_firma, 360, 50,width=110,height=80,mask="auto")
    #c.drawImage(ruta_firma, 360, 50,width=110,height=80,mask="auto")

    #la valicaion del cancelado
        #la valicaion del cancelado
    if estado_factura == "Cancelada":
        # Gris claro con opacidad (R, G, B, Alpha)
        c.saveState()
        c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.21))  # Gris claro con 15% opacidad
        c.setFont("Helvetica-Bold", 60)
        c.translate(width / 2, height / 2)
        c.rotate(15)  # texto diagonal
        c.drawCentredString(0, -20, "CANCELADO")
        c.restoreState()
    elif estado_factura == "Abonando":
        c.saveState()
        c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.21))
        c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(0, -20, "ABONO")
        c.restoreState()
    guardar_factura_en_facturas(datos,estado_factura)
    c.save()

        # --- Convertir el PDF en imagen ---
    # Convertir el PDF
    try:
        paginas = convert_from_path(ruta_pdf, dpi=300, poppler_path=poppler_path)
        imagen_factura = os.path.join(carpeta_imagenes, f"{nombre_base}.png")
        paginas[0].save(imagen_factura, "PNG")
        #print(f"Imagen guardada en: {imagen_factura}")
    except Exception as e:
        print("NO se genero la imagen")

    messagebox.showinfo("Éxito", f"Factura guardada en PDF e Imagen: {ruta_pdf}")
    subprocess.run(["start", "", ruta_pdf], shell=True)  # Abre el PDF automáticamente


    # Número al que deseas enviar (con +57 si estás en Colombia)
    numero = f"+57{datos['Celular']}"
    #print(numero)

    # Fecha actual para usarla si quieres mostrarla
    FECHA_ACTUAL_HOY = datetime.now().strftime("%d/%m/%Y")
    print("Fecha:", FECHA_ACTUAL_HOY)


#Aqui empieza el GUI 

# ----------------------------------------------------Crear ventana principal


root = tk.Tk()
# Cambiar el color de fondo de la ventana
root.config(bg="lightblue")
root.title("Sistema de Facturación")
validar_cmd = root.register(validar_numeros)#Lo usan el telefono y el documento
tk.Label(root, text="DATOS DE LA FACTURA\n Optica Liza Vision SEDE 2", font=("Helvetica", 16, "bold")).pack(pady=20)

# Tamaño más pequeño y centrado
ancho = 600
alto = 600
pantalla_ancho = root.winfo_screenwidth()
pantalla_alto = root.winfo_screenheight()
x = (pantalla_ancho // 2) - (ancho // 2)
y = (pantalla_alto // 2) - (alto // 2)
root.geometry(f"{ancho}x{alto}+{x}+{y}")

#------------------------- Frame contenedor con scroll-------------Es el que permite usar la ruedita del mouse-----------------------------
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

frame_principal = tk.Frame(root)
frame_principal.pack()


#Funciones para mostrar las diferentes vistas
def mostrar_nueva_factura():
    frame_principal.pack_forget()
    frame_nueva_factura.pack()
def mostrar_buscar_factura():
    frame_principal.pack_forget()
    frame_buscar_factura.pack()
def mostrar_modificar_factura():
    frame_principal.pack_forget()
    frame_modificar_factura.pack()
#
#----------------------Valdiacion de ejecucion del programa# Crear un archivo temporal para bloqueo
lock_file_path = os.path.join(tempfile.gettempdir(), 'logica_facturas.lock')
lock_file = open(lock_file_path, 'w')

try:
    # Intenta bloquear el archivo
    msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
except OSError: 
    
    # Ya está en ejecución
    
    messagebox.showwarning("Aviso", "La aplicación ya está en ejecución.")
    sys.exit()



#------------------------------------------------------------------Datos del cliente - Frame cliente

labels1 = ["Nombre", "Documento", "Celular", "Dirección", "Forma de pago"]
entries1 = []
frame_inputs = ttk.Frame(scrollable_frame)
frame_inputs.pack(anchor="center")

formas_pago = [ 
    "Sistecrédito", 
    "Nequi o Daviplata", 
    "Efectivo", 
    "Tarjeta de crédito"
]

for idx, label in enumerate(labels1):
    ttk.Label(frame_inputs, text=f"{label}:").grid(column=0, row=idx, padx=5, pady=5, sticky="e")
    
    if label == "Forma de pago":
        entry = ttk.Combobox(frame_inputs, values=formas_pago, state="readonly")
        entry.set("Seleccione")
    
    elif label in ["Documento", "Celular"]:
        validar_numero = root.register(validar_numeros)  
        entry = ttk.Entry(frame_inputs, validate="key", validatecommand=(validar_numero, "%P"))
    
    elif label in ["Nombre"]:
        validar_letras = root.register(validar_texto)  
        entry = ttk.Entry(frame_inputs, validate="key", validatecommand=(validar_letras, "%P"))  
    
    else:
        entry = ttk.Entry(frame_inputs)

    entry.grid(column=1, row=idx, padx=5, pady=5, sticky="ew")
    entries1.append(entry)

frame_inputs.columnconfigure(1, weight=1)

# Si deseas acceder a los campos individualmente
entry_cliente, entry_documento, entry_celular, entry_direccion, entry_formadepago = entries1
entry_cliente, entry_documento, entry_celular, entry_direccion, entry_formadepago = entries1

# -----------------------------------------------------------------------Frame para la tabla de los precios
frame_tabla = ttk.Frame(scrollable_frame)
frame_tabla.pack(anchor="center", pady=10)

ttk.Label(frame_tabla, text="#", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
ttk.Label(frame_tabla, text="Cant", font=("Helvetica", 10, "bold")).grid(row=0, column=1, padx=5, pady=5)
ttk.Label(frame_tabla, text="Detalle", font=("Helvetica", 10, "bold")).grid(row=0, column=2, padx=5, pady=5)
ttk.Label(frame_tabla, text="V. Uni", font=("Helvetica", 10, "bold")).grid(row=0, column=3, padx=5, pady=5)
ttk.Label(frame_tabla, text="V. Total", font=("Helvetica", 10, "bold")).grid(row=0, column=4, padx=5, pady=5)
entries_compras = []
validar = root.register(limitar_caracteres)#Validacion de minimo 24 caracteres
num_filas = 4  # cámbialo si quieres más o menos

for i in range(1, num_filas + 1):
    ttk.Label(frame_tabla, text=str(i)).grid(row=i, column=0, padx=5, pady=5)

    entry_cant = ttk.Entry(frame_tabla, width=10,validate="key", validatecommand=(validar_cmd, "%P"))
    entry_cant.grid(row=i, column=1, padx=5, pady=5)

    entry_detalle = ttk.Entry(frame_tabla, width=20, validate="key", validatecommand=(validar, "%P"))
    entry_detalle.grid(row=i, column=2, padx=5, pady=5)

    entry_valorunidad = ttk.Entry(frame_tabla, width=10, validate="key", validatecommand=(validar_cmd, "%P"))
    entry_valorunidad.grid(row=i, column=3, padx=5, pady=5, sticky="ew")

    entry_valortotal = ttk.Entry(frame_tabla, width=10, state="readonly")
    entry_valortotal.grid(row=i, column=4, padx=5, pady=5)

    # Enlazamos los eventos
    entry_cant.bind("<KeyRelease>", lambda e, ec=entry_cant, ev=entry_valorunidad, et=entry_valortotal: actualizar_total(ec, ev, et))
    entry_valorunidad.bind("<KeyRelease>", lambda e, ec=entry_cant, ev=entry_valorunidad, et=entry_valortotal: actualizar_total(ec, ev, et))

    entries_compras.append({
        "Cantidad": entry_cant,
        "Detalle": entry_detalle,
        "Valor Unidad": entry_valorunidad,
        "Valor Total": entry_valortotal
    })


#.------------------------------------------------------------------------- Frame para totales
frame_totales = ttk.Frame(scrollable_frame)
frame_totales.pack(pady=10)

# Variables como StringVar para mantener el formato visual
var_total = tk.StringVar()
var_abono = tk.StringVar()

# ----------------Entry Total----------------------
ttk.Label(frame_totales, text="Total:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_total = ttk.Entry(frame_totales, width=15, state="readonly")
entry_total.grid(row=0, column=1) 

# --------------Entry Abono con formateo-----------
ttk.Label(frame_totales, text="Abono:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_abono = ttk.Entry(frame_totales, textvariable=var_abono, width=15)
entry_abono.grid(row=1, column=1)
var_abono.trace_add("write", lambda *args: [formatear_gui(var_abono)])

entry_abono.bind("<KeyRelease>", calcular_total_y_saldo)# Ejecutar cuando cambia el abono

# ---------------Entry Saldo (readonly)------------
ttk.Label(frame_totales, text="Saldo:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_saldo = ttk.Entry(frame_totales, width=15, state="readonly")
entry_saldo.grid(row=2, column=1)

#____________________________________Observaciones--------------------------------------------

def limitar_observaciones(event=None):
    contenido = entries_obs.get("1.0", "end-1c")  # end-1c para no contar salto de línea final
    if len(contenido) > 67:
        entries_obs.delete("1.0", "end")
        entries_obs.insert("1.0", contenido[:67])

# Frame para Observaciones
frame_observaciones = ttk.LabelFrame(scrollable_frame, text="Observaciones", padding=(10, 10))
frame_observaciones.pack(fill="x", padx=20, pady=20)

# Campo de texto tipo Text
entries_obs = tk.Text(
    frame_observaciones,
    height=5,
    width=40,
    wrap="word",
    font=("Segoe UI", 10)
)
entries_obs.pack(fill="x", padx=10, pady=10)

# Vincular la función al escribir
entries_obs.bind("<KeyRelease>", limitar_observaciones)
#-------------------------------Limpiar campos ---------------
btn_limpiar = tk.Button(root, text="Limpiar", command=limpiar_campos)
btn_limpiar.pack()


#-------------------------------------------------------------------------- RECETA
frame_tabla = ttk.Frame(scrollable_frame)
frame_tabla.pack(anchor="center", pady=10)

ttk.Label(frame_tabla, text=" ", font=("Helvetica", 10, "bold")).grid(row=0, column=0, padx=5, pady=5)
campos = ["Esfera", "Cilindro", "Eje", "Adición", "Alt Bif", "Dist P.", "Color"]
for j, campo in enumerate(campos, start=1):
    ttk.Label(frame_tabla, text=campo, font=("Helvetica", 10, "bold")).grid(row=0, column=j, padx=5, pady=5)
# Etiquetas para los ojos
ttk.Label(frame_tabla, text="OD").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Label(frame_tabla, text="OI").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entries_tabla = {}
for j, campo in enumerate(campos, start=1):
    entry_derecho = ttk.Entry(frame_tabla, width=10)
    entry_derecho.grid(row=1, column=j, padx=5, pady=5, sticky="ew")
    entry_izquierdo = ttk.Entry(frame_tabla, width=10)
    entry_izquierdo.grid(row=2, column=j, padx=5, pady=5, sticky="ew")
    # Guardamos las referencias
    entries_tabla[f"{campo} Derecho"] = entry_derecho
    entries_tabla[f"{campo} Izquierdo"] = entry_izquierdo


#-------------------------------------------------------------------Principal

btn_nueva = tk.Button(frame_principal, text="1. Nueva factura", width=30, command=mostrar_nueva_factura,bg="lightgreen",fg="black")
btn_nueva.pack(pady=10)
btn_buscar = tk.Button(frame_principal, text="2. Factura existente - Abonar", width=30, command=mostrar_buscar_factura,bg="lightblue",fg="black")
btn_buscar.pack(pady=10)
btn_modificar = tk.Button(frame_principal,text="3. Modificar",width=30,command=mostrar_modificar_factura,bg="#FFD580",fg="black")
btn_modificar.pack(pady=10)


# ----------------------------------------------------------Vista nueva factura.
frame_nueva_factura = tk.Frame(root)

tk.Button(frame_nueva_factura, text="Generar Factura", command=generar_factura, bg="lightgreen", fg="black").pack(pady=40)
btn_volver1 = tk.Button(frame_nueva_factura, text="Menu Principal", command=lambda: [ frame_nueva_factura.pack_forget(), frame_principal.pack(),limpiar_campos()],bg="Red",fg="black")
btn_volver1.pack(pady=10)

#---------------------------------------------------------- Vista buscar factura
numero_factura = 0
frame_buscar_factura = tk.Frame(root)



tk.Label(frame_buscar_factura, text="Digite el número de documento para la búsqueda de la factura").pack()
entrada_busqueda = tk.Entry(frame_buscar_factura)
entrada_busqueda.pack(pady=5)

# Crear un frame dentro de frame_buscar_factura para organizar las columnas
frame_buscar_factura_columnas = tk.Frame(frame_buscar_factura)
frame_buscar_factura_columnas.pack(pady=10)  # Añade un espacio alrededor de todo el frame 


btn_buscar_por_documento = tk.Button(frame_buscar_factura_columnas,text="Buscar por documento",command=seleccionar_factura_por_documento, bg="lightblue",fg="black" )  # <- Usa la función que muestra las facturas
btn_buscar_por_documento.pack(pady=2)


#------------------Saldo precargado abono-------------
# Campo para mostrar el saldo anterior
tk.Label(frame_buscar_factura_columnas, text="Saldo anterior").pack(side="left",pady=5)
entry_saldo_anterior = tk.Entry(frame_buscar_factura_columnas)
entry_saldo_anterior.pack(side="left",pady=5)
#-------------------nuevo abono-------------------------
# Campo para ingresar el nuevo abono
tk.Label(frame_buscar_factura_columnas, text="Nuevo abono").pack(side="left",pady=10)
entry_nuevo_abono = tk.Entry(frame_buscar_factura_columnas)
entry_nuevo_abono.pack(side="left",pady=10)

entry_nuevo_abono.bind("<KeyRelease>", lambda e: resta_de_abono_nuevo())

#-------------------------------------Generar abono----------------------------------------------------------------
btn_generar_abono = tk.Button(frame_buscar_factura_columnas,text="Generar abono",command=lambda: generar_factura(numero_factura_abono),bg="lightblue",fg="black" ) # <- Usa la factura cargada
btn_generar_abono.pack(pady=5)


btn_volver2 = tk.Button(frame_buscar_factura_columnas,text="Menú Principal",command=lambda: [frame_buscar_factura.pack_forget(), frame_principal.pack(),limpiar_campos()],bg="Red",fg="black")
btn_volver2.pack(pady=10)


#---------------------------------------------------------------Modificar factura--------------------------------
frame_modificar_factura = tk.Frame(root)


tk.Label(frame_modificar_factura, text="Digite el numero de la factura").pack()
entrada_busqueda_num_factura = tk.Entry(frame_modificar_factura)
entrada_busqueda_num_factura.pack(pady=5)

btn_buscar_numero_fatura = tk.Button(frame_modificar_factura,text="Buscar Factura",command=lambda: buscar_factura_para_modificar(),bg="#FFD580",fg="black")
btn_buscar_numero_fatura.pack(pady=2)

btn_guardar_factura_modificada = tk.Button(frame_modificar_factura,text="Guardar",command=lambda: generar_factura(entrada_busqueda_num_factura.get()),bg="#FFD580",fg="black")
btn_guardar_factura_modificada.pack(pady=2)

btn_volver3 = tk.Button(frame_modificar_factura,text="Menú Principal", command=lambda: [limpiar_entrada(), frame_modificar_factura.pack_forget(), frame_principal.pack(),limpiar_entrada()],bg="Red",fg="black")
btn_volver3.pack(pady=10)

#print(entrada_busqueda_num_factura)



def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

root.bind_all("<MouseWheel>", _on_mousewheel)

def mostrar_pantalla_carga():
    """Muestra una pantalla de carga mientras se inicializa la aplicación."""
    
    # Crea una ventana nueva para la pantalla de carga
    splash = tk.Toplevel(root)
    splash.title("Cargando...")
    splash.overrideredirect(True) # Quita los bordes de la ventana
    
    # Centra la ventana de carga
    window_width = 300
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    splash.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    label = tk.Label(splash, text="> Espere, cargando...", font=("Helvetica", 12))
    label.pack(pady=30)

    def iniciar_app_en_hilo():
        """Función que ejecuta la lógica de inicio en un hilo separado."""
        
        # Aquí puedes llamar a cualquier función pesada de inicialización,
        # como obtener el consecutivo de la factura o cargar alguna configuración.
        limpiar_campos()
        obtener_dataframe_desde_sheets(nombre_hoja_interna="Facturas")
        # Simula una pequeña demora para que el usuario vea la pantalla de carga
        time.sleep(1) 
        
        # Oculta la ventana de carga y muestra el menú principal
        splash.destroy()
        root.deiconify()
        
        # Muestra el menú principal, que es lo que el usuario verá primero
        frame_principal.pack()

    # Oculta la ventana principal y lanza la carga en un hilo separado
    root.withdraw()
    threading.Thread(target=iniciar_app_en_hilo).start()
mostrar_pantalla_carga()

root.mainloop()
