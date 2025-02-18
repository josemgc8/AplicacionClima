import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO

#Configuración de la API
API = "a1c009aa929da9bca776f20176cffb07"
URL = "http://api.openweathermap.org/data/2.5/weather"

#Funcion para obtener el clima
def obtener_clima():
    #Obtener el nombre de la ciudad ingresada por el usuario
    ciudad = entrada_ciudad.get()
    if not ciudad:
        messagebox.showerror("Error", "Por favor ingrese una ciudad")
        return
    
    #Parametros para la solicitud de la API de OpenWeatherMap
    parametros ={"q": ciudad, "appid": API, "units": "metric", "lang": "es"}
    respuesta = requests.get(URL, params=parametros)

    #Verificar si la respuesta de la API fue exitosa
    if respuesta.status_code == 200:
        datos = respuesta.json()

        #Extraer datos del JSON recibido
        temperatura = datos["main"]["temp"]
        humedad = datos["main"]["humidity"]
        descripcion = datos["weather"][0]["description"].capitalize()
        icono_codigo = datos["weather"][0]["icon"]

        #Actualizar la etiqueta con los datos del clima
        etiqueta_resultado.config(text=f"{descripcion}\nTemperatura: {temperatura}°C\nHumedad: {humedad}%")

        #Construir la URL para obtener la imagen del icono del clima
        url_icono = f"http://openweathermap.org/img/wn/{icono_codigo}@2x.png"

        #Descargar la imagen del icono y mostrarla en la interfaz
        imagen_respuesta = requests.get(url_icono)
        imagen_bytes = Image.open(BytesIO(imagen_respuesta.content))
        imagen_tk = ImageTk.PhotoImage(imagen_bytes)
        etiqueta_icono.config(image=imagen_tk)
        etiqueta_icono.image = imagen_tk
    else:
        messagebox.showerror("Error", "No se pudo obtener el clima")

#Configuracion de la interfaz gráfica con tkinter
ventana = tk.Tk()
ventana.title("Aplicación del Clima")
ventana.geometry("300x400")


#Etiqueta y campo de entrada para la ciudad
etiqueta_ciudad = tk.Label(ventana, text="Ingrese una ciudad:")
etiqueta_ciudad.pack()

entrada_ciudad = tk.Entry(ventana)
entrada_ciudad.pack()

#Boton para buscar el clima
boton_buscar = tk.Button(ventana, text="Buscar clima", command=obtener_clima)
boton_buscar.pack()

#Etiqueta para mostrar el icono del clima
etiqueta_icono = tk.Label(ventana)
etiqueta_icono.pack()

#Etiqueta para mostrar la informacion del clima
etiqueta_resultado = tk.Label(ventana, font=("Arial", 12))
etiqueta_resultado.pack()

#print("La aplicación se está ejecutando correctamente.")

tk.mainloop()
