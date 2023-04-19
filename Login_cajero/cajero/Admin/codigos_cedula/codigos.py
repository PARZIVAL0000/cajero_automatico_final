#!/usr/bin/env python3
#_*_ coding:utf-8 _*_ 

#ESTO CORRESPONDE A LA SECCION DONDE VALIDAMOS LA CEDULA.. 
#Teniendo en cuenta que los dos primeros digitos son un identificador de donde fue sacada la cedula usaremos estos codigos para
#poder hacer la respectiva validacion....
provincias = {
    "01" : "Azuay",
    "02" : "Bolivar",
    "03" : "Cañar",
    "04" : "Carchi",
    "05" : "Cotopaxi",
    "06" : "Chimborazo",
    "07" : "El Oro",
    "08" : "Esmeraldas",
    "09" : "Guayas",
    "10" : "Imbabura",
    "11" : "Loja",
    "12" : "Los Ríos",
    "13" : "Manabí",
    "14" : "Morona Santiago",
    "15" : "Napo",
    "16" : "Pastaza",
    "17" : "Pichincha",
    "18" : "Tungurahua",
    "19" : "Zamora Chinchipe",
    "20" : "Galápagos",
    "21" : "Sucumbios",
    "22" : "Orellana",
    "23" : "Santo Domingo de los Tsáchilas",
    "24" : "Santa Elena",
    "30" : "Extranjero"
}