"""import tkinter as tk
import sqlite3

def leer_codigo_barra():
    # Obtener el código de barras del campo de entrada
    codigo_barras = codigo_var.get()
    print("Código de barras leído:", codigo_barras)

# Crear la ventana principal
root = tk.Tk()
root.title("Lectura de Código de Barras")

# Crear una variable de control para el código de barras
codigo_var = tk.StringVar()

# Crear un campo de entrada para ingresar el código de barras
codigo_entry = tk.Entry(root, textvariable=codigo_var)
codigo_entry.pack(pady=10)

# Crear un botón para leer el código de barras
leer_button = tk.Button(root, text="Leer Código de Barras", command=leer_codigo_barra)
leer_button.pack(pady=5)

# Ejecutar la aplicación
root.mainloop()
"""