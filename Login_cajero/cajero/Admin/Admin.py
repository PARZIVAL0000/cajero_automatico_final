#!/usr/bin/env python3
#_*_ coding:utf-8 _*_ 


"""
    La interfaz de nuestro administrador
    poseera un CRUD referente: CREAR USUARIOS (CLIENTE O ADMINISTRADOR) / LEER CUENTAS / ELIMINAR / 
    ACTUALIZAR TODAS LAS CUENTAS -> si es necesario hacerlo ....
"""

import tkinter as tk 
import threading
import time, re 
from functools import partial
from tkinter import ttk 
from tkinter import messagebox
from tkinter import * 
from cajero import Login
from cajero.db import database as DB
from cajero.Admin.codigos_cedula import codigos


def admin(nombre, id):
    class Admin(Frame):

        #Eliminacion y restauracion de widgets
        def mostrar(self, tipo = ''):
            if(tipo == 'OBSERVAR'):
                self.marco.destroy()
                self.Regresar.destroy()


                self.Descripcion['text'] = 'GESTIÓN DE CUENTAS BANCARIAS'
                self.ReadUsers.grid()
                self.CreateUsers.grid()
                self.DeleteUsers.grid()
                self.UpdateUsers.grid()
            else:
                #eliminamos algunos widgets de espacios anteriores.
                self.preguntar = messagebox.askquestion('Regresar', '¿Deseas continuar?, perderás los cambios que realizaste hasta este momento')
                if(self.preguntar == 'yes'):
                    self.marco.destroy()
                    self.Regresar.destroy()


                    self.Descripcion['text'] = 'GESTIÓN DE CUENTAS BANCARIAS'
                    self.ReadUsers.grid()
                    self.CreateUsers.grid()
                    self.DeleteUsers.grid()
                    self.UpdateUsers.grid()
            

        def __init__(self, parent):
            self.ejecutarOjo = "VER" #Esta variable esta relacionado en como mostrar el ojito....
            self.CedulaCopia = ['']
            super().__init__(parent)
            parent.title("ADMINISTRADOR {}".format(nombre))
            parent.configure(bg="#002643")
            # parent.configure(width=600, height=650)
            parent.geometry("600x650")


            self.headers = Label(self, text="ADMINISTRADOR : ", fg="white", bg="#005e99", font=("Arial", 12), width=15)
            self.headers.grid(row=0, column=0, ipady=15, ipadx=25)

            self.NombreAdministrador = Label(self, text="{}".format(nombre), fg="white", bg="#005e99", font=("Arial", 12), width=20, anchor="w")
            self.NombreAdministrador.grid(
                row=0, 
                column=1,
                ipady=15,
            )

            self.separador = Label(self, text="", fg="white", bg="#005e99", font=("Arial", 12), width=40)
            self.separador.grid(
                row=0, 
                column=2,
                ipady=15,
            )
            

            self.BotonLogout = Button(self, text='Cerrar Sesión', command=self.logout, anchor="center", border=0, bg="#840907", fg="white", cursor="hand1", activebackground="#5c0907", activeforeground="white", borderwidth=0)
            self.BotonLogout.grid(
                row=0, column=2,
                padx=100,
                sticky="w", 
                ipady=5, 
                ipadx=5
            )


            self.Descripcion = Label(self, text="GESTIÓN DE CUENTAS BANCARIAS", bg="#00759f", fg="white", width=75, anchor="center")
            self.Descripcion.grid(
                row=1, 
                column=0,
                columnspan=4,
                ipady=10,
                ipadx=50,
                sticky="w"
            )

            #Crearemos una opciones en forma de boton para que el usuario los pueda eleguir .... 
            self.iconoRead = PhotoImage(file="./cajero/img/search.png")
            self.ReadUsers = Button(
            self, 
            text="VER CUENTAS", 
            border=0,
            width=175,
            height=120,
            font=("Arial", 12),
            bg="#e07500",
            fg="white",
            cursor="hand1",
            activebackground="#f19d1c",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarReadUsers,
            image=self.iconoRead,
            compound=tk.TOP,
            padx=10
            )
            self.ReadUsers.grid(
                row=2, 
                column=0,
                pady=100,
                padx=50,
                columnspan=2, 
                sticky="w"
            )

            self.iconoCrear = PhotoImage(file="./cajero/img/crear.png")
            self.CreateUsers = Button(
            self, 
            text="CREAR CUENTAS", 
            border=0,
            width=195,
            height=120,
            font=("Arial", 12),
            bg="#a981e5",
            fg="white",
            cursor="hand1",
            activebackground="#810053",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarCreateUsers,
            image=self.iconoCrear,
            compound=tk.TOP
            )
            self.CreateUsers.grid(
                row=3, 
                column=0,
                pady=10,
                padx=50,
                columnspan=2,
                sticky="w"
            )

            self.iconoDelete = PhotoImage(file="./cajero/img/eliminar.png")
            self.DeleteUsers = Button(
            self, 
            text="ELIMINAR CUENTAS", 
            border=0,
            width=195,
            height=120,
            font=("Arial", 12),
            bg="#680930",
            fg="white",
            cursor="hand1",
            activebackground="#b2283a",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarDeleteUsers,
            image=self.iconoDelete,
            compound=tk.TOP
            )
            self.DeleteUsers.grid(
                row=2, 
                column=1,
                pady=100,
                padx=160,
                columnspan=2, 
                sticky="w"
            )

            self.iconoUpdate = PhotoImage(file="./cajero/img/update.png")
            self.UpdateUsers = Button(
            self, 
            text="ACTUALIZAR CUENTAS", 
            border=0,
            width=195,
            height=120,
            font=("Arial", 12),
            bg="#004800",
            fg="white",
            cursor="hand1",
            activebackground="#6f8800",
            activeforeground="white",
            borderwidth=2,
            command=self.ejecutarUpdateUsers,
            image=self.iconoUpdate,
            compound=tk.TOP
            )
            self.UpdateUsers.grid(
                row=3, 
                column=1,
                pady=10,
                padx=160,
                columnspan=2, 
                sticky="w"
            )


            self.grid(sticky="nsew")    
            self.configure(bg="#002643")


        def ejecutarDesplazamiento(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            
            #CORREGIR LOS SIGUIENTES ERRORES:
                # 1.-) QUE NO TIEMBLE AL MOMENTO DE HACER UN DESPLAZAMIENTO LENTO.
                # 2.-) QUE LA INTERFAZ PUEDA DESPLAZARSE LENTAMENTE..... NO GENERE UN GOLPETEO A LA IZQUIERDA
            try:
               
                if(args[0].x >= 0):
                    if(aumentarAncho > 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerNombre['width'] = aumentarAncho
                        self.ListadoNombres['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerNombre['width'] = aumentarAncho
                        self.ListadoNombres['width'] = aumentarAncho
                

                #este es el control para que pueda funcionar el scroll horizontal.
                if(args[0].key == 6):
                    time.sleep(1)
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento2(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerCedula['width'] = aumentarAncho
                        self.ListadoCedula['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerCedula['width'] = aumentarAncho
                        self.ListadoCedula['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento3(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerTelefono['width'] = aumentarAncho
                        self.ListadoTelefono['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerTelefono['width'] = aumentarAncho
                        self.ListadoTelefono['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento4(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerEmail['width'] = aumentarAncho
                        self.ListadoEmail['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerEmail['width'] = aumentarAncho
                        self.ListadoEmail['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass

        def ejecutarDesplazamiento5(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerProvincia['width'] = aumentarAncho
                        self.ListadoProvincia['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerProvincia['width'] = aumentarAncho
                        self.ListadoProvincia['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass


        def ejecutarDesplazamiento6(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerPermisos['width'] = aumentarAncho
                        self.ListadoPermisos['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerPermisos['width'] = aumentarAncho
                        self.ListadoPermisos['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass

        def ejecutarDesplazamiento7(self, aumentarAncho, *args):
            # 6 -> desplazar 
            # 5 -> Boton Liberado
            try:
                if(args[0].x >= 0):
                    if(aumentarAncho >= 0 and aumentarAncho < 25):
                        aumentarAncho += 1
                        self.headerPresupuesto['width'] = aumentarAncho
                        self.ListadoPresupuesto['width'] = aumentarAncho
                    
                else:
                    if(aumentarAncho > 5):
                        aumentarAncho -= 1
                        self.headerPresupuesto['width'] = aumentarAncho
                        self.ListadoPresupuesto['width'] = aumentarAncho
                

                if(args[0].key == 6):
                    self.after(0000, self.ejecutarDesplazamiento, aumentarAncho, args[0])
                        

            except AttributeError:
                pass
    

        def ejecutarEvento(self,*args):
            #este es para el primero evento
            self.anchura = self.headerNombre['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento2(self,*args):
            #este es para el primero evento
            self.anchura = self.headerCedula['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento2(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento3(self,*args):
            #este es para el primero evento
            self.anchura = self.headerTelefono['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento3(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento4(self,*args):
            #este es para el primero evento
            self.anchura = self.headerEmail['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento4(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento5(self,*args):
            #este es para el primero evento
            self.anchura = self.headerProvincia['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento5(self.anchura, args[0]))
            self.hiloEjecucion.start()


        def ejecutarEvento6(self,*args):
            #este es para el primero evento
            self.anchura = self.headerPermisos['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento6(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        def ejecutarEvento7(self,*args):
            #este es para el primero evento
            self.anchura = self.headerPresupuesto['width']

            self.hiloEjecucion = threading.Thread(target=self.ejecutarDesplazamiento7(self.anchura, args[0]))
            self.hiloEjecucion.start() 


        """
        =======================================================================
                TODOS LAS FUNCIONES DE ABAJO CORRESPONDE AL CRUD.
        =======================================================================
        """
        def ejecutarReadUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'VER CUENTAS DE USUARIOS'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=partial(self.mostrar, 'OBSERVAR'), cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", borderwidth=0)
            self.Regresar.grid(
                row=1, 
                column=0
            )

            
            self.marco = LabelFrame(self, text="")
            self.marco.configure(width=585, height=490, bg="#928aa5")
            self.marco.grid(
                row=2,
                column=0, 
                sticky="w",
                columnspan=4,
                pady=40,
                padx=5
            )

            self.marco.grid_propagate(False)
    
            #dentro de esta seccion lo que haremos es generar un listado de todos los datos 
            #sacados de nuestra base de datos.
            self.headerNombre = Label(self.marco, text='NOMBRE', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=15)
            self.headerNombre.grid(
                row=2, 
                column=0,
                sticky="nsew",
                ipady=5
            )
            
            self.LineaDivisora = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora.bind('<Button1-Motion>' , self.ejecutarEvento)
            self.LineaDivisora.grid(
                row=2,
                column=1, 
                sticky="nsew"
            )

            self.headerCedula = Label(self.marco, text='CÉDULA', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerCedula.grid(
                row=2, 
                column=2,
                sticky="nsew",
               
            )

            self.LineaDivisora2 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora2.bind('<Button1-Motion>', self.ejecutarEvento2)
            self.LineaDivisora2.grid(
                row=2,
                column=3, 
                sticky="nsew",
            
            )


            self.headerTelefono = Label(self.marco, text='TELÉFONO', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerTelefono.grid(
                row=2, 
                column=4,
                sticky="nsew",
              
            )

            self.LineaDivisora3 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora3.bind('<Button1-Motion>', self.ejecutarEvento3)
            self.LineaDivisora3.grid(
                row=2,
                column=5, 
                sticky="nsew",
              
            )

            self.headerEmail = Label(self.marco, text='EMAIL', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerEmail.grid(
                row=2, 
                column=6,
                sticky="nsew",
               
            )

            self.LineaDivisora4 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora4.bind('<Button1-Motion>', self.ejecutarEvento4)
            self.LineaDivisora4.grid(
                row=2,
                column=7, 
                sticky="nsew",
               
            )


            self.headerProvincia = Label(self.marco, text='PROVINCIA', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerProvincia.grid(
                row=2, 
                column=8,
                sticky="nsew"
            )


            self.LineaDivisora5 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora5.bind('<Button1-Motion>', self.ejecutarEvento5)
            self.LineaDivisora5.grid(
                row=2,
                column=9, 
                sticky="nsew",
               
            )

            self.headerPermisos = Label(self.marco, text='PERMISOS', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerPermisos.grid(
                row=2, 
                column=10,
                sticky="nsew"
            )

            self.LineaDivisora6 = Label(self.marco, text='|', bg="white", fg="black", font=("Bold", 9), cursor="hand1")
            self.LineaDivisora6.bind('<Button1-Motion>', self.ejecutarEvento6)
            self.LineaDivisora6.grid(
                row=2,
                column=11, 
                sticky="nsew",
                
            )

            self.headerPresupuesto = Label(self.marco, text='PRESUPUESTO', bg="white", fg="#d7013a", font=("Bold", 9), anchor="center", width=20)
            self.headerPresupuesto.grid(
                row=2, 
                column=12,
                sticky="nsew"
            )

            #generaremos informacion...
            #=============================================================================
            #                INFORMACION OBTENIDA DE LA BASE DE DATOS
            #=============================================================================
            self.query = DB.db.select('usuarios')
           
            self.ListadoNombres = Listbox(self.marco, width=0)
            self.ListadoNombres.grid(
                row = 3, 
                column=0, 
                sticky="nsew"
            )
            
            self.ListadoCedula = Listbox(self.marco, border=0)
            self.ListadoCedula.grid(
                row = 3, 
                column=2, 
                sticky="nsew"
            )

            self.ListadoTelefono = Listbox(self.marco, border=0)
            self.ListadoTelefono.grid(
                row = 3, 
                column=4,  
                sticky="nsew"
            )

            self.ListadoEmail = Listbox(self.marco, border=0)
            self.ListadoEmail.grid(
                row = 3, 
                column=6,  
                sticky="nsew"
            )

            self.ListadoProvincia = Listbox(self.marco, border=0)
            self.ListadoProvincia.grid(
                row = 3, 
                column=8,  
                sticky="nsew"
            )

            self.ListadoPermisos = Listbox(self.marco, border=0)
            self.ListadoPermisos.grid(
                row = 3,
                column=10,  
                sticky="nsew"
            )

            self.ListadoPresupuesto = Listbox(self.marco, border=0)
            self.ListadoPresupuesto.grid(
                row = 3, 
                column=12,  
                sticky="nsew"
            )

            self.ListadoNombres.configure(height=120)
            self.ListadoCedula.configure(height=120)
            self.ListadoTelefono.configure(height=120)
            self.ListadoEmail.configure(height=120)
            self.ListadoProvincia.configure(height=120)
            self.ListadoPermisos.configure(height=120)
            self.ListadoPresupuesto.configure(height=120)
        
            for i in self.query:
                self.ListadoNombres.insert(tk.END, i['Nombre'])
                self.ListadoCedula.insert(tk.END, i['Cedula'])
                self.ListadoTelefono.insert(tk.END, i['Telefono'])
                self.ListadoEmail.insert(tk.END, i['Email'])
                self.ListadoProvincia.insert(tk.END, i['Provincia'])
                self.ListadoPermisos.insert(tk.END, i['Permisos'])
                self.ListadoPresupuesto.insert(tk.END, i['Presupuesto'])

                
        def validarEntrada(self, entrada):
            return not entrada.isdigit()


        def validarEntrada2(self, entrada):
            return entrada.isdigit()

        #funcion encargada de validar cada campo para la creacion de una nueva cuenta .
        def verificandoEntradas(self):
            self.Nombres = self.EntradaNombreCuenta.get()
            self.Telefono = self.EntradaTelefonoCuenta.get()
            self.Cedula = self.EntradaCedulaCuenta.get()
            self.Email = self.EntradaEmailCuenta.get()
            self.TipoUsuario = self.EntradaTipoUsuarioCuenta.get()
            self.Password = self.EntradaPasswordCuenta.get()
            self.Presupuesto = self.EntradaPresupuestoCuenta.get()

            if(self.Nombres == "" or self.Telefono == "" or self.Cedula == "" or 
               self.Email == "" or self.TipoUsuario == "" or self.Password == "" or self.Presupuesto == ""):
                #highlightcolor

                self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaTelefonoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaCedulaCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaEmailCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                # self.EntradaTipoUsuarioCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaPasswordCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                self.EntradaPresupuestoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)

                messagebox.showwarning('CREAR CUENTA', 'TODOS LOS CAMPOS SON OBLIGATORIOS')
            else:
                #cuando todos los campos sean llenaos por completo... lo que haremos a continuacion es verificar por si se han 
                #introducido correctamente los datos.

                #El diccionario nos ayudara mucho para guardar la informacion en la base de datos de manera mucho mas flexible.
                self.informacion = {
                    "Nombre" : "",
                    "Telefono" : "",
                    "Cedula" : "",
                    "Email" : "",
                    "Provincia" : "",
                    "Permisos" : "",
                    "Password" : "",
                    "Presupuesto" : ""
                }


                if(len(self.Nombres.split(" ")) != 2):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta['text'] = 'DEBES INSERTAR UN NOMBRE Y UN APELLIDO'
                    self.MensajeAlerta.grid_configure(
                        row = 2, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    try:
                        self.informacion["Nombre"] = self.Nombres
                        self.EntradaNombreCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta.destroy()
                    except (AttributeError, NameError):
                        pass 
                   

                if(len(self.Telefono) != 10):
                    self.EntradaTelefonoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta2['text'] = 'NÚMERO TELEFÓNICO INVÁLIDO'
                    self.MensajeAlerta2.grid_configure(
                        row = 4, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #vamos a realizar una comprobacion a nuestro numero telefonico....
                    self.pattern = r"^09[0-9]+"

                    if(re.search(self.pattern, self.Telefono)):
                        try:
                            #En el caso de que un usuario haya introducido bien nuestro formato basico, comprobaremos si
                            #no pertenece a un telefono ya registrado.
                            self.comprobar = DB.db.select('usuarios', 'Telefono = "+593 {}"'.format(self.Telefono))
                            if(len(self.comprobar) == 0):
                                self.informacion["Telefono"] = self.Telefono
                                self.EntradaTelefonoCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta2.destroy()
                            else:
                                self.EntradaTelefonoCuenta.configure(highlightbackground="#9b1322", highlightthickness=2)
                                self.MensajeAlerta2['text'] = 'NÚMERO TELEFÓNICO YA REGISTRADO'
                                self.MensajeAlerta2.grid_configure(
                                row = 4, 
                                column = 1,
                                sticky="ew",
                                padx=5
                                )

                        except (AttributeError, NameError):
                            pass 
                    else:
                        self.EntradaTelefonoCuenta.configure(highlightbackground="#9b1322", highlightthickness=2)
                        self.MensajeAlerta2['text'] = 'NÚMERO TELEFÓNICO INVÁLIDO'
                        self.MensajeAlerta2.grid_configure(
                        row = 4, 
                        column = 1,
                        sticky="ew",
                        padx=5
                        )


                if(len(self.Cedula) != 10):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta3['text'] = 'EL NUMERO DE CÉDULA DEBE POSEER UNA LONGITUD DE 10'
                    self.MensajeAlerta3.grid_configure(
                        row = 6, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #VAMOS A REALIZAR UNAS CUANTAS VALIDACIONES A NUESTRO CODIGO...
                    impares = self.Cedula[0::2]
                    save_valores = []
                    for i in range(len(impares)):
                        numero = int(impares[i]) * 2 
                        if(numero > 9):
                            numero -= 9 
                            save_valores.append(numero)
                        else:
                            save_valores.append(numero)

                    resultado_impares = 0
                    for j in range(len(save_valores)):
                        if(resultado_impares == 0):
                            resultado_impares = save_valores[j]
                        else:
                            resultado_impares += save_valores[j]


                    #Procedimiento que haremos para los numeros pares.
                    pares =  self.Cedula[1:-2:2]

                    resultado_pares = 0
                    for i in range(len(pares)):
                        if(resultado_pares == 0):
                            resultado_pares = int(pares[i])
                        else:
                            resultado_pares += int(pares[i])


                    #Calculamos para poder verificar por el ultimo numero y ver si coincide....
                    suma_total = resultado_pares + resultado_impares

                    restante = suma_total%10 
                
                    #sacamos modulo 10.
                    if(not restante == 0):
                        #si es distinto de 0 ....
                        numero_verificador = 10 - restante

                        if(numero_verificador == int(self.Cedula[-1])):

                            #Aqui haremos una comprobacion para saber si nuestra cedula ya se encuentra registrada o no...
                            #lo hacemos aqui, debido a que ya ha pasado por todo el proceso de verificacion para ser una cedula correcta
                            self.comprobar = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.Cedula))

                            if(len(self.comprobar) == 0):
                                try:
                                    self.informacion["Provincia"] = codigos.provincias[self.Cedula[0:2]]
                                    self.informacion["Cedula"] = self.Cedula
                                    self.EntradaCedulaCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta3.destroy()
                                except (AttributeError, NameError):
                                    pass 
                            else:
                                self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                                self.MensajeAlerta3['text'] = 'CÉDULA YA REGISTRADA'
                                self.MensajeAlerta3.grid_configure(
                                    row = 6, 
                                    column = 1,
                                    sticky="ew",
                                    padx=5
                                )

                        else:
                            self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta3['text'] = 'NÚMERO DE CÉDULA INCORRECTA'
                            self.MensajeAlerta3.grid_configure(
                                row = 6, 
                                column = 1,
                                sticky="ew",
                                padx=5
                            )
                        
                    else:
                        if(restante == int(self.Cedula[-1])):
                            self.comprobar = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.Cedula))

                            if(len(self.comprobar) == 0):
                                try:
                                    self.informacion["Provincia"] = codigos.provincias[self.Cedula[0:2]]
                                    self.informacion["Cedula"] = self.Cedula
                                    self.EntradaCedulaCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta3.destroy()
                                except (AttributeError, NameError):
                                    pass 
                            else:
                                #llegados a este punto sabemos que ya es una cedula registrada......
                                self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                                self.MensajeAlerta3['text'] = 'CÉDULA YA REGISTRADA'
                                self.MensajeAlerta3.grid_configure(
                                    row = 6, 
                                    column = 1,
                                    sticky="ew",
                                    padx=5
                                )

                        else:
                            self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta3['text'] = 'NÚMERO DE CÉDULA INCORRECTA'
                            self.MensajeAlerta3.grid_configure(
                                row = 6, 
                                column = 1,
                                sticky="ew",
                                padx=5
                            )

                    


                #DEBEMOS REALIZAR CIERTAS CORRECIONES AL CODIGO A CONTINUACION..........
                if(self.Email.find('@') == -1):
                    self.EntradaEmailCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta4['text'] = 'DEBES INSERTAR UN EMAIL VÁLIDO'
                    self.MensajeAlerta4.grid_configure(
                        row = 8, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #vamos a realizar unas cuantas validaciones a la direccion email para que puead pasar y ser 
                    #almacenado en la base de datos de manera mucho mejor de lo que ya se haya encontrado.
                    self.pattern = r"^[A-Za-z]+([0-9]*|-*|_*|[A-Za-z]*)+@[a-z]+\.[a-z]+$"

                    if(re.search(self.pattern, self.Email)):
                        try:
                            self.informacion["Email"] = self.Email
                            self.EntradaEmailCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                            self.MensajeAlerta4.destroy()
                        except (AttributeError, NameError):
                            pass 
                    else:
                    
                        self.MensajeAlerta4 = Label(self.marco, text='DEBES INSERTAR UN EMAIL VÁLIDO',  bg="red", fg="white", font=("Arial", 8))
                        self.MensajeAlerta4.grid(
                            row = 8, 
                            column = 1, 
                            sticky="ew",
                            padx=5
                        )
                        


                #TIPOS DE USUARIO
                if(self.TipoUsuario == ""):
                    self.EntradaNombreCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta5['text'] = 'DEBES INSERTAR UN TIPO DE USUARIO'
                    self.MensajeAlerta5.grid_configure(
                        row = 2, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:

                    match(self.TipoUsuario):
                        case "CLIENTE":
                            self.informacion["Permisos"] = "0"

                        case "ADMINISTRADOR":
                            self.informacion["Permisos"] = "1"

    
                    try:
                        self.EntradaNombreCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                        self.MensajeAlerta5.destroy()
                    except (AttributeError, NameError):
                        pass 


                if(len(self.Password) != 5):
                    self.EntradaPasswordCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta6['text'] = 'TU CONTRASEÑA DEBE TENER UNA LONGITUD DE 5'
                    self.MensajeAlerta6.grid_configure(
                        row = 12, 
                        column = 1,
                        sticky="ew",
                        padx=5
                    )
                else:
                    #Vamos hacer unas cuantas validaciones a nuestro password. 
                    #EN ESTE CASO SOLAMENTE HAREMOS QUE NUESTRO PASSWORD SEA NUMERICA PARA UN CLIENTE Y ALFANUMERICA PARA UN ADMINISTRADOR....
                    if(int(self.informacion["Permisos"]) == 0):
                        #generaremos un password para un cliente comun....
                        self.pattern = r"[0-9]{5}" #debera haber solo 5 numeros del 1 al 9

                        if(re.search(self.pattern, self.Password)):
                            try:
                                self.informacion["Password"] = self.Password
                                self.EntradaPasswordCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta6.destroy()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            #generaremos una alerta para que ingrese nuevamente los datos.
                            self.EntradaPasswordCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta6['text'] = 'Tu contraseña solo debe contener 5 digitos del 1 al 9'

                    elif(int(self.informacion["Permisos"]) == 1):
                        #generaremos un password para un administrador....
                        self.pattern = r"([A-Z]|[a-z]|[0-9]){5}" #debera haber solo 5 numeros del 1 al 9

                        if(re.search(self.pattern, self.Password)):
                            try:
                                self.informacion["Password"] = self.Password
                                self.EntradaPasswordCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta6.destroy()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            #generaremos una alerta para que ingrese nuevamente los datos.
                            self.EntradaPasswordCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta6['text'] = 'La contraseña debe poseer una longitud de 5 con carácteres alfanuméricos '
                            self.MensajeAlerta6.grid_configure(
                                row = 12, 
                                column = 1,
                                sticky="ew",
                                padx=5
                            )


                if(self.Presupuesto != ""):

                    self.MaximoPresupuesto = 1000 #este es el limite, solo para generar un deposito inicial...
                    self.MinimoPresupuesto = 20 #este es el valor inicial donde un usuario puede comenzar.... 

                    if(int(self.Presupuesto) >= self.MinimoPresupuesto and int(self.Presupuesto) <= self.MaximoPresupuesto):
                        try:
                            self.informacion['Presupuesto'] = self.Presupuesto
                            self.EntradaPresupuestoCuenta.configure(highlightbackground="#0971a6",highlightthickness=2)
                            self.MensajeAlerta7.destroy()
                        except (NameError, AttributeError):
                            pass 
                    else: 
                        self.EntradaPresupuestoCuenta.configure(highlightbackground="#9b1322",highlightthickness=2)
                        self.MensajeAlerta7['text'] = 'DEBES GENERAR UNA ENTRADA COMO MÍNIMO DE 20 DÓLARES HASTA 1000 DÓLARES '
                        self.MensajeAlerta7.grid_configure(
                            row = 12, 
                            column = 1,
                            sticky="ew",
                            padx=5
                        )


                if(self.informacion['Nombre'] != "" and self.informacion['Telefono'] != "" and self.informacion['Cedula'] != "" and 
                  self.informacion['Email'] != "" and self.informacion['Provincia'] != "" and self.informacion['Permisos'] != "" and 
                  self.informacion['Password'] != "" and self.informacion['Presupuesto'] != ""):

                    DB.db.insert('usuarios', {
                        'Nombre' : self.informacion['Nombre'],
                        'Telefono' : "+593 "+self.informacion['Telefono'],
                        'Cedula' : self.informacion['Cedula'],
                        'Email' : self.informacion['Email'],
                        'Provincia' : self.informacion['Provincia'],
                        'Permisos' : self.informacion['Permisos'],
                        'Password' : self.informacion['Password'],
                        'Presupuesto' : self.informacion['Presupuesto']
                    })

                    messagebox.showinfo('Crear Cuenta', 'Cuenta creada exitosamente!')

                    self.EntradaNombreCuenta.delete(0, tk.END)
                    self.EntradaTelefonoCuenta.delete(0, tk.END)
                    self.EntradaCedulaCuenta.delete(0, tk.END)
                    self.EntradaEmailCuenta.delete(0, tk.END)
                    self.EntradaTipoUsuarioCuenta.set(" ")
                    self.EntradaPasswordCuenta.delete(0, tk.END)
                    self.EntradaPresupuestoCuenta.delete(0, tk.END)    


        def ejecutarCreateUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'CREAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )

            #lo que vamos hacer desntro de esta parte es generar un formulario con datos para que se comience a generar el perfil de
            #nuestro usuario....
            self.marco = LabelFrame(self, text='', width=590, height=515, border=0, bg="#125160")
            self.marco.grid(
                row=2, 
                column=0, 
                columnspan=3,
                pady=30,
                padx=5,
                sticky="w"
            )
            self.marco.grid_propagate(False)

            self.headerFormulario = Label(self.marco, text='INSERTA LOS DATOS A CONTINUACIÓN', bg="#ef8200", fg="white", font=("Arial", 11))
            self.headerFormulario.grid(
                row=0, 
                column=0, 
                columnspan=3,
                sticky="w", 
                ipadx=155
            )

            """
            Desactivar para otra ocasion el siguiente codigo comentado para posibles soluciones a otras cosas.
            """
            #==========================================================================================================
            self.NombreCuenta = Label(self.marco, text='INSERTA NOMBRES: ', fg="white", bg="#125160", justify="left")
            self.NombreCuenta.grid(
                row=1, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )

            self.EntradaNombreCuenta = Entry(
                self.marco, 
                width=40, 
                validate="key", 
                validatecommand=(self.register(self.validarEntrada),"%S"), 
            )
            self.EntradaNombreCuenta.grid(
                row=1, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta = Label(self.marco, text="DEBES INTRODUCIR DOS NOMBRES", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 2, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            # =====================================================================================================

            self.TelefonoCuenta = Label(self.marco, text='INSERTA TELÉFONO: ', fg="white", bg="#125160")
            self.TelefonoCuenta.grid(
                row=3, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaTelefonoCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaTelefonoCuenta.grid(
                row=3, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta2 = Label(self.marco, text="DEBES INTRODUCIR UN NÚMERO TELEFÓNICO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 4, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )
            


            self.CedulaCuenta = Label(self.marco, text='INSERTA CÉDULA: ', fg="white", bg="#125160")
            self.CedulaCuenta.grid(
                row=5, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaCedulaCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaCedulaCuenta.grid(
                row=5, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3,
            )

            self.MensajeAlerta3 = Label(self.marco, text="DEBES INTRODUCIR UN NÚMERO DE CÉDULA", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 6, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.EmailCuenta = Label(self.marco, text='INSERTA EMAIL: ', fg="white", bg="#125160")
            self.EmailCuenta.grid(
                row=7, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaEmailCuenta = Entry(self.marco, width=40)
            self.EntradaEmailCuenta.grid(
                row=7, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            """
                CLARIFICAR _tkinter.TclError: invalid command name ".!admin.!labelframe.!label9"
            """
            self.MensajeAlerta4 = Label(self.marco, text="DEBES INTRODUCIR UN EMAIL", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 8, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.TipoUsuarioCuenta = Label(self.marco, text='INSERTA TIPO DE USUARIO: ', fg="white", bg="#125160")
            self.TipoUsuarioCuenta.grid(
                row=9, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaTipoUsuarioCuenta = ttk.Combobox(self.marco, width=40, values=['CLIENTE', 'ADMINISTRADOR'], state='readonly', background="white")
            self.EntradaTipoUsuarioCuenta.grid(
                row=9, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )


            self.MensajeAlerta5 = Label(self.marco, text="INSERTA EL TIPO DE USUARIO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 10, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )


            self.PasswordCuenta = Label(self.marco, text='INSERTA CONTRASEÑA: ', fg="white", bg="#125160")
            self.PasswordCuenta.grid(
                row=11, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaPasswordCuenta = Entry(self.marco, width=40, show="*")
            self.EntradaPasswordCuenta.grid(
                row=11, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3
            )

            self.MensajeAlerta6 = Label(self.marco, text="CREA UNA CONTRASEÑA PARA LA CUENTA", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 12, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            self.PresupuestoCuenta = Label(self.marco, text='INSERTA PRESUPUESTO CUENTA: ', fg="white", bg="#125160")
            self.PresupuestoCuenta.grid(
                row=13, 
                column=0, 
                pady=12,
                padx=5,
                sticky="e"
            )
            self.EntradaPresupuestoCuenta = Entry(
                self.marco, 
                width=40,
                validate="key", 
                validatecommand=(self.register(self.validarEntrada2),"%S")
            )
            self.EntradaPresupuestoCuenta.grid(
                row=13, 
                column=1,
                sticky="ew",
                padx=5,
                ipady=3,
            )
 
            self.MensajeAlerta7 = Label(self.marco, text="DIGITA UN PRESUPUESTO", bg="red", fg="white", font=("Arial", 8))
            # self.MensajeAlerta.grid(
            #     row = 14, 
            #     column = 1,
            #     sticky="ew",
            #     padx=5
            # )

            self.BotonCuenta = Button(
                self.marco, 
                text='GENERAR CUENTA', 
                font=("Arial", 9), width=25, 
                bg="#aa054a", 
                fg="white", 
                border=0, 
                cursor="hand1", 
                activebackground="#fe0041", 
                activeforeground="white",
                command=self.verificandoEntradas)
            self.BotonCuenta.grid(
                row=15, 
                column=0, 
                columnspan=2,
                pady=10, 
                ipady=2
            )
            #A CONTINUACION SERA LA CREACION DE UN FORMULARIO... CADA UNO DE LOS CAMPOS SERA VALIDADO A CORDE A LO QUE SE PIDA.


        def ejecutarDeleteUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'ELIMINAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )


            """
                El administrador tendra solamente la habilidad de eliminar una cuenta por completo... por medio de la cedula de la cuenta a eliminar
                para completar el proceso de eliminacion... 
                Es realmente algo simple.... ya no tocaria hacer nuevamente un barrido de datos, porque el administrador puede ir a la seccion de VER CUENTAS
                y comprobar por medio de ahi la cedula....
            """
            self.marco = LabelFrame(self, text="", width=579, height=500, bg="#125160")
            self.marco.grid(
                row=2, 
                column=0,
                pady=30,
                padx=10,
                columnspan=3,    
                sticky="w"
            )
            self.marco.grid_propagate(False)

            self.headerFormulario = Label(self.marco, text='INSERTA LA CÉDULA PARA ELIMINAR LA CUENTA', bg="#ef8200", fg="white", font=("Arial", 11), width=20)
            self.headerFormulario.grid(
                row=0, 
                column=0, 
                columnspan=4,
                sticky="nsew",
                ipadx=50
            )

            self.CedulaTexto = Label(self.marco, text='INTRODUCE CÉDULA:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.CedulaTexto.grid(
                row = 1, 
                column = 0, 
                padx = 10,
                pady=20
            )


            self.VerificandoEntradaCedula = StringVar()
            self.CedulaEntrada = Entry(
                self.marco,
                width=55, 
                justify="center", 
                highlightbackground="#ef8200", 
                highlightthickness=2, 
                textvariable=self.VerificandoEntradaCedula, 
                validate="key", 
                validatecommand=(self.register(self.verificarEntrada), "%S"), 
                
            )
            self.CedulaEntrada.grid(
                row = 1, 
                column = 1, 
                padx = 20, 
                ipady = 3,
                pady=10, 
                sticky="w"
            )

            

            self.NombresTexto = Label(self.marco, text='NOMRES CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.NombresTexto.grid(
                row = 2, 
                column = 0, 
                padx = 10,
            
            )
            self.NombresEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.NombresEntrada.grid(
                row = 2, 
                column = 1, 
                padx = 10, 
                ipady = 3,
            )
            self.NombresEntrada.insert(0, 'SIN CUENTA')
            self.NombresEntrada['state'] = 'readonly'

            self.TelefonoTexto = Label(self.marco, text='TELEFONO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.TelefonoTexto.grid(
                row = 3, 
                column = 0, 
                padx = 10,
                pady = 20
            )
            self.TelefonoEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.TelefonoEntrada.grid(
                row = 3, 
                column = 1, 
                padx = 10, 
                ipady = 3,
                pady = 20
            )   
            self.TelefonoEntrada.insert(0, 'SIN CUENTA')
            self.TelefonoEntrada['state'] = 'readonly'


            self.EmailTexto = Label(self.marco, text='EMAIL CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.EmailTexto.grid(
                row = 4, 
                column = 0, 
                padx = 10,
               
            )
            self.EmailEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.EmailEntrada.grid(
                row = 4, 
                column = 1, 
                padx = 10, 
                ipady = 3,
            
            )
            self.EmailEntrada.insert(0, 'SIN CUENTA')
            self.EmailEntrada['state'] = 'readonly'

            self.ProvinciaTexto = Label(self.marco, text='PROVINCIA CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.ProvinciaTexto.grid(
                row = 5, 
                column = 0, 
                padx = 10,
                pady = 20
            )
            self.ProvinciaEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.ProvinciaEntrada.grid(
                row = 5, 
                column = 1, 
                padx = 10, 
                ipady = 3, 
                pady = 20
            )
            self.ProvinciaEntrada.insert(0, 'SIN CUENTA')
            self.ProvinciaEntrada['state'] = 'readonly'


            self.TipoUsuarioTexto = Label(self.marco, text='TIPO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.TipoUsuarioTexto.grid(
                row = 6, 
                column = 0, 
                padx = 10
            )
            self.TipoUsuarioEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.TipoUsuarioEntrada.grid(
                row = 6, 
                column = 1, 
                padx = 10, 
                ipady = 3
            )
            self.TipoUsuarioEntrada.insert(0, 'SIN CUENTA')
            self.TipoUsuarioEntrada['state'] = 'readonly'

            self.PresupuestoTexto = Label(self.marco, text='PRESUPUESTO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.PresupuestoTexto.grid(
                row = 7, 
                column = 0, 
                padx = 10,
                pady =20
            )
            self.PresupuestoEntrada = Entry(self.marco, width=55, justify="center", fg="black")
            self.PresupuestoEntrada.grid(
                row = 7, 
                column = 1, 
                padx = 10, 
                ipady = 3,
                pady = 20
            )
            self.PresupuestoEntrada.insert(0, 'SIN CUENTA')
            self.PresupuestoEntrada['state'] = 'readonly'

            self.BotonVerificar = Button(
                self.marco, 
                text='VERIFICAR CUENTA',
                font=("Arial", 10), 
                border=0, 
                bg="#a1ff68", 
                fg="black", 
                highlightbackground="#a1ff68", 
                width=20,
                command=partial(self.VerificarCuenta, 'ELIMINAR'), 
                cursor="hand1", 
                activebackground="#128163", 
                activeforeground="white"
            )
            self.BotonVerificar.grid(
                row = 8, 
                column = 0, 
                ipady=2,
                padx=70,
                columnspan=2,
                sticky="w",
          
            )

            self.BotonEliminar = Button(
                self.marco, 
                text='ELIMINAR CUENTA', 
                font=("Arial", 10), 
                border=0, 
                bg="#aa003a", 
                fg="white", 
                highlightbackground="#aa003a",
                width=22,
                state='disabled',
                command=self.EliminarCuenta, 
                cursor="hand1",
            )
            self.BotonEliminar.grid(
                row = 8, 
                column = 0,  
                pady = 30,
                ipady = 5, 
                padx = 85,
                sticky="e",
                columnspan=2,
                
            )
            

        def verificarEntrada(self, entrada):
            return entrada.isdigit()
        
       
        def VerificarCuenta(self, *args):
            if(args[0] == 'ELIMINAR'):
                if(self.VerificandoEntradaCedula.get() == ""):
                    messagebox.showinfo('Eliminar Cuenta', 'La cédula es obligatoria para poder hacer el proceso de eliminación de cuenta')
                else: 
                    if(len(self.VerificandoEntradaCedula.get()) != 10):
                        self.limpiarFormulario(args[0])

                        messagebox.showinfo('Eliminar Cuenta', 'Debes introducir un número de cédula válida')
                    else:
                        self.query = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.VerificandoEntradaCedula.get()))

                        if(len(self.query) == 0):
                            # no existe dicha cuenta....
                            #desactivamos el boton de eliminar y rellenamos los demas campos que se encuentran vacios por el momento.
                            self.limpiarFormulario(args[0])
                            messagebox.showinfo('Eliminar Cuenta', 'No existe dicha cuenta')
                        else: 
                            #desactivamos el boton de eliminar y rellenamos los demas campos que se encuentran vacios por el momento.
                            self.BotonEliminar['state'] = 'normal'

                            self.NombresEntrada['state'] = 'normal'
                            self.NombresEntrada.delete(0, tk.END)
                            self.NombresEntrada.insert(0, self.query[0]['Nombre'])
                            self.NombresEntrada['state'] = 'readonly'

                            self.TelefonoEntrada['state'] = 'normal'
                            self.TelefonoEntrada.delete(0, tk.END)
                            self.TelefonoEntrada.insert(0, self.query[0]['Telefono'])
                            self.TelefonoEntrada['state'] = 'readonly'

                            self.EmailEntrada['state'] = 'normal'
                            self.EmailEntrada.delete(0, tk.END)
                            self.EmailEntrada.insert(0, self.query[0]['Email'])
                            self.EmailEntrada['state'] = 'readonly'

                            self.ProvinciaEntrada['state'] = 'normal'
                            self.ProvinciaEntrada.delete(0, tk.END)
                            self.ProvinciaEntrada.insert(0, self.query[0]['Provincia'])
                            self.ProvinciaEntrada['state'] = 'readonly'

                            if(int(self.query[0]['Permisos']) == 0):
                                self.TipoUsuarioEntrada['state'] = 'normal'
                                self.TipoUsuarioEntrada.delete(0, tk.END)
                                self.TipoUsuarioEntrada.insert(0, 'CLIENTE')
                                self.TipoUsuarioEntrada['state'] = 'readonly'
                            elif(int(self.query[0]['Permisos']) == 1):
                                self.TipoUsuarioEntrada['state'] = 'normal'
                                self.TipoUsuarioEntrada.delete(0, tk.END)
                                self.TipoUsuarioEntrada.insert(0, 'ADMINISTRADOR')
                                self.TipoUsuarioEntrada['state'] = 'readonly'

                            self.PresupuestoEntrada['state'] = 'normal'
                            self.PresupuestoEntrada.delete(0, tk.END)
                            self.PresupuestoEntrada.insert(0, self.query[0]['Presupuesto'])
                            self.PresupuestoEntrada['state'] = 'readonly'

            elif(args[0] == 'ACTUALIZAR'):
                #esta seccion corresponde a nuestra funcion de actualizar cuentas .... self.ejecutarUpdateUsers()
                if(self.VerificandoEntradaCedula.get() == ""):
                    self.limpiarFormulario(args[0])
                    messagebox.showinfo('Actualizar Cuenta', 'Debes insertar la cédula para empezar con el proceso de actualización')
                else:
                    if(len(self.VerificandoEntradaCedula.get()) != 10):
                        self.limpiarFormulario(args[0])
                        messagebox.showinfo('Actualizar Cuenta', 'Debes introducir un número de cédula válida')
                    else:
                        self.query = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.VerificandoEntradaCedula.get()))
                        #dentro de esta fase nuestro proposito es rellenar los campos para que puedan empezar la actualizacion de datos.
                        if(len(self.query) == 0):
                            self.limpiarFormulario(args[0])
                            messagebox.showinfo('Actualizar Cuenta', 'No existe dicha cuenta!')
                        else:
                            self.BotonActualizar['state'] = 'normal'
                            self.CedulaCopia[0] = self.query[0]['Cedula']

                            self.NombresEntrada['state'] = 'normal'
                            self.NombresEntrada.delete(0, tk.END)
                            self.NombresEntrada.insert(0, self.query[0]['Nombre'])

                            self.TelefonoEntrada['state'] = 'normal'
                            self.TelefonoEntrada.delete(0, tk.END)
                            self.TelefonoEntrada.insert(0, self.query[0]['Telefono'][5:])

                            self.EmailEntrada['state'] = 'normal'
                            self.EmailEntrada.delete(0, tk.END)
                            self.EmailEntrada.insert(0, self.query[0]['Email'])

                            self.ProvinciaEntrada['state'] = 'normal'
                            self.ProvinciaEntrada.delete(0, tk.END)
                            self.ProvinciaEntrada.insert(0, self.query[0]['Provincia'])

                            if(int(self.query[0]['Permisos']) == 0):
                                self.PermisosUsuariosEntrada.set("CLIENTE")
                            elif(int(self.query[0]['Permisos']) == 1):
                                self.PermisosUsuariosEntrada.set("ADMINISTRADOR")

                            self.PresupuestoEntrada['state'] = 'normal'
                            self.PresupuestoEntrada.delete(0, tk.END)
                            self.PresupuestoEntrada.insert(0, str(int(self.query[0]['Presupuesto'])))

                            self.PasswordEntrada['state'] = 'normal'
                            self.PasswordEntrada.delete(0, tk.END)
                            self.PasswordEntrada.insert(0, self.query[0]['Password'])
                            self.PasswordEntrada.configure(show="*")

                            #la primera vez que empezamos con el boton es desde este lugar...

                            self.ejecutarOjo = "VER"
                            
                            self.imgPass = PhotoImage(file="./cajero/img/ocultar.png")
                            self.buttonImg = Button(self.marco, image=self.imgPass, border=0, cursor="hand1", command=self.mostrarPassword)
                            self.buttonImg.grid(row=8, column=1, )
                            # self.buttonImg.lift(self.PasswordEntrada)
                            self.buttonImg.grid(
                                row = 15, 
                                column = 1, 
                                sticky="e",
                                padx = 28
                            )

                                                            
        def EliminarCuenta(self):
            self.cedula = self.VerificandoEntradaCedula.get()
            self.ID = DB.db.select('usuarios', 'Cedula = {}'.format(self.cedula))
            self.decidir = messagebox.askquestion('Eliminar Cuenta', '¿Deseas eliminar dicha cuenta?')

            if(self.decidir == 'yes'):

                #Evitar que se elimine la misma cuenta que lo usa un administrador.
                self.query = DB.db.select('usuarios', 'id = "{}"'.format(id))[0]

                if(self.cedula == self.query['Cedula']):
                    messagebox.showwarning('Eliminar Cuenta', 'No se puede eliminar esta cuenta de administrador en uso!')
                    self.limpiarFormulario('ELIMINAR')
                else:
                    #la eliminacino de una cuenta...
                    DB.db.delete('usuarios', 'id = {}'.format(self.ID[0]['id']))
                    messagebox.showinfo('Eliminar Cuenta', 'Cuenta eliminada exitosamente!')
                    self.limpiarFormulario('ELIMINAR')
            else: 
                self.limpiarFormulario('ELIMINAR')

        def limpiarFormulario(self, entrada):
            if(entrada == 'ELIMINAR'):
                self.BotonEliminar['state'] = 'disabled'

                self.TipoUsuarioEntrada['state'] = 'normal'
                self.TipoUsuarioEntrada.delete(0, tk.END)
                self.TipoUsuarioEntrada.insert(0, 'SIN CUENTA')
                self.TipoUsuarioEntrada['state'] = 'readonly'
            elif(entrada == 'ACTUALIZAR'):
                try:
                    self.BotonActualizar['state'] = 'disabled'
                    self.PasswordEntrada.configure(show="")
                    self.PasswordEntrada.delete(0, tk.END)
                    self.PasswordEntrada.insert(0, 'SIN CUENTA')
                    self.PasswordEntrada['state'] = 'readonly'

                    self.PermisosUsuariosEntrada['state'] = 'normal'
                    self.PermisosUsuariosEntrada.delete(0, tk.END)
                    self.PermisosUsuariosEntrada.insert(0, 'SIN CUENTA')
                    self.PermisosUsuariosEntrada['state'] = 'readonly'

                    self.buttonImg.grid_forget()
                except (NameError,AttributeError):
                    pass

            self.NombresEntrada['state'] = 'normal'
            self.NombresEntrada.delete(0, tk.END)
            self.NombresEntrada.insert(0, 'SIN CUENTA')
            self.NombresEntrada['state'] = 'readonly'

            self.TelefonoEntrada['state'] = 'normal'
            self.TelefonoEntrada.delete(0, tk.END)
            self.TelefonoEntrada.insert(0, 'SIN CUENTA')
            self.TelefonoEntrada['state'] = 'readonly'

            self.EmailEntrada['state'] = 'normal'
            self.EmailEntrada.delete(0, tk.END)
            self.EmailEntrada.insert(0, 'SIN CUENTA')
            self.EmailEntrada['state'] = 'readonly'

            self.ProvinciaEntrada['state'] = 'normal'
            self.ProvinciaEntrada.delete(0, tk.END)
            self.ProvinciaEntrada.insert(0, 'SIN CUENTA')
            self.ProvinciaEntrada['state'] = 'readonly'

            self.PresupuestoEntrada['state'] = 'normal'
            self.PresupuestoEntrada.delete(0, tk.END)
            self.PresupuestoEntrada.insert(0, 'SIN CUENTA')
            self.PresupuestoEntrada['state'] = 'readonly'

        def ejecutarUpdateUsers(self):
            self.ReadUsers.grid_remove() 
            self.CreateUsers.grid_remove() 
            self.DeleteUsers.grid_remove() 
            self.UpdateUsers.grid_remove() 

            self.Descripcion['text'] = 'ACTUALIZAR CUENTA DE USUARIO'

            #configurar boton con una flecha.
            self.icono = PhotoImage(file="./cajero/img/flecha_izquierda.png")
            self.Regresar = Button(self, image=self.icono, command=self.mostrar, cursor="hand1", border=0, fg="white", bg="#00759f", activebackground="#00759f", activeforeground="white", )
            self.Regresar.grid(
                row=1, 
                column=0
            )

            self.marco = LabelFrame(self, text="", width=579, height=530, bg="#125160")
            self.marco.grid(
                row=2, 
                column=0,
                pady=10,
                padx=10,
                columnspan=3,    
                sticky="w"
            )
            self.marco.grid_propagate(False)

            self.headerFormulario = Label(self.marco, text='INSERTA LA CÉDULA PARA ACTUALIZAR CUENTA', bg="#ef8200", fg="white", font=("Arial", 11), width=20)
            self.headerFormulario.grid(
                row=0, 
                column=0, 
                columnspan=4,
                sticky="nsew",
                ipadx=50
            )

            self.CedulaTexto = Label(self.marco, text='INTRODUCE CÉDULA:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.CedulaTexto.grid(
                row = 1, 
                column = 0, 
                padx = 10,
                pady=10
            )

            self.VerificandoEntradaCedula = StringVar()
            self.CedulaEntrada = Entry(
                self.marco,
                width=56, 
                justify="center", 
                highlightbackground="#ef8200", 
                highlightthickness=2, 
                textvariable=self.VerificandoEntradaCedula, 
                validate="key", 
                validatecommand=(self.register(self.verificarEntrada), "%S"), 
                
            )
            self.CedulaEntrada.grid(
                row = 1, 
                column = 1, 
                padx = 20, 
                ipady = 1,
                pady=5, 
                sticky="w"
            )

            #MENSAJE DE ALERTA
            self.MensajeAlerta = Label(self.marco, text="DEBES INTRODUCIR LA CEDULA", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta.grid(
                row = 2, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta.grid_remove()
            #--------------------------------------------------------------------------------------------------------------------
            self.NombresTexto = Label(self.marco, text='NOMRES CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.NombresTexto.grid(
                row = 3, 
                column = 0, 
                padx = 10,
            )
            self.NombresEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.NombresEntrada.grid(
                row = 3, 
                column = 1, 
                padx = 20, 
                ipady = 1,
                pady = 7
            )
            self.NombresEntrada.insert(0, 'SIN CUENTA')
            self.NombresEntrada['state'] = 'readonly'

             #MENSAJE DE ALERTA
            self.MensajeAlerta2 = Label(self.marco, text="DEBES INTRODUCIR DOS NOMBRES", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta2.grid(
                row = 4, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta2.grid_remove()
            #-------------------------------------------------------------------------------------------------------------------

            self.TelefonoTexto = Label(self.marco, text='TELEFONO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.TelefonoTexto.grid(
                row = 5, 
                column = 0, 
                padx = 10,
            )
            self.TelefonoEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.TelefonoEntrada.grid(
                row = 5, 
                column = 1, 
                padx = 20, 
                ipady = 1,
                pady = 7
            )   
            self.TelefonoEntrada.insert(0, 'SIN CUENTA')
            self.TelefonoEntrada['state'] = 'readonly'

              #MENSAJE DE ALERTA
            self.MensajeAlerta3 = Label(self.marco, text="DEBES INTRODUCIR UN TELEFONO", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta3.grid(
                row = 6, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta3.grid_remove()

            #-----------------------------------------------------------------------------------------------------------------------

            self.EmailTexto = Label(self.marco, text='EMAIL CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.EmailTexto.grid(
                row = 7, 
                column = 0, 
                padx = 10,
               
            )
            self.EmailEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.EmailEntrada.grid(
                row = 7, 
                column = 1, 
                padx = 20, 
                ipady = 1,
                pady = 7
            )
            self.EmailEntrada.insert(0, 'SIN CUENTA')
            self.EmailEntrada['state'] = 'readonly'

            #MENSAJE DE ALERTA
            self.MensajeAlerta4 = Label(self.marco, text="DEBES INTRODUCIR UN EMAIL", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta4.grid(
                row = 8, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta4.grid_remove()

            #------------------------------------------------------------------------------------------------------------------------------

            self.ProvinciaTexto = Label(self.marco, text='PROVINCIA CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.ProvinciaTexto.grid(
                row = 9, 
                column = 0, 
                padx = 10,
            )
            self.ProvinciaEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.ProvinciaEntrada.grid(
                row = 9, 
                column = 1, 
                padx = 20, 
                ipady = 1, 
                pady = 7
            )
            self.ProvinciaEntrada.insert(0, 'SIN CUENTA')
            self.ProvinciaEntrada['state'] = 'readonly'

            #MENSAJE DE ALERTA
            self.MensajeAlerta5 = Label(self.marco, text="DEBES INTRODUCIR UNA PROVINCIA", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta5.grid(
                row = 10, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta5.grid_remove()

            #--------------------------------------------------------------------------------------------------------------------

            self.TipoUsuarioTexto = Label(self.marco, text='TIPO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.TipoUsuarioTexto.grid(
                row = 11, 
                column = 0, 
                padx = 10
            )
            self.PermisosUsuariosEntrada = ttk.Combobox(self.marco, width=53, justify="center", values=["CLIENTE", "ADMINISTRADOR"])
            self.PermisosUsuariosEntrada.grid(
                row = 11, 
                column = 1, 
                padx = 10, 
                ipady = 1,
                pady = 7
            )
            self.PermisosUsuariosEntrada.set("SIN CUENTA")
            self.PermisosUsuariosEntrada['state'] = 'readonly'

            #MENSAJE DE ALERTA
            self.MensajeAlerta6 = Label(self.marco, text="DEBES INTRODUCIR UN TIPO CLIENTE", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta6.grid(
                row = 12, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta6.grid_remove()

            #---------------------------------------------------------------------------------------------------------------------------

            self.PresupuestoTexto = Label(self.marco, text='PRESUPUESTO CLIENTE:  ', width=25, anchor="e", bg="#125160", fg="white")
            self.PresupuestoTexto.grid(
                row = 13, 
                column = 0, 
                padx = 10,
            )
            self.PresupuestoEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.PresupuestoEntrada.grid(
                row = 13, 
                column = 1, 
                padx = 10, 
                ipady = 1,
                pady = 7
            )
            self.PresupuestoEntrada.insert(0, 'SIN CUENTA')
            self.PresupuestoEntrada['state'] = 'readonly'

             #MENSAJE DE ALERTA
            self.MensajeAlerta7 = Label(self.marco, text="DEBES INTRODUCIR UN PRESUPUESTO CLIENTE", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta7.grid(
                row = 14, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta7.grid_remove()

            #-------------------------------------------------------------------------------------------------------------------------------

            self.PasswordTexto = Label(self.marco, text='CONTRASEÑA CLIENTE: ', width=25, anchor="e", bg="#125160", fg="white")
            self.PasswordTexto.grid(
                row = 15, 
                column = 0, 
                padx = 10, 
            )
            self.PasswordEntrada = Entry(self.marco, width=56, justify="center", fg="black")
            self.PasswordEntrada.grid(
                row = 15, 
                column = 1, 
                ipady = 1,
                pady = 7
            )
            self.PasswordEntrada.insert(0, 'SIN CUENTA')
            self.PasswordEntrada['state'] = 'readonly'

             #MENSAJE DE ALERTA
            self.MensajeAlerta8 = Label(self.marco, text="DEBES INTRODUCIR UNA CONTRASEÑA", bg="red", fg="white", font=("Arial", 8))
            self.MensajeAlerta8.grid(
                row = 16, 
                column = 1,
                sticky="ew",
                padx=20
            )
            self.MensajeAlerta8.grid_remove()

            #-------------------------------------------------------------------------------------------------------------------------------

            #ESTE SERA IDENTICO AL DE LA CREACION DE UN NUEVO USUARIO. 
            self.BotonVerificar = Button(
                self.marco, 
                text='VERIFICAR CUENTA',
                font=("Arial", 10), 
                border=0, 
                bg="#a1ff68", 
                fg="black", 
                highlightbackground="#a1ff68", 
                width=20,
                command=partial(self.VerificarCuenta, 'ACTUALIZAR'), 
                cursor="hand1", 
                activebackground="#128163", 
                activeforeground="white"
            )
            self.BotonVerificar.grid(
                row = 17, 
                column = 0, 
                ipady=3,
                padx=70,
                columnspan=2,
                sticky="nw",
                pady = 15
            )
            self.BotonActualizar = Button(
                self.marco, 
                text='ACTUALIZAR CUENTA', 
                font=("Arial", 10), 
                border=0, 
                bg="#0387fa", 
                fg="black", 
                highlightbackground="#0387fa",
                width=22,
                state='disabled',
                command=self.ActualizarCuenta, 
                cursor="hand1",
            )
            self.BotonActualizar.grid(
                row = 17, 
                column = 0,  
                ipady = 5, 
                padx = 85,
                sticky="ne",
                columnspan=2,
                pady = 15
            )
        
        def mostrarPassword(self):
            #La primera vez que se presione el ojito, terminara cambiando al archivo ver1.png
            #la segunda vez que se presione verificamos si es el ojito abierto, entonces cambiamos de archivo.
            imagenes = {
                "1" : "./cajero/img/ver1.png",
                "2" : "./cajero/img/ocultar.png"
            }

            #self.ejecutar = "VER" #es el predeterminado

            if(self.ejecutarOjo == "VER"):
                self.imgPass.configure(file=imagenes["1"])
                self.PasswordEntrada.configure(show="")
                self.ejecutarOjo = "OCULTAR"
            elif(self.ejecutarOjo == "OCULTAR"):
                self.imgPass.configure(file=imagenes["2"])
                self.PasswordEntrada.configure(show="*")
                self.ejecutarOjo = "VER"
            
        def ActualizarCuenta(self):
            #vamos a verificar cada campo del formulario para poder continuar con el proceso de actualizacion de los datos.
            self.Cedula = self.CedulaEntrada.get()
            self.Nombres = self.NombresEntrada.get()
            self.Telefono = self.TelefonoEntrada.get()
            self.Email = self.EmailEntrada.get()
            self.Provincia = self.ProvinciaEntrada.get()
            self.Permisos = self.PermisosUsuariosEntrada.get()
            self.Presupuesto = self.PresupuestoEntrada.get()
            self.Password = self.PasswordEntrada.get()

            if(self.Cedula == "" or self.Nombres == "" or self.Telefono == "" or self.Email == "" or self.Provincia == "" or self.Permisos == "" or 
               self.Presupuesto == "" or self.Password == ""):
                self.CedulaEntrada.configure(highlightbackground="#e20172")
                self.NombresEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                self.TelefonoEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                self.EmailEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                self.ProvinciaEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                # self.TipoUsuarioEntrada.configure(highlightbackground="#e20172")
                self.PresupuestoEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                self.PasswordEntrada.configure(highlightbackground="#e20172", highlightthickness=1)
                messagebox.showerror('Actualizar Cuenta', 'Todos los campos son obligatorios')
            else:
                #caso contrario en que todos los campos esten llenos... pasaremos al proceso de validar cada uno de ellos....
                #cuando todos los campos sean llenaos por completo... lo que haremos a continuacion es verificar por si se han 
                #introducido correctamente los datos.

                #El diccionario nos ayudara mucho para guardar la informacion en la base de datos de manera mucho mas flexible.
                self.informacion = {
                    "Nombre" : "",
                    "Telefono" : "",
                    "Cedula" : "",
                    "Email" : "",
                    "Provincia" : "",
                    "Permisos" : "",
                    "Password" : "",
                    "Presupuesto" : ""
                }

                if(len(self.Nombres.split(None)) != 2):
                    self.NombresEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta2["text"] = "DEBES INTRODUCIR UN NOMBRE Y UN APELLIDO"
                    self.MensajeAlerta2.grid_configure(
                        row = 4, 
                        column = 1,
                        sticky="ew",
                        padx=20
                    )
                else:
                    if(len(self.Nombres.split(None)) == 2):
                        #cuando sean dos elementos verifiquemos si 
                        self.flag = False 
                        for i in self.Nombres.split(None):
                            if(re.search(r"([0-8]|[`~_\-\|\\\/\\\\\+\*\{\}\[\]\(\)\:\;\<\>\?\.\,\%\$\#\@\!\=\'\"\&])+", i)):
                                self.flag = True 
                                break 

                        if(not self.flag):
                            try:
                                self.informacion["Nombre"] = self.Nombres.split(None)[0] + " " + self.Nombres.split(None)[1]
                                self.NombresEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta2.grid_remove()
                            except (AttributeError, NameError):
                                pass 
                        else: 
                            self.MensajeAlerta2['text'] = 'SOLAMENTE ES PERMITIDO INSERTAR LETRAS'
                            self.MensajeAlerta2.grid_configure(
                                row = 4, 
                                column = 1, 
                                sticky = "ew",
                                padx = 20
                            )
                    else: 
                        self.MensajeAlerta2['text'] = 'SOLAMENTE DEBES INSERTAR UN NOMBRE Y UN APELLIDO'
                        self.MensajeAlerta2.grid_configure(
                            row = 4, 
                            column = 1, 
                            sticky="ew",
                            padx = 20
                        )
                   

                #VALIDACION DEL CAMPO TELEFONO...
                if(len(self.Telefono) != 10):
                    self.TelefonoEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                    self.MensajeAlerta3['text'] = 'NÚMERO TELEFÓNICO INVÁLIDO'
                    self.MensajeAlerta3.grid_configure(
                        row = 6, 
                        column = 1,
                        sticky="ew",
                        padx=20
                    )
                else:
                    #verificar antes de que no contenta letras o cualquier otro tipo de caracter
                    self.pattern = r"([A-Za-z]|[`~_\-\|\\\/\\\\\+\*\{\}\[\]\(\)\:\;\<\>\?\.\,\%\$\#\@\!\=\'\"\&])+"
                    if(re.search(self.pattern, self.Telefono)):
                        self.MensajeAlerta3['text'] = 'NO DEBES INGRESAR LETRAS O OTRO TIPO DE CARÁCTER ESPECIAL'
                        self.MensajeAlerta3.grid_configure(
                            row = 6, 
                            column = 1, 
                            sticky= "ew",
                            padx = 20
                        )
                    else:
                        #vamos a realizar una comprobacion a nuestro numero telefonico....
                        self.pattern = r"^09[0-9]+"

                        if(re.search(self.pattern, self.Telefono)):
                            try:
                                #En el caso de que un usuario haya introducido bien nuestro formato basico, comprobaremos si
                                #no pertenece a un telefono ya registrado.

                                #cuando desea lograr hacer una validacion en esta parte, choca con el campo de cambiar nuestra cedula.... asi que haremos una copia para 
                                #solo hacer una validacion a este y no afecte para nada en otra parte...
                                self.comprobar = DB.db.select('usuarios', 'Cedula = {}'.format(self.CedulaCopia[0]))

                                if(self.Telefono == self.comprobar[0]['Telefono'][5:]):
                                    self.informacion["Telefono"] = self.Telefono
                                    self.TelefonoEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta3.grid_remove()
                                else:
                                    self.infoDB = DB.db.select('usuarios', 'Cedula != {}'.format(self.Cedula))
                                    self.flag = False 
                                    for i in self.infoDB:
                                        if(self.Telefono == i['Telefono'][5:]):
                                            self.flag = True 
                                            break


                                    if(not self.flag):
                                    
                                        self.informacion["Telefono"] = self.Telefono
                                        self.TelefonoEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                        self.MensajeAlerta3.grid_remove()
                                    else:
                                        self.TelefonoEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                                        self.MensajeAlerta3['text'] = 'NÚMERO TELEFÓNICO YA REGISTRADO'
                                        self.MensajeAlerta3.grid_configure(
                                        row = 6, 
                                        column = 1,
                                        sticky="ew",
                                        padx=20
                                        )

                            except (AttributeError, NameError):
                                pass 
                        else:
                            self.TelefonoEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                            self.MensajeAlerta3['text'] = 'NÚMERO TELEFÓNICO INVÁLIDO'
                            self.MensajeAlerta3.grid_configure(
                            row = 6, 
                            column = 1,
                            sticky="ew",
                            padx=20
                            )

               
                # #==============================================================================================
                
                if(len(self.Cedula) != 10):
                    self.CedulaEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta['text'] = "CEDULA INVÁLIDA"
                    self.MensajeAlerta.grid_configure(
                        row = 2, 
                        column = 1,
                        sticky="ew",
                        padx=20
                    )
                else:
                    #VAMOS A REALIZAR UNAS CUANTAS VALIDACIONES A NUESTRO CODIGO...
                    impares = self.Cedula[0::2]
                    save_valores = []
                    for i in range(len(impares)):
                        numero = int(impares[i]) * 2 
                        if(numero > 9):
                            numero -= 9 
                            save_valores.append(numero)
                        else:
                            save_valores.append(numero)

                    resultado_impares = 0
                    for j in range(len(save_valores)):
                        if(resultado_impares == 0):
                            resultado_impares = save_valores[j]
                        else:
                            resultado_impares += save_valores[j]


                    #Procedimiento que haremos para los numeros pares.
                    pares =  self.Cedula[1:-2:2]

                    resultado_pares = 0
                    for i in range(len(pares)):
                        if(resultado_pares == 0):
                            resultado_pares = int(pares[i])
                        else:
                            resultado_pares += int(pares[i])


                    #Calculamos para poder verificar por el ultimo numero y ver si coincide....
                    suma_total = resultado_pares + resultado_impares

                    restante = suma_total%10 
                
                    #sacamos modulo 10.
                    if(not restante == 0):
                        #si es distinto de 0 ....
                        numero_verificador = 10 - restante

                        if(numero_verificador == int(self.Cedula[-1])):
                            
                            #Dentro de esta seccion haremos la respectiva validacion de un modo completamente diferente al que habiamos hecho 
                            #para la seccion de creacion de cuenta.
                            try:
                                self.comprobar = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.CedulaCopia[0]))

                                if(self.Cedula == self.comprobar[0]['Cedula']):
                                    self.informacion["Cedula"] = self.Cedula 
                                    self.CedulaEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta.grid_remove()
                                else: 
                                    #si la cedula es diferente...
                                    self.comprobar = DB.db.select('usuarios', 'Cedula != "{}"'.format(self.CedulaCopia[0]))
                                    self.flag = False 

                                    for i in self.comprobar:
                                        if(self.Cedula == i['Cedula']):
                                            self.flag = True 
                                            break 

                                    if(not self.flag):
                                        #introducimos los datos....
                                        self.informacion["Cedula"] = self.Cedula
                                        self.CedulaEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                        self.MensajeAlerta.grid_remove()
                                    else:
                                        self.CedulaEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                                        self.MensajeAlerta['text'] = "CÉDULA YA REGISTRADA"
                                        self.MensajeAlerta.grid_configure(
                                            row = 2, 
                                            column = 1,
                                            sticky="ew",
                                            padx=20
                                        )

                            except (AttributeError, NameError):
                                pass 

                        else:
                            self.CedulaEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta['text'] = "NÚMERO DE CÉDULA INCORRECTA"
                            self.MensajeAlerta.grid_configure(
                                row = 2, 
                                column = 1,
                                sticky="ew",
                                padx=20
                            )
                        
                    else:
                        if(restante == int(self.Cedula[-1])):

                            try:
                                self.comprobar = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.CedulaCopia[0]))

                                if(self.Cedula == self.comprobar[0]['Cedula']):
                                    self.informacion["Cedula"] = self.Cedula 
                                    self.CedulaEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta.grid_remove()
                                else: 
                                    #si la cedula es diferente...
                                    self.comprobar = DB.db.select('usuarios', 'Cedula != "{}"'.format(self.CedulaCopia[0]))
                                    self.flag = False

                                    for i in self.comprobar:
                                        if(self.Cedula == i['Cedula']):
                                            self.flag = True 
                                            break 

                                    if(not self.flag):
                                        #introducimos los datos....
                                        self.informacion["Cedula"] = self.Cedula
                                        self.CedulaEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                        self.MensajeAlerta.grid_remove()
                                    else:
                                        self.CedulaEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                                        self.MensajeAlerta['text'] = "CÉDULA YA REGISTRADA"
                                        self.MensajeAlerta.grid_configure(
                                            row = 2, 
                                            column = 1,
                                            sticky="ew",
                                            padx=20
                                        )

                            except (AttributeError, NameError):
                                pass
                        else:
                            self.CedulaEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta['text'] = "NÚMERO DE CÉDULA INCORRECTA"
                            self.MensajeAlerta.grid_configure(
                                row = 2, 
                                column = 1,
                                sticky="ew",
                                padx=20
                            )

                    
                #DEBEMOS REALIZAR CIERTAS CORRECIONES AL CODIGO A CONTINUACION..........
                if(self.Email.find('@') == -1):
                    self.EmailEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta4['text'] = 'DEBES INSERTAR UN EMAIL VÁLIDO'
                    self.MensajeAlerta4.grid_configure(
                        row = 8, 
                        column = 1, 
                        sticky="ew",
                        padx=20
                    )
                else:
                    #vamos a realizar unas cuantas validaciones a la direccion email para que puead pasar y ser 
                    #almacenado en la base de datos de manera mucho mejor de lo que ya se haya encontrado.
                    self.pattern = r"^[A-Za-z]+([0-9]*|-*|_*|[A-Za-z]*)+@[a-z]+\.[a-z]+$"

                    if(re.search(self.pattern, self.Email)):
                        try:
                            self.informacion["Email"] = self.Email
                            self.EmailEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                            self.MensajeAlerta4.grid_remove()
                        except (AttributeError, NameError):
                            pass 
                    else:
                        self.MensajeAlerta4['text'] = 'DEBES INSERTAR UN EMAIL VÁLIDO'
                        self.MensajeAlerta4.grid_configure(
                            row = 8, 
                            column = 1, 
                            sticky="ew",
                            padx=20
                        )


                
                if(self.Provincia == ""):
                    self.ProvinciaEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                    self.MensajeAlerta5['text'] = 'DEBES ASIGNAR UNA PROVINCIA'
                    self.MensajeAlerta5.grid_configure(
                        row = 10, 
                        column = 1, 
                        sticky = "ew", 
                        padx = 20 
                    )
                else: 
                    if(len(self.Provincia.split(None)) == 1):
                        #validar que la entra solo sea no numeros o otros caracteres especiales...
                        try:
                            self.pattern = r"([0-9]|[`~_\-\|\\\/\\\\\+\*\{\}\[\]\(\)\:\;\<\>\?\.\,\%\$\#\@\!\=\'\"\&])+"
                            if(re.search(self.pattern, self.Provincia.split(None)[0])):
                                self.ProvinciaEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                                self.MensajeAlerta5['text'] = 'SOLAMENTE SE PERMITE INSERTAR LETRAS'
                                self.MensajeAlerta5.grid_configure(
                                    row = 10, 
                                    column = 1, 
                                    sticky= "ew",
                                    padx = 20
                                )
                            else: 
                                self.informacion["Provincia"] = self.Provincia.split(None)[0]
                                self.ProvinciaEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta5.grid_remove()
                        except (NameError, AttributeError):
                            pass 
                    else: 
                        self.ProvinciaEntrada.configure(highlightbackground="#9b1322", highlightthickness=2)
                        self.MensajeAlerta5['text'] = 'SOLO ES PERMITIDO INSERTAR UNA PROVINCIA'
                        self.MensajeAlerta5.grid_configure(
                            row = 10, 
                            column = 1, 
                            sticky= "ew", 
                            padx = 20 
                        )

              

                #TIPOS DE USUARIO
                if(self.Permisos == ""):
                    self.MensajeAlerta6['text'] = 'DEBES INSERTAR UN TIPO DE USUARIO'
                    self.MensajeAlerta6.grid_configure(
                        row = 12, 
                        column = 1,
                        sticky="ew",
                        padx=20
                    )
                else:
                    try:
                        match(self.Permisos):
                            case "CLIENTE":
                                self.informacion["Permisos"] = "0"

                            case "ADMINISTRADOR":
                                self.informacion["Permisos"] = "1"

                        self.MensajeAlerta6.grid_remove()
                    except (AttributeError, NameError):
                        pass 

                
                if(len(self.Password) != 5):
                    self.PasswordEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta8['text'] = 'TU CONTRASEÑA DEBE TENER UNA LONGITUD DE 5'
                    self.MensajeAlerta8.grid_configure(
                        row = 16, 
                        column = 1,
                        sticky="ew",
                        padx=20
                    )
                else:
                    #Vamos hacer unas cuantas validaciones a nuestro password. 
                    #EN ESTE CASO SOLAMENTE HAREMOS QUE NUESTRO PASSWORD SEA NUMERICA PARA UN CLIENTE Y ALFANUMERICA PARA UN ADMINISTRADOR....
                    if(int(self.informacion["Permisos"]) == 0):
                        #generaremos un password para un cliente comun....
                        self.pattern = r"[0-9]{5}" #debera haber solo 5 numeros del 1 al 9

                        if(re.search(self.pattern, self.Password)):
                            try:
                                self.informacion["Password"] = self.Password
                                self.PasswordEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta8.grid_remove()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            #generaremos una alerta para que ingrese nuevamente los datos.
                            self.PasswordEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta8['text'] = 'Tu contraseña solo debe contener 5 digitos del 1 al 9'.upper()
                            self.MensajeAlerta8.grid_configure(
                                row = 16, 
                                column = 1,
                                sticky="ew",
                                padx=20
                            )

                    elif(int(self.informacion["Permisos"]) == 1):
                        #generaremos un password para un administrador....
                        self.pattern = r"([A-Z]|[a-z]|[0-9]){5}" #debera haber solo 5 numeros del 1 al 9

                        if(re.search(self.pattern, self.Password)):
                            try:
                                self.informacion["Password"] = self.Password
                                self.PasswordEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                self.MensajeAlerta8.grid_remove()
                            except (AttributeError, NameError):
                                pass 
                        else:
                            #generaremos una alerta para que ingrese nuevamente los datos.
                            self.PasswordEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta8['text'] = 'La contraseña debe poseer una longitud de 5 con carácteres alfanuméricos '.upper()
                            self.MensajeAlerta8.grid_configure(
                                row = 16, 
                                column = 1,
                                sticky="ew",
                                padx=20
                            )

            
                if(self.Presupuesto == ""):
                    #presupuesto 7
                    self.PresupuestoEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                    self.MensajeAlerta7['text'] = 'DEBES INSERTAR UN PRESUPUESTO'
                    self.MensajeAlerta7.grid_configure(
                        row = 14, 
                        column = 1, 
                        sticky = "ew", 
                        padx = 20 
                    ) 
                else:
                    #cuando la entrada no se encuentra vacia.... 
                    #tendremos que hacer unas cuantas validaciones respecticas.... 
                    if(len(self.Presupuesto.split(None)) == 1):
                        #cuando sea solamente una entrada numerica, lo que haremos a continuacion es validar que dicha entrada es numerica.
                        self.pattern = r"([A-Za-z]|[`~_\-\|\\\/\\\\\+\*\{\}\[\]\(\)\:\;\<\>\?\.\,\%\$\#\@\!\=\'\"\&])+"

                        if(re.search(self.pattern, self.Presupuesto)):
                            self.PresupuestoEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                            self.MensajeAlerta7['text'] = 'LA ENTRADA SÓLO ACEPTA ENTRADAS NUMERICAS ENTERAS'
                            self.MensajeAlerta7.grid_configure(
                                row = 14, 
                                column = 1, 
                                sticky = "ew", 
                                padx = 20 
                            ) 
                        else:
                            try:
                                #debemos fijar un limite de presupuesto.
                                self.MaximoPresupuesto = 1000 #este es el limite, solo para generar un deposito inicial...
                                self.MinimoPresupuesto = 20 #este es el valor inicial donde un usuario puede comenzar.... 
                                #como banco le regalamos 20 dolares como entrada para que pueda iniciar... 
                                if(int(self.Presupuesto) >= self.MinimoPresupuesto and int(self.Presupuesto) <= self.MaximoPresupuesto): 
                                    self.informacion['Presupuesto'] = self.Presupuesto
                                    self.PresupuestoEntrada.configure(highlightbackground="#0971a6",highlightthickness=2)
                                    self.MensajeAlerta7.grid_remove()
                                else: 
                                    self.PresupuestoEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                                    self.MensajeAlerta7['text'] = 'DEBE HABER UNA ENTRADA COMO MINIMO DE 20 DÓLARES'
                                    self.MensajeAlerta7.grid_configure(
                                        row = 14, 
                                        column = 1, 
                                        sticky = "ew", 
                                        padx = 20 
                                    ) 
                            except (NameError, AttributeError):
                                pass 

                    else: 
                        self.PresupuestoEntrada.configure(highlightbackground="#9b1322",highlightthickness=2)
                        self.MensajeAlerta7['text'] = 'DEBES INSERTAR UNA SOLA ENTRADA NUMÉRICA'
                        self.MensajeAlerta7.grid_configure(
                            row = 14, 
                            column = 1, 
                            sticky = "ew", 
                            padx = 20 
                        ) 
                        


                # ESTO LO INTRODUCIRA DENTRO DE LA BASE DE DATOS.
                if(self.informacion['Nombre'] != "" and self.informacion['Telefono'] != "" and self.informacion['Cedula'] != "" and 
                  self.informacion['Email'] != "" and self.informacion['Provincia'] != "" and self.informacion['Permisos'] != "" and 
                  self.informacion['Password'] != "" and self.informacion['Presupuesto'] != ""):

                    

                    self.preguntar = messagebox.askquestion('Actualizar Cuenta', '¿Deseas continuar con la actualización?')

                    if(self.preguntar == "yes"):
                        DB.db.update('usuarios', {
                            'Nombre' : self.informacion['Nombre'],
                            'Telefono' : "+593 "+self.informacion['Telefono'],
                            'Cedula' : self.informacion['Cedula'],
                            'Email' : self.informacion['Email'],
                            'Provincia' : self.informacion['Provincia'],
                            'Permisos' : self.informacion['Permisos'],
                            'Password' : self.informacion['Password'],
                            'Presupuesto' : self.informacion['Presupuesto']
                        },{
                            'Cedula' : f"{self.CedulaCopia[0]}"
                        })

                        messagebox.showinfo('Crear Cuenta', 'Cuenta actualizada exitosamente!')

                    self.NombresEntrada.delete(0, tk.END)
                    self.NombresEntrada.insert(0, "SIN CUENTA")
                    self.NombresEntrada['state'] = 'readonly'

                    self.TelefonoEntrada.delete(0, tk.END)
                    self.TelefonoEntrada.insert(0, "SIN CUENTA")
                    self.TelefonoEntrada['state'] = 'readonly'

                    self.CedulaEntrada.delete(0, tk.END)

                    self.EmailEntrada.delete(0, tk.END)
                    self.EmailEntrada.insert(0, "SIN CUENTA")
                    self.EmailEntrada['state'] = 'readonly'

                    self.PermisosUsuariosEntrada.set("SIN CUENTA")
                    self.PermisosUsuariosEntrada['state'] = 'readonly'

                    self.PasswordEntrada.delete(0, tk.END)
                    self.PasswordEntrada.insert(0, "SIN CUENTA")
                    self.PasswordEntrada['state'] = 'readonly'
                    self.PasswordEntrada['show'] = ""

                    self.buttonImg.grid_remove()

                    self.ProvinciaEntrada.delete(0, tk.END)
                    self.ProvinciaEntrada.insert(0, "SIN CUENTA")
                    self.ProvinciaEntrada['state'] = 'readonly'

                    self.PresupuestoEntrada.delete(0, tk.END)    
                    self.PresupuestoEntrada.insert(0, "SIN CUENTA")
                    self.PresupuestoEntrada['state'] = 'readonly'

                    self.BotonActualizar['state'] = 'disabled'


        def logout(self):
            root.destroy()
            Login.login()
            return 


    root = Tk()
    start = Admin(root)
    root.resizable( 0 , 0) # type: ignore
    root.mainloop()
