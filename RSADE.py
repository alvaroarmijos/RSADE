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
from datetime import date
from datetime import datetime, timedelta

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
        nsta             = nstaText.get()
        nlta             = nltaText.get()
        triggerOn        = triggerOnText.get()
        triggerOff       = triggerOffText.get()
        hInicio          = horaInicio.get()
        hFin             = horaFin.get()
        factorConversion = factorConversionText.get()
        

        if miAlgoritmo == "Classic STA/LTA":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 1, factorConversion)
        elif miAlgoritmo == "Recursive STA/LTA":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 2, factorConversion)
        elif miAlgoritmo == "Delayed STA/LTA":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 3, factorConversion)
        elif miAlgoritmo == "Z-detector":
            graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 4, factorConversion)
        elif miAlgoritmo == "Baer- and Kradolfer-picker":
            graficarBaer()
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
        factorConversion = factorConversionText.get()
        

        if miAlgoritmo == "Classic STA/LTA":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 1, factorConversion)
        elif miAlgoritmo == "Recursive STA/LTA":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 2, factorConversion)
        elif miAlgoritmo == "Delayed STA/LTA":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 3, factorConversion)
        elif miAlgoritmo == "Z-detector":
            eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, 4, factorConversion)
        elif miAlgoritmo == "Baer- and Kradolfer-picker":
            eventosBaer()
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
    global init_time, end_time
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    miArchivo.set(filename)
    n=filename.rfind('/')
    nombreArchivo=filename[n+1:]
    archivo.configure(text='Archivo seleccionado: ' + nombreArchivo, font=(12))
    st = obspy.read(miArchivo.get())[0]
    print(st)
    init_time = st.stats.starttime.strftime('%H:%M:%S')
    end_time = st.stats.endtime.strftime('%H:%M:%S')
    data.configure(text='Datos del archivo =>       Hora de Inicio: '+init_time + '           Hora final: '+end_time, font=(12))
    
    
def comprobar(nsta):
    if nsta == "":
        print("sin datos")
    else:
        print(nsta)
        
def graficarAr():
    
    #AR picker 
    f1=f1Text.get()
    f2=f2Text.get()
    lta_p=lta_pText.get()
    sta_p=sta_pText.get()
    lta_s=lta_sText.get()
    sta_s=sta_sText.get()
    m_p=m_pText.get()
    m_s=m_sText.get()
    l_p=l_pText.get()
    l_s=l_sText.get()
    hInicio     = horaInicio.get()
    hFin        = horaFin.get()
    factorConversion = factorConversionText.get()
    
    
    if f1=="" or f2=="" or lta_p=="" or sta_p=="" or lta_s=="" or sta_s=="" or m_p=="" or m_s==""or l_p=="" or l_s=="" or factorConversion=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
    else:



        st = obspy.read(miArchivo.get())
        
        if hInicio == "" and hFin == "" :
            trace1 = st[0]#.trim(t1,t2)
            trace2 = st[1]#.trim(t1,t2)
            trace3 = st[2]#.trim(t1,t2)
        else:
            t = st[0].stats.starttime
            ti=datetime.strptime(hInicio,"%H:%M" )
            tf=datetime.strptime(hFin,"%H:%M" )
            #t1 = t + 3600 * float(hInicio)
            t1 = t + (ti.hour * 60 + ti.minute) * 60
            t2 = t + (tf.hour * 60 + tf.minute) * 60
            trace1 = st[0].trim(t1,t2)
            trace2 = st[1].trim(t1,t2)
            trace3 = st[2].trim(t1,t2)
            
        
        trace1.data = trace1.data/float(factorConversion)
        trace2.data = trace2.data/float(factorConversion)
        trace3.data = trace3.data/float(factorConversion)
        trace1.filter('bandpass', freqmin = 5, freqmax = 20)
        trace2.filter('bandpass', freqmin = 5, freqmax = 20)
        trace3.filter('bandpass', freqmin = 5, freqmax = 20)
        df = trace1.stats.sampling_rate
        #p_pick, s_pick = ar_pick(trace1.data, trace2.data, trace3.data, df, 1.0, 20.0, 1.0, 0.1, 4.0, 1.0, 2, 8, 0.1, 0.2)
        p_pick, s_pick = ar_pick(trace1.data, trace2.data, trace3.data, df, float(f1), float(f2), float(lta_p), float(sta_p),
                                 float(lta_s), float(sta_s), int(m_p), int(m_s), float(l_p), float(l_s))
        
        f = plt.Figure(figsize=(16, 8))
        a = f.add_subplot(211)
        #ax = a.subplot(211)
        a.plot(trace1.data, 'k')
        ymin, ymax = a.get_ylim()
        a.axvline(x=p_pick*100,linewidth=2, color='r')
        a.axvline(x=s_pick*100,linewidth=2, color='b')
        
        global canvas
        global toolbar
        #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
        try:
            canvas.get_tk_widget().pack_forget() # use the delete method here
            toolbar.pack_forget()
        except:
            pass
        
        
        canvas = FigureCanvasTkAgg(f, top_frame)
        
        canvas.get_tk_widget().pack(side="left", fill="both")
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side="left", fill="both")
    
