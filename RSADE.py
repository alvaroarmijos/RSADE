from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import obspy
from obspy.signal.trigger import classic_sta_lta, plot_trigger, trigger_onset
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

#-------------------------Variables--------------------------------------------



#--------------------------Funciones--------------------------------------------

#Funcion de graficar eventos
def graficarEvento():
    #variable del algoritmo seleccionado
    miAlgoritmo =lista_desplegable.get()
    
    if miAlgoritmo=="":
        mb.showinfo("Información", "Debe seleccionar un Algoritmo")
    elif miArchivo.get()=="":
        mb.showinfo("Información", "Debe seleccionar un archivo antes de Graficar")
    else:

        #se obtienen los parametros ingresadors por el usuario
        nsta        = nstaText.get()
        nlta        = nltaText.get()
        triggerOn   = triggerOnText.get()
        triggerOff  = triggerOffText.get()
        hInicio     = horaInicio.get()
        hFin        = horaFin.get()
        

        if miAlgoritmo == "Classic STA/LTA":
            graficarClassicSta(nsta, nlta, triggerOn, triggerOff, hInicio, hFin)
        elif miAlgoritmo == "Recursive STA/LTA":
            print(miAlgoritmo)
        else:
            print('ninguna opcion valida')
        
def obtenerEvento():
    #variable del algoritmo seleccionado
    miAlgoritmo =lista_desplegable.get()
    
    if miAlgoritmo=="":
        mb.showinfo("Información", "Debe seleccionar un Algoritmo")
    elif miArchivo.get()=="":
        mb.showinfo("Información", "Debe seleccionar un archivo antes de obtener los eventos")
    else:

        #se obtienen los parametros ingresadors por el usuario
        nsta        = nstaText.get()
        nlta        = nltaText.get()
        triggerOn   = triggerOnText.get()
        triggerOff  = triggerOffText.get()
        hInicio     = horaInicio.get()
        hFin        = horaFin.get()
        

        if miAlgoritmo == "Classic STA/LTA":
            eventosClassicSta(nsta, nlta, triggerOn, triggerOff, hInicio, hFin)
        elif miAlgoritmo == "Recursive STA/LTA":
            print(miAlgoritmo)
        else:
            print('ninguna opcion valida')
        
def guardarMiniSeed():
    
    hInicio     = horaInicio.get()
    hFin        = horaFin.get()
    
    if miArchivo.get()=="":
        mb.showinfo("Información", "Debe seleccionar un archivo de eventos antes de Guardar otro")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            t = st.stats.starttime
            t1 = t + 3600 * float(hInicio)
            #t1 = t
            t2 = t + 3600 * float(hFin)
            #t2 = st.stats.endtime
            trace = st.trim(t1,t2)
        trace.write(miArchivo.get()+hInicio+"-"+hFin+'.mseed', format='MSEED')
        mb.showinfo("Información", "Archivo guardado correctamente en: " + miArchivo.get()+hInicio+"-"+hFin+'.mseed')
    

def seleccionarArchivo():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    miArchivo.set(filename)
    
def comprobar(nsta):
    if nsta == "":
        print("sin datos")
    else:
        print(nsta)
    
def graficarClassicSta(nsta, nlta, triggerOn, triggerOff, hInicio, hFin):
    print("Classic STA/LTA")
    
    if nsta=="" or nlta=="" or triggerOn=="" or triggerOff=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            t = st.stats.starttime
            t1 = t + 3600 * float(hInicio)
            #t1 = t
            t2 = t + 3600 * float(hFin)
            #t2 = st.stats.endtime
            trace = st.trim(t1,t2)
        trace.data = trace.data/6553.6
        trace.filter('bandpass', freqmin = 5, freqmax = 20)
        df = trace.stats.sampling_rate
        cft = classic_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        #plot_trigger(trace, cft, float(triggerOn), float(triggerOff))
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        # Plotting the results
        ax = plt.subplot(211)
        plt.plot(trace.data, 'k')
        ymin, ymax = ax.get_ylim()
        plt.vlines(on_of[:, 0], ymin, ymax, color='r', linewidth=2)
        plt.vlines(on_of[:, 1], ymin, ymax, color='b', linewidth=2)
        plt.subplot(212, sharex=ax)
        plt.plot(cft, 'k')
        plt.hlines([3.5, 0.5], 0, len(cft), color=['r', 'b'], linestyle='--')
        plt.axis('tight')
        #plt.show()
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(trace.data, 'k')
        canvas = FigureCanvasTkAgg(fig, master=raiz)  # CREAR AREA DE DIBUJO DE TKINTER.
        canvas.draw()
        canvas.get_tk_widget().pack(side=nstaText.BOTTOM, fill=tkinter.BOTH, expand=1)
    
def eventosClassicSta(nsta, nlta, triggerOn, triggerOff, hInicio, hFin):
    print("Classic STA/LTA")
    
    if nsta=="" or nlta=="" or triggerOn=="" or triggerOff=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de obtener los eventos")
    else:
        st = obspy.read("200428000000-CH0.mseed")[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            t = st.stats.starttime
            t1 = t + 3600 * float(hInicio)
            #t1 = t
            t2 = t + 3600 * float(hFin)
            #t2 = st.stats.endtime
            trace = st.trim(t1,t2)
        
        trace.data = trace.data/6553.6
        trace.filter('bandpass', freqmin = 5, freqmax = 20)
        df = trace.stats.sampling_rate

        #cft = classic_sta_lta(trace.data, int(10 * df), int(70 * df))
        cft = classic_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        #print(trace.stats)
        #print(trace.data)
        #print(on_of)
        #np.savetxt("Classic-STA/LTA-"+hInicio+"-"+hFin+".txt", on_of)
        #plot_trigger(trace, cft, 1.15, 0.5)
        #plot_trigger(trace, cft, float(triggerOn), float(triggerOff))
        nombrearch=fd.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            archi1=open(nombrearch, "w", encoding="utf-8")
            archi1.write(str(on_of))
            archi1.close()
            mb.showinfo("Información", "Los datos fueron guardados en el archivo.")

#---------------------#Interfaz------------------------------------------------
raiz=Tk()

raiz.title("Red Sísmica del Austro")

#agregar imagen a la ventana
#raiz.iconbitmap("ucuenca.ico")

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
horaInicio=Entry(miFrame)
horaInicio.grid(row=2, column=7)

#Hora Fin
horaFin=Entry(miFrame)
horaFin.grid(row=3, column=7)

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
Button(miFrame, text="Obtener Eventos", command=obtenerEvento).grid(row=4, column=4, padx=50, pady=10)
# Boton para extraer archivo miniSeed
Button(miFrame, text="Obtener miniSeed", command=guardarMiniSeed).grid(row=4, column=5, padx=50, pady=10)


#-------------------------Imagenes--------------------------------------------
# Eventos
#miImagen = PhotoImage(file="p7.png")
#Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=7)

#pantalla completa
raiz.state('zoomed')

raiz.mainloop()