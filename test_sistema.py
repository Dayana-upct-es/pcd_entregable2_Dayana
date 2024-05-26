import pytest
from datetime import datetime
from entregable_2 import *


def test_calculo_media_desviacion():
    estrategia = EstrategiaMediaDesviacion()
    temperaturas = [19, 20, 3, 24, 25]
    media, desviacion = estrategia.calcular(temperaturas)
    assert round(media, 4) == round(statistics.mean(temperaturas), 4)
    assert round(desviacion, 4) == round(statistics.stdev(temperaturas), 4)

def test_calculo_cuantiles():
    estrategia = EstrategiaCuantiles()
    temperaturas = [20, 40, 10, 22, 19]
    cuantil_1, mediana, cuantil_75 = estrategia.calcular(temperaturas)
    cuartiles = statistics.quantiles(temperaturas, n=4)
    assert cuantil_1 == cuartiles[0]
    assert mediana == statistics.median(temperaturas)
    assert cuantil_75 == cuartiles[2]

def test_manejador_umbral(capfd):
    manejador = ManejadorUmbral(30)
    solicitud1 = SolicitudTemperatura([(time.time(), 32)], 32)
    solicitud2 = SolicitudTemperatura([(time.time(), 28)], 28)
    manejador.manejar_solicitud(solicitud1)
    manejador.manejar_solicitud(solicitud2)
    out, err = capfd.readouterr()
    assert "La temperatura actual 32 está por encima del umbral de 30 grados." in out
    assert "La temperatura actual 28 está por debajo del umbral de 30 grados." in out


def test_manejador_temperatura(capfd):
    manejador = ManejadorTemperatura()
    solicitud1 = SolicitudTemperatura([(930, 22), (1000, 25)], 25)
    manejador.manejar_solicitud(solicitud1)
    out, _ = capfd.readouterr()
    assert "No ha habido un aumento significativo de temperatura en los últimos 30 segundos." in out

import time

def test_manejador_temperatura2(capfd):
    manejador = ManejadorTemperatura()
    tiempo_actual = time.time()
    solicitud1 = SolicitudTemperatura([(tiempo_actual - 20, 10), (tiempo_actual, 20)], 40)
    manejador.manejar_solicitud(solicitud1)
    out, _ = capfd.readouterr()
    assert "La temperatura ha aumentado más de 10 grados en los últimos 30 segundos." in out