def graficarBaer():
    
    
    #se obtienen los parametros ingresadors por el usuario
    tdownmax    = tdownmaxText.get()
    tupevent    = tupeventText.get()
    triggerOn   = triggerOnText.get()
    triggerOff  = triggerOffText.get()
    hInicio     = horaInicio.get()
    hFin        = horaFin.get()
    thr1        = thr1Text.get()
    thr2        = thr2Text.get()
    preset_len  = preset_lenText.get()
    p_dur       = p_durText.get()
    factorConversion = factorConversionText.get()
    
    
    if tdownmax=="" or tupevent=="" or triggerOn=="" or triggerOff=="" or thr1=="" or thr2=="" or preset_len=="" or p_dur=="" or factorConversion=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            ti=datetime.strptime(hInicio,"%H:%M" )
            tf=datetime.strptime(hFin,"%H:%M" )
            t = st.stats.starttime
            #t1 = t + 3600 * float(hInicio)
            t1 = t + (ti.hour * 60 + ti.minute) * 60
            t2 = t + (tf.hour * 60 + tf.minute) * 60
            trace = st.trim(t1,t2)
        trace.data = trace.data/float(factorConversion)
        trace.filter('bandpass', freqmin = 5, freqmax = 20)
        df = trace.stats.sampling_rate
        print(int(int(preset_len)*df))
        print(float(p_dur))
        p_pick, phase_info, cft = pk_baer(trace.data, df, int(tdownmax), int(float(tupevent)*df), float(thr1), float(thr2),
                                          int(int(preset_len)*df), int(p_dur), True)
        cft=np.append(cft, 0)
        
        #plot_trigger(trace, cft, float(triggerOn), float(triggerOff))
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        # Plotting the results
        f = plt.Figure(figsize=(16, 8))
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
        global canvas
        global toolbar
        #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
        try:
            canvas.get_tk_widget().pack_forget() # use the delete method here
            toolbar.pack_forget()
        except:
            pass
        
        
        canvas = FigureCanvasTkAgg(f, top_frame)
        
        canvas.get_tk_widget().pack(side="left", fill="both")
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side="left", fill="both")
    
    
    
def graficar(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, tipoAlgoritmo, factorConversion):
    
    if nsta=="" or triggerOn=="" or triggerOff=="" or factorConversion=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            ti=datetime.strptime(hInicio,"%H:%M" )
            tf=datetime.strptime(hFin,"%H:%M" )
            t = st.stats.starttime
            #t1 = t + 3600 * float(hInicio)
            t1 = t + (ti.hour * 60 + ti.minute) * 60
            t2 = t + (tf.hour * 60 + tf.minute) * 60
            trace = st.trim(t1,t2)
        trace.data = trace.data/float(factorConversion)
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
        trace.data=trace.data/df
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        # Plotting the results
        f = plt.Figure(figsize=(16, 8))
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
        global canvas
        global toolbar
        #se intenta borrar la grafica en caso de que ya este dibujada en la interfaz
        try:
            canvas.get_tk_widget().pack_forget() # use the delete method here
            toolbar.pack_forget()
        except:
            pass
        
        
        canvas = FigureCanvasTkAgg(f, top_frame)
        
        canvas.get_tk_widget().pack(side="left", fill="both")
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, bottom_frame)
        toolbar.update()
        canvas._tkcanvas.pack(side="left", fill="both")
        
