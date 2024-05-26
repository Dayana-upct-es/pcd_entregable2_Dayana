from datetime import datetime
import statistics
import time
import threading
from collections import deque
import random

#R4: patron Strategy para el cálculo de los estdisticos:
class EstrategiaEstadisticas:
    def calcular(self, temperaturas):
        pass

class EstrategiaMediaDesviacion(EstrategiaEstadisticas):
    # Aplico la librer´´ía statics para obtener los cálculos necesaarios.
    def calcular(self, temperaturas):
        media = statistics.mean(temperaturas)
        desviacion = statistics.stdev(temperaturas) if len(temperaturas) > 1 else 0
        print(f"media: {media}, desviación típica: {desviacion}")
        return media, desviacion

class EstrategiaCuantiles(EstrategiaEstadisticas):
    def calcular(self, temperaturas):
        cuartil_1 = statistics.quantiles(temperaturas, n=4)[0]
        cuartil_2 = statistics.median(temperaturas)
        cuartil_3 = statistics.quantiles(temperaturas, n=4)[2]
        print(f"cuantil_1: {cuartil_1}, Mediana: {cuartil_2}, Cuantil 75: {cuartil_3}")
        return cuartil_1, cuartil_2, cuartil_3



# R3 Procesamiento de Datos: Se sigue un patrón chain of responsability.
class Manejador:
    def __init__(self, sucesor=None):
        self.sucesor = sucesor

    def manejar_solicitud(self, solicitud):
        if self.sucesor:
            self.sucesor.manejar_solicitud(solicitud)

class ManejadorEstadisticos(Manejador):
    def __init__(self, estrategia, sucesor=None):
        super().__init__(sucesor)
        self.estrategia = estrategia

    def manejar_solicitud(self, solicitud):
        ahora = time.time()#registro el tiempo

        #Hallo las temperaturas sleccionando con un filtro para quedarme con las que menciona el enunciado
        temperaturas = list(map(lambda x: x[1], filter(lambda x: ahora - x[0] <= 60, solicitud.temperaturas))) 
        
        if temperaturas:
            solicitud.estadisticas = self.estrategia.calcular(temperaturas)
        super().manejar_solicitud(solicitud)

class ManejadorUmbral(Manejador):
    def __init__(self, umbral, sucesor=None):
        super().__init__(sucesor)
        self.umbral = umbral

    def manejar_solicitud(self, solicitud):
        if solicitud.temperatura_actual > self.umbral:
            print(f"La temperatura actual {solicitud.temperatura_actual} está por encima del umbral de {self.umbral} grados.")
        else:
            print(f"La temperatura actual {solicitud.temperatura_actual} está por debajo del umbral de {self.umbral} grados.")
        super().manejar_solicitud(solicitud)

class ManejadorTemperatura(Manejador):
    def manejar_solicitud(self, solicitud):
        ahora = time.time() #para tener el tiempo registrado
        temperaturas = list(map(lambda x: x[1], filter(lambda x: ahora - x[0] <= 60, solicitud.temperaturas)))
        if temperaturas and (solicitud.temperatura_actual - temperaturas[0] >= 10):
            print(f"La temperatura ha aumentado más de 10 grados en los últimos 30 segundos.")
        
        else:
            print(f"No ha habido un aumento significativo de temperatura en los últimos 30 segundos.")
        super().manejar_solicitud(solicitud)

class SolicitudTemperatura:
    def __init__(self, temperaturas, temperatura_actual):
        self.temperaturas = temperaturas  # son tuplas del tipo (timestamp, temperatura)
        self.temperatura_actual = temperatura_actual
        self.estadisticas = None



#Una clase Sistema que se encargará de la gestión completa (Sigleton):
class Sistema:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.initialized = False
        self.temperaturas = deque()
        self.cadena_manejadores = None

    def obtener_instancia():
        if not Sistema._instance:
            with Sistema._lock:
                if not Sistema._instance:
                    Sistema._instance = Sistema()
        return Sistema._instance

    def set_cadena_manejadores(self, cadena):
        self.cadena_manejadores = cadena

    def agregar_temperatura(self, temperatura):
        self.temperaturas.append((time.time(), temperatura))
        solicitud = SolicitudTemperatura(self.temperaturas, temperatura)
        if self.cadena_manejadores:
            self.cadena_manejadores.manejar_solicitud(solicitud)



