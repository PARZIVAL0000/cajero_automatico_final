#!/usr/bin/python3
#_*_ coding:utf-8 _*_ 

import os
from easymysql.mysql import mysql 

try:
    db = mysql("", "user", "password", "cajero_automatico")
except:
    print("[!] Error de conexion... Verificar el directorio: {}".format(os.getcwd()))


    
