# RSADE
 Herramienta para el análisis de eventos sísmicos empleando diferentes algoritmos de detección
 
 <p>
    <img src="https://res.cloudinary.com/dzgd10ssq/image/upload/v1609543282/tesis/madzogzsxzhg2gzwsfgd.png" width="300"/ hspace="5"> 
</p>

# Comenzando 🚀

Estas instrucciones te permitirán obtener una copia de la aplicacion para propósitos de desarrollo y pruebas.



## Pre-requisitos 📋

Que librerias necesitas para el funcionamiento de la aplicación
- [ObsPy](https://github.com/obspy/obspy/wiki "ObsPy")
- [tkinter](https://docs.python.org/es/3/library/tkinter.html#module-tkinter "tkinter")
- [matplotlib](https://matplotlib.org/ "matplotlib")
- [numpy](https://numpy.org/ "numpy")

## Ejecución

Para ejecutar la herrmaienta, en la terminal colocar el siguiente comando:

```
python RSADE.py
```
  
## Funcionamiento
Para mayor informacion puede consultar el [manual de usuario](https://github.com/alvaroarmijos/RSADE/blob/main/Manual%20de%20usuario.pdf "manual de usuario")

Esta herramienta sirve para diferentes algoritmos disponibles en [ObsPy](https://docs.obspy.org/tutorial/code_snippets/trigger_tutorial.html "obspy")
  
 - Classic STA/LTA, Recursive STA/LTA, Delayed STA/LTA, Z-detector. Para estos algoritmo se tiene la interfaz que se muestra a continuación. Los parámetros que se requiere ingresar se pueden consultar en la siguiente  [documentación](https://docs.obspy.org/packages/autogen/obspy.signal.trigger.classic_sta_lta.html#obspy.signal.trigger.classic_sta_lta "documentación")
 <p>
    <img src="https://res.cloudinary.com/dzgd10ssq/image/upload/v1609543282/tesis/madzogzsxzhg2gzwsfgd.png" width="600"/ hspace="5"> 
 </p>
 
 - P-picker routine by M. Baer, Schweizer Erdbebendienst. Para este algoritmo se tiene la siguiente interfaz. Los parámetros necesarios se pueden consultar en la siguiente [documentación](https://docs.obspy.org/packages/autogen/obspy.signal.trigger.pk_baer.html#obspy.signal.trigger.pk_baer "documentación") 

 <p>
     <img src="https://res.cloudinary.com/dzgd10ssq/image/upload/v1609543282/tesis/kjaeot8niqhsbuhyvoxf.png" width="600"/ hspace="5"> 
 </p>

- Pick P and S arrivals with an AR-AIC + STA/LTA algorithm. Para este algoritmo se tiene  la siguiente interfaz. Los parámetros necesarios se pueden consultar en la siguiente [documentación](https://docs.obspy.org/packages/autogen/obspy.signal.trigger.ar_pick.html#obspy.signal.trigger.ar_pick "documentación") 
 <p>
     <img src="https://res.cloudinary.com/dzgd10ssq/image/upload/v1609543282/tesis/xc6itwca6ibfvbxyep4w.png" width="600"/ hspace="5"> 
 </p>
  
  # Construido con 🛠️
  - [ObsPy](https://github.com/obspy/obspy/wiki "ObsPy")
  - [tkinter](https://docs.python.org/es/3/library/tkinter.html#module-tkinter "tkinter")
  - [matplotlib](https://matplotlib.org/ "matplotlib")
  - [numpy](https://numpy.org/ "numpy")
