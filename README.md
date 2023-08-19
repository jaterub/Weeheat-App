# Data Sciece Desafío de Tripulaciones
![img](./img/Step%20By%20Step%20Decluttering%20Process%20Graph%20Instagram%20Post%20(1).jpg)![readme img](https://github.com/jaterub/Weeheat-App/assets/117780949/29328c7b-1950-4011-926a-0610e74dbc7c)


# El reto del desafío de tripulaciones trataba de dar una solución a los problemas que puede atravesar un turista que viene a Madrid en épocas y momentos de mucho calor.  

## 1. Recopilación de datos. 
* Para ello primero debíamos de recopilar datos de temperaturas y de servicios que pueden ser utilizados por turistas en este tipo de situaciones de mucho calor.
Toda la información recopilada pertenece a la [API del Ayuntamiento de Madrid](https://datos.madrid.es/portal/site/egob/menuitem.214413fe61bdd68a53318ba0a8a409a0/?vgnextoid=b07e0f7c5ff9e510VgnVCM1000008a4a900aRCRD&vgnextchannel=b07e0f7c5ff9e510VgnVCM1000008a4a900aRCRD&vgnextfmt=default).
* Todos los datos recopilados se encuentran en la carpeta de [data](https://github.com/Kuja182/desafio_data/tree/main/data) donde podrá ver tanto los datos obtenidos de las [temperaturas](https://github.com/Kuja182/desafio_data/tree/main/data/temp_ok) ya tratados en diferentes estaciones meteorológicas como los datos de los diferentes servicios del [turista](https://github.com/Kuja182/desafio_data/tree/main/data/madrid).

## 2. Preparación de datos y envío.  
* Transformación de los datos obtenidos anteriormente para obtener un análisis utilizando Python y otras librerias de representaciones como Matplotlib o seaborn entre otras.
* En la siguiente [carpeta](https://github.com/Kuja182/desafio_data/tree/main/notebooks) obtendrá todas la información sobre los notebook realizados para el tratamiento de los datos y su posterior conversión a .json para poder enviar al departamento de FullStack.

## 3. Entrenamiento de Modelos.
*  En este [pdf](https://github.com/Kuja182/desafio_data/blob/main/Informes/MODELO%20DE%20PREDICI%C3%93N%20DE%20TEMPERATURAS%20API%20DEPOYMENT.pdf) obtendrá un breve resumen del entrenamiento del modelo de temperaturas, si quiere obtener un documento más extenso, consulte este [enlace](https://github.com/Kuja182/desafio_data/blob/main/notebooks/EDA_ML_tiempo_diario.ipynb).
* También además del modelo de temperaturas está implementado [varios](https://github.com/Kuja182/desafio_data/blob/main/notebooks/Turistas_internacionales.ipynb) modelos de turismo y de su afluecia dependiendo de su procedencia que van a tener gran relevancia en posibles acciones del departamento de marketing en el futuro.

## 4. Despliegue de la API.
Para ello planeamos tener tres endpoints en la misma [API](https://github.com/Kuja182/desafio_data/tree/main/API_temperaturas) para que se pudieran nutrir de ella el equipo de FullStack.  
En un principio iba a estar alojada en un servidor de AWS, pero después de muchos error y problemas con la página lo decidimos lanzarla en [pythonanywhere](https://www.pythonanywhere.com/).
* Predicción de temperaturas:  
v1/predict - Con ella accedemos con una entrada de año,mes,día y hora a una futura predicción de la temperatura, la cual elegirá el turista dentro de la APP.
* Temperatura actual:  
v1/temp_actual - Con ella obtendremos la temperatura actual obtenida de la API de [OpenWeatherMap](https://openweathermap.org/api).
* Eventos en 10 días:  
v1/eventos - Con ella obtendremos los eventos que transcurren en el momento que esta viendo la API durante los proximos 10 días.  

El equipo de Data Science esta formado por:  
[Javier Tejero](https://github.com/jaterub)  
[Javier Fernandez](https://github.com/jaferdy)  
[Santiago Valencia](https://github.com/Kuja182)  