def eventosBaer():
    
    
    #se obtienen los parametros ingresadors por el usuario
    tdownmax    = tdownmaxText.get()
    tupevent    = tupeventText.get()
    triggerOn   = triggerOnText.get()
    triggerOff  = triggerOffText.get()
    hInicio     = horaInicio.get()
    hFin        = horaFin.get()
    thr1        = thr1Text.get()
    thr2        = thr2Text.get()
    preset_len  = preset_lenText.get()
    p_dur       = p_durText.get()
    factorConversion = factorConversionText.get()
    
    
    if tdownmax=="" or tupevent=="" or triggerOn=="" or triggerOff=="" or thr1=="" or thr2=="" or preset_len=="" or p_dur=="" or factorConversion=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de Graficar")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            ti=datetime.strptime(hInicio,"%H:%M" )
            tf=datetime.strptime(hFin,"%H:%M" )
            t = st.stats.starttime
            #t1 = t + 3600 * float(hInicio)
            t1 = t + (ti.hour * 60 + ti.minute) * 60
            t2 = t + (tf.hour * 60 + tf.minute) * 60
            trace = st.trim(t1,t2)
        trace.data = trace.data/float(factorConversion)
        trace.filter('bandpass', freqmin = 5, freqmax = 20)
        df = trace.stats.sampling_rate
        print(int(int(preset_len)*df))
        print(float(p_dur))
        p_pick, phase_info, cft = pk_baer(trace.data, df, int(tdownmax), int(float(tupevent)*df), float(thr1), float(thr2),
                                          int(int(preset_len)*df), int(p_dur), True)
        cft=np.append(cft, 0)
        
        #plot_trigger(trace, cft, float(triggerOn), float(triggerOff))
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        path=os.path.abspath(os.getcwd())
        on_of=on_of/df
        evetos_obtenidos=[]
        #funcion para converitr las meustras en horas minutos y segundos
        for i in range(len(on_of)):
            for j in range(len(on_of[i])):
                sec = timedelta(seconds=on_of[i][j])
                evetos_obtenidos.append(str(sec))
        nombrearch=fd.asksaveasfilename(initialdir = path,title = "Guardar como",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            archi1=open(nombrearch, "w", encoding="utf-8")
            archi1.write(str(evetos_obtenidos))
            archi1.close()
            mb.showinfo("Información", "Los eventos fueron guardados en el archivo.")
        
    
        
    
def eventos(nsta, nlta, triggerOn, triggerOff, hInicio, hFin, tipoAlgoritmo, factorConversion):
    print("Classic STA/LTA")
    
    if nsta=="" or nlta=="" or triggerOn=="" or triggerOff=="" or factorConversion=="":
        mb.showinfo("Información", "Debe ingresar los parámetros necesarios antes de obtener los eventos")
    else:
        st = obspy.read(miArchivo.get())[0]
        
        if hInicio == "" and hFin == "" :
            t = st.stats.starttime
            trace = st
        else:
            ti=datetime.strptime(hInicio,"%H:%M" )
            tf=datetime.strptime(hFin,"%H:%M" )
            t = st.stats.starttime
            #t1 = t + 3600 * float(hInicio)
            t1 = t + (ti.hour * 60 + ti.minute) * 60
            t2 = t + (tf.hour * 60 + tf.minute) * 60
            trace = st.trim(t1,t2)
        
        trace.data = trace.data/float(factorConversion)
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
        else:
            mb.showinfo("Información", "Debe seleccionar un Algoritmo correcto")
            
        on_of = trigger_onset(cft, float(triggerOn), float(triggerOff))
        path=os.path.abspath(os.getcwd())
        on_of=on_of/df
        evetos_obtenidos=[]
        #funcion para converitr las meustras en horas minutos y segundos
        for i in range(len(on_of)):
            for j in range(len(on_of[i])):
                sec = timedelta(seconds=on_of[i][j])
                evetos_obtenidos.append(str(sec))
        print(np.array(evetos_obtenidos).reshape(len(on_of), 2))      
        nombrearch=fd.asksaveasfilename(initialdir = path ,title = "Guardar como",filetypes = (("txt files","*.txt"),("todos los archivos","*.*")))
        if nombrearch!='':
            archi1=open(nombrearch, "w", encoding="utf-8")
            archi1.write(str(np.array(evetos_obtenidos).reshape(len(on_of), 2)))
            archi1.close()
            mb.showinfo("Información", "Los eventos fueron guardados en el archivo.")
            
def actualizarVista(event):
    miAlgoritmo =lista_desplegable.get()
    if miAlgoritmo=="AR-AIC":
        parametrosTitle.grid(row=1, column=2, padx=10, pady=10, columnspan=5)
        #se eliminana los elementos de la vista
        eliminarParametros()
        #Parametros ar picker
        f1Title.grid(row=2, column=2, padx=10, pady=10)
        f2tTitle.grid(row=2, column=4, padx=10, pady=10)
        m_pTitle.grid(row=2, column=6, padx=10, pady=10)
        hInicioTitle.grid(row=2, column=8, padx=10, pady=10)
        
        lta_pTitle.grid(row=3, column=2, padx=10, pady=10)
        sta_pTitle.grid(row=3, column=4, padx=10, pady=10)
        lta_sTitle.grid(row=3, column=6, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        hFinTitle.grid(row=3, column=8, padx=10, pady=10)
        
        l_pTitle.grid(row=4, column=2, padx=10, pady=10)
        l_sTitle.grid(row=4, column=4, padx=10, pady=10)
        sta_sTitle.grid(row=4, column=6, padx=10, pady=10)
        m_sTitle.grid(row=4, column=8, padx=10, pady=10)
        
        #AR picker 
        f1Text.grid(row=2, column=3, padx=10, pady=10)
        f2Text.grid(row=2, column=5, padx=10, pady=10)
        lta_pText.grid(row=3, column=3, padx=10, pady=10)
        sta_pText.grid(row=3, column=5, padx=10, pady=10)
        lta_sText.grid(row=3, column=7, padx=10, pady=10)
        sta_sText.grid(row=4, column=7, padx=10, pady=10)
        m_pText.grid(row=2, column=7, padx=10, pady=10)
        m_sText.grid(row=4, column=9, padx=10, pady=10)
        l_pText.grid(row=4, column=3, padx=10, pady=10)
        l_sText.grid(row=4, column=5, padx=10, pady=10)
        
        horaInicio.grid(row=2, column=9)
        horaFin.grid(row=3, column=9)
        
        factorCTitle.grid(row=5, column=1, padx=10, pady=10)
        factorConversionText.grid(row=5, column=2, padx=10, pady=10)
        
        #--------------------Botones----------------
        
        # Boton para Seleccionar Archivo
        seleccionArchivoBtn.grid(row=4, column=1, padx=50, pady=10)
        # Boton Graficar Eventos seleccionarArchivo
        graficarEventosBtn.grid(row=5, column=3, padx=50, pady=10)
        

        # Boton para extraer archivo miniSeed
        obtenerMiniSeedBtn.grid(row=5, column=5, padx=50, pady=10)
        
        
                
        
    elif miAlgoritmo=="Baer- and Kradolfer-picker":
        parametrosTitle.grid(row=1, column=2, padx=10, pady=10, columnspan=5)
        #se eliminana los elementos de la vista
        eliminarParametros()
        
        #-------------Inputs------------------------
        ## Titulo de Ingresar hora fin
        tdownmaxTitle.grid(row=2, column=2, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        tupeventTitle.grid(row=2, column=4, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        thr1Title.grid(row=4, column=2, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        thr2Title.grid(row=4, column=4, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        preset_lenTitle.grid(row=2, column=6, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        p_durTitle.grid(row=3, column=6, padx=10, pady=10)
        ## Titulo de Triger On
        triggerOnTitle.grid(row=3, column=2, padx=10, pady=10)
        ## Titulo de Triger Off
        triggerOffTitle.grid(row=3, column=4, padx=10, pady=10)
        hInicioTitle.grid(row=2, column=8, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        hFinTitle.grid(row=3, column=8, padx=10, pady=10)
        
        tdownmaxText.grid(row=2, column=3)
        tupeventText.grid(row=2, column=5)
        thr1Text.grid(row=4, column=3)
        thr2Text.grid(row=4, column=5)
        preset_lenText.grid(row=2, column=7)
        p_durText.grid(row=3, column=7)
        triggerOnText.grid(row=3, column=3)
        triggerOffText.grid(row=3, column=5)

        #Hora Inicio
        #horaInicio=Entry(miFrame)
        horaInicio.grid(row=2, column=9)
        horaFin.grid(row=3, column=9)
        
        factorCTitle.grid(row=5, column=1, padx=10, pady=10)
        factorConversionText.grid(row=5, column=2, padx=10, pady=10)
        
        
        
        #--------------------Botones----------------
        
        # Boton para Seleccionar Archivo
        seleccionArchivoBtn.grid(row=4, column=1, padx=50, pady=10)
        # Boton Graficar Eventos seleccionarArchivo
        graficarEventosBtn.grid(row=5, column=3, padx=50, pady=10)
        
        # Boton Obtener Eventos
        obtenerEventosBtn.grid(row=5, column=4, padx=50, pady=10)

        # Boton para extraer archivo miniSeed
        obtenerMiniSeedBtn.grid(row=5, column=5, padx=50, pady=10)
    else:
        
        eliminarParametros()
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
        hInicioTitle.grid(row=2, column=8, padx=10, pady=10)
        ## Titulo de Ingresar hora fin
        hFinTitle.grid(row=3, column=8, padx=10, pady=10)
        
        factorCTitle.grid(row=5, column=1, padx=10, pady=10)
        factorConversionText.grid(row=5, column=2, padx=10, pady=10)
        
        
        
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
        horaInicio.grid(row=2, column=9)

        #Hora Fin
        #horaFin=Entry(miFrame)
        horaFin.grid(row=3, column=9)

        #--------------------Botones----------------
        
        # Boton para Seleccionar Archivo
        seleccionArchivoBtn.grid(row=4, column=1, padx=50, pady=10)
        # Boton Graficar Eventos seleccionarArchivo
        graficarEventosBtn.grid(row=5, column=3, padx=50, pady=10)
        
        # Boton Obtener Eventos
        obtenerEventosBtn.grid(row=5, column=4, padx=50, pady=10)

        # Boton para extraer archivo miniSeed
        obtenerMiniSeedBtn.grid(row=5, column=5, padx=50, pady=10)
        
def eliminarParametros():
    nstaText.grid_forget()
    nltaText.grid_forget()
    nstaTitle.grid_forget()
    nltaTitle.grid_forget()
    obtenerEventosBtn.grid_forget()
    tdownmaxTitle.grid_forget()
    tupeventTitle.grid_forget()
    thr1Title.grid_forget()
    thr2Title.grid_forget()
    preset_lenTitle.grid_forget()
    p_durTitle.grid_forget()
    triggerOnTitle.grid_forget()
    triggerOffTitle.grid_forget()
    hInicioTitle.grid_forget()
    hFinTitle.grid_forget()
    
    tdownmaxText.grid_forget()
    tupeventText.grid_forget()
    thr1Text.grid_forget()
    thr2Text.grid_forget()
    preset_lenText.grid_forget()
    p_durText.grid_forget()
    triggerOnText.grid_forget()
    triggerOffText.grid_forget()
    
    f1Title.grid_forget()
    f2tTitle.grid_forget()
    lta_pTitle.grid_forget()
    sta_pTitle.grid_forget()
    lta_sTitle.grid_forget()
    sta_sTitle.grid_forget()
    m_pTitle.grid_forget()
    m_sTitle.grid_forget()
    l_pTitle.grid_forget()
    l_sTitle.grid_forget()
    f1Text.grid_forget()
    f2Text.grid_forget()
    lta_pText.grid_forget()
    sta_pText.grid_forget()
    lta_sText.grid_forget()
    sta_sText.grid_forget()
    m_pText.grid_forget()
    m_sText.grid_forget()
    l_pText.grid_forget()
    l_sText.grid_forget()
    
    
        
        

#---------------------#Interfaz------------------------------------------------
raiz=Tk()

raiz.title("Red Sísmica del Austro")
raiz.attributes('-zoomed', True)

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

## Titulo de factor de conversion
factorCTitle=Label(miFrame, text="Factor de conversión:", font=(18))

#PArametros de pk baer
tdownmaxTitle=Label(miFrame, text="tdownmax:", font=(18))
tupeventTitle=Label(miFrame, text="tupevent:", font=(18))
thr1Title=Label(miFrame, text="thr1:", font=(18))
thr2Title=Label(miFrame, text="thr2:", font=(18))
preset_lenTitle=Label(miFrame, text="preset_len:", font=(18))
p_durTitle=Label(miFrame, text="p_dur:", font=(18))

#Parametros ar picker
f1Title=Label(miFrame, text="f1:", font=(18))
f2tTitle=Label(miFrame, text="f2:", font=(18))
lta_pTitle=Label(miFrame, text="lta_p:", font=(18))
sta_pTitle=Label(miFrame, text="sta_p:", font=(18))
lta_sTitle=Label(miFrame, text="lta_s:", font=(18))
sta_sTitle=Label(miFrame, text="sta_s:", font=(18))
m_pTitle=Label(miFrame, text="m_p:", font=(18))
m_sTitle=Label(miFrame, text="m_s:", font=(18))
l_pTitle=Label(miFrame, text="l_p:", font=(18))
l_sTitle=Label(miFrame, text="l_s:", font=(18))

#------------------- Lista desplegable ---------------------------------------------
lista_desplegable = ttk.Combobox(miFrame, width=25)
lista_desplegable.grid(row=2, column=1, padx=10, pady=10)

# Lista de opciones
algoritmos = ["Classic STA/LTA", "Recursive STA/LTA", "Delayed STA/LTA", "Z-detector", "Baer- and Kradolfer-picker", "AR-AIC"]
lista_desplegable['values']=algoritmos

lista_desplegable.bind("<<ComboboxSelected>>", actualizarVista)

# ---------------Inputs-----------------------------

## Nombre del archivo seleccionado
archivo=Label(miFrame, text="", font=(12))
archivo.grid(row=6, column=1, columnspan=3)

## data del archivo seleccionado
data=Label(miFrame, text="", font=(12))
data.grid(row=6, column=3, columnspan=7)

#global nstaText, nltaText, triggerOnText, triggerOffText, horaInicio, horaFin

nstaText=Entry(miFrame, width=10)
#nstaText.grid(row=2, column=3)

#NLTA input
nltaText=Entry(miFrame, width=10)
#nltaText.grid(row=2, column=5)

#Trigger On
triggerOnText=Entry(miFrame, width=10)
#triggerOnText.grid(row=3, column=3)

#Trigger Off
triggerOffText=Entry(miFrame, width=10)
#triggerOffText.grid(row=3, column=5)

#Hora Inicio
horaInicio=Entry(miFrame, width=10)
#horaInicio.grid(row=2, column=7)

#Hora Fin
horaFin=Entry(miFrame, width=10)
#horaFin.grid(row=3, column=7)

factorConversionText=Entry(miFrame, width=10)

#Pk Baer
tdownmaxText=Entry(miFrame, width=10)
tupeventText=Entry(miFrame, width=10)
thr1Text=Entry(miFrame, width=10)
thr2Text=Entry(miFrame, width=10)
preset_lenText=Entry(miFrame, width=10)
p_durText=Entry(miFrame, width=10)


#AR picker 
f1Text=Entry(miFrame, width=10)
f2Text=Entry(miFrame, width=10)
lta_pText=Entry(miFrame, width=10)
sta_pText=Entry(miFrame, width=10)
lta_sText=Entry(miFrame, width=10)
sta_sText=Entry(miFrame, width=10)
m_pText=Entry(miFrame, width=10)
m_sText=Entry(miFrame, width=10)
l_pText=Entry(miFrame, width=10)
l_sText=Entry(miFrame, width=10)


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


raiz.mainloop()