# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:04:59 2020

@author: Alvaro Armijos
"""

from tkinter import *

raiz=Tk()

raiz.title("Red Sismica del Austro")

#impide que se modifique el tamano de la ventana
#raiz.resizable(0,0)

#agregar imagen a la ventana
raiz.iconbitmap("ucuenca.ico")

#tamano de la ventana
#raiz.geometry("400x400")

#color de fondo de la ventana
#raiz.config(bg="blue")

########################## Se crea el frame ######################################

#Se crea el frame
miFrame=Frame()

#se empaqueta el frame side=rigth al redimensionar la venta se queda anclada a ese lado
#miFrame.pack(side="right")

#se empaueta el frame y este se acomoda al tamano de la ventana
miFrame.pack(fill="both", expand="True")

#color del frame
#miFrame.config(bg="blue")

#tamano del frame
miFrame.config(width="400", height="400")

########################### Label Textos Imagenes ##########################################

miLabel=Label(miFrame, text="Hola mundo", font=(18))

#ubica el texto dentro del frame
miLabel.place(x=400, y=200)

# Imagen
miImagen = PhotoImage(file="p7.png")
Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=2)

#variable del nombre
miNombre=StringVar()

# Input text
cuadroNombre=Entry(miFrame, textvariable=miNombre)
cuadroNombre.grid(row=0, column=1)

cuadroPass=Entry(miFrame)
cuadroPass.grid(row=1, column=1)
cuadroPass.config(show="*")

cuadroApellido=Entry(miFrame)
cuadroApellido.grid(row=2, column=1)

cuadroDireccion=Entry(miFrame)
cuadroDireccion.grid(row=3, column=1)



nombreLabel=Label(miFrame, text="Nombre: ")
nombreLabel.grid(row=0, column=0, padx=10, pady=20)

passLabel=Label(miFrame, text="Password: ")
passLabel.grid(row=1, column=0, padx=10, pady=20)



apellidoLabel=Label(miFrame, text="Apellido: ")
apellidoLabel.grid(row=2, column=0, padx=10, pady=20)

direccionLabel=Label(miFrame, text="Direccion: ")
direccionLabel.grid(row=3, column=0, padx=10, pady=20)


############################### Widgets Text y Button ############################################

comentariosLabel=Label(miFrame, text="Comentarios: ")
comentariosLabel.grid(row=4, column=0, padx=10, pady=20)

textComentario=Text(miFrame, width=16, height=5)
textComentario.grid(row=4, column=1, padx=10, pady=20)

# ScrollVert
scrollVert = Scrollbar(miFrame, command=textComentario.yview)
scrollVert.grid(row=4, column=2, sticky="nsew")

textComentario.config(yscrollcommand=scrollVert.set)


#funcion del boton
def codigoBoton():

    miNombre.set("Alvaro")


#boton
botonEnvio=Button(raiz, text="Enviar", command=codigoBoton)
botonEnvio.pack()

#obtener info de los campos
#botonEnvio=Button(raiz, text="Enviar", command=lamba:codigoBoton)



raiz.mainloop()