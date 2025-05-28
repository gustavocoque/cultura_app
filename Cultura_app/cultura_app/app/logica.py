
# Clase para manejar los datos de los participantes

class Participante:
    PRECIOS = {
        "Pintura": 6000,
        "Teatro": 8000,
        "Música": 10000,
        "Danza": 7000
    }
    
    def __init__(self, nombre, edad, taller, mes, clases_asistidas):
        self.nombre = nombre
        self.edad = edad
        self.taller = taller
        self.mes = mes
        self.clases_asistidas = clases_asistidas
    
    def calcular_pago(self):
        """Calcula el total pagado por el participante"""
        precio = self.PRECIOS.get(self.taller, 0)
        return precio * self.clases_asistidas
    
    def __str__(self):
        return f"{self.nombre} - {self.taller} ({self.mes})"
    
    # TODO: Agregar métodos para validar datos