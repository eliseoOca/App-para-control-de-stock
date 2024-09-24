import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from ttkthemes import ThemedStyle
import os
import subprocess
from tkinter import messagebox
from datetime import datetime
#from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
import subprocess
import random
import string

class ProductCRUD:
    def __init__(self, root):
        self.root = root
        self.root.title("CRUD de Productos, Ventas y Gestión de Fiados y Embases Prestados")
        self.root.geometry("1500x750")  # Establecer el tamaño de la ventana principal
        
        # Conectar a la base de datos o crearla si no existe
        self.conn = sqlite3.connect("productos.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Variables de control para los campos de entrada
        self.nombre_var = tk.StringVar()
        self.codigo_var = tk.IntVar()
        self.marca_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.cantidad_var = tk.IntVar()

        # Variables de control para la pestaña de ventas
        self.codigo_venta_var = tk.IntVar()
        
        # Variables de control para la pestaña de embases prestados
        self.nombre_emb_var = tk.StringVar()
        self.monto_emb_var = tk.DoubleVar()
        self.fecha_emb_var = tk.StringVar()

        # Crear la interfaz de usuario
        self.create_gui()
        
    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                codigo_de_barras INTEGER,
                                marca TEXT,
                                precio REAL,
                                cantidad INTEGER)''')
        self.conn.commit()
        
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS embases (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                monto REAL,
                                fecha TEXT)''')
        self.conn.commit()

        # Crear la nueva tabla cerrar_caja
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS cerrar_caja (
                                id INTEGER PRIMARY KEY,
                                nombre TEXT,
                                marca TEXT,
                                precio REAL,
                                cantidad INTEGER,
                                total REAL)''')
        self.conn.commit()
         

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fiado (
                            id INTEGER PRIMARY KEY,
                            nombre_cliente TEXT,
                            fecha TEXT,
                            monto INTEGER,
                            tipo_fiado TEXT CHECK(tipo_fiado IN ('Transferencias', 'Anotado', 'Otro'))
                          )''')
        self.conn.commit()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS embases_pre (
                            id INTEGER PRIMARY KEY,
                            nombre_cliente TEXT,
                            fecha TEXT,
                            valor_emba INTEGER,
                            tipo_em TEXT CHECK(tipo_em IN ('Cerveza', 'Coca'))
                          )''')
        self.conn.commit()

    def create_gui(self):
        # Crear un objeto de estilo ttkthemes
        style = ThemedStyle(self.root)
        style.set_theme("blue")
        
        # Crear un ttk.Notebook para agregar pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True)
        
        # Pestaña de Productos
        product_tab = ttk.Frame(notebook)
        notebook.add(product_tab, text='Productos')
        
        # Crear un LabelFrame para los campos de entrada en la pestaña de productos
        input_frame = tk.LabelFrame(product_tab, text="Datos del Producto", font=("Arial", 14, "bold"), bg="#F5F5DC")
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Etiquetas y campos de entrada dentro del LabelFrame en la pestaña de productos
        tk.Label(input_frame, text="Nombre:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.nombre_var, font=("Arial", 12)).grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Código de Barras:", font=("Arial", 12), bg="#F5F5DC").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.codigo_var, font=("Arial", 12)).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Marca:", font=("Arial", 12), bg="#F5F5DC").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.marca_var, font=("Arial", 12)).grid(row=2, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Precio:", font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.precio_var, font=("Arial", 12)).grid(row=3, column=3, padx=5, pady=5, sticky="w")

        tk.Label(input_frame, text="Cantidad:", font=("Arial", 12), bg="#F5F5DC").grid(row=4, column=2, padx=5, pady=5, sticky="e")
        tk.Entry(input_frame, textvariable=self.cantidad_var, font=("Arial", 12)).grid(row=4, column=3, padx=5, pady=5, sticky="w")

        tk.Button(input_frame, text="*****Actualizar Panel*****", command=self.update_treeview, font=("Arial", 12)).grid(row=5, column=3, padx=5, pady=5, sticky="w")

        

        # Crear un LabelFrame para los botones CRUD en la pestaña de productos
        button_frame = tk.LabelFrame(product_tab, text="Acciones", font=("Arial", 14, "bold"), bg="#F5F5DC")
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Botón Limpiar en la pestaña de productos
        tk.Button(button_frame, text="Limpiar", command=self.limpiar_campos, font=("Arial", 12)).grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Botones CRUD dentro del LabelFrame en la pestaña de productos
        tk.Button(button_frame, text="Crear", command=self.create_product, font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Buscar Producto", command=self.buscar_producto_gui, font=("Arial", 12)).grid(row=0, column=8, padx=5, pady=5, sticky="w")
        tk.Button(button_frame, text="Actualizar", command=self.update_product, font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame, text="Eliminar", command=self.delete_selected_product, font=("Arial", 12)).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        #tk.Entry(button_frame, font=("Arial", 12)).grid(row=0, column=6, padx=5, pady=5, sticky="nsew")
        tk.Label(button_frame, text="Nombre de Producto:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.nombre_producto_entry_gui = tk.Entry(button_frame, font=("Arial", 12))
        self.nombre_producto_entry_gui.grid(row=0, column=7, padx=5, pady=5, sticky="w")


        # Crear un Treeview para mostrar los datos de la base de datos en la pestaña de productos
        self.tree = ttk.Treeview(product_tab, columns=("ID", "Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"))
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tree.heading("#0", text="")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Código de Barras", text="Código de Barras")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Cantidad", text="Cantidad")

        self.tree.column("ID", anchor="center")
        self.tree.column("Nombre", anchor="center", width=100)
        self.tree.column("Código de Barras", anchor="center", width=100)
        self.tree.column("Marca", anchor="center", width=100)
        self.tree.column("Precio", anchor="center", width=100)
        self.tree.column("Cantidad", anchor="center", width=100)
        self.tree.column("#0", width=5)  # Configurar la anchura de la columna ID
       
         # Configurar el evento de selección en el Treeview
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select_gui)

        # Pestaña de Ventas
        self.add_sales_tab(notebook)

        # Pestaña de Cobro de Fiados
        self.add_fiados_tab(notebook)

        # Pestaña de Embases Prestados
        self.add_embases_prestados_tab(notebook)

        self.add_consult_tab(notebook)

        # Configurar el Grid para que los componentes se expandan automáticamente
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Configurar el Grid de las pestañas para que se expandan automáticamente
        product_tab.grid_columnconfigure(0, weight=1)
        product_tab.grid_rowconfigure(0, weight=1)
        product_tab.grid_rowconfigure(1, weight=1)
        product_tab.grid_rowconfigure(2, weight=1)

        self.cargar_productos_gui()

    def buscar_producto_gui(self):
        try:
            # Limpiar el Treeview antes de realizar una nueva búsqueda
            for record in self.tree.get_children():
                self.tree.delete(record)
            
            nombre = self.nombre_producto_entry_gui.get()  # Obtener el nombre ingresado en el campo de búsqueda
            
            if not nombre:
                messagebox.showwarning("Advertencia", "Por favor, ingrese un nombre de producto para buscar.")
                return

            query = "SELECT * FROM productos WHERE nombre LIKE ?"
            self.cursor.execute(query, ('%' + nombre + '%',))
            rows = self.cursor.fetchall()
            
            # Mostrar los resultados en el Treeview
            if rows:
                for row in rows:
                    self.tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                messagebox.showinfo("Éxito", "Productos encontrados y mostrados en la tabla.")
            else:
                messagebox.showinfo("Información", "No se encontraron productos con el nombre ingresado.")
            
            # Limpiar el campo de búsqueda después de la búsqueda
            self.nombre_producto_entry_gui.delete(0, tk.END)
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de base de datos", f"Ocurrió un error al buscar los productos: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")
    
    def cargar_productos_gui(self):
        try:
            # Limpiar el Treeview antes de cargar los datos
            for record in self.tree.get_children():
                self.tree.delete(record)
            
            # Consultar todos los productos desde la base de datos
            self.cursor.execute("SELECT * FROM productos")
            rows = self.cursor.fetchall()
            
            # Mostrar los resultados en el Treeview
            if rows:
                for row in rows:
                    self.tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]))
                messagebox.showinfo("Éxito", "Productos cargados exitosamente.")
            else:
                messagebox.showinfo("Información", "No hay productos disponibles para mostrar.")
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de base de datos", f"Ocurrió un error al cargar los productos: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")

    def on_tree_select_gui(self, event):
        try:
            # Obtener el índice seleccionado
            selected_item = self.tree.focus()

            # Verificar si se ha seleccionado algún elemento
            if not selected_item:
                raise ValueError("No se ha seleccionado ningún elemento en el Treeview.")

            # Obtener los valores del ítem seleccionado
            values = self.tree.item(selected_item, "values")

            # Verificar si los valores están disponibles
            if not values:
                raise ValueError("No se encontraron valores para el elemento seleccionado.")

            # Actualizar los Entry con los valores del ítem seleccionado
            self.nombre_var.set(values[1])
            self.codigo_var.set(values[2])
            self.marca_var.set(values[3])
            self.precio_var.set(values[4])
            self.cantidad_var.set(values[5])
        
        except ValueError as e:
            messagebox.showwarning("Advertencia", f"Advertencia: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")

    def update_treeview(self):
        try:
            # Limpiar el Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Consultar los datos de la base de datos
            self.cursor.execute("SELECT * FROM productos")
            productos = self.cursor.fetchall()

            # Insertar los datos en el Treeview
            for producto in productos:
                self.tree.insert("", "end", values=producto)

            # Hacer que el Treeview se ajuste automáticamente a los datos
            for col in self.tree['columns']:
                self.tree.heading(col, text=col, anchor=tk.CENTER)
            
            self.cargar_productos_gui()
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error con la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, expand=True)

        self.add_sales_tab(notebook)

    def add_sales_tab(self, notebook):
        sales_tab = ttk.Frame(notebook)
        notebook.add(sales_tab, text='Ventas')

        self.codigo_sales = tk.IntVar()
        self.total_precio_var = tk.DoubleVar(value=0.0)  # Variable para la suma total de los precios

        tk.Label(sales_tab, text="Código de Barras:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        codigo_entry = tk.Entry(sales_tab, textvariable=self.codigo_sales, font=("Arial", 12))
        codigo_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        codigo_entry.bind("<Return>", self.process_barcode)

        input_sales_tab = tk.LabelFrame(sales_tab, text="Datos de la Venta", font=("Arial", 14, "bold"), bg="#F5F5DC")
        input_sales_tab.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        self.nombre_sales = tk.StringVar()
        self.marca_sales = tk.StringVar()
        self.precio_sales = tk.DoubleVar()
        self.cantidad_sales = tk.IntVar()

        tk.Label(input_sales_tab, text="Nombre:", font=("Arial", 12), bg="#F5F5DC").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.nombre_sales, font=("Arial", 12)).grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Marca:", font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.marca_sales, font=("Arial", 12)).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Precio:", font=("Arial", 12), bg="#F5F5DC").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.precio_sales, font=("Arial", 12)).grid(row=4, column=1, padx=5, pady=5, sticky="w")

        tk.Label(input_sales_tab, text="Cantidad:", font=("Arial", 12), bg="#F5F5DC").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        tk.Entry(input_sales_tab, textvariable=self.cantidad_sales, font=("Arial", 12)).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Label para mostrar el total de los precios
        total_label_frame = tk.LabelFrame(sales_tab, text="Total Precio", font=("Arial", 14, "bold"), bg="#F5F5DC")
        total_label_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(total_label_frame, text="Total:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(total_label_frame, textvariable=self.total_precio_var, font=("Arial", 12)).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        button_frame_sales_tab = tk.LabelFrame(sales_tab, text="Acciones", font=("Arial", 14, "bold"), bg="#F5F5DC")
        button_frame_sales_tab.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        tk.Button(button_frame_sales_tab, text="Limpiar Venta", command=self.limpiar_campos_sales, font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame_sales_tab, text="Actualizar Venta", command=self.update_product_sales, font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame_sales_tab, text="Eliminar Venta", command=self.delete_selected_product_sales, font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(button_frame_sales_tab, text="Cerrar Venta", command=self.cerrar_venta, font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky="ew") 
        tk.Button(button_frame_sales_tab, text="Cerrar caja", command=self.cerrar_caja, font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky="ew")  # Botón para cerrar venta

        # Crear y configurar el estilo del Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))  # Fuente del Treeview
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))  # Fuente de las cabeceras del Treeview

        self.sales_tree = ttk.Treeview(sales_tab, columns=("ID", "Nombre", "Código de Barras", "Marca", "Precio", "Cantidad"))
        self.sales_tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.sales_tree.heading("#0", text="")
        self.sales_tree.heading("ID", text="ID")
        self.sales_tree.heading("Nombre", text="Nombre")
        self.sales_tree.heading("Código de Barras", text="Código de Barras")
        self.sales_tree.heading("Marca", text="Marca")
        self.sales_tree.heading("Precio", text="Precio")
        self.sales_tree.heading("Cantidad", text="Cantidad")
        self.sales_tree.column("#0", width=50)

        self.sales_tree.column("ID", anchor="center")
        self.sales_tree.column("Nombre", anchor="center", width=100)
        self.sales_tree.column("Código de Barras", anchor="center", width=100)
        self.sales_tree.column("Marca", anchor="center", width=100)
        self.sales_tree.column("Precio", anchor="center", width=100)
        self.sales_tree.column("Cantidad", anchor="center", width=100)

        # Configurar el Grid para que los componentes se expandan automáticamente
        sales_tab.grid_columnconfigure(0, weight=1)
        sales_tab.grid_columnconfigure(1, weight=1)
        sales_tab.grid_rowconfigure(0, weight=1)
        sales_tab.grid_rowconfigure(1, weight=1)
        sales_tab.grid_rowconfigure(2, weight=1)
        sales_tab.grid_rowconfigure(3, weight=1)

        # Vincular el evento de selección al Treeview
        self.sales_tree.bind("<<TreeviewSelect>>", self.on_treeview_select)
    
    def cerrar_caja(self):
        try:
            # Mostrar mensaje de confirmación
            respuesta = messagebox.askyesno("Confirmar cierre de caja", "¿Desea generar e imprimir el cierre de caja?")
            if not respuesta:
                # Si la respuesta es no, cancelar la operación
                return

            # Crear un nombre de archivo único basado en la fecha y hora actual
            nombre_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"

            # Carpeta donde se guardará el comprobante en el escritorio
            carpeta_caja = os.path.join(os.path.expanduser("~"), "Desktop", "caja")

            # Crear la carpeta si no existe
            if not os.path.exists(carpeta_caja):
                os.makedirs(carpeta_caja)

            # Ruta completa del archivo PDF
            ruta_pdf = os.path.join(carpeta_caja, nombre_archivo)

            # Crear el PDF con tamaño personalizado
            width, height = 48 * mm, 210 * mm  # Convertir a milímetros
            c = canvas.Canvas(ruta_pdf, pagesize=(width, height))

            # Ajustar el tamaño de la fuente
            c.setFont("Helvetica", 8)  # Usar la fuente Helvetica con tamaño 8

            c.drawString(10, height - 30, "Cierre de Caja 2")
            c.drawString(10, height - 50, "*** POLIRUBRO ENZO ***")
            c.drawString(10, height - 70, "Fecha de Cierre: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Consultar los datos de la tabla cerrar_caja
            self.cursor.execute("SELECT nombre, marca, precio, cantidad, total FROM cerrar_caja")
            ventas = self.cursor.fetchall()

            # Acumular las cantidades de artículos repetidos
            acumulados = {}
            for venta in ventas:
                nombre, marca, precio, cantidad, total_venta = venta
                clave = (nombre, marca, precio)
                if clave in acumulados:
                    acumulados[clave]['cantidad'] += cantidad
                    acumulados[clave]['total'] += total_venta
                else:
                    acumulados[clave] = {'cantidad': cantidad, 'total': total_venta}

            # Agregar detalle del cierre
            y_offset = height - 90
            total = 0.0
            for (nombre, marca, precio), datos in acumulados.items():
                cantidad = datos['cantidad']
                total_venta = datos['total']
                total += total_venta
                detalle = f"{nombre}, {marca}, ${precio:.2f} x {cantidad} = ${total_venta:.2f}"

                c.drawString(10, y_offset, detalle)
                y_offset -= 20  # Mover la siguiente línea hacia arriba

            c.drawString(10, y_offset - 20, f"Total de Ventas: ${total:.2f}")

            c.save()

            messagebox.showinfo("Cierre de Caja", f"Se ha generado el cierre de caja: {nombre_archivo} en la carpeta {carpeta_caja}")

            # Abrir el menú de impresión usando subprocess
            try:
                subprocess.run(['cmd', '/c', 'start', '/wait', ruta_pdf, 'print'], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error de impresión", f"No se pudo abrir el menú de impresión para el archivo: {ruta_pdf}\nError: {e}")

            # Borrar los datos de la tabla cerrar_caja
            self.cursor.execute("DELETE FROM cerrar_caja")
            self.conn.commit()
            messagebox.showinfo("Cierre de Caja", "Los datos de la caja han sido borrados exitosamente.")
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error con la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")

    def actualizar_total_venta(self):
        total = 0.0
        for item in self.sales_tree.get_children():
            precio_producto = float(self.sales_tree.item(item, "values")[4])
            cantidad_producto = int(self.sales_tree.item(item, "values")[5])
            total += precio_producto * cantidad_producto
        self.total_precio_var.set(total)

    def delete_selected_product_sales(self):
        try:
            selected_item = self.sales_tree.selection()
            if selected_item:
                item = self.sales_tree.item(selected_item)
                cantidad_actual = item['values'][5]
                precio_producto = item['values'][4]

                if cantidad_actual > 1:
                    nueva_cantidad = cantidad_actual - 1
                    self.sales_tree.item(selected_item, values=(item['values'][0], item['values'][1], item['values'][2], item['values'][3], precio_producto, nueva_cantidad))
                else:
                    self.sales_tree.delete(selected_item)

                total_venta_actual = float(self.total_precio_var.get())  # Convertir el total de la venta a float
                nuevo_total_venta = total_venta_actual - float(precio_producto)  # Convertir precio_producto a float antes de la resta
                self.total_precio_var.set(nuevo_total_venta)
                self.actualizar_total_venta()  # Llamar a la función para actualizar el total de la venta
            else:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para eliminar.")
        except ValueError as e:
            messagebox.showerror("Error de Valor", f"Ocurrió un error al convertir valores: {e}")
        except IndexError as e:
            messagebox.showerror("Error de Índice", f"Ocurrió un error al acceder a los elementos seleccionados: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")
   
    def on_treeview_select(self, event):
        selected_item = self.sales_tree.selection()
        if selected_item:
            item = self.sales_tree.item(selected_item)
            values = item['values']
            # Asume que los valores están en el mismo orden que las columnas definidas
            self.nombre_sales.set(values[1])  # Nombre
            self.marca_sales.set(values[3])   # Marca
            self.precio_sales.set(values[4])  # Precio
            self.cantidad_sales.set(values[5])  # Cantidad
            
    def cerrar_venta(self):
        try:
            total_precio = self.total_precio_var.get()

            if total_precio == 0.0:
                messagebox.showwarning("Venta Vacía", "No hay productos en la venta actual.")
                return

            # Actualizar la cantidad de productos en la base de datos
            for item in self.sales_tree.get_children():
                id = self.sales_tree.item(item, "values")[0]
                cantidad_vendida = int(self.sales_tree.item(item, "values")[5])

                # Obtener la cantidad actual del producto en la base de datos
                self.cursor.execute("SELECT cantidad FROM productos WHERE id = ?", (id,))
                cantidad_actual = self.cursor.fetchone()[0]

                # Calcular la nueva cantidad
                nueva_cantidad = cantidad_actual - cantidad_vendida

                if nueva_cantidad < 0:
                    messagebox.showwarning("Cantidad Insuficiente", f"No hay suficiente stock para el producto ID {id}.")
                    return

                # Actualizar la cantidad en la base de datos
                self.cursor.execute("UPDATE productos SET cantidad = ? WHERE id = ?", (nueva_cantidad, id))

            # Confirmar los cambios en la base de datos
            self.conn.commit()
            
            # Generar comprobante PDF
            self.generar_comprobante_pdf()

            # Limpiar la interfaz para una nueva venta
            self.sales_tree.delete(*self.sales_tree.get_children())
            self.total_precio_var.set(0.0)
            self.limpiar_campos_sales()

            messagebox.showinfo("Venta Cerrada", f"La venta ha sido cerrada. Total: ${total_precio:.2f}")
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error con la base de datos: {e}")
            self.conn.rollback()  # Revertir los cambios en caso de error
        except ValueError as e:
            messagebox.showerror("Error de Valor", f"Ocurrió un error al convertir valores: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")
   
    def update_product_sales(self):
        try:
            # Obtener el ID del producto seleccionado en el Treeview
            selected_item = self.sales_tree.selection()
            if not selected_item:
                messagebox.showerror("Error", "Por favor, selecciona un producto para actualizar.")
                return

            # Obtener los detalles del producto seleccionado
            item_values = self.sales_tree.item(selected_item, 'values')
            product_id = item_values[0]  # El ID del producto es el primer valor

            # Obtener los nuevos valores del nombre, marca y precio
            nombre_actual = self.nombre_sales.get()
            marca_actual = self.marca_sales.get()
            precio_actual = self.precio_sales.get()

            # Obtener la cantidad actual del producto (sin modificarla)
            cantidad_actual = item_values[5]  # Suponiendo que el índice 5 corresponde a la cantidad

            # Actualizar el producto en la base de datos con los nuevos valores
            self.cursor.execute("UPDATE productos SET nombre=?, marca=?, precio=? WHERE id=?",
                                (nombre_actual, marca_actual, precio_actual, product_id))
            self.conn.commit()
            messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

            # Actualizar el Treeview para reflejar los cambios
            self.sales_tree.item(selected_item, values=(product_id, nombre_actual, item_values[2], marca_actual, precio_actual, cantidad_actual))
            self.actualizar_total_venta()  # Llamar a la función para actualizar el total de la venta
        
        except sqlite3.DatabaseError as e:
            messagebox.showerror("Error de Base de Datos", f"Ocurrió un error con la base de datos: {e}")
            self.conn.rollback()  # Revertir los cambios en caso de error
        except ValueError as e:
            messagebox.showerror("Error de Valor", f"Ocurrió un error al convertir valores: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error inesperado: {e}")

    def generar_comprobante_pdf(self):
        # Crear un nombre de archivo único basado en la fecha y hora actual
        nombre_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"

        # Carpeta donde se guardará el comprobante en el escritorio
        carpeta_ventas = os.path.join(os.path.expanduser("~"), "Desktop", "ventas")

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta_ventas):
            os.makedirs(carpeta_ventas)

        # Carpeta con el nombre de la fecha actual
        carpeta_fecha_actual = os.path.join(carpeta_ventas, datetime.now().strftime("%Y-%m-%d"))

        # Crear la carpeta si no existe
        if not os.path.exists(carpeta_fecha_actual):
            os.makedirs(carpeta_fecha_actual)

        # Ruta completa del archivo PDF
        ruta_pdf = os.path.join(carpeta_fecha_actual, nombre_archivo)

        # Crear el PDF con tamaño personalizado
        width, height = 48 * mm, 210 * mm  # Convertir a milímetros
        c = canvas.Canvas(ruta_pdf, pagesize=(width, height))

        # Ajustar el tamaño de la fuente
        c.setFont("Helvetica", 8)  # Usar la fuente Helvetica con tamaño 8

        c.drawString(10, height - 30, "Comprobante de Venta")
        c.drawString(10, height - 50, "*** POLIRUBRO ENZO ***")
        c.drawString(10, height - 70, "Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.drawString(10, height - 90, "Total Precio: $" + str(self.total_precio_var.get()))

        # Agregar detalle de la venta
        y_offset = height - 100
        for item in self.sales_tree.get_children():
            nombre = self.sales_tree.item(item, "values")[1]
            marca = self.sales_tree.item(item, "values")[3]
            precio = self.sales_tree.item(item, "values")[4]
            cantidad = self.sales_tree.item(item, "values")[5]
            detalle = f"Detalle: {nombre}, {marca}, {precio} x {cantidad}"

            c.drawString(10, y_offset, detalle)
            y_offset -= 20  # Mover la siguiente línea hacia arriba

            # Guardar los datos en la base de datos
            total = float(precio) * int(cantidad)
            self.cursor.execute('''INSERT INTO cerrar_caja (nombre, marca, precio, cantidad, total)
                                VALUES (?, ?, ?, ?, ?)''',
                                (nombre, marca, float(precio), int(cantidad), total))
            self.conn.commit()

        c.save()

        messagebox.showinfo("Comprobante Generado", f"Se ha generado el comprobante: {nombre_archivo} en la carpeta {carpeta_fecha_actual}")

        # Mostrar mensaje de guardado exitoso
        messagebox.showinfo("Guardado Exitoso", "Los datos se han guardado correctamente en la tabla cerrar_caja")

        # Abrir el menú de impresión usando subprocess
        try:
            subprocess.run(['cmd', '/c', 'start', '/wait', ruta_pdf, 'print'], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error de impresión", f"No se pudo abrir el menú de impresión para el archivo: {ruta_pdf}\nError: {e}")
       
    def process_barcode(self, event):
        codigo = self.codigo_sales.get()
        self.cursor.execute("SELECT * FROM productos WHERE codigo_de_barras = ?", (codigo,))
        producto = self.cursor.fetchone()
        
        if producto:
            id, nombre, codigo, marca, precio, cantidad = producto
            for item in self.sales_tree.get_children():
                if self.sales_tree.item(item, "values")[2] == str(codigo):
                    current_quantity = int(self.sales_tree.item(item, "values")[5])
                    new_quantity = current_quantity + 1
                    self.sales_tree.item(item, values=(id, nombre, codigo, marca, precio, new_quantity))
                    self.update_total_price()
                    self.codigo_sales.set("")  # Limpiar el campo de entrada del código
                    return
            self.sales_tree.insert("", "end", values=(id, nombre, codigo, marca, precio, 1))
            self.update_total_price()  # Actualizar el total de precios después de agregar un nuevo producto
        else:
            messagebox.showwarning("Código no encontrado", "El código de barras no está en la base de datos.")    
        
        self.codigo_sales.set("")  # Limpiar el campo de entrada del código si no se encontró el producto

    def update_total_price(self):
        total = 0.0
        for item in self.sales_tree.get_children():
            precio = float(self.sales_tree.item(item, "values")[4])
            cantidad = int(self.sales_tree.item(item, "values")[5])
            total += precio * cantidad
        self.total_precio_var.set(total)

    def limpiar_campos_sales(self):
        # Limpiar los campos de entrada
        self.nombre_sales.set("")
        self.codigo_sales.set("")
        self.marca_sales.set("")
        self.precio_sales.set("")
        self.cantidad_sales.set("")
    
    def add_consult_tab(self, notebook):
        # Agregar la pestaña de cobro de fiados al cuaderno
        consult_tab = ttk.Frame(notebook)
        notebook.add(consult_tab, text='Consultar Producto')

        input_consult = tk.LabelFrame(consult_tab, text="Gestionar Productos", font=("Arial", 14, "bold"), bg="#F5F5DC")
        input_consult.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
         # Crear una etiqueta y un campo de entrada para el nombre en la pestaña de cobro de fiados
        
        # Etiqueta y campo de entrada para el nombre del producto
        tk.Label(input_consult, text="Nombre de Producto:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.nombre_producto_entry = tk.Entry(input_consult, font=("Arial", 12))
        self.nombre_producto_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        tk.Button(input_consult, text="Buscar Producto", font=("Arial", 12), command=self.buscar_producto).grid(row=0, column=5, padx=5, pady=5, sticky="w")
        # Dentro de add_consult_tab
        tk.Button(input_consult, text="Limpiar Busqueda", font=("Arial", 12), command=self.limpiar_busqueda_producto).grid(row=1, column=5, padx=5, pady=5, sticky="w")
        tk.Button(input_consult, text="Eliminar", font=("Arial", 12), command=self.eliminar_producto_sal).grid(row=2, column=5, padx=5, pady=5, sticky="w")
        tk.Button(input_consult, text="*****Actualizar Panel*****", font=("Arial", 12), command=self.actualizar_panel_pro).grid(row=1, column=4, padx=5, pady=5, sticky="w")
        

        # Crear un Treeview para mostrar los datos de cobro de fiados
        self.consult_tab_tree = ttk.Treeview(consult_tab, columns=("ID", "Nombre", "Codigo", "Marca", "Precio", "Cantidad"))
        self.consult_tab_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.consult_tab_tree.heading("#0", text="")
        self.consult_tab_tree.heading("ID", text="ID")
        self.consult_tab_tree.heading("Nombre", text="Nombre")
        self.consult_tab_tree.heading("Codigo", text="Codigo")
        self.consult_tab_tree.heading("Marca", text="Marca")
        self.consult_tab_tree.heading("Precio", text="Precio")
        self.consult_tab_tree.heading("Cantidad", text="Cantidad")
        self.consult_tab_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        
        self.consult_tab_tree.column("ID", anchor="center")
        self.consult_tab_tree.column("Nombre", anchor="center", width=100)
        self.consult_tab_tree.column("Codigo", anchor="center", width=100)
        self.consult_tab_tree.column("Marca", anchor="center", width=100)
        self.consult_tab_tree.column("Precio", anchor="center", width=100)
        self.consult_tab_tree.column("Cantidad", anchor="center", width=100)

        consult_tab.grid_columnconfigure(0, weight=1)
       # consult_tab.grid_columnconfigure(1, weight=1)

        consult_tab.grid_rowconfigure(0, weight=1)
        consult_tab.grid_rowconfigure(1, weight=1)
        consult_tab.grid_rowconfigure(2, weight=1)
        consult_tab.grid_rowconfigure(3, weight=1)

        # Botones para agregar, eliminar, actualizar y buscar cobro de fiados
        button_frame = tk.Frame(consult_tab)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        

        self.cargar_productos()

    def eliminar_producto_sal(self):
        selected_item = self.consult_tab_tree.selection()
        if selected_item:
            # Obtener el ID del elemento seleccionado
            item_id = self.consult_tab_tree.item(selected_item, "values")[0]
            
            # Eliminar el elemento del Treeview
            self.consult_tab_tree.delete(selected_item)
            
            # Eliminar el registro de la tabla en la base de datos
            self.cursor.execute('DELETE FROM productos WHERE id = ?', (item_id,))
            self.conn.commit()  # Asegúrate de hacer commit para que los cambios se guarden
        else:
            print("Por favor, seleccione un elemento para eliminar.")

    def actualizar_panel_pro(self):
        # Limpiar el Treeview antes de cargar los datos
        for record in self.consult_tab_tree.get_children():
            self.consult_tab_tree.delete(record)
        
        # Volver a cargar los productos desde la base de datos
        self.cargar_productos()

    def limpiar_busqueda_producto(self):
        # Limpiar el Treeview
        for record in self.consult_tab_tree.get_children():
            self.consult_tab_tree.delete(record)
        
        # Cargar todos los productos nuevamente
        self.cargar_productos()

        # Limpiar el campo de búsqueda
        self.nombre_producto_entry.delete(0, tk.END)

    def buscar_producto(self):
        # Limpiar el Treeview antes de realizar una nueva búsqueda
        for record in self.consult_tab_tree.get_children():
            self.consult_tab_tree.delete(record)
        
        nombre_producto = self.nombre_producto_entry.get()  # Obtener el nombre del producto a buscar
        self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_producto + '%',))
        rows = self.cursor.fetchall()
        
        # Mostrar los resultados en el Treeview
        for row in rows:
            # Determinar el color de fondo según la cantidad de productos
            cantidad = row[5]  # Suponiendo que la cantidad está en la sexta columna (índice 5)
            if cantidad < 10:
                bg_color = "red"
            elif cantidad <= 20:
                bg_color = "yellow"
            else:
                bg_color = "green"  # Color por defecto
            
            self.consult_tab_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=(bg_color,))
            self.consult_tab_tree.tag_configure(bg_color, background=bg_color)

    def cargar_productos(self):
        # Limpiar el Treeview antes de cargar los datos
        for record in self.consult_tab_tree.get_children():
            self.consult_tab_tree.delete(record)
        
        # Ejecutar la consulta SQL ordenada por cantidad
        self.cursor.execute("SELECT * FROM productos ORDER BY cantidad ASC")
        rows = self.cursor.fetchall()
        
        # Mostrar los resultados ordenados en el Treeview
        for row in rows:
            # Determinar el color de fondo según la cantidad de productos
            cantidad = row[5]  # Suponiendo que la cantidad está en la sexta columna (índice 5)
            if cantidad < 10:
                bg_color = "red"
            elif cantidad <= 20:
                bg_color = "yellow"
            else:
                bg_color = "green"  # Color por defecto
            
            self.consult_tab_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=(bg_color,))
            self.consult_tab_tree.tag_configure(bg_color, background=bg_color)
    
    def add_fiados_tab(self, notebook):

        # Agregar la pestaña de cobro de fiados al cuaderno
        fiados_tab = ttk.Frame(notebook)
        notebook.add(fiados_tab, text='Cobro de Fiados')

        # Crear un LabelFrame para los campos de entrada en la pestaña de productos
        input_fiados = tk.LabelFrame(fiados_tab, text="Gestionar Fiados", font=("Arial", 14, "bold"), bg="#F5F5DC")
        input_fiados.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(input_fiados, text="Nombre Cliente:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.nombre_cliente_entry = tk.Entry(input_fiados, font=("Arial", 12))
        self.nombre_cliente_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_fiados, text="Fecha:", font=("Arial", 12), bg="#F5F5DC").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.fecha_entry = tk.Entry(input_fiados, font=("Arial", 12))
        self.fecha_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_fiados, text="Monto:", font=("Arial", 12), bg="#F5F5DC").grid(row=2, column=3, padx=5, pady=5, sticky="e")
        self.monto_entry = tk.Entry(input_fiados, font=("Arial", 12))
        self.monto_entry.grid(row=2, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_fiados, text="Buscar Cliente:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.buscar_cliente_entry = tk.Entry(input_fiados, font=("Arial", 12))
        self.buscar_cliente_entry.grid(row=0, column=7, padx=5, pady=5, sticky="w")

        tk.Button(input_fiados, text="Buscar Cliente", font=("Arial", 12), command=self.buscar_cliente).grid(row=0, column=8, padx=5, pady=5, sticky="w")
        tk.Button(input_fiados, text="Limpiar Busqueda", font=("Arial", 12), command=self.limpiar_busqueda).grid(row=1, column=8, padx=5, pady=5, sticky="w")
        tk.Button(input_fiados, text="*****Actualizar Panel*****", font=("Arial", 12), command=self.actualizar_panel).grid(row=1, column=7, padx=5, pady=5, sticky="w")
        tk.Button(input_fiados, text="******Imprimir Ticket******", font=("Arial", 12), command=self.imprimir_ticket).grid(row=2, column=7, padx=5, pady=5, sticky="w")


        # Checkbuttons con opciones
        self.transferencias_var = tk.BooleanVar()
        self.anotado_var = tk.BooleanVar()
        self.otro_var = tk.BooleanVar()

        tk.Label(input_fiados, text="Tipo de Fiado:", font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=3, padx=5, pady=5, sticky="e")
        tk.Checkbutton(input_fiados, text='Transferencias', variable=self.transferencias_var, font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=4, padx=5, pady=5, sticky="w")
        tk.Checkbutton(input_fiados, text='Anotado', variable=self.anotado_var, font=("Arial", 12), bg="#F5F5DC").grid(row=4, column=4, padx=5, pady=5, sticky="w")
        tk.Checkbutton(input_fiados, text='Otro', variable=self.otro_var, font=("Arial", 12), bg="#F5F5DC").grid(row=5, column=4, padx=5, pady=5, sticky="w")

        # Crear un Treeview para mostrar los datos de cobro de fiados
        self.fiados_tree = ttk.Treeview(fiados_tab, columns=("ID", "Nombre", "Fecha", "Monto", "Tipo"))
        self.fiados_tree.grid(row=1, column=0, columnspan=2, padx=50, pady=50, sticky="nsew")

        self.fiados_tree.heading("#0", text="")
        self.fiados_tree.heading("ID", text="ID")
        self.fiados_tree.heading("Nombre", text="Nombre")
        self.fiados_tree.heading("Monto", text="Monto")
        self.fiados_tree.heading("Fecha", text="Fecha")
        self.fiados_tree.heading("Tipo", text="Tipo")
        #self.fiados_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        
        self.fiados_tree.column("ID", anchor="center")
        self.fiados_tree.column("Nombre", anchor="center", width=100)
        self.fiados_tree.column("Monto", anchor="center", width=100)
        self.fiados_tree.column("Fecha", anchor="center", width=100)
        self.fiados_tree.column("Tipo", anchor="center", width=100)

        fiados_tab.grid_columnconfigure(0, weight=1)
       # fiados_tab.grid_columnconfigure(1, weight=1)

        fiados_tab.grid_rowconfigure(0, weight=1)
        fiados_tab.grid_rowconfigure(1, weight=1)
        fiados_tab.grid_rowconfigure(2, weight=1)
        fiados_tab.grid_rowconfigure(3, weight=1)

        self.fiados_tree.bind("<ButtonRelease-1>", self.on_tree_select_fiados)

        # Botones para agregar, eliminar, actualizar y buscar cobro de fiados
        button_frame = tk.Frame(fiados_tab)
        button_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        tk.Button(button_frame, text="Agregar", command=self.agregar_fiado).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Eliminar", command=self.eliminar_fiado).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Actualizar", command=self.actualizar_fiado).pack(side="left", padx=5, pady=5, fill="x", expand=True)

        # Cargar los fiados al iniciar la interfaz
        self.cargar_fiados()

    def actualizar_panel(self):
        # Limpiar los campos de entrada
        self.nombre_cliente_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.buscar_cliente_entry.delete(0, tk.END)
        self.transferencias_var.set(False)
        self.anotado_var.set(False)
        self.otro_var.set(False)

        # Actualizar el Treeview con los datos más recientes de la base de datos
        self.cargar_fiados()

    def generar_codigo_aleatorio(self, longitud=8):
        letras_y_numeros = string.ascii_uppercase + string.digits
        return ''.join(random.choice(letras_y_numeros) for _ in range(longitud))

    def imprimir_ticket(self):
        if hasattr(self, 'selected_fiado'):
            id_fiado, nombre, fecha, monto, tipo = self.selected_fiado

            # Crear un nombre de archivo único basado en la fecha y hora actual
            nombre_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"

            # Carpeta donde se guardará el ticket en el escritorio
            carpeta_tickets = os.path.join(os.path.expanduser("~"), "Desktop", "ticket")

            # Crear la carpeta si no existe
            if not os.path.exists(carpeta_tickets):
                os.makedirs(carpeta_tickets)

            # Carpeta con el nombre de la fecha actual
            carpeta_fecha_actual = os.path.join(carpeta_tickets, datetime.now().strftime("%Y-%m-%d"))

            # Crear la carpeta si no existe
            if not os.path.exists(carpeta_fecha_actual):
                os.makedirs(carpeta_fecha_actual)

            # Ruta completa del archivo PDF
            ruta_pdf = os.path.join(carpeta_fecha_actual, nombre_archivo)

            # Crear el PDF con tamaño personalizado
            width, height = 48 * mm, 210 * mm  # Convertir a milímetros
            c = canvas.Canvas(ruta_pdf, pagesize=(width, height))

            # Ajustar el tamaño de la fuente
            c.setFont("Helvetica", 8)  # Usar la fuente Helvetica con tamaño 8

            # Generar código aleatorio
            codigo_aleatorio = self.generar_codigo_aleatorio()

            # Agregar título y código aleatorio
            c.drawString(10, height - 10, "Comprobante de deuda")
            c.drawString(10, height - 20, f"Código: {codigo_aleatorio}")

            # Agregar el texto centrado "Polirubro Enzo" con la fecha y hora actuales
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.drawCentredString(width / 2, height - 40, "*** POLIRUBRO ENZO ***")
            c.drawCentredString(width / 2, height - 50, f"Fecha: {fecha_actual}")

            # Agregar los detalles del fiado
            x, y = 10, height - 70
            c.drawString(x, y, f"ID: {id_fiado}")
            c.drawString(x, y - 10, f"Nombre: {nombre}")
            c.drawString(x, y - 20, f"Fecha: {fecha}")
            c.drawString(x, y - 30, f"Monto: {monto}")
            c.drawString(x, y - 40, f"Tipo: {tipo}")

            c.save()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Ticket generado correctamente en {ruta_pdf}")

            # Abrir el menú de impresión usando subprocess
            try:
                if os.name == 'nt':  # Para Windows
                    subprocess.run(['cmd', '/c', 'start', '/wait', ruta_pdf, 'print'], check=True)
                elif os.name == 'posix':  # Para macOS y Linux
                    subprocess.Popen(['open', ruta_pdf])
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error de impresión", f"No se pudo abrir el menú de impresión para el archivo: {ruta_pdf}\nError: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un fiado.")
    
    def buscar_cliente(self):
        # Limpiar el Treeview antes de realizar una nueva búsqueda
        for record in self.fiados_tree.get_children():
            self.fiados_tree.delete(record)
        
        nombre = self.buscar_cliente_entry.get()
        self.cursor.execute("SELECT * FROM fiado WHERE nombre_cliente LIKE ?", ('%' + nombre + '%',))
        rows = self.cursor.fetchall()
        
        # Mostrar los resultados en el Treeview
        for row in rows:
            self.fiados_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4]))

    def limpiar_busqueda(self):
        self.buscar_cliente_entry.delete(0, tk.END)
        self.cargar_fiados()

    def cargar_fiados(self):
        # Limpiar el Treeview antes de cargar los datos
        for record in self.fiados_tree.get_children():
            self.fiados_tree.delete(record)
        
        self.cursor.execute("SELECT * FROM fiado")
        rows = self.cursor.fetchall()
        
        # Mostrar los resultados en el Treeview
        for row in rows:
            self.fiados_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4]))  

    def actualizar_fiado(self):
        selected_item = self.fiados_tree.selection()
        if selected_item:
            nombre = self.nombre_cliente_entry.get()
            fecha = self.fecha_entry.get()
            monto = self.monto_entry.get()
            tipo = []
            if self.transferencias_var.get():
                tipo.append('Transferencias')
            if self.anotado_var.get():
                tipo.append('Anotado')
            if self.otro_var.get():
                tipo.append('Otro')
            tipo = ', '.join(tipo)
            self.fiados_tree.item(selected_item, values=(self.fiados_tree.item(selected_item, 'values')[0], nombre, monto, fecha, tipo))
        else:
            print("Por favor, seleccione un elemento para actualizar.")

    def on_tree_select_fiados(self, event):
        # Obtener el elemento seleccionado del Treeview
        item = self.fiados_tree.selection()
        if not item:
            return

        # Obtener los valores de la fila seleccionada
        values = self.fiados_tree.item(item, "values")
        if not values:
            return

        # Mostrar los valores en los campos de entrada y checkbuttons
        self.nombre_cliente_entry.delete(0, tk.END)
        self.nombre_cliente_entry.insert(0, values[1])  # Nombre del cliente

        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, values[2])  # Fecha

        self.monto_entry.delete(0, tk.END)
        self.monto_entry.insert(0, values[3])  # Monto

        tipo_fiado = values[4]
        self.transferencias_var.set(False)
        self.anotado_var.set(False)
        self.otro_var.set(False)

        if tipo_fiado == 'Transferencias':
            self.transferencias_var.set(True)
        elif tipo_fiado == 'Anotado':
            self.anotado_var.set(True)
        elif tipo_fiado == 'Otro':
            self.otro_var.set(True)

    # Guardar los valores seleccionados en una variable de instancia
        self.selected_fiado = values

    def eliminar_fiado(self):
        selected_item = self.fiados_tree.selection()
        if selected_item:
            # Obtener el ID del elemento seleccionado
            item_id = self.fiados_tree.item(selected_item, "values")[0]
            
            # Eliminar el elemento del árbol
            self.fiados_tree.delete(selected_item)
            
            # Eliminar el registro de la tabla en la base de datos
            self.cursor.execute('DELETE FROM fiado WHERE id = ?', (item_id,))
            self.conn.commit()  # Asegúrate de hacer commit para que los cambios se guarden
        else:
            print("Por favor, seleccione un elemento para eliminar.")

    def limpiar_campos_fiado(self):
        self.nombre_cliente_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.transferencias_var.set(False)
        self.anotado_var.set(False)
        self.otro_var.set(False)

    """def cargar_fiados(self):
        for row in self.fiados_tree.get_children():
            self.fiados_tree.delete(row)
        
        self.cursor.execute("SELECT * FROM fiado")
        fiados = self.cursor.fetchall()
        
        for fiado in fiados:
            self.fiados_tree.insert("", "end", values=fiado)"""
  
    def agregar_fiado(self):
        nombre_cliente = self.nombre_cliente_entry.get()
        monto = self.monto_entry.get()
        fecha = self.fecha_entry.get()
        

        tipo_fiado = []
        if self.transferencias_var.get():
            tipo_fiado.append('Transferencias')
        if self.anotado_var.get():
            tipo_fiado.append('Anotado')
        if self.otro_var.get():
            tipo_fiado.append('Otro')

        # Verificar que solo un tipo de fiado está seleccionado
        if len(tipo_fiado) != 1:
            messagebox.showwarning("Advertencia", "Debe seleccionar un solo tipo de fiado")
            return

        tipo_fiado = tipo_fiado[0]

        if not nombre_cliente or not fecha or not monto:
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados")
            return

        try:
            monto = int(monto)
        except ValueError:
            messagebox.showwarning("Advertencia", "El monto debe ser un número entero")
            return

        try:
            self.cursor.execute('''
                INSERT INTO fiado (nombre_cliente, fecha, monto, tipo_fiado) 
                VALUES (?, ?, ?, ?)''', (nombre_cliente, fecha, monto, tipo_fiado))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Fiado agregado correctamente")
            self.cargar_fiados()  # Llama a la función para actualizar el Treeview
            self.limpiar_campos_fiado()  # Llama a la función para limpiar los campos
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error de Integridad", str(e))

    def add_embases_prestados_tab(self, notebook):
        # Agregar la pestaña de embases prestados al cuaderno
        embases_tab = ttk.Frame(notebook)
        notebook.add(embases_tab, text='Embases Prestados')

        # Crear un LabelFrame para los campos de entrada en la pestaña de productos
        input_embases = tk.LabelFrame(embases_tab, text="Gestionar Fiados", font=("Arial", 14, "bold"), bg="#F5F5DC")
        input_embases.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(input_embases, text="Nombre Cliente:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.nombre_clientem_entry = tk.Entry(input_embases, font=("Arial", 12))
        self.nombre_clientem_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_embases, text="Fecha:", font=("Arial", 12), bg="#F5F5DC").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.fecham_entry = tk.Entry(input_embases, font=("Arial", 12))
        self.fecham_entry.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_embases, text="Valor Embase:", font=("Arial", 12), bg="#F5F5DC").grid(row=2, column=3, padx=5, pady=5, sticky="e")
        self.valor_embam_entry = tk.Entry(input_embases, font=("Arial", 12))
        self.valor_embam_entry.grid(row=2, column=4, padx=5, pady=5, sticky="w")

        tk.Label(input_embases, text="Buscar Cliente:", font=("Arial", 12), bg="#F5F5DC").grid(row=0, column=6, padx=5, pady=5, sticky="e")
        self.buscar_clientem_entry = tk.Entry(input_embases, font=("Arial", 12))
        self.buscar_clientem_entry.grid(row=0, column=7, padx=5, pady=5, sticky="w")

        tk.Button(input_embases, text="Buscar Cliente", font=("Arial", 12), command=self.buscar_cliente_em).grid(row=0, column=8, padx=5, pady=5, sticky="w")
        tk.Button(input_embases, text="Limpiar Busqueda", font=("Arial", 12), command=self.limpiar_busqueda_em).grid(row=1, column=8, padx=5, pady=5, sticky="w")
        tk.Button(input_embases, text="*****Actualizar Panel*****", font=("Arial", 12), command=self.actualizar_panel_em).grid(row=1, column=7, padx=5, pady=5, sticky="w")
        tk.Button(input_embases, text="******Imprimir Ticket******", font=("Arial", 12), command=self.imprimir_ticket_embases).grid(row=2, column=7, padx=5, pady=5, sticky="w")

        # Checkbuttons con opciones
        self.cerveza_var_e = tk.BooleanVar()
        self.coca_var_e = tk.BooleanVar()

        tk.Label(input_embases, text="Tipo de Fiado:", font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=3, padx=5, pady=5, sticky="e")
        tk.Checkbutton(input_embases, text='Cerveza', variable=self.cerveza_var_e, font=("Arial", 12), bg="#F5F5DC").grid(row=3, column=4, padx=5, pady=5, sticky="w")
        tk.Checkbutton(input_embases, text='Coca', variable=self.coca_var_e, font=("Arial", 12), bg="#F5F5DC").grid(row=4, column=4, padx=5, pady=5, sticky="w")

        # Crear un Treeview para mostrar los datos de embases prestados
        self.embases_tree = ttk.Treeview(embases_tab, columns=("ID", "Nombre", "Fecha", "Valor", "TipoE"))
        self.embases_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.embases_tree.heading("#0", text="")
        self.embases_tree.heading("ID", text="ID")
        self.embases_tree.heading("Nombre", text="Nombre")
        self.embases_tree.heading("Fecha", text="Fecha")
        self.embases_tree.heading("Valor", text="Valor")
        self.embases_tree.heading("TipoE", text="Tipo Em")
        self.embases_tree.column("#0", width=50)  # Configurar la anchura de la columna ID
        for col in ("Nombre", "Fecha", "Valor", "TipoE"):
            self.embases_tree.column(col, width=100)  # Configurar la anchura de las otras columnas

        self.embases_tree.column("ID", anchor="center")
        self.embases_tree.column("Nombre", anchor="center", width=100)
        self.embases_tree.column("Fecha", anchor="center", width=100)
        self.embases_tree.column("Valor", anchor="center", width=100)
        self.embases_tree.column("TipoE", anchor="center", width=100)

        embases_tab.grid_columnconfigure(0, weight=1)
       # embases_tab.grid_columnconfigure(1, weight=1)

        embases_tab.grid_rowconfigure(0, weight=1)
        embases_tab.grid_rowconfigure(1, weight=1)
        embases_tab.grid_rowconfigure(2, weight=1)
        embases_tab.grid_rowconfigure(3, weight=1)

        # Botones para agregar, eliminar, actualizar y buscar embases prestados
        button_frame = tk.Frame(embases_tab)
        button_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        tk.Button(button_frame, text="Agregar", command=self.agregar_embase).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Eliminar", command=self.eliminar_embase).pack(side="left", padx=5, pady=5, fill="x", expand=True)
        tk.Button(button_frame, text="Actualizar", command=self.actualizar_embase).pack(side="left", padx=5, pady=5, fill="x", expand=True)

        self.cargar_embases()

        # Asignar evento de selección
        self.embases_tree.bind("<<TreeviewSelect>>", self.mostrar_fila_seleccionada)

    def actualizar_panel_em(self):
        # Limpiar los campos de entrada
        self.nombre_clientem_entry.delete(0, tk.END)
        self.fecham_entry.delete(0, tk.END)
        self.valor_embam_entry.delete(0, tk.END)
        self.buscar_clientem_entry.delete(0, tk.END)
        self.cerveza_var_e.set(False)
        self.coca_var_e.set(False)
        

        # Actualizar el Treeview con los datos más recientes de la base de datos
        self.cargar_embases()
    
    def imprimir_ticket_embases(self):
        if hasattr(self, 'selected_embase'):
            id_embase, nombre, fecha, valor, tipo_em = self.selected_embase

            # Crear un nombre de archivo único basado en la fecha y hora actual
            nombre_archivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".pdf"

            # Carpeta donde se guardará el ticket en el escritorio
            carpeta_tickets = os.path.join(os.path.expanduser("~"), "Desktop", "envases")

            # Crear la carpeta si no existe
            if not os.path.exists(carpeta_tickets):
                os.makedirs(carpeta_tickets)

            # Carpeta con el nombre de la fecha actual
            carpeta_fecha_actual = os.path.join(carpeta_tickets, datetime.now().strftime("%Y-%m-%d"))

            # Crear la carpeta si no existe
            if not os.path.exists(carpeta_fecha_actual):
                os.makedirs(carpeta_fecha_actual)

            # Ruta completa del archivo PDF
            ruta_pdf = os.path.join(carpeta_fecha_actual, nombre_archivo)

            # Crear el PDF con tamaño personalizado
            width, height = 48 * mm, 210 * mm  # Convertir a milímetros
            c = canvas.Canvas(ruta_pdf, pagesize=(width, height))

            # Ajustar el tamaño de la fuente
            c.setFont("Helvetica", 8)  # Usar la fuente Helvetica con tamaño 8

            # Generar código aleatorio
            codigo_aleatorio = self.generar_codigo_aleatorio()

            # Agregar título y código aleatorio
            c.drawString(10, height - 10, "Comprobante de envase")
            c.drawString(10, height - 20, f"Código: {codigo_aleatorio}")

            # Agregar el texto centrado "Polirubro Enzo" con la fecha y hora actuales
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.drawCentredString(width / 2, height - 40, "*** POLIRUBRO ENZO ***")
            c.drawCentredString(width / 2, height - 50, f"Fecha: {fecha_actual}")

            # Agregar los detalles del envase
            x, y = 10, height - 70
            c.drawString(x, y, f"ID: {id_embase}")
            c.drawString(x, y - 10, f"Nombre: {nombre}")
            c.drawString(x, y - 20, f"Fecha: {fecha}")
            c.drawString(x, y - 30, f"Valor: {valor}")
            c.drawString(x, y - 40, f"Tipo: {tipo_em}")

            c.save()

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Ticket generado correctamente en {ruta_pdf}")

            # Abrir el menú de impresión usando subprocess
            try:
                if os.name == 'nt':  # Para Windows
                    subprocess.run(['cmd', '/c', 'start', '/wait', ruta_pdf, 'print'], check=True)
                elif os.name == 'posix':  # Para macOS y Linux
                    subprocess.Popen(['open', ruta_pdf])
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error de impresión", f"No se pudo abrir el menú de impresión para el archivo: {ruta_pdf}\nError: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un envase.")
  
    def buscar_cliente_em(self):
        # Limpiar el Treeview antes de realizar una nueva búsqueda
        for record in self.embases_tree.get_children():
            self.embases_tree.delete(record)
        
        nombre = self.buscar_clientem_entry.get()
        self.cursor.execute("SELECT * FROM embases_pre WHERE nombre_cliente LIKE ?", ('%' + nombre + '%',))
        rows = self.cursor.fetchall()
        
        # Mostrar los resultados en el Treeview
        for row in rows:
            self.embases_tree.insert("", "end", text=row[0], values=(row[0], row[1], row[2], row[3], row[4]))

    def limpiar_busqueda_em(self):
        self.buscar_clientem_entry.delete(0, tk.END)
        self.cargar_embases()
    
    def actualizar_embase(self):
        selected_item = self.embases_tree.selection()
        if selected_item:
            item = self.embases_tree.item(selected_item)
            item_id = item['values'][0]

            nombre_cliente = self.nombre_clientem_entry.get()
            fecha = self.fecham_entry.get()
            valor_emba = self.valor_embam_entry.get()
            tipo_em = 'Cerveza' if self.cerveza_var_e.get() else 'Coca'

            self.cursor.execute('''
                UPDATE embases_pre
                SET nombre_cliente = ?, fecha = ?, valor_emba = ?, tipo_em = ?
                WHERE id = ?
            ''', (nombre_cliente, fecha, valor_emba, tipo_em, item_id))
            self.conn.commit()

            # Actualizar el Treeview
            self.cargar_embases()

            # Limpiar los campos de entrada
            self.nombre_clientem_entry.delete(0, tk.END)
            self.fecham_entry.delete(0, tk.END)
            self.valor_embam_entry.delete(0, tk.END)
            self.cerveza_var_e.set(False)
            self.coca_var_e.set(False)

    def mostrar_fila_seleccionada(self, event):
        selected_item = self.embases_tree.selection()
        if selected_item:
            item = self.embases_tree.item(selected_item)
            values = item['values']

            self.nombre_clientem_entry.delete(0, tk.END)
            self.nombre_clientem_entry.insert(0, values[1])

            self.fecham_entry.delete(0, tk.END)
            self.fecham_entry.insert(0, values[2])

            self.valor_embam_entry.delete(0, tk.END)
            self.valor_embam_entry.insert(0, values[3])

            if values[4] == 'Cerveza':
                self.cerveza_var_e.set(True)
                self.coca_var_e.set(False)
            elif values[4] == 'Coca':
                self.cerveza_var_e.set(False)
                self.coca_var_e.set(True)
        
        self.selected_embase= values

    def eliminar_embase(self):
        selected_item = self.embases_tree.selection()
        if selected_item:
            item = self.embases_tree.item(selected_item)
            item_id = item['values'][0]

            # Eliminar de la base de datos
            self.cursor.execute('DELETE FROM embases_pre WHERE id = ?', (item_id,))
            self.conn.commit()

            # Eliminar del Treeview
            self.embases_tree.delete(selected_item)

    def cargar_embases(self):
        # Limpiar el Treeview
        for row in self.embases_tree.get_children():
            self.embases_tree.delete(row)

        # Cargar los datos desde la base de datos
        self.cursor.execute('SELECT * FROM embases_pre')
        for row in self.cursor.fetchall():
            self.embases_tree.insert('', 'end', values=row)

    def agregar_embase(self):
        nombre_cliente = self.nombre_clientem_entry.get()
        fecha = self.fecham_entry.get()
        valor_emba = self.valor_embam_entry.get()
        tipo_em = 'Cerveza' if self.cerveza_var_e.get() else 'Coca'

        self.cursor.execute('''
            INSERT INTO embases_pre (nombre_cliente, fecha, valor_emba, tipo_em)
            VALUES (?, ?, ?, ?)
        ''', (nombre_cliente, fecha, valor_emba, tipo_em))
        self.conn.commit()

        # Agregar el nuevo registro al Treeview
        self.cargar_embases()

        # Limpiar los campos de entrada
        self.nombre_clientem_entry.delete(0, tk.END)
        self.fecham_entry.delete(0, tk.END)
        self.valor_embam_entry.delete(0, tk.END)
        self.cerveza_var_e.set(False)
        self.coca_var_e.set(False)
      
    def limpiar_campos(self):
        # Limpiar los campos de entrada
        self.nombre_var.set("")
        self.codigo_var.set("")
        self.marca_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")

    def create_product(self):
        nombre = self.nombre_var.get()
        codigo_de_barras = self.codigo_var.get()
        marca = self.marca_var.get()
        precio_str = self.precio_var.get()  # Obtener el valor como cadena
        cantidad_str = self.cantidad_var.get()  # Obtener el valor como cadena
        
        # Validar que los campos obligatorios no estén vacíos
        if nombre and codigo_de_barras and marca and cantidad_str:
            if precio_str or precio_str == "0":  # Aceptar también el valor 0
                try:
                    # Convertir el precio y la cantidad a valores numéricos
                    precio = float(precio_str)
                    cantidad = int(cantidad_str)

                    # Insertar los datos en la base de datos
                    self.cursor.execute("INSERT INTO productos (nombre, codigo_de_barras, marca, precio, cantidad) VALUES (?, ?, ?, ?, ?)",
                                        (nombre, codigo_de_barras, marca, precio, cantidad))
                    self.conn.commit()
                    self.show_data_in_treeview()
                    self.limpiar_campos()
                except ValueError:
                    messagebox.showwarning("Advertencia", "Precio debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "El precio no puede estar vacío")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

    """ def buscar_product(self):
        nombre_busqueda = self.nombre_var.get().strip()  # Obtener el nombre de búsqueda y eliminar espacios en blanco

        if nombre_busqueda:
            # Realizar la búsqueda en la base de datos por nombre
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_busqueda + '%',))
            productos_encontrados = self.cursor.fetchall()

            if productos_encontrados:
                # Limpiar el Treeview antes de mostrar los resultados de la búsqueda
                self.tree.delete(*self.tree.get_children())

                # Mostrar los productos encontrados en el Treeview
                for producto in productos_encontrados:
                    self.tree.insert("", "end", values=producto)
            else:
                messagebox.showinfo("Información", f"No se encontraron productos con el nombre '{nombre_busqueda}'.")
        else:
            # Si no se ingresó ningún nombre de búsqueda, mostrar todos los productos en el Treeview
            self.show_data_in_treeview()"""

    def update_product(self):
        # Obtener el ID del producto seleccionado en el Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un producto para actualizar.")
            return

        # Obtener los detalles del producto seleccionado
        item_values = self.tree.item(selected_item, 'values')
        product_id = item_values[0]  # El ID del producto es el primer valor

        # Obtener los valores actuales del producto seleccionado
        nombre_actual = self.nombre_var.get()
        codigo_actual = self.codigo_var.get()
        marca_actual = self.marca_var.get()
        precio_actual = self.precio_var.get()
        cantidad_actual = self.cantidad_var.get()

        # Validar si se han realizado cambios en los campos
        if nombre_actual == item_values[1] and codigo_actual == item_values[2] and marca_actual == item_values[3] \
                and precio_actual == item_values[4] and cantidad_actual == item_values[5]:
            messagebox.showinfo("Información", "No se han realizado cambios en los campos.")
            return

        # Obtener los nuevos valores introducidos por el usuario
        nombre_nuevo = self.nombre_var.get()
        codigo_nuevo = self.codigo_var.get()
        marca_nueva = self.marca_var.get()
        precio_nuevo = self.precio_var.get()
        cantidad_nueva = self.cantidad_var.get()

        # Actualizar el producto en la base de datos con los nuevos valores
        self.cursor.execute("UPDATE productos SET nombre=?, codigo_de_barras=?, marca=?, precio=?, cantidad=? WHERE id=?",
                            (nombre_nuevo, codigo_nuevo, marca_nueva, precio_nuevo, cantidad_nueva, product_id))
        self.conn.commit()
        messagebox.showinfo("Éxito", "Producto actualizado correctamente.")

        # Actualizar el Treeview para reflejar los cambios
        self.show_data_in_treeview()

    def delete_selected_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un producto para eliminar.")
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar el producto seleccionado?")
        if confirm:
            for item in selected_item:
                product_id = self.tree.item(item, "values")[0]
                self.cursor.execute("DELETE FROM productos WHERE id=?", (product_id,))
                self.conn.commit()
            messagebox.showinfo("Éxito", "Producto(s) eliminado(s) correctamente.")
            self.show_data_in_treeview()  # Actualizar la vista de Treeview

    def show_data_in_treeview(self):
        # Eliminar todos los elementos actuales del Treeview
        self.tree.delete(*self.tree.get_children())
        
        # Ejecutar la consulta para obtener los datos de la base de datos
        self.cursor.execute("SELECT * FROM productos")
        
        # Iterar sobre las filas obtenidas y agregarlas al Treeview
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)
        
        # Programar la próxima actualización
        #self.root.after(2000, self.show_data_in_treeview)  # Actualiza cada 5 segundos

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductCRUD(root)
    root.mainloop()
