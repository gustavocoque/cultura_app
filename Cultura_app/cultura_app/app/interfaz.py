
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from logica import Participante
from analisis import Analisis

class AppTalleres:
    def __init__(self, root):
        self.root = root
        self.root.title("Casa de la Cultura - Gestión de Talleres")
        self.root.geometry("800x600")
        
        # Variable para almacenar participantes
        self.participantes = []
        
        # Cargar datos existentes si hay
        self.cargar_datos()
        
        # Crear widgets
        self.crear_widgets()
        
        # TODO: Agregar validación de campos más robusta
    
    def crear_widgets(self):
        """Crea y organiza los elementos de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de registro
        reg_frame = ttk.LabelFrame(main_frame, text="Registro de Participante", padding="10")
        reg_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Campos de entrada
        ttk.Label(reg_frame, text="Nombre:").grid(row=0, column=0, sticky="w")
        self.nombre_entry = ttk.Entry(reg_frame, width=30)
        self.nombre_entry.grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(reg_frame, text="Edad:").grid(row=1, column=0, sticky="w")
        self.edad_entry = ttk.Entry(reg_frame, width=10)
        self.edad_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(reg_frame, text="Taller:").grid(row=2, column=0, sticky="w")
        self.taller_combo = ttk.Combobox(reg_frame, values=["Pintura", "Teatro", "Música", "Danza"])
        self.taller_combo.grid(row=2, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(reg_frame, text="Mes:").grid(row=3, column=0, sticky="w")
        self.mes_combo = ttk.Combobox(reg_frame, values=[
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.mes_combo.grid(row=3, column=1, padx=5, pady=2, sticky="w")
        
        ttk.Label(reg_frame, text="Clases asistidas:").grid(row=4, column=0, sticky="w")
        self.clases_entry = ttk.Entry(reg_frame, width=10)
        self.clases_entry.grid(row=4, column=1, padx=5, pady=2, sticky="w")
        
        # Botones de acción
        btn_frame = ttk.Frame(reg_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Registrar", command=self.registrar_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Modificar", command=self.modificar_participante).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_participante).pack(side=tk.LEFT, padx=5)
        
        # Frame de visualización
        vis_frame = ttk.LabelFrame(main_frame, text="Visualización de Datos", padding="10")
        vis_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Tabla para mostrar participantes
        self.tabla = ttk.Treeview(vis_frame, columns=("Nombre", "Edad", "Taller", "Mes", "Clases", "Total"), show="headings")
        self.tabla.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        for col in self.tabla["columns"]:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100, anchor=tk.CENTER)
        
        # Botones de reportes
        report_frame = ttk.Frame(main_frame)
        report_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        ttk.Button(report_frame, text="Mostrar Todos", command=self.mostrar_todos).pack(side=tk.LEFT, padx=5)
        ttk.Button(report_frame, text="Generar Reportes", command=self.generar_reportes).pack(side=tk.LEFT, padx=5)
        
        # Configurar expansión de filas/columnas
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=3)
        main_frame.columnconfigure(0, weight=1)
    
    def cargar_datos(self):
        """Intenta cargar datos desde archivo"""
        try:
            df = pd.read_csv("datos/participantes.csv")
            for _, row in df.iterrows():
                participante = Participante(
                    row["Nombre"], row["Edad"], row["Taller"],
                    row["Mes"], row["Clases"]
                )
                self.participantes.append(participante)
        except FileNotFoundError:
            print("No se encontró archivo de datos, empezando con lista vacía")
        except Exception as e:
            print(f"Error al cargar datos: {e}")
    
    def guardar_datos(self):
        """Guarda los datos en archivo CSV"""
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
        
        df = pd.DataFrame(datos)
        df.to_csv("datos/participantes.csv", index=False)
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.nombre_entry.delete(0, tk.END)
        self.edad_entry.delete(0, tk.END)
        self.taller_combo.set("")
        self.mes_combo.set("")
        self.clases_entry.delete(0, tk.END)
    
    def registrar_participante(self):
        """Registra un nuevo participante"""
        try:
            nombre = self.nombre_entry.get().strip()
            edad = int(self.edad_entry.get())
            taller = self.taller_combo.get()
            mes = self.mes_combo.get()
            clases = int(self.clases_entry.get())
            
            if not nombre or not taller or not mes:
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos")
                return
            
            participante = Participante(nombre, edad, taller, mes, clases)
            self.participantes.append(participante)
            
            self.guardar_datos()
            self.limpiar_campos()
            messagebox.showinfo("Éxito", "Participante registrado correctamente")
            
        except ValueError:
            messagebox.showerror("Error", "Edad y clases asistidas deben ser números")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")
    
    def modificar_participante(self):
        """Modifica los datos de un participante existente"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor seleccione un participante")
            return
        
        item = self.tabla.item(seleccion[0])
        nombre = item["values"][0]
        
        # Buscar participante
        participante = next((p for p in self.participantes if p.nombre == nombre), None)
        if not participante:
            messagebox.showerror("Error", "Participante no encontrado")
            return
        
        # Actualizar datos
        try:
            participante.edad = int(self.edad_entry.get() or participante.edad)
            participante.taller = self.taller_combo.get() or participante.taller
            participante.mes = self.mes_combo.get() or participante.mes
            participante.clases_asistidas = int(self.clases_entry.get() or participante.clases_asistidas)
            
            self.guardar_datos()
            messagebox.showinfo("Éxito", "Participante modificado correctamente")
            self.mostrar_todos()
            
        except ValueError:
            messagebox.showerror("Error", "Edad y clases asistidas deben ser números")
    
    def eliminar_participante(self):
        """Elimina un participante seleccionado"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Selección vacía", "Por favor seleccione un participante")
            return
        
        item = self.tabla.item(seleccion[0])
        nombre = item["values"][0]
        
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar a {nombre}?")
        if confirmar:
            self.participantes = [p for p in self.participantes if p.nombre != nombre]
            self.guardar_datos()
            self.mostrar_todos()
            messagebox.showinfo("Éxito", "Participante eliminado correctamente")
    
    def mostrar_todos(self):
        """Muestra todos los participantes en la tabla"""
        self.tabla.delete(*self.tabla.get_children())
        
        for p in self.participantes:
            self.tabla.insert("", tk.END, values=(
                p.nombre, p.edad, p.taller, p.mes, 
                p.clases_asistidas, p.calcular_pago()
            ))
    
    def generar_reportes(self):
        """Genera reportes estadísticos"""
        if not self.participantes:
            messagebox.showwarning("Datos vacíos", "No hay participantes registrados")
            return
        
        analisis = Analisis(self.participantes)
        analisis.generar_reportes()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppTalleres(root)
    root.mainloop()