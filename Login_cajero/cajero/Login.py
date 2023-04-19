#!/usr/bin/env python
#_*_ coding:utf-8 _*_ 

import time, random  
import tkinter as tk
from tkinter import *
from cajero.db import database as DB
from cajero.User import User 
from cajero.Admin import Admin

def login():
    class Login(Frame):

        def __init__(self,parent=""):
            
            super().__init__(parent)
            parent.title("Login")
            parent.columnconfigure(0, weight=1)
            parent.rowconfigure(0, weight=1)
            parent.configure(background="#262b5a")
            parent.geometry("600x650")


            #Generamos el contador respectivo para que solamente el usuario pueda poseer 3 intentos ... 
            self.intentos = 3
            #generaremos un cuadro....
           
            
            self.titulo = Label(self,text="JADAC C.A EN CONFIANZA", 
                background="#0a5b98",foreground="white", font=("Cabria", 13), anchor="center")
            self.titulo.grid(row=0, column=0, sticky="nsew", ipady=5, columnspan=3)

            self.separador = Label(self, text="\n",bg="#262b5a")
            self.separador.grid(row=1, column=0)
            
            self.inicioSesion = Label(self, text="INICIAR SESIÓN", bg="#6a3d7f", width=35,fg="white", font=("Arial", 18))
            self.inicioSesion.grid(row=2, column=0, pady=20, sticky="nsew", ipady=5)

            self.separadorIntermedio = Label(self, text=" ",bg="#262b5a")
            self.separadorIntermedio.grid(row=3, column=0)

            #vamos a generar nuestros campos para introducir ciertos valores...
            self.textoID = Label(self, text="INSERTA EL IDENTIFICADOR", foreground="white", font=("Arial", 12), bg="#262b5a", width=48)
            self.textoID.grid(row=4, column=0, ipady=10, ipadx=90, sticky="ns")
            #validaremos nuestro identificador ...
            """
                1.- Solo sea numeros...
                2.- Posea solamente una longitud de 10 numeros...
                3.- EL campo no debe estar vacio...
            """
            self.inputID = Entry(self, width=65, justify="center", bg="#12537d", fg="white",
            #nuestra configuracion para validar
            validate="key",
            validatecommand=(parent.register(self.verificarID),'%S'), 
            highlightbackground="#fffbf4", 
            highlightthickness=2
            )
            self.inputID.grid(row=5, column=0, pady=15, ipady=7, sticky="ns")

            self.separador = Label(self, text="\n",bg="#262b5a")
            self.separador.grid(row=6, column=0)

            self.textoPASS = Label(self, text="INSERTA LA CONTRASEÑA", foreground="white", font=("Arial", 12), bg="#262b5a")
            self.textoPASS.grid(row=7, column=0)
            self.inputPASS = Entry(self, width=65, justify="center", bg="#12537d", fg="white", show="*", highlightbackground="#fffbf4", highlightthickness=2)
            self.inputPASS.grid(row=8, column=0, pady=15, ipady=7, sticky="ns")

            self.separador = Label(self, text="\n",bg="#262b5a")
            self.separador.grid(row=9, column=0)

            
            self.boton = Button(self, text="Iniciar Sesión", font=("Arial", 15), bg="#ffd030", fg="black", border=0, width=35, command=self.validandoFormulario, cursor="hand1")
            self.boton.grid(row=10, column=0, pady=20, ipady=5)

            self.grid(sticky="nsew")
            self.configure(background="#262b5a")

            
        def verificarID(self,entrada):
            return entrada.isdigit()
        
        def ejecutando_tiempo(self, contador=5):
            restar=random.randint(1,1)
            contador-=restar 

            #actualizamos el mensaje
            self.separadorIntermedio['text'] = " LA SESIÓN SE DESBLOQUEARÁ EN : {} seg.".format(contador)

            respuesta = root.after(1000, self.ejecutando_tiempo,contador)

            if(contador == 0):
                self.inputID['state'] = 'normal'
                self.inputID.delete(0, tk.END)
                self.inputPASS['state'] = 'normal'
                self.inputPASS.delete(0, tk.END)
                self.boton['state'] = 'normal'
                self.separadorIntermedio['text'] = "\n"
                self.separadorIntermedio['bg'] = '#262b5a'
                self.separadorIntermedio['fg'] = '#262b5a'
                self.separadorIntermedio['font'] = ("Arial", 13)
                self.separadorIntermedio.grid(pady=0)
                root.after_cancel(respuesta)

        def validandoFormulario(self):
            ID = self.inputID.get()
            PASS = self.inputPASS.get()

            if(len(ID) == 0 or len(PASS) == 0):
                #generamos una alerta... o error... renderizado.
                self.separadorIntermedio['text'] = " TODOS LOS CAMPOS SON OBLIGATORIOS "
                self.separadorIntermedio['bg'] = 'red'
                self.separadorIntermedio['fg'] = 'white'
                self.separadorIntermedio['font'] = ("Arial", 13)
                self.separadorIntermedio.grid(pady=10)
                
            else:
                
                query = DB.db.select('usuarios', 'Cedula = "{}"'.format(ID))
                
                if(len(query) == 0):
                    self.separadorIntermedio['text'] = " IDENTIFICADOR NO REGISTRADO "
                    self.separadorIntermedio['bg'] = 'red'
                    self.separadorIntermedio['fg'] = 'white'
                    self.separadorIntermedio['font'] = ("Arial", 13)
                    self.separadorIntermedio.grid(pady=10)
                else:
                    #validamos nuestro password...
                    self.separadorIntermedio['text'] = "\n"
                    self.separadorIntermedio['bg'] = '#262b5a'
                    self.separadorIntermedio['fg'] = '#262b5a'
                    self.separadorIntermedio['font'] = ("Arial", 13)
                    self.separadorIntermedio.grid(pady=0)
                    
                    if(PASS == query[0]["Password"]):
                        #verificaremos si el usuario es un administrador o un usuario comun...
                        permisos = query[0]['Permisos']

                        if(permisos == 0): #-> usuario
                            self.nombre = query[0]['Nombre']
                            self.identificador = query[0]['id']

                            root.destroy()
                            User.User(self.nombre, self.identificador)
                        elif(permisos == 1): #-> administrador 
                            self.nombre = query[0]['Nombre']
                            self.identificador = query[0]['id']

                            root.destroy()
                            Admin.admin(self.nombre, self.identificador)
                    else:
                        #AQUI JUGAREMOS CON LA VARIABLE DE LOS INTENTOS PARA EL USUARIO.
                        self.separadorIntermedio['text'] = " CONTRASEÑA INCORRECTA "
                        self.separadorIntermedio['bg'] = 'red'
                        self.separadorIntermedio['fg'] = 'white'
                        self.separadorIntermedio['font'] = ("Arial", 13)
                        self.separadorIntermedio.grid(pady=10)

                        if(self.intentos > 0 and self.intentos <= 3):
                            self.intentos -= 1
                        else:
                            self.bloqueo = 5
                            self.separadorIntermedio['text'] = " LA SESIÓN SE DESBLOQUEARÁ EN : 5 seg."
                            self.separadorIntermedio['bg'] = 'red'
                            self.separadorIntermedio['fg'] = 'white'
                            self.separadorIntermedio['font'] = ("Arial", 13)
                            self.separadorIntermedio.grid(pady=10)
                            self.inputID['state'] = 'readonly'
                            self.inputPASS['state'] = 'readonly'
                            self.boton['state'] = 'disabled'

                            root.after(1000, self.ejecutando_tiempo)

                            self.intentos = 3
                            


    root = Tk() 
    root.configure(width=600, height=650)
    start = Login(root)
    root.resizable(0,0)
    root.mainloop()


