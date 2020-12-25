from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

#--------------------------Funciones--------------------------------------------

#Funcion de graficar eventos
def graficarEvento():
    #variable del algoritmo seleccionado
    miAlgoritmo =lista_desplegable.get()

    #se obtienen los parametros ingresadors por el usuario
    nsta        = nstaText.get()
    nlta        = nltaText.get()
    triggerOn   = triggerOnText.get()
    triggerOff  = triggerOffText.get()
    print(nlta)

    if miAlgoritmo == "Classic STA/LTA":
        print(miAlgoritmo)
    elif miAlgoritmo == "Recursive STA/LTA":
        print(miAlgoritmo)
    else:
        print('ninguna opcion valida')

def seleccionarArchivo():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    miArchivo.set(filename)


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
Label(miFrame, text="NSTA:", font=(18)).grid(row=2, column=2, padx=10, pady=10)
## Titulo de NLTA
Label(miFrame, text="NLTA:", font=(18)).grid(row=2, column=4, padx=10, pady=10)
## Titulo de Triger On
Label(miFrame, text="TRIGGER_ON:", font=(18)).grid(row=3, column=2, padx=10, pady=10)
## Titulo de Triger Off
Label(miFrame, text="TRIGGER_OFF:", font=(18)).grid(row=3, column=4, padx=10, pady=10)
## Titulo de Ingresar hora inicio
Label(miFrame, text="Hora Inicio:", font=(18)).grid(row=2, column=6, padx=10, pady=10)
## Titulo de Ingresar hora fin
Label(miFrame, text="Hora Fin:", font=(18)).grid(row=3, column=6, padx=10, pady=10)

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

#Hora Inicio
triggerOnText=Entry(miFrame)
triggerOnText.grid(row=2, column=7)

#Hora Fin
triggerOffText=Entry(miFrame)
triggerOffText.grid(row=3, column=7)

#variable del nombre del archivo seleccionado
miArchivo=StringVar()

# Input text
cuadroNombre=Entry(miFrame, textvariable=miArchivo, width=40)
cuadroNombre.grid(row=3, column=1, padx=10)

#--------------------Botones----------------
# Boton para Seleccionar Archivo
Button(miFrame, text="Seleccionar Archivo", command=seleccionarArchivo).grid(row=4, column=1, padx=50, pady=10)
# Boton Graficar Eventos seleccionarArchivo
Button(miFrame, text="Graficar Eventos", command=graficarEvento).grid(row=4, column=3, padx=50, pady=10)
# Boton Obtener Eventos
Button(miFrame, text="Obtener Eventos").grid(row=4, column=4, padx=50, pady=10)
# Boton para extraer archivo miniSeed
Button(miFrame, text="Obtener miniSeed").grid(row=4, column=5, padx=50, pady=10)


#-------------------------Imagenes--------------------------------------------
# Eventos
miImagen = PhotoImage(file="p7.png")
Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=7)

#pantalla completa
raiz.state('zoomed')

raiz.mainloop()