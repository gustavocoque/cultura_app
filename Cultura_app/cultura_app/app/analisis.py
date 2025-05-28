
# Módulo para análisis de datos y generación de gráficos
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Analisis:
    def __init__(self, participantes):
        self.participantes = participantes
    
    def generar_dataframe(self):
        """Convierte la lista de participantes a DataFrame"""
        datos = []
        for p in self.participantes:
            datos.append({
                "Nombre": p.nombre,
                "Edad": p.edad,
                "Taller": p.taller,
                "Mes": p.mes,
                "Clases": p.clases_asistidas,
                "Total": p.calcular_pago()
            })
        return pd.DataFrame(datos)
    
    def generar_reportes(self):
        """Genera todos los reportes y gráficos"""
        df = self.generar_dataframe()
        
        # Ventana para reportes
        report_window = tk.Toplevel()
        report_window.title("Reportes Estadísticos")
        report_window.geometry("1000x800")
        
        # Frame para gráficos
        graph_frame = tk.Frame(report_window)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto con estadísticas
        stats_text = self.obtener_estadisticas(df)
        tk.Label(report_window, text=stats_text).pack(pady=10)
        
        # Gráfico de barras (participantes por taller)
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        df["Taller"].value_counts().plot(kind="bar", ax=ax1, color="skyblue")
        ax1.set_title("Participantes por Taller")
        ax1.set_xlabel("Taller")
        ax1.set_ylabel("Cantidad")
        
        canvas1 = FigureCanvasTkAgg(fig1, master=graph_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Histograma de edades
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        df["Edad"].plot(kind="hist", ax=ax2, bins=10, color="lightgreen")
        ax2.set_title("Distribución de Edades")
        ax2.set_xlabel("Edad")
        ax2.set_ylabel("Frecuencia")
        
        canvas2 = FigureCanvasTkAgg(fig2, master=graph_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Gráfico circular (distribución por taller)
        fig3, ax3 = plt.subplots(figsize=(6, 6))
        df["Taller"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax3)
        ax3.set_title("Distribución por Taller")
        ax3.set_ylabel("")  # Eliminar etiqueta 'None'
        
        canvas3 = FigureCanvasTkAgg(fig3, master=graph_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def obtener_estadisticas(self, df):
        """Genera texto con estadísticas resumidas"""
        total_participantes = len(df)
        datos_incompletos = df.isnull().sum().sum()
        
        # Promedio de pagos por taller
        promedios = df.groupby("Taller")["Total"].mean()
        
        # Taller más popular
        taller_popular = df["Taller"].mode()[0]
        
        # Participante que más pagó
        max_pago = df["Total"].max()
        participante_max = df[df["Total"] == max_pago].iloc[0]["Nombre"]
        
        stats = f"""s
        ESTADÍSTICAS:
        - Total participantes: {total_participantes}
        - Datos incompletos/nulos: {datos_incompletos}
        
        PROMEDIO DE PAGOS POR TALLER:
        {promedios.to_string()}
        
        - Taller con más participantes: {taller_popular}
        - Participante con mayor pago: {participante_max} (${max_pago:,})
        """
        
        return stats