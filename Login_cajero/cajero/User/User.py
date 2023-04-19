#!/usr/bin/env python3
#_*_ coding:utf-8 _*_ 

"""
    GENERAREMOS LA INTERFAZ DE NUESTRO USUARIO. 
    NUESTRO USUARIO PODRA TENER LAS SIGUIENTES FUNCIONALIDADES PARA SU CUENTA: 
    -------------------------------------------------------------------------------
                        [1.-] DEPOSITAR EN CUENTA BANCARIA
                        [2.-] RETIRAR EN CUENTA BANCARIA
                        [4.-] TRANSACCION A OTRAS CUENTAS
                        [5.-] INFORMACION DE CUENTA BANCARIA
                        [6.-] HISTORIAL DE TRANSACCIONES ---
                                                            | -> DEPOSITOS REALIZADOS
                                                            | -> RETIROS REALIZADOS
                                                            | -> TRANSACCIONES REALIZADAS
    -------------------------------------------------------------------------------
"""

import threading
import time, datetime
import tkinter as tk
from tkinter import ttk
from datetime import datetime  
from datetime import *
from tkinter import *
from tkinter import messagebox
from cajero import Login
from cajero.db import database as DB


def User(nombre, id):
    class Depositos(Frame):
        
        def __init__(self,*args, **kwargs):
            
            super().__init__(*args, **kwargs)

            self.TextoInformativo = Label(self, text="BIENVENIDO A LA SECCIÓN DEPÓSITO", font=("Arial", 10))
            self.TextoInformativo.grid(row=0, column=0, sticky="w")

            #A continuacion generaremos unas opciones el cual el usuario puede seleccionar...
            self.DineroSeleccionado = IntVar()
            #lo renderizaremos en nuestro tablero.
            self.marco = LabelFrame(self, text="DEPOSITAR DINERO")
            self.marco.grid(row=1, column=0, padx=20, pady=30, columnspan=2, sticky="ns")
            
            Radiobutton(self.marco, text="Depositar $10", 
            variable=self.DineroSeleccionado, value=1, command=self.opcionSeleccionado).grid(row=2,column=0, pady=20, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $20", 
            variable=self.DineroSeleccionado, value=2, command=self.opcionSeleccionado).grid(row=2,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Depositar $50", 
            variable=self.DineroSeleccionado, value=3, command=self.opcionSeleccionado).grid(row=3,column=0, pady=20, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $100", 
            variable=self.DineroSeleccionado, value=4, command=self.opcionSeleccionado).grid(row=3,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Depositar $200", 
            variable=self.DineroSeleccionado, value=5, command=self.opcionSeleccionado).grid(row=4,column=0, pady=20, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $500", 
            variable=self.DineroSeleccionado, value=6, command=self.opcionSeleccionado).grid(row=4,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Depositar $700", 
            variable=self.DineroSeleccionado, value=7, command=self.opcionSeleccionado).grid(row=5,column=0, pady=20, padx=60,sticky="w")
            Radiobutton(self.marco, text="OTRO VALOR", 
            variable=self.DineroSeleccionado, value=8, command=self.opcionSeleccionado).grid(row=5,column=1, pady=20, padx=65,sticky="w")

            self.NuevoDeposito = ""
            self.Descripcion = ""

            self.BotonDeposito = Button(self.marco, text="Depositar", width=25, border=0, command=self.depositarDinero,bg="#e1e631", fg="black", cursor="hand1")
            self.BotonDeposito.grid(row=7, column=0, columnspan=2, pady=10)

            self.grid(sticky="nsew")

        def opcionSeleccionado(self):
            if(self.DineroSeleccionado.get() == 8):
                self.Descripcion = Label(self.marco, text="INSERTA NUEVO DEPÓSITO: ", font=("Arial", 9))
                self.Descripcion.grid(row=6, column=0)

                self.NuevoDeposito = Entry(self.marco, validate="key", validatecommand=(self.register(self.validarNuevoDeposito),"%S"))
                self.NuevoDeposito.grid(row=6, column=1, columnspan=3, pady=5)

                self.BotonDeposito.configure(command=self.depositarNuevoDeposito)
               
            elif(self.DineroSeleccionado.get() != 8):
                #Eliminamos los campos....
                try:
                    self.NuevoDeposito.destroy()
                    self.Descripcion.destroy()
                    self.BotonDeposito.configure(command=self.depositarDinero)

                    
                except AttributeError:
                    pass 

            return self.DineroSeleccionado.get()

        def validarNuevoDeposito(self, entrada):
            if(not entrada.isdigit()):
                messagebox.showerror("Deposito", "La entrada solamente es numérica")
                return False 
            else:
                return True 

        #!Encargado de insertar en la base de datos.
        def DineroDepositador(self, total):
            #tenemos que hacer actualizaciones en nuestro dinero... 
            self.cuenta = DB.db.select('usuarios', 'id = "{}"'.format(id))
            self.presupuesto = self.cuenta[0]['Presupuesto']
            #lo que haremos a continuacion es una actualizacion de los datos...
            self.presupuesto += total

            
            DB.db.update("usuarios",{
                "Presupuesto": self.presupuesto
            },{
                "id":id
            })


            self.fecha = datetime.now().timetuple()
            # vamos a insertar nuevos datos en la tabla de depositos.
            DB.db.insert('depositos', {
                'Dinero' : total,
                'Fecha' : f"{self.fecha[0]}/{self.fecha[1]}/{self.fecha[2]}",
                'usuarioId' : id
            })


        def llamarNuevamente(self, hilo):
            root.after(1000, self.verificar_finalizacion, hilo)

        def verificar_finalizacion(self, hilo):
            
            if(not hilo.is_alive()):
                try:
                    messagebox.showinfo("Deposito", "Depósito exitoso!")
                    self.BotonDeposito['state'] = 'normal'
                    self.BotonDeposito.configure(command=self.depositarDinero)
                    self.NuevoDeposito.destroy()
                    self.Descripcion.destroy()
                  
                except AttributeError:
                   pass 

            else:
                self.llamarNuevamente(hilo)
            
        def depositarNuevoDeposito(self):
            
            if(len(self.NuevoDeposito.get()) == 0):
                messagebox.showinfo('Deposito', 'Debes introducir una cantidad')
            else:
                if(int(self.NuevoDeposito.get()) <= 1000):
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        #TENEMOS QUE GENERAR UN HILO QUE FUNCIONA A PARTE DEL PROGRAMA PRINCIPAL QUE TENEMOS...
                        #vamos a generar una barra de progreso.
                        
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(int(self.NuevoDeposito.get())))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)
                else:
                    messagebox.showwarning("Deposito", "El depósito máximo es de hasta $1000")

        def depositarDinero(self):
            self.dinero = self.opcionSeleccionado()

            match(self.dinero):
                case 1:
                    #Generaremos un ventana, el cual preguntara por si se desea continuar con el proceso.
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        #TENEMOS QUE GENERAR UN HILO QUE FUNCIONA A PARTE DEL PROGRAMA PRINCIPAL QUE TENEMOS...
                        #vamos a generar una barra de progreso.
                        self.total = 10   

                        self.BotonDeposito['state'] = 'disabled'
                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)
                       
                case 2:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        self.total = 20
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 3:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        self.total = 50
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 4:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        self.total = 100
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 5:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')
                    if(self.confirmar == 'yes'):
                        self.total = 200
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 6:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        self.total = 500
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)
                
                case 7:
                    self.confirmar = messagebox.askquestion('Depositar', '¿Desea continuar con el depósito?')

                    if(self.confirmar == 'yes'):
                        self.total = 700
                        self.BotonDeposito['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroDepositador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case _:
                    messagebox.showinfo("DEPOSITAR", "Inserta una cantidad a depositar")                    

    class Retiros(Frame):

        def __init__(self,*args, **kwargs):
            
            super().__init__(*args, **kwargs)

            self.TextoInformativo = Label(self, text="BIENVENIDO A LA SECCIÓN RETIROS", font=("Arial", 10))
            self.TextoInformativo.grid(row=0, column=0, sticky="w")

            #A continuacion generaremos unas opciones el cual el usuario puede seleccionar...
            self.DineroSeleccionado = IntVar()
            #lo renderizaremos en nuestro tablero.
            self.marco = LabelFrame(self, text="RETIRAR DINERO")
            self.marco.grid(row=1, column=0, padx=20, pady=30, columnspan=2, sticky="n")
            
            Radiobutton(self.marco, text="Retirar $10", 
            variable=self.DineroSeleccionado, value=1, command=self.opcionSeleccionado).grid(row=2,column=0, pady=20, padx=70,sticky="w")
            Radiobutton(self.marco, text="Retirar $20", 
            variable=self.DineroSeleccionado, value=2, command=self.opcionSeleccionado).grid(row=2,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Retirar $50", 
            variable=self.DineroSeleccionado, value=3, command=self.opcionSeleccionado).grid(row=3,column=0, pady=20, padx=70,sticky="w")
            Radiobutton(self.marco, text="Retirar $100", 
            variable=self.DineroSeleccionado, value=4, command=self.opcionSeleccionado).grid(row=3,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Retirar $200", 
            variable=self.DineroSeleccionado, value=5, command=self.opcionSeleccionado).grid(row=4,column=0, pady=20, padx=70,sticky="w")
            Radiobutton(self.marco, text="Retirar $500", 
            variable=self.DineroSeleccionado, value=6, command=self.opcionSeleccionado).grid(row=4,column=1, pady=20, padx=65,sticky="w")
            Radiobutton(self.marco, text="Retirar $700", 
            variable=self.DineroSeleccionado, value=7, command=self.opcionSeleccionado).grid(row=5,column=0, pady=20, padx=70,sticky="w")
            Radiobutton(self.marco, text="OTRO VALOR", 
            variable=self.DineroSeleccionado, value=8, command=self.opcionSeleccionado).grid(row=5,column=1, pady=20, padx=65,sticky="w")

            self.NuevoRetiro = ""
            self.DescripcionRetiro = ""

            self.BotonRetiro = Button(self.marco, text="Retirar", width=25, border=0, command=self.retirarDinero,bg="#e1e631", fg="black", cursor="hand1")
            self.BotonRetiro.grid(row=7, column=0, columnspan=2, pady=10)

            self.grid(sticky="nsew")


        def opcionSeleccionado(self):

            if(self.DineroSeleccionado.get() == 8):
                self.DescripcionRetiro = Label(self.marco, text="INSERTA NUEVO RETIRO: ", font=("Arial", 9))
                self.DescripcionRetiro.grid(row=6, column=0)

                self.NuevoRetiro = Entry(self.marco, validate="key", validatecommand=(self.register(self.validarNuevoRetiro),"%S"))
                self.NuevoRetiro.grid(row=6, column=1, columnspan=3, pady=5)

                self.BotonRetiro.configure(command=self.retirarNuevoRetiro)
               
            elif(self.DineroSeleccionado.get() != 8):
                #Eliminamos los campos....
                try:
                    self.NuevoRetiro.destroy()
                    self.DescripcionRetiro.destroy()
                    self.BotonRetiro.configure(command=self.retirarDinero)

                except AttributeError:
                    pass  

            return self.DineroSeleccionado.get()

        def validarNuevoRetiro(self, entrada):
            if(not entrada.isdigit()):
                messagebox.showerror("Deposito", "La entrada solamente es numérica")
                return False 
            else:
                return True 

        def DineroRetirador(self, total):
            self.cuenta = DB.db.select('usuarios', 'id = "{}"'.format(id))
            self.presupuesto = self.cuenta[0]['Presupuesto']
           
            #lo que haremos a continuacion es una actualizacion de los datos...
            if(total <= self.presupuesto):
            
                self.presupuesto -= total

                DB.db.update("usuarios",{
                    "Presupuesto": self.presupuesto
                },{
                    "id":id
                })


                self.fecha = datetime.now().timetuple()
                # vamos a insertar nuevos datos en la tabla de depositos.
                DB.db.insert('retiros', {
                    'Dinero' : total,
                    'Fecha' : f"{self.fecha[0]}/{self.fecha[1]}/{self.fecha[2]}",
                    'usuarioId' : id
                })                

                messagebox.showinfo("Retiro", "Retiro exitoso!")
            else:
                messagebox.showerror("Retiro", "Fondos Insuficientes: Dirigete a la sección CUENTA")



        def llamarNuevamente(self, hilo):
            root.after(1000, self.verificar_finalizacion, hilo)

        def verificar_finalizacion(self, hilo, flag = False):
            
            if(not hilo.is_alive()):
                try:
                    #todos los depositos pasaran por aqui... asi que debemos controlar el error que se pueda llegar a generar... por aqui..
                    self.BotonRetiro['state'] = 'normal'
                    self.BotonRetiro.configure(command=self.retirarDinero)
                    self.NuevoRetiro.destroy()
                    self.DescripcionRetiro.destroy()
                except AttributeError:
                   pass 

            else:
                self.llamarNuevamente(hilo)
            
        def retirarNuevoRetiro(self):
            if(len(self.NuevoRetiro.get()) == 0):
                messagebox.showinfo('Retiro', 'Debes introducir una cantidad')
            else:
                self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                if(self.confirmar == 'yes'):
                    #TENEMOS QUE GENERAR UN HILO QUE FUNCIONA A PARTE DEL PROGRAMA PRINCIPAL QUE TENEMOS...
                    #vamos a generar una barra de progreso.
                    
                    self.BotonRetiro['state'] = 'disabled'

                    self.hilo = threading.Thread(target=self.DineroRetirador(int(self.NuevoRetiro.get())))
                    self.hilo.start()

                    self.verificar_finalizacion(self.hilo, True)
                

        def retirarDinero(self):
            self.dinero = self.opcionSeleccionado()
            
            match(self.dinero):
                case 1:
                    #Generaremos un ventana, el cual preguntara por si se desea continuar con el proceso.
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        #TENEMOS QUE GENERAR UN HILO QUE FUNCIONA A PARTE DEL PROGRAMA PRINCIPAL QUE TENEMOS...
                        #vamos a generar una barra de progreso.
                        self.total = 10
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)
                       
                case 2:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        self.total = 20
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 3:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        self.total = 50
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 4:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        self.total = 100
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 5:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')
                    if(self.confirmar == 'yes'):
                        self.total = 200
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case 6:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        self.total = 500
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)
                
                case 7:
                    self.confirmar = messagebox.askquestion('Retiro', '¿Desea continuar con el retiro?')

                    if(self.confirmar == 'yes'):
                        self.total = 700
                        self.BotonRetiro['state'] = 'disabled'

                        self.hilo = threading.Thread(target=self.DineroRetirador(self.total))
                        self.hilo.start()

                        self.verificar_finalizacion(self.hilo)

                case _:
                    messagebox.showinfo("RETIRAR", "Inserta una cantidad a retirar")      

    # !!! IMPORTANTE -> LA SECCION TRANSACCION QUEDA PENDIENTE.... 
    class Transacciones(Frame):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


            self.TextoInformativo = Label(self, text="BIENVENIDO A LA SECCIÓN TRANSACCIÓN", font=("Arial", 10))
            self.TextoInformativo.grid(row=0, column=0, sticky="w")


            self.marco = LabelFrame(self, text="PROCESO TRANSFERENCIA")
            self.marco.grid(row=1, column=0, sticky="w", pady=20, ipadx=5, padx=15)

            
            self.DniClienteDepositado = Label(self.marco, text="DNI DEL USUARIO: ", font=("Arial", 9))
            self.DniClienteDepositado.grid(row=2, column=0, pady=15, padx=5,sticky="w")
            self.EntryDniClienteDepositado = Entry(self.marco, 
            justify="center", 
            width=25,
            validate="key",
            validatecommand=(self.register(self.validarEntryDNI),"%S"))

            self.EntryDniClienteDepositado.grid(row=2, column=1, padx=5, pady=15)


            self.TextoTransaccion = Label(self.marco, text="ESCOGE UNA CANTIDAD A DEPOSITAR", font=("Arial underline", 9))
            self.TextoTransaccion.grid(row=3, column=0, padx=5)


            self.DineroSeleccionado = IntVar()

            Radiobutton(self.marco, text="Depositar $10", 
            variable=self.DineroSeleccionado, value=1, command=self.opcionSeleccionado).grid(row=4,column=0, pady=10, padx=45,sticky="w")
            Radiobutton(self.marco, text="Depositar $20", 
            variable=self.DineroSeleccionado, value=2, command=self.opcionSeleccionado).grid(row=4,column=1, pady=10, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $50", 
            variable=self.DineroSeleccionado, value=3, command=self.opcionSeleccionado).grid(row=5,column=0, pady=10, padx=45,sticky="w")
            Radiobutton(self.marco, text="Depositar $100", 
            variable=self.DineroSeleccionado, value=4, command=self.opcionSeleccionado).grid(row=5,column=1, pady=10, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $200", 
            variable=self.DineroSeleccionado, value=5, command=self.opcionSeleccionado).grid(row=6,column=0, pady=10, padx=45,sticky="w")
            Radiobutton(self.marco, text="Depositar $500", 
            variable=self.DineroSeleccionado, value=6, command=self.opcionSeleccionado).grid(row=6,column=1, pady=10, padx=60,sticky="w")
            Radiobutton(self.marco, text="Depositar $700", 
            variable=self.DineroSeleccionado, value=7, command=self.opcionSeleccionado).grid(row=7,column=0, pady=10, padx=45,sticky="w")
            Radiobutton(self.marco, text="OTRO VALOR", 
            variable=self.DineroSeleccionado, value=8, command=self.opcionSeleccionado).grid(row=7,column=1, pady=10, padx=60,sticky="w")

            self.BotonTransaccion = Button(self.marco, text="Transferir", border=0, bg="#e1e631", width=25, cursor="hand1", command=self.transaccion)
            self.BotonTransaccion.grid(row=9, column=0, columnspan=2, pady=10)

            self.grid(sticky="nsew")


        #Validar el campo del DNI que se debe introducir solamente numeros...
        def validarEntryDNI(self, entrada):
            return entrada.isdigit()


        def validarNuevoDeposito(self, entrada):
            return entrada.isdigit()

        def opcionSeleccionado(self):
            if(self.DineroSeleccionado.get() == 8):
                self.Descripcion = Label(self.marco, text="INSERTA NUEVO DEPÓSITO: ", font=("Arial", 9))
                self.Descripcion.grid(row=8, column=0)

                self.NuevoDeposito = Entry(self.marco, validate="key", validatecommand=(self.register(self.validarNuevoDeposito),"%S"))
                self.NuevoDeposito.grid(row=8, column=1, columnspan=3, pady=5)

                self.BotonTransaccion.configure(command=self.otraTransaccion)
               
            elif(self.DineroSeleccionado.get() != 8):
                #Eliminamos los campos....
                try:
                    self.NuevoDeposito.destroy()
                    self.Descripcion.destroy()
                    self.BotonTransaccion.configure(command=self.transaccion)

                except AttributeError:
                    pass 

            return self.DineroSeleccionado.get()



        

        def llamar_nuevamente(self, hilo):

            self.after(1000, self.verificar_hilo, hilo)

        def generarTransaccion(self, cantidad, cedula):
            #vamos a depositar en otra cuenta la cantidad que el usuario introdujo....
            """
                -------------------------------------------------------------------------------
                1.- Verificamos primero el presupuesto del usuario quien deposita. SI no tiene -> mensaje de error.....
                2.- cantidad -> lo restamos del presupuesto del usuario quien deposita, porque se verifico que si tiene presupuesto.
                3.- Entonces actualizamos el presupuesto del usuario quien depositar en la DB.
                ---------------------------------------------------------------------------------

                1.- Obtenemos el presupuesto del depositado en la DB (con ayuda de la cedula validada).
                2.- Sumamos la cantidad con y volvemos a guardarla en la DB, con una actualizacion....
                ------------------------------------------------------------------------------------------
            """


            #PRIMER PASO -> EL CLIEnTE PROPIETARIO DE LA CUENTA Y REALIZA LA TRANSFERENCIA.
            self.usuario = DB.db.select('usuarios', 'id = "{}"'.format(id))[0]
            self.presupuesto = self.usuario['Presupuesto']
            #veirificar si el presupuesto es mayor a la cantidad
            if(cantidad <= int(self.presupuesto)):
                self.presupuesto -= cantidad 

                DB.db.update('usuarios', {
                    'Presupuesto' : self.presupuesto
                },{
                    'id':id
                })


                #SEGUNDO PASO -> EL cliente destino, quien recibe la transferencia
                self.usuarioDestino = DB.db.select('usuarios', 'Cedula = "{}"'.format(cedula))[0]
                self.presupuestoDestino = self.usuarioDestino['Presupuesto']
                self.presupuestoDestino += cantidad 

                DB.db.update('usuarios', {
                    'Presupuesto' : self.presupuestoDestino
                },{
                    'Cedula': cedula 
                })

                self.fecha = datetime.now().timetuple()
                # vamos a insertar nuevos datos en la tabla de depositos.
                DB.db.insert('transaccion', {
                    'Dinero' : cantidad,
                    'Fecha' : f"{self.fecha[0]}/{self.fecha[1]}/{self.fecha[2]}",
                    'usuarioId' : id,
                    'depositadorId' : self.usuarioDestino['id']
                })

                messagebox.showinfo('Transacción', 'Transferencia exitosa')

            else:
                messagebox.showerror('Transacción', 'No tienes fondos suficientes para realizar la transferencia!')


        def verificar_hilo(self, hilo):

            if(not hilo.is_alive()):
                try:
                    self.BotonTransaccion['state'] = 'normal'
                    self.BotonTransaccion.configure(command=self.transaccion)
                    self.NuevoDeposito.destroy()
                    self.Descripcion.destroy()
                except AttributeError:
                    pass 
            else:
                self.llamar_nuevamente(hilo)


        def otraTransaccion(self):
            self.cedula = self.EntryDniClienteDepositado.get()

            if(self.cedula == ""):
                messagebox.showwarning('Transacción', 'El DNI es obligatorio')

            else:
                #validar si es el DNI registrado ....
                self.verificacion = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.cedula))

                if(len(self.verificacion) != 0):
                    #Cuando el cliente haya introducido el numero de DNI correcto... 
                    #nos encargamos de la cantidad que inserte... la cantidad no debe estar vacia..

                    self.presupuesto = self.NuevoDeposito.get() 

                    if(self.presupuesto == "" or int(self.presupuesto) == 0):
                        messagebox.showinfo('Transacción', 'Debes introducir una cantidad válida!')
                    else:
                        self.confirmar = messagebox.askquestion('Transacción', '¿Desea continuar con la transacción?')

                        if(self.confirmar == 'yes'):

                            self.BotonTransaccion['state'] = 'disabled'

                            self.hilo = threading.Thread(target=self.generarTransaccion(int(self.presupuesto), self.cedula))
                            self.hilo.start()

                            self.verificar_hilo(self.hilo)

                else: 
                    messagebox.showwarning("Transaccion", "DNI inválido!") 



        def transaccion(self):
            self.numeroRadio = self.opcionSeleccionado()
            self.cedula = self.EntryDniClienteDepositado.get()

            #validaremos de que existe una cedula...
            if(self.cedula == ""):
                messagebox.showwarning('Transacción', 'El DNI es obligatorio')
            else:

                #Cuando el usuario haya introducido la cedula... debemos verificar que sea valida y no una inventda
                self.comprobacion = DB.db.select('usuarios', 'Cedula = "{}"'.format(self.cedula))

                if(len(self.comprobacion) != 0):
                    match(self.numeroRadio):
                        case 1:

                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 10 

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo)
                            
                        case 2:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 20

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo) 

                        case 3:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 50

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo)

                        case 4:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 100

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo)

                        case 5:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 200

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo) 

                        case 6:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')
                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 500

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo) 

                        case 7:
                            self.confirmacion = messagebox.askquestion('Retiro', '¿Desea continuar con la transacción?')

                            if(self.confirmacion == 'yes'):
                                self.BotonTransaccion['state'] = 'disabled'
                                self.cantidad = 700

                                self.hilo = threading.Thread(target=self.generarTransaccion(self.cantidad, self.cedula))
                                self.hilo.start()

                                self.verificar_hilo(self.hilo)

                        case _:
                            messagebox.showwarning('Transacción', 'Debes insertar una cantidad')
                else:
                    messagebox.showwarning("Transaccion", "DNI inválido!")    


    class Cuenta(Frame):
        def __init__(self, presupuesto ,entrada,*args, **kwargs):
            self.presupuesto = presupuesto 
            self.entrada = entrada 
            
            super().__init__(*args, **kwargs)

            # !INFORMACION DE LA BASE DE DATOS
            self.query = DB.db.select('usuarios', 'id = "{}"'.format(id))[0]

            self.TextoInformativo = Label(self, text="BIENVENIDO A LA SECCIÓN CUENTA", font=("Arial", 10))
            self.TextoInformativo.grid(row=0, column=0, sticky="w")

            #Crearemos un marco justamente para la informacion de las cuentas...

            self.marco = LabelFrame(self, text="INFORMACIÓN CUENTA")
            self.marco.grid(row=1, column=0, padx=20, pady=30, columnspan=2, sticky="n")
            
            self.NombresCliente = Label(self.marco, text="Nombres: ")
            self.NombresCliente.grid(row=2, column=0, sticky="w", pady=10, padx=30)
            self.EntryNombreCliente = Entry(self.marco, textvariable="Nombre", fg="black",justify="center", width=42)
            self.EntryNombreCliente.grid(row=2,column=1,sticky="w", pady=10, columnspan=2, padx=33, ipady=5)
            self.EntryNombreCliente.insert(0, self.query["Nombre"])
            self.EntryNombreCliente['state'] = 'readonly'


            self.CedulaCliente = Label(self.marco, text="Cedula: ")
            self.CedulaCliente.grid(row=3,column=0, sticky="w", pady=10, padx=30)
            self.EntryCedulaCliente = Entry(self.marco, textvariable="Cedula", fg="black", justify="center", width=42)
            self.EntryCedulaCliente.grid(row=3,column=1,sticky="w", pady=10, padx=33, ipady=5)
            self.EntryCedulaCliente.insert(0, self.query["Cedula"])
            self.EntryCedulaCliente['state'] = 'readonly'


            self.TelefonoCliente = Label(self.marco, text="Teléfono: ")
            self.TelefonoCliente.grid(row=4, column=0, pady=10, sticky="w", padx=30)
            self.EntryTelefonoCliente = Entry(self.marco, textvariable="Telefono", fg="black", justify="center", width=42)
            self.EntryTelefonoCliente.grid(row=4,column=1,sticky="w", pady=10, padx=33, ipady=5)
            self.EntryTelefonoCliente.insert(0, self.query["Telefono"])
            self.EntryTelefonoCliente['state'] = 'readonly'


            self.EmailCliente = Label(self.marco, text="Email: ")
            self.EmailCliente.grid(row=5, column=0, pady=10, sticky="w", padx=30)
            self.EntryEmailCliente = Entry(self.marco, textvariable="Email", fg="black", justify="center", width=42)
            self.EntryEmailCliente.grid(row=5,column=1,sticky="w", pady=10, padx=33, ipady=5)
            self.EntryEmailCliente.insert(0, self.query["Email"])
            self.EntryEmailCliente['state'] = 'readonly'

            self.ProvinciaCliente = Label(self.marco, text="Provincia: ")
            self.ProvinciaCliente.grid(row=6, column=0, pady=10, sticky="w", padx=30)
            self.EntryProvinciaCliente = Entry(self.marco, textvariable="Provincia", fg="black", justify="center", width=42)
            self.EntryProvinciaCliente.grid(row=6,column=1,sticky="w", pady=10, padx=33, ipady=5)
            self.EntryProvinciaCliente.insert(0, self.query["Provincia"])
            self.EntryProvinciaCliente['state'] = 'readonly'

            self.PresupuestoCliente = Label(self.marco, text="Presupuesto: ")
            self.PresupuestoCliente.grid(row=7, column=0, pady=10, sticky="w", padx=30)
            #nos muestra el valor de nuestro presupuesto....
            #debera actualizarse constantemente ....
            self.EntryPresupuestoCliente = Entry(self.marco, textvariable="Presupuesto", fg="black", justify="center", width=42)
            self.EntryPresupuestoCliente.insert(0, self.presupuesto)
            self.EntryPresupuestoCliente['state'] = 'readonly'
            self.EntryPresupuestoCliente.grid(row=7,column=1,sticky="w", pady=10, padx=33, ipady=5)
         
            self.query_perfil(self.entrada)
    
            self.grid(sticky="nsew")

        def ejecucion_query_perfil(self):
            self.presupuesto = DB.db.select('usuarios', 'id = "{}"'.format(id))[0]['Presupuesto']
            self.EntryPresupuestoCliente = Entry(self.marco, textvariable="Presupuesto", fg="black", justify="center", width=42)
            self.EntryPresupuestoCliente.delete(0, tk.END)
            self.EntryPresupuestoCliente.insert(0, self.presupuesto)
            self.EntryPresupuestoCliente['state'] = 'readonly'
            self.EntryPresupuestoCliente.grid(row=7,column=1,sticky="w", pady=10, padx=33, ipady=5)

            root.after(1000, self.ejecucion_query_perfil)

        def query_perfil(self, entrada):
            if(entrada):
                self.hilo = threading.Thread(target=self.ejecucion_query_perfil)
                self.hilo.start()


    class VentanaDepositos(Toplevel):
        def __init__(self, fecha, *args, **kwargs):
            self.fecha = fecha 
            super().__init__(*args, **kwargs)
            self.title("HISTORIAL DEPOSITOS")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.geometry("800x400")

            self.Headers = Label(self, text='INFORMACIÓN DEPÓSITOS', bg="#5175C6", fg="white", height=3, font=("Arial", 14), anchor="w", padx=10)
            self.Headers.place(x=0, y=0, relwidth=1.0)


            self.BotonCerrar = Button(self, text="Cerrar Historial", font=("Arial", 12), 
            bg="#e1e631", fg="black", border=0, command=self.destroy, cursor="hand1")
            self.BotonCerrar.place(relx=0.8, y=18)

            #Generaremos la informacion en forma de tabla.

            self.columnaCedula = Label(self, text="NÚMERO CÉDULA", bg="white", fg="#5175C6")
            self.columnaCedula.place(relx=0.1, rely=0.3, relwidth=0.2, height=30)

            self.columnaFecha = Label(self, text="FECHA DEPÓSITO", bg="white", fg="#5175C6")
            self.columnaFecha.place(relx=0.4, rely=0.3, relwidth=0.2, height=30)

            self.columnaDeposito = Label(self, text="MONTO DEPÓSITO", bg="white", fg="#5175C6")
            self.columnaDeposito.place(relx=0.7, rely=0.3, relwidth=0.2, height=30)

            #mostraremos la informacion de nuestra base de datos.
            self.informacion = DB.db.select('depositos', 'usuarioId = "{}"'.format(id))

            self.filas = 0.4
            self.listadoDeposito = Listbox(self, border=2,bg="#1d7bbb", fg="black", height=10)
            self.listadoDeposito.insert(tk.END, *("           "+DB.db.select('usuarios', 'id = "{}"'.format(j['usuarioId']))[0]['Cedula']+"                                                               "+self.fecha+"                                                                      "+str(j['Dinero']) for j in self.informacion if j['Fecha'] == self.fecha ))
            self.listadoDeposito.place(relx=0.1, rely=0.4, relwidth=0.8)

            self.scrollbar = Scrollbar(self.listadoDeposito, orient=tk.VERTICAL, command=self.listadoDeposito.yview)
            self.listadoDeposito.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.place(x=625, y=0, height=200)
        
            self.focus()
            self.grab_set()
            self.configure(bg="#1F516F")
            

    class VentanaRetiro(Toplevel):
        def __init__(self, fecha, *args, **kwargs):
            self.fecha = fecha 
            super().__init__(*args, **kwargs)
            self.title("HISTORIAL RETIROS")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.geometry("800x400")

            self.Headers = Label(self, text='INFORMACIÓN RETIROS', bg="#5175C6", fg="white", height=3, font=("Arial", 14), anchor="w", padx=10)
            self.Headers.place(x=0, y=0, relwidth=1.0)


            self.BotonCerrar = Button(self, text="Cerrar Historial", font=("Arial", 12), 
            bg="#e1e631", fg="black", border=0, command=self.destroy, cursor="hand1")
            self.BotonCerrar.place(relx=0.8, y=18)

            #Generaremos la informacion en forma de tabla.

            self.columnaCedula = Label(self, text="NÚMERO CÉDULA", bg="white", fg="#5175C6")
            self.columnaCedula.place(relx=0.1, rely=0.3, relwidth=0.2, height=30)

            self.columnaFecha = Label(self, text="FECHA RETIRO ", bg="white", fg="#5175C6")
            self.columnaFecha.place(relx=0.4, rely=0.3, relwidth=0.2, height=30)

            self.columnaDeposito = Label(self, text="MONTO RETIRO ", bg="white", fg="#5175C6")
            self.columnaDeposito.place(relx=0.7, rely=0.3, relwidth=0.2, height=30)


            #mostraremos la informacion de nuestra base de datos.
            self.informacion = DB.db.select('retiros', 'usuarioId = "{}"'.format(id))

            self.filas = 0.4
            self.listadoDeposito = Listbox(self, border=2,bg="#1d7bbb", fg="black", height=10)
            self.listadoDeposito.insert(tk.END, *("           "+DB.db.select('usuarios', 'id = "{}"'.format(j['usuarioId']))[0]['Cedula']+"                                                              "+self.fecha+"                                                                      "+str(j['Dinero']) for j in self.informacion if j['Fecha'] == self.fecha ))
            self.listadoDeposito.place(relx=0.1, rely=0.4, relwidth=0.8)

            self.scrollbar = Scrollbar(self.listadoDeposito, orient=tk.VERTICAL, command=self.listadoDeposito.yview)
            self.listadoDeposito.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.place(x=625, y=0, height=200)
        

            self.focus()
            self.grab_set()
            self.configure(bg="#1F516F")

    
    class VentanaTransaccion(Toplevel):
        def __init__(self,fecha,*args, **kwargs):
            self.fecha = fecha 
            super().__init__(*args, **kwargs)
            self.title("HISTORIAL TRANSACCIONES")
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.geometry("800x400")

            self.Headers = Label(self, text='INFORMACIÓN TRANSACCIONES', bg="#5175C6", fg="white", height=3, font=("Arial", 14), anchor="w", padx=10)
            self.Headers.place(x=0, y=0, relwidth=1.0)


            self.BotonCerrar = Button(self, text="Cerrar Historial", font=("Arial", 12), 
            bg="#e1e631", fg="black", border=0, command=self.destroy, cursor="hand1")
            self.BotonCerrar.place(relx=0.8, y=18)

            #Generaremos la informacion en forma de tabla.

            self.columnaCedula = Label(self, text="N.CÉDULA ORG", bg="white", fg="#5175C6")
            self.columnaCedula.place(relx=0.1, rely=0.3, relwidth=0.2, height=30)

            self.columnaCedula = Label(self, text="N.CÉDULA DEST", bg="white", fg="#5175C6")
            self.columnaCedula.place(relx=0.3, rely=0.3, relwidth=0.2, height=30)

            self.columnaFecha = Label(self, text="FECHA TRAN ", bg="white", fg="#5175C6")
            self.columnaFecha.place(relx=0.5, rely=0.3, relwidth=0.2, height=30)

            self.columnaDeposito = Label(self, text="MONTO TRANS ", bg="white", fg="#5175C6")
            self.columnaDeposito.place(relx=0.7, rely=0.3, relwidth=0.2, height=30)


            # mostraremos la informacion de nuestra base de datos.
            self.informacion = DB.db.select('transaccion', 'usuarioId = "{}"'.format(id))

            self.filas = 0.4
            self.listadoDeposito = Listbox(self, border=2,bg="#1d7bbb", fg="black", height=10)
            self.listadoDeposito.insert(tk.END, *("           "+DB.db.select('usuarios', 'id = "{}"'.format(j['usuarioId']))[0]['Cedula']+"                                   "+DB.db.select('usuarios', 'id = "{}"'.format(j['depositadorId']))[0]['Cedula']+"                                     "+self.fecha+"                                         "+str(j['Dinero']) for j in self.informacion if j['Fecha'] == self.fecha ))
            self.listadoDeposito.place(relx=0.1, rely=0.4, relwidth=0.8)

            self.scrollbar = Scrollbar(self.listadoDeposito, orient=tk.VERTICAL, command=self.listadoDeposito.yview)
            self.listadoDeposito.config(yscrollcommand=self.scrollbar.set)
            self.scrollbar.place(x=625, y=0, height=200)
        

            self.focus()
            self.grab_set()
            self.configure(bg="#1F516F")


    class Historial(Frame):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.TextoInformativo = Label(self, text="BIENVENIDO A LA SECCIÓN HISTORIAL", font=("Arial", 10))
            self.TextoInformativo.grid(row=0, column=0, sticky="w")

            """
                Nuestro historial... sera un registro de todos los depositos, retiros, transacciones, el cual el 
                usuario de la cuenta puede hacer....

                Nos manejaremos con fechas y algunos RadiosButton para que se pueda eleguir libremente.
            """

            self.marco = LabelFrame(self, text='HISTORIAL DE CUENTA')
            self.marco.grid(row=1, column=0, pady=30, sticky="ns", ipadx=5, columnspan=3, padx=20)    

            self.opcionHistorial = IntVar()

            Radiobutton(self.marco, text="Depósitos", 
            variable=self.opcionHistorial, 
            value=1, 
            command=self.opcionVerificar).grid(row=2, column=0, pady=5, padx=40)

            Radiobutton(self.marco, text="Retiros", 
            variable=self.opcionHistorial, 
            value=2, 
            command=self.opcionVerificar).grid(row=2, column=1, pady=5, padx=20)

            Radiobutton(self.marco, text="Transacciones", 
            variable=self.opcionHistorial, 
            value=3, 
            command=self.opcionVerificar).grid(row=2, column=2, pady=5, padx=40)


            self.textoFecha = Label(self.marco, text="ESCOGE LA FECHA DE BÚSQUEDA", font=("Arial", 10))
            self.textoFecha.grid(
                row=3,
                column=0,
                pady=10,
                columnspan=3
            )

            #nos encargaremos de generar las fechas respectivas.
            self.listadoYears = []
            self.listadoMonth = []
            self.listadoDays = []
            
            self.MaxYear = datetime.now().timetuple()[0]
            self.MinYear = 2020

            self.hilo = threading.Thread(target=self.generarFechas(self.MaxYear, self.MinYear))
            self.hilo.start()

            # !El proceso de arriba se ejecutara dentro de un hilo distinto


            #Nuestra lista desplegable de fechas... desde el 2000 hasta la fecha actual... que constantemente ira avanzando.
            self.LabeltextoYears = Label(self.marco, text='Año: ', font=("Arial", 11))
            self.LabeltextoYears.grid(
                row = 4, 
                column= 0,
                sticky="e",
                padx=10
            )

            self.EntrytextoYears = ttk.Combobox(
            self.marco, 
            state="readonly",
            values=self.listadoYears,
            width=20)
            self.EntrytextoYears.grid(
                row=4, 
                column=1,
                pady=5,
                columnspan=3,
                sticky="w"
            )

            self.LabeltextoMonth = Label(self.marco, text="Mes: ", font=("Arial", 11))
            self.LabeltextoMonth.grid(
                row = 5, 
                column = 0,
                sticky="e",
                padx=10
            )

            self.EntrytextoMonth = ttk.Combobox(
            self.marco,  
            state="readonly",
            values=self.listadoMonth,
            width=20)
            self.EntrytextoMonth.grid(
                row=5, 
                column=1,
                pady=5,
                columnspan=3,
                sticky="w"
            )


            self.LabeltextoDays = Label(self.marco, text="Día: ", font=("Arial", 11))
            self.LabeltextoDays.grid(
                row=6, 
                column=0,
                sticky="e",
                padx=10
            )

            self.EntrytextoDays = ttk.Combobox(
            self.marco,  
            state="readonly",
            values=self.listadoDays,
            width=20)
            self.EntrytextoDays.grid(
                row=6, 
                column=1,
                pady=5,
                columnspan=3,
                sticky="w"
            )

            self.botonBusqueda = Button(self.marco, text="Buscar", bg="#e1e631", border=0, width=40, cursor="hand1", command=self.search)
            self.botonBusqueda.grid(
                row=7,
                column=0,
                columnspan=3,
                pady=20,
                sticky="ns"
            )

            self.grid(sticky="nsew")


        def generarFechas(self, maxYear, minYear):
            years = []
            mes = []
            dias = []
            while(maxYear >= minYear):
                years.append(maxYear)
                maxYear -= 1
                

            mesMaximo = 12 
            mesMinimo = 1 

            while(mesMaximo >= mesMinimo):

                if(len(str(mesMaximo)) == 1):
                    mes.append(f"0{str(mesMaximo)}")
                else:
                    mes.append(mesMaximo)

                mesMaximo -= 1


            diaMaximo = 31
            diaMinimo = 1

            while(diaMaximo >= diaMinimo):

                dias.append(diaMaximo)

                diaMaximo -= 1


            self.listadoYears = years 
            self.listadoMonth = mes 
            self.listadoDays = dias 

        def opcionVerificar(self):
            return self.opcionHistorial.get()


        def search(self):
            self.opcion = self.opcionVerificar()

            #Modificaciones a la Fecha
            self.fecha = ""

            self.years = self.EntrytextoYears.get()
            self.month = self.EntrytextoMonth.get()
            self.days = self.EntrytextoDays.get()


            if(self.opcion == 0):
                messagebox.showwarning('Historial', 'Debes escoger una opción de búsqueda')
            else:
                if(self.years == "" or self.month == "" or self.days == ""):
                    messagebox.showwarning('Historial', 'Debes introducir una fecha de búsqueda completa')
                else:
                    if(int(self.month) <= 9):
                        self.fecha = f"{self.years}/{str(self.month[1])}/{self.days}"
                    else:
                        self.fecha = f"{self.years}/{str(self.month)}/{self.days}"
                    
                    self.marco = LabelFrame(self, text="", border=0)
                    self.marco.grid(
                        row=8,
                        column=0,
                        sticky="ns",
                        padx=5
                    )


                    #vamos a generar ventana(s) secundaria(s) para que se pueda mostrar la informacion
                    #respectiva de cada historial.....

                   
                    match(self.opcion):
                        case 1:
                            #deposito
                            self.busquedaDeposito = DB.db.select('depositos', 'usuarioId = "{}"'.format(id)) 
                            self.flag = False            
                            #GENERAMOS EL ENCABEZADO DE NUESTRO CONTENIDO Y DESPUES EL CONTENIDO RESPECTIVO #1fa3d9
                            for i in self.busquedaDeposito:
                                if(i['Fecha'] == self.fecha):
                                    self.flag = True

                            if(self.flag):
                                try:
                                    self.OpenModal = VentanaDepositos(self.fecha)
                                    self.OpenModal.resizable(0,0)

                                    self.MensajeError.destroy()
                                except AttributeError:
                                    pass 
                            else:
                                self.MensajeError = Label(self.marco, text='NO SE HAN ENCONTRADO COINCIDENCIAS', font=("Arial", 11), bg="red", fg="white")
                                self.MensajeError.grid(
                                    row=9, 
                                    column=1,
                                    columnspan=3,
                                    ipadx=10, 
                                    ipady=10,
                                    sticky="ns",
                                    padx=72
                                )
                        case 2:
                            #retiro
                            self.busquedaDeposito = DB.db.select('retiros', 'usuarioId = "{}"'.format(id)) 
                            self.flag = False            
                            #GENERAMOS EL ENCABEZADO DE NUESTRO CONTENIDO Y DESPUES EL CONTENIDO RESPECTIVO #1fa3d9
                            for i in self.busquedaDeposito:
                                if(i['Fecha'] == self.fecha):
                                    self.flag = True

                            if(self.flag):
                                try:
                                    self.OpenModal = VentanaRetiro(self.fecha)
                                    self.OpenModal.resizable(0,0)
                                    self.MensajeError.destroy()
                                except AttributeError:
                                    pass 
                            else:
                                self.MensajeError = Label(self.marco, text='NO SE HAN ENCONTRADO COINCIDENCIAS', font=("Arial", 11), bg="red", fg="white")
                                self.MensajeError.grid(
                                    row=9, 
                                    column=1,
                                    columnspan=3,
                                    ipadx=10, 
                                    ipady=10,
                                    sticky="ns",
                                    padx=72
                                )

                        case 3:                        
                            #transaccion
                            self.busquedaDeposito = DB.db.select('transaccion', 'usuarioId = "{}"'.format(id)) 
                            self.flag = False            
                            #GENERAMOS EL ENCABEZADO DE NUESTRO CONTENIDO Y DESPUES EL CONTENIDO RESPECTIVO #1fa3d9
                            for i in self.busquedaDeposito:
                                if(i['Fecha'] == self.fecha):
                                    self.flag = True

                            if(self.flag):
                                try:
                                    self.OpenModal = VentanaTransaccion(self.fecha)
                                    self.OpenModal.resizable(0,0)
                                    self.MensajeError.destroy()
                                except AttributeError:
                                    pass 
                            else:
                                self.MensajeError = Label(self.marco, text='NO SE HAN ENCONTRADO COINCIDENCIAS', font=("Arial", 11), bg="red", fg="white")
                                self.MensajeError.grid(
                                    row=9, 
                                    column=1,
                                    columnspan=3,
                                    ipadx=10, 
                                    ipady=10,
                                    sticky="ns",
                                    padx=72
                                )


    class Usuario(Frame):
        def __init__(self, parent):
            self.presupuesto = 0
            super().__init__(parent)
            parent.title("USUARIO {}".format(nombre))
            parent.configure(bg="#1F516F")
            parent.columnconfigure(0, weight=1)
            parent.rowconfigure(0, weight=1)
            parent.geometry("600x650")

            self.header = Label(self, text="USUARIO: ", 
            bg="#5175C6", fg="white", font=("Bold", 16), anchor="w", padx=10)
            self.header.grid(row=0, column=0, ipady=10, ipadx=10,sticky="nsew") #5175C6

            self.usuarioNombre = Label(self, text="{}".format(nombre), 
            bg="#5175C6", fg="white", font=("Arial", 12), anchor="w", width=16)
            self.usuarioNombre.grid(row=0, column=1, ipady=10, ipadx=15,sticky="nsew")

            self.usuarioNombre = Label(self, text="", 
            bg="#5175C6", fg="white", font=("Arial", 12), anchor="w", width=0)
            self.usuarioNombre.grid(row=0, column=2, ipady=10,sticky="nsew")



            #---------------------------------------------------------------
            #LA SECCIÓN QUE CONTINÚA VA A SER UNA CONFIGURACIÓN DE UN NOTEBOOK 
            #----------------------------------------------------------------
            self.notebook = ttk.Notebook(self, width=555, height=490) 
            #vamos a estar buscando por este dato...
            self.query_perfil()


            self.deposito = Depositos(self.notebook)

            self.retiro = Retiros(self.notebook)

            self.transaccion = Transacciones(self.notebook)

            self.informacionCuenta = Cuenta(self.presupuesto,True,self.notebook)
            
            self.historial = Historial(self.notebook)

            self.notebook.add(self.deposito, text="DEPÓSITOS", padding=25)
            self.notebook.add(self.retiro, text="RETIROS", padding=25)
            self.notebook.add(self.transaccion, text="TRANSACCIONES", padding=25)
            self.notebook.add(self.informacionCuenta, text="CUENTA", padding=25)
            self.notebook.add(self.historial, text="HISTORIAL", padding=25)

            #configuracion de la subventana....
            self.notebook.grid(row=1,column=0, pady=50, padx=20,columnspan=3, sticky="w")
            #configuraciones de la ventana principal...
            self.grid(sticky="nsew")
            
            self.botonLogout = Button(self, text="Cerrar Sesión", cursor="hand1",border=0, padx=30,bg="#e1e631", fg="black", anchor="center",
            command=self.logout)
            self.botonLogout.grid(row=0, column=2, padx=100, sticky="e")

            self.configure(background="#1F516F")


        def query_perfil(self):
            self.presupuesto = DB.db.select('usuarios', 'id = "{}"'.format(id))[0]['Presupuesto']            
        

        def logout(self):
            root.destroy()
            Login.login()
            return 


    root = Tk()
    start = Usuario(root)
    root.resizable(0,0)
    root.mainloop()


# User("name name", 24)

