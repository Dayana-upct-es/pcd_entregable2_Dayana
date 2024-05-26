from entregable_2 import *

# Para la prueba utilizaré la libreria random con el fin de crear datos aleatorios, este archivo se irá ejecutando
# infinitamente hasta que lo pares:

sistema = Sistema.obtener_instancia()

# Configuramos la cadena de manejadores
estrategia = EstrategiaMediaDesviacion()
cadena_manejadores = ManejadorEstadisticos(estrategia,
                                            sucesor=ManejadorUmbral(30,
                                            sucesor=ManejadorTemperatura()))
sistema.set_cadena_manejadores(cadena_manejadores)

# Recolectamos y procesamos datos
while True:
    temperatura = random.uniform(15, 35)
    sistema.agregar_temperatura(temperatura)
    time.sleep(5)