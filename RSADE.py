from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
import obspy
from obspy.signal.trigger import classic_sta_lta, recursive_sta_lta,delayed_sta_lta, z_detect, pk_baer, ar_pick, plot_trigger, trigger_onset
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
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 1)
        elif miAlgoritmo == "Recursive STA/LTA":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 2)
        elif miAlgoritmo == "Delayed STA/LTA":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 3)
        elif miAlgoritmo == "Z-detector":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 4)
        elif miAlgoritmo == "Baer- and Kradolfer-picker":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 5)
        elif miAlgoritmo == "AR-AIC":
            graficarAr()
        else:
            mb.showinfo("Información", "Debe seleccionar un Algoritmo correcto")
        
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
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 1)
        elif miAlgoritmo == "Recursive STA/LTA":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 2)
        elif miAlgoritmo == "Delayed STA/LTA":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 3)
        elif miAlgoritmo == "Z-detector":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 4)
        elif miAlgoritmo == "Baer- and Kradolfer-picker":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 5)
        else:
            mb.showinfo("Información", "Debe seleccionar un Algoritmo correcto")
        
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
    archivo.configure(text=filename, font=(12)) 
    
def comprobar(nsta):
    if nsta == "":
        print("sin datos")
    else:
        print(nsta)
        
def graficarAr():
    st = obspy.read(miArchivo.get())
    trace1 = st[0]#.trim(t1,t2)
    trace2 = st[1]#.trim(t1,t2)
    trace3 = st[2]#.trim(t1,t2)
    trace1.data = trace1.data/6553.6
    trace2.data = trace2.data/6553.6
    trace3.data = trace3.data/6553.6
    trace1.filter('bandpass', freqmin = 5, freqmax = 20)
    trace2.filter('bandpass', freqmin = 5, freqmax = 20)
    trace3.filter('bandpass', freqmin = 5, freqmax = 20)
    df = trace1.stats.sampling_rate
    p_pick, s_pick = ar_pick(trace1.data, trace2.data, trace3.data, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
    
    f = plt.Figure(figsize=(16, 9))
    a = f.add_subplot(211)
    #ax = a.subplot(211)
    a.plot(trace1.data, 'k')
    ymin, ymax = a.get_ylim()
    a.axvline(x=p_pick*100,linewidth=2, color='r')
    a.axvline(x=s_pick*100,linewidth=2, color='b')
    
    global canvas
    
    #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
    try:
        canvas.get_tk_widget().pack_forget() # use the delete method here
    except:
        pass
    
    
    canvas = FigureCanvasTkAgg(f, top_frame)
    
    canvas.get_tk_widget().pack(side="left", fill="both")
    canvas.draw()

    toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
    toolbar.update()
    canvas._tkcanvas.pack(side="left", fill="both")
    
    
def graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, tipoAlgoritmo):
    
    if nsta=="" or triggerOn=="" or triggerOff=="":
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
        
        # se define el tipo de algoritmo a usar
        #1 = "Classic STA/LTA", 2 = "Recursive STA/LTA", 3 = "Delayed STA/LTA", 4 = "Z-detector", 5="Baer- and Kradolfer-picker", 6 = "AR-AIC"
        if tipoAlgoritmo == 1:
            cft = classic_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 2:
            cft = recursive_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 3:
            cft = delayed_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 4:
            cft = z_detect(trace.data, int(float(nsta) * df))
        elif tipoAlgoritmo == 5:
            p_pick, phase_info, cft = pk_baer(trace.data, df, 1, int(float(nsta)*df), 10, 2, int(float(nlta)*df), 6, True)
            cft=np.append(cft, 0)
        else:
            mb.showinfo("Información", "Debe seleccionar un Algoritmo correcto")
        
        #plot_trigger(trace, cft, float(triggerOn), float(triggerOff))
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        # Plotting the results
        f = plt.Figure(figsize=(16, 9))
        a = f.add_subplot(211)
        #ax = a.subplot(211)
        a.plot(trace.data, 'k')
        ymin, ymax = a.get_ylim()
        a.vlines(on_of[:, 0], ymin, ymax, color='r', linewidth=2)
        a.vlines(on_of[:, 1], ymin, ymax, color='b', linewidth=2)
        b = f.add_subplot(212)
        #b.subplot(212, sharex=ax)
        b.plot(cft, 'k')
        b.hlines([3.5, 0.5], 0, len(cft), color=['r', 'b'], linestyle='--')
        b.axis('tight')
        #plt.show()
        #global canvas
        
        #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
        try:
            canvas.get_tk_widget().pack_forget() # use the delete method here
        except:
            pass
        
        
        canvas = FigureCanvasTkAgg(f, top_frame)
        
        canvas.get_tk_widget().pack(side="left", fill="both")
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side="left", fill="both")
        
    
def eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, tipoAlgoritmo):
    print("Classic STA/LTA")
    
    if nsta=="" or nlta=="" or triggerOn=="" or triggerOff=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de obtener los eventos")
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

        # se define el tipo de algoritmo a usar
        #1 = "Classic STA/LTA", 2 = "Recursive STA/LTA", 3 = "Delayed STA/LTA", 4 = "Z-detector", 5="Baer- and Kradolfer-picker", 6 = "AR-AIC"
        if tipoAlgoritmo == 1:
            cft = classic_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 2:
            cft = recursive_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 3:
            cft = delayed_sta_lta(trace.data, int(float(nsta) * df), int(float(nlta) * df))
        elif tipoAlgoritmo == 4:
            cft = z_detect(trace.data, int(float(nsta) * df))
        elif tipoAlgoritmo == 5:
            p_pick, phase_info, cft = pk_baer(trace.data, df, 1, int(float(nsta)*df), 10, 2, int(float(nlta)*df), 6, True)
            cft=np.append(cft, 0)
        else:
            mb.showinfo("Información", "Debe seleccionar un Algoritmo correcto")
            
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        nombrearch=fd.asksaveasfilename(initialdir = "/",title = "Guardar como",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            archi1=open(nombrearch, "w", encoding="utf-8")
            archi1.write(str(on_of))
            archi1.close()
            mb.showinfo("Información", "Los eventos fueron guardados en el archivo.")
            
def actualizarVista(event):
    miAlgoritmo =lista_desplegable.get()
    if miAlgoritmo=="AR-AIC":
        #se eliminana los elementos de la vista
        nstaText.grid_forget()
        nltaText.grid_forget()
        triggerOnText.grid_forget()
        triggerOffText.grid_forget()
        horaInicio.grid_forget()
        horaFin.grid_forget()
        nstaTitle.grid_forget()
        nltaTitle.grid_forget()
        triggerOnTitle.grid_forget()
        triggerOffTitle.grid_forget()
        hInicioTitle.grid_forget()
        hFinTitle.grid_forget()
        obtenerEventosBtn.grid_forget();
        
        
    elif miAlgoritmo=="Baer- and Kradolfer-picker":
        Button(miFrame, text="Obtener Eventos", command=obtenerEvento).grid(row=4, column=4, padx=50, pady=10)
    else:
        # ---------------Inputs-----------------------------
        
        parametrosTitle.grid(row=1, column=2, padx=10, pady=10, columnspan=5)
        
        ## Titulo de NSTA
        nstaTitle.grid(row=2, column=2, padx=10, pady=10)
        ## Titulo de NLTA
        nltaTitle.grid(row=2, column=4, padx=10, pady=10)
        ## Titulo de Triger On
        triggerOnTitle.grid(row=3, column=2, padx=10, pady=10)
        ## Titulo de Triger Off
        triggerOffTitle.grid(row=3, column=4, padx=10, pady=10)
        ## Titulo de Ingresar hora inicio
        hInicioTitle.grid(row=2, column=6, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        hFinTitle.grid(row=3, column=6, padx=10, pady=10)
        
        
        
        #NSTA input
        #nstaText=Entry(miFrame)
        nstaText.grid(row=2, column=3)

        #NLTA input
        #nltaText=Entry(miFrame)
        nltaText.grid(row=2, column=5)

        #Trigger On
        #triggerOnText=Entry(miFrame)
        triggerOnText.grid(row=3, column=3)

        #Trigger Off
        #triggerOffText=Entry(miFrame)
        triggerOffText.grid(row=3, column=5)

        #Hora Inicio
        #horaInicio=Entry(miFrame)
        horaInicio.grid(row=2, column=7)

        #Hora Fin
        #horaFin=Entry(miFrame)
        horaFin.grid(row=3, column=7)

        #--------------------Botones----------------
        
        # Boton para Seleccionar Archivo
        seleccionArchivoBtn.grid(row=4, column=1, padx=50, pady=10)
        # Boton Graficar Eventos seleccionarArchivo
        graficarEventosBtn.grid(row=4, column=3, padx=50, pady=10)
        
        # Boton Obtener Eventos
        obtenerEventosBtn.grid(row=4, column=4, padx=50, pady=10)

        # Boton para extraer archivo miniSeed
        obtenerMiniSeedBtn.grid(row=4, column=5, padx=50, pady=10)
        
        

#---------------------#Interfaz------------------------------------------------
raiz=Tk()

raiz.title("Red Sísmica del Austro")

#agregar imagen a la ventana
#raiz.iconbitmap("ucuenca.ico")

#Se crea el frame
miFrame=Frame()

#se empaueta el frame y este se acomoda al tamano de la ventana
miFrame.pack(fill="both", expand="True")

top_frame = Frame(raiz)
top_frame.pack(side="top", fill="both", expand=True)
bottom_frame = Frame(raiz)
bottom_frame.pack(side="top", fill="both", expand=True)

#variable del nombre del archivo seleccionado
miArchivo=StringVar()



#-----------------------------Titulos----------------------
## Titulo de la lista desplegable
Label(miFrame, text="Algoritmo de Detección", font=(20)).grid(row=1, column=1, padx=10, pady=10)

## Titulo de parametros
parametrosTitle=Label(miFrame, text="Parámetros del Algoritmo", font=(20))

nstaTitle=Label(miFrame, text="NSTA:", font=(18))
## Titulo de NLTA
nltaTitle=Label(miFrame, text="NLTA:", font=(18))
## Titulo de Triger On
triggerOnTitle=Label(miFrame, text="TRIGGER_ON:", font=(18))
## Titulo de Triger Off
triggerOffTitle=Label(miFrame, text="TRIGGER_OFF:", font=(18))
## Titulo de Ingresar hora inicio
hInicioTitle=Label(miFrame, text="Hora Inicio:", font=(18))
## Titulo de Ingresar hora fin
hFinTitle=Label(miFrame, text="Hora Fin:", font=(18))


#------------------- Lista desplegable ---------------------------------------------
lista_desplegable = ttk.Combobox(miFrame, width=40)
lista_desplegable.grid(row=2, column=1, padx=10, pady=10)

# Lista de opciones
algoritmos = ["Classic STA/LTA", "Recursive STA/LTA", "Delayed STA/LTA", "Z-detector", "Baer- and Kradolfer-picker", "AR-AIC"]
lista_desplegable['values']=algoritmos

lista_desplegable.bind("<<ComboboxSelected>>", actualizarVista)

# ---------------Inputs-----------------------------

## Nombre del archivo seleccionado
archivo=Label(miFrame, text="", font=(12))
archivo.grid(row=3, column=1, padx=10)

global nstaText, nltaText, triggerOnText, triggerOffText, horaInicio, horaFin

nstaText=Entry(miFrame)
#nstaText.grid(row=2, column=3)

#NLTA input
nltaText=Entry(miFrame)
#nltaText.grid(row=2, column=5)

#Trigger On
triggerOnText=Entry(miFrame)
#triggerOnText.grid(row=3, column=3)

#Trigger Off
triggerOffText=Entry(miFrame)
#triggerOffText.grid(row=3, column=5)

#Hora Inicio
horaInicio=Entry(miFrame)
#horaInicio.grid(row=2, column=7)

#Hora Fin
horaFin=Entry(miFrame)
#horaFin.grid(row=3, column=7)


#--------------------Botones----------------
        
# Boton para Seleccionar Archivo
seleccionArchivoBtn = Button(miFrame, text="Seleccionar Archivo", command=seleccionarArchivo)
# Boton Graficar Eventos seleccionarArchivo
graficarEventosBtn=Button(miFrame, text="Graficar Eventos", command=graficarEvento)

# Boton Obtener Eventos
obtenerEventosBtn=Button(miFrame, text="Obtener Eventos", command=obtenerEvento)

# Boton para extraer archivo miniSeed
obtenerMiniSeedBtn=Button(miFrame, text="Obtener miniSeed", command=guardarMiniSeed)





    

    

    
    




#-------------------------Imagenes--------------------------------------------
# Eventos
#miImagen = PhotoImage(file="p7.png")
#Label(miFrame, image=miImagen).grid(row=5, column=0, columnspan=7)

#pantalla completa
raiz.state('zoomed')

raiz.mainloop()