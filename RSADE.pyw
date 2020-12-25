from tkinter import *
from tkinter import ttk

##funcion para obtener el elemento seleccionado de la lista de opciones
def obtener_info():
    miAlgoritmo=lista_desplegable.get()
    print(miAlgoritmo)


#variable del algoritmo seleccionado
#miAlgoritmo=StringVar()

raiz=Tk()

raiz.title("Red Sísmica del Austro")

#agregar imagen a la ventana
raiz.iconbitmap("ucuenca.ico")

#Se crea el frame
miFrame=Frame()

#se empaueta el frame y este se acomoda al tamano de la ventana
miFrame.pack(fill="both", expand="True")

#tamano del frame
#miFrame.config(width="800", height="800")

#-----------------------------Titulos----------------------
## Titulo de la lista desplegable
Label(miFrame, text="Algoritmo de Detección", font=(20)).grid(row=1, column=1, padx=10, pady=10)

## Titulo de parametros
Label(miFrame, text="Parámetros del Algoritmo", font=(20)).grid(row=1, column=2, padx=10, pady=10, columnspan=5)


#------------------- Lista desplegable ---------------------------------------------
lista_desplegable = ttk.Combobox(miFrame, width=40)
lista_desplegable.grid(row=2, column=1, padx=10, pady=10)

# Lista de opciones
algoritmos = ["Classic STA/LTA", "Recursive STA/LTA", "Delayed STA/LTA", "Z-detector", "Baer- and Kradolfer-picker", "AR-AIC"]
lista_desplegable['values']=algoritmos

# ---------------Inputs-----------------------------
## Titulo de NSTA
Label(miFrame, text="NSTA", font=(18)).grid(row=2, column=2, padx=10, pady=10)
## Titulo de NLTA
Label(miFrame, text="NLTA", font=(18)).grid(row=2, column=4, padx=10, pady=10)
## Titulo de Triger On
Label(miFrame, text="TRIGGER_ON", font=(18)).grid(row=3, column=2, padx=10, pady=10)
## Titulo de Triger Off
Label(miFrame, text="TRIGGER_OFF", font=(18)).grid(row=3, column=4, padx=10, pady=10)
## Titulo de Ingresar hora inicio
Label(miFrame, text="Hora Inicio", font=(18)).grid(row=2, column=6, padx=10, pady=10)
## Titulo de Ingresar hora fin
Label(miFrame, text="Hora Fin", font=(18)).grid(row=3, column=6, padx=10, pady=10)

#NSTA input
nstaText=Entry(miFrame)
nstaText.grid(row=2, column=3)

#NLTA input
nltaText=Entry(miFrame)
nltaText.grid(row=2, column=5)

#Trigger On
triggerOnText=Entry(miFrame)
triggerOnText.grid(row=3, column=3)

#Trigger Off
triggerOffText=Entry(miFrame)
triggerOffText.grid(row=3, column=5)

#--------------------Botones----------------
# Boton Graficar Eventos
#Button(miFrame, text="Graficar Eventos", command=obtener_info).grid(row=2, column=6, padx=50, pady=10)
# Boton Obtener Eventos
#Button(miFrame, text="Obtener Eventos").grid(row=3, column=6, padx=50, pady=10)


#-------------------------Imagenes--------------------------------------------
# Eventos
miImagen = PhotoImage(file="p7.png")
Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=6)

#pantalla completa
raiz.state('zoomed')

raiz.mainloop()