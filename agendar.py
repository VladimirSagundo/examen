from tkinter import ttk
import tkinter as tk
import subprocess
import mysql.connector

class crear_cita:
        
    def __init__(self, master):
        self.master = master
        self.master.title("Registro de citas")
        self.master.config(padx=120, pady=130, bg='#383838')
        self.crear_espacios()
        self.datos_ingresados = False

    def crear_espacios(self):
        def menú():
            cita.destroy()
            subprocess.call(["python", "Proyecto_menú.py"])
        
        def limitar_entry(entrada, limit):
            def limitar(event):
                texto = entrada.get()
                if len(texto) >= limit and not event.keysym == 'BackSpace':
                    return "break"
            entrada.bind("<Key>", limitar)  
        
        def letra(char):
            return char in "qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNMáéíóúÁÉÍÓÚ"
        
        def numero(char):
            return char in "0123456789/"
        
        def numero_hora(char):
            return char in "0123456789:"
        
        validatecommand_letra = cita.register(letra)
        
        label_titulo = tk.Label(cita, text="- Agendar cita -", font="Times 30", fg="white", bg="#383838").grid(row=0, column=0, pady=0)
        
        tk.Label(self.master, text= "Nombre:", fg="white", bg="#383838", font="Times 12").grid(row=2, column=0, pady=10)
        self.nombre_entry = tk.Entry(self.master, bg="#D7D8DA", fg="black", validate="key", validatecommand=(validatecommand_letra, "%S"))
        limitar_entry(self.nombre_entry, 30)
        self.nombre_entry.grid(row=2, column=1)
        
        tk.Label(self.master, text= "Fecha de la cita (DMA):", fg="white", bg="#383838", font="Times 12").grid(row=3, column=0, pady=10)
        dia=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]
        mes=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
        año=["2023"]
        self.fecha_entry = ttk.Combobox(self.master, values=dia, style='TCombobox', state="readonly", justify="center", width=5)
        self.fecha_mes = ttk.Combobox(self.master, values=mes, style='TCombobox', state="readonly", justify="center", width=5)
        self.fecha_año = ttk.Combobox(self.master, values=año, style='TCombobox', state="disabled", justify="center", width=5)
        self.fecha_año.set("2023")
        self.fecha_mes.set("12")
        self.fecha_entry.set("1")
        self.fecha_entry.grid(row=3, column=1)
        self.fecha_mes.grid(row=3, column=2)
        self.fecha_año.grid(row=3, column=3)

        dia= self.fecha_entry.get()
        mes= self.fecha_mes.get()
        año= self.fecha_año.get()
        self.fecha_completa=f"{año}/{mes}/{dia}"

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TCombobox', fieldbackground='#424242')
        horas=["12:00 pm", "12:30 pm", "1:00 pm", "1:30 pm", "2:00 pm", "2:30 pm", "3:00 pm", "3:30 pm", "4:00 pm", "4:30 pm", "5:00 pm", "5:30 pm", "6:00 pm"]
        tk.Label(self.master, text= "Hora (Unicamente de 12:00 pm a 6:00 pm):", fg="white", bg="#383838", font="Times 12").grid(row=4, column=0, pady=10)
        self.combo = ttk.Combobox(self.master, values=horas, style='TCombobox', state="readonly", justify="center", width=17)
        self.combo.set("12:00 pm")
        self.combo.grid(row=4, column=1)

        self.registrar_button = tk.Button(self.master, text="Registrar citas", command=self.registrar_cita, bg="#585858", fg="white")
        self.registrar_button.grid(row=5, column=1, pady=10)
        
        self.actualizar_button = tk.Button(self.master, text="Actualizar registro", command=self.actualizar_registro, bg="#585858", fg="white")
        self.actualizar_button.grid(row=5, column=0)
        
        regresar_button = tk.Button(self.master, text="Regresar", command=menú, fg="white", bg="#585858")
        regresar_button.grid(row=6, column=1, pady=10)

        self.registro_exitoso_label = tk.Label(self.master, text="", fg="white", bg="#383838")
        self.registro_exitoso_label.grid(row=7, column=1)

    def registrar_cita(self):
        if self.datos_ingresados:
            self.registro_exitoso_label.configure(text="¡LOS DATOS YA HAN SIDO REGISTRADOS!", bg='#710C04', fg="black", font='Times 10')
            self.registro_exitoso_label.grid(row=7, column=0)
            return

        nombre = self.nombre_entry.get()
        dia= self.fecha_entry.get()
        mes= self.fecha_mes.get()
        año= self.fecha_año.get()
        fecha = f"{año}/{mes}/{dia}"
        hora = self.combo.get()
        

        try:
            connection = mysql.connector.connect(host='localhost', database='veterinario', user='root', password='')

            mySql_insert_query = """INSERT INTO veterinario (nombre_apellido, fecha, hora) VALUES ('"""+nombre+"','"+fecha+"','" + hora + "')" 
         
            print(mySql_insert_query)
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into veterinario table")
            cursor.close()

            self.datos_ingresados = True

        except mysql.connector.Error as error:
            print("Failed to insert record into veterinario table {}".format(error))

        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")

        self.nombre_entry.delete(0, tk.END)
        dia= self.fecha_entry.delete(0, tk.END)
        mes= self.fecha_mes.delete(0, tk.END)
        año= self.fecha_año.delete(0, tk.END)
        fecha = f"{año}/{mes}/{dia}"
        self.combo.delete(0, tk.END)

        self.registro_exitoso_label.configure(text="¡REGISTRO EXITOSO!")

    def actualizar_registro(self):
        nombre = self.nombre_entry.get()
        dia = self.fecha_entry.get()
        mes = self.fecha_mes.get()
        año = self.fecha_año.get()
        fecha = f"{año}/{mes}/{dia}"
        hora = self.combo.get()

        try:
            connection = mysql.connector.connect(host='localhost', database='veterinario', user='root', password='')

            mySql_update_query = """UPDATE veterinario SET fecha = '""" + fecha + """', hora = '""" + hora + """' WHERE nombre_apellido = '""" + nombre + """'"""
         
            print(mySql_update_query)
            cursor = connection.cursor()
            cursor.execute(mySql_update_query)
            connection.commit()
            print(cursor.rowcount, "Record updated successfully in veterinario table")
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to update record in veterinario table {}".format(error))

        finally:
            if connection.is_connected():
                connection.close()
                print("MySQL connection is closed")

        self.nombre_entry.delete(0, tk.END)
        dia= self.fecha_entry.delete(0, tk.END)
        mes= self.fecha_mes.delete(0, tk.END)
        año= self.fecha_año.delete(0, tk.END)
        fecha = f"{año}/{mes}/{dia}"
        self.combo.delete(0, tk.END)

        self.registro_exitoso_label.configure(text="¡ACTUALIZACIÓN EXITOSA!")


cita = tk.Tk()
ancho_ventana = 620
alto_ventana = 480
x_ventana = cita.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = cita.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
cita.geometry(posicion)
crear = crear_cita(cita)
cita.resizable(width=0, height=0)
cita.mainloop()