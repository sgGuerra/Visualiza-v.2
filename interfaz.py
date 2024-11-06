import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from app.model import AsistenteVisualiza
from app.datos_usuario import SolicitudDatos
from app.reconocer_objetos import DetectorObjetos


class InterfazVisualiza:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Visualiza - Asistente Visual")
        self.ventana.geometry("800x600")

        self.asistente = AsistenteVisualiza()
        self.solicitud = SolicitudDatos()
        self.detector = DetectorObjetos()

        self.crear_widgets()

    def crear_widgets(self):
        # Frame principal
        self.frame_principal = ttk.Frame(self.ventana, padding="10")
        self.frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título
        titulo = ttk.Label(self.frame_principal,
                           text="Bienvenido a Visualiza",
                           font=("Arial", 24))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # Botones principales
        ttk.Button(self.frame_principal,
                   text="Registrar Datos",
                   command=self.iniciar_registro).grid(row=1, column=0, pady=10, padx=5)

        ttk.Button(self.frame_principal,
                   text="Iniciar Detección",
                   command=self.iniciar_deteccion).grid(row=1, column=1, pady=10, padx=5)

        # Área de información
        self.info_text = tk.Text(self.frame_principal, height=10, width=50)
        self.info_text.grid(row=2, column=0, columnspan=2, pady=10)

    def iniciar_registro(self):
        self.ventana_registro = tk.Toplevel(self.ventana)
        self.ventana_registro.title("Registro de Usuario")
        self.ventana_registro.geometry("600x400")

        # Campos de registro
        campos = ["Nombre", "Género", "Edad", "Estado Civil"]
        self.entradas = {}

        for i, campo in enumerate(campos):
            ttk.Label(self.ventana_registro, text=campo).grid(row=i, column=0, pady=5, padx=5)
            entrada = ttk.Entry(self.ventana_registro)
            entrada.grid(row=i, column=1, pady=5, padx=5)
            self.entradas[campo] = entrada

            # Botón para entrada por voz
            ttk.Button(self.ventana_registro,
                       text="🎤",
                       command=lambda c=campo: self.entrada_por_voz(c)).grid(row=i, column=2)

        ttk.Button(self.ventana_registro,
                   text="Guardar",
                   command=self.guardar_datos).grid(row=len(campos), column=0, columnspan=3, pady=20)

    def entrada_por_voz(self, campo):
        self.asistente.hablar(f"Por favor, diga su {campo}")
        respuesta = self.asistente.obtener_respuesta()
        if respuesta:
            self.entradas[campo].delete(0, tk.END)
            self.entradas[campo].insert(0, respuesta)

    def guardar_datos(self):
        datos = {campo: entrada.get() for campo, entrada in self.entradas.items()}
        # Aquí puedes agregar la validación de datos
        self.solicitud.datos_usuario = datos
        self.mostrar_datos_guardados()
        self.ventana_registro.destroy()

    def mostrar_datos_guardados(self):
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, "Datos guardados:\n\n")
        for campo, valor in self.solicitud.datos_usuario.items():
            self.info_text.insert(tk.END, f"{campo}: {valor}\n")

    def iniciar_deteccion(self):
        if not self.solicitud.datos_usuario:
            messagebox.showwarning("Advertencia", "Por favor, registre sus datos primero")
            return

        self.ventana.withdraw()  # Ocultar ventana principal
        self.detector.iniciar_deteccion()
        self.ventana.deiconify()  # Mostrar ventana principal

    def iniciar(self):
        self.asistente.hablar("Bienvenido a Visualiza")
        self.ventana.mainloop()


def interfaz():
    return None