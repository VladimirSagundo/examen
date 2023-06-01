import tkinter as tk
import mysql.connector
from tkinter import ttk
import subprocess

bd = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="veterinario"
)

mi_cursor = bd.cursor()
mi_cursor.execute("SELECT id, nombre_apellido, fecha, hora from veterinario order by fecha desc, hora desc")
resultado = mi_cursor.fetchall()

# crear ventana de Tkinter
ventana = tk.Tk()
ancho_ventana = 620
alto_ventana = 480
x_ventana = ventana.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = ventana.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
ventana.geometry(posicion)
ventana.title("Registros")
primero = tk.Label(ventana, text="- Registro de Citas -", bg='#383838', fg="white", font='Times 20').pack(pady=30)

# crear Table
tabla = ttk.Treeview(ventana)
tabla['columns'] = ('nombre_apellido', 'fecha', 'hora')

# ajustar las columnas
tabla.column('#0', width=0, stretch=tk.NO)
tabla.column('nombre_apellido', anchor=tk.CENTER, width=200)
tabla.column('fecha', anchor=tk.CENTER, width=100)
tabla.column('hora', anchor=tk.CENTER, width=100)

# heading
tabla.heading('#0', text='', anchor=tk.CENTER)
tabla.heading('nombre_apellido', text='Nombre', anchor=tk.CENTER)
tabla.heading('fecha', text='Fecha', anchor=tk.CENTER)
tabla.heading('hora', text='Hora', anchor=tk.CENTER)

ban = True
# agregamos datos
for valor in resultado:
    iid = valor[0]  # Asignamos el ID del registro como el iid
    if ban:
        tabla.insert(parent='', index='end', iid=iid, tag=['t1'], values=(valor[1], valor[2], valor[3]))
        ban = False
    else:
        tabla.insert(parent='', index='end', iid=iid, tag=['t2'], values=(valor[1], valor[2], valor[3]))
        ban = True

tabla.tag_configure('t1', foreground='white', background='#383838', font="Times 12")
tabla.tag_configure('t2', foreground='#FFCC00', background='#003366', font="Times 12")

# mostramos tabla en ventana
tabla.pack()


def eliminar_registro():
    seleccionado = tabla.focus()  # Obtenemos el ID del registro seleccionado
    if seleccionado:
        id_registro = seleccionado  # El ID del registro es el propio valor seleccionado
        eliminar_sql = "DELETE FROM veterinario WHERE id = %s"
        mi_cursor.execute(eliminar_sql, (id_registro,))
        bd.commit()
        tabla.delete(seleccionado)  # Eliminamos el registro de la tabla


def regresar():
    ventana.destroy()
    subprocess.call(["python", "administrador.py"])


button_eliminar = tk.Button(ventana, text="Eliminar", command=eliminar_registro, font="Times", bg="#585858", fg="white")
button_eliminar.pack(side=tk.LEFT, padx=10, pady=10)
button_regresar = tk.Button(ventana, text="Regresar", command=regresar, font="Times", bg="#585858", fg="white")
button_regresar.pack(side=tk.RIGHT, padx=10, pady=10)

ventana['bg'] = '#383838'
ventana.resizable(width=0, height=0)
ventana.mainloop()