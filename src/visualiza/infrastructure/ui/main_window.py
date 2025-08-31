import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading

from src.visualiza.application.services.user_service import UserApplicationService
from src.visualiza.infrastructure.services.voice_service import VoiceService
from src.visualiza.infrastructure.services.vision_service import VisionService

class MainWindow:
    def __init__(
        self,
        user_service: UserApplicationService,
        voice_service: VoiceService,
        vision_service: VisionService,
    ):
        self.user_service = user_service
        self.voice_service = voice_service
        self.vision_service = vision_service

        self.window = tk.Tk()
        self.window.title("Visualiza - Asistente Visual")
        self.window.geometry("800x600")

        self.video_panel = None
        self.detection_running = False

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        title = ttk.Label(main_frame, text="Bienvenido a Visualiza", font=("Arial", 24))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Button(main_frame, text="Registrar Datos", command=self.open_registration_window).grid(row=1, column=0, pady=10, padx=5)
        ttk.Button(main_frame, text="Iniciar Detección", command=self.start_detection_thread).grid(row=1, column=1, pady=10, padx=5)

        self.info_text = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
        self.info_text.grid(row=2, column=0, columnspan=2, pady=10)
        self.update_user_display()

    def open_registration_window(self):
        reg_window = tk.Toplevel(self.window)
        reg_window.title("Registro de Usuario")
        reg_window.geometry("400x250")

        fields = {"Name": "Nombre", "Gender": "Género", "Age": "Edad", "Marital Status": "Estado Civil"}
        self.entries = {}

        for i, (field_en, field_es) in enumerate(fields.items()):
            ttk.Label(reg_window, text=field_es).grid(row=i, column=0, pady=5, padx=5, sticky="w")
            entry = ttk.Entry(reg_window)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[field_en.lower().replace(" ", "_")] = entry

            # Voice input button
            voice_btn = ttk.Button(reg_window, text="🎤", width=3, command=lambda f=field_es, e=entry: self.voice_input(f, e))
            voice_btn.grid(row=i, column=2)

        save_btn = ttk.Button(reg_window, text="Guardar", command=lambda: self.save_user_data(reg_window))
        save_btn.grid(row=len(fields), column=0, columnspan=3, pady=20)

    def voice_input(self, field_name: str, entry: ttk.Entry):
        self.voice_service.speak(f"Por favor, diga su {field_name}")
        response = self.voice_service.listen_and_transcribe()
        if response:
            entry.delete(0, tk.END)
            entry.insert(0, response)

    def save_user_data(self, window_to_close):
        try:
            data = {key: entry.get() for key, entry in self.entries.items()}
            age = int(data["age"])

            self.user_service.register_user(
                name=data["name"],
                age=age,
                gender=data["gender"],
                marital_status=data["marital_status"]
            )
            self.update_user_display()
            self.voice_service.speak("Datos guardados correctamente.")
            window_to_close.destroy()
        except ValueError:
            messagebox.showerror("Error de Validación", "La edad debe ser un número válido.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def update_user_display(self):
        user = self.user_service.get_user()
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        if user:
            self.info_text.insert(tk.END, "Datos del Usuario:\n\n")
            self.info_text.insert(tk.END, f"Nombre: {user.name}\n")
            self.info_text.insert(tk.END, f"Edad: {user.age}\n")
            self.info_text.insert(tk.END, f"Género: {user.gender}\n")
            self.info_text.insert(tk.END, f"Estado Civil: {user.marital_status}\n")
        else:
            self.info_text.insert(tk.END, "No hay datos de usuario registrados.")
        self.info_text.config(state=tk.DISABLED)

    def start_detection_thread(self):
        if self.user_service.get_user() is None:
            messagebox.showwarning("Advertencia", "Por favor, registre sus datos primero.")
            return

        if self.detection_running:
            self.stop_detection()
        else:
            self.detection_running = True
            self.thread = threading.Thread(target=self.run_detection_loop, daemon=True)
            self.thread.start()
            self.voice_service.speak("Iniciando detección de objetos.")

    def stop_detection(self):
        self.detection_running = False
        self.voice_service.speak("Deteniendo detección.")
        if self.video_panel and self.video_panel.winfo_exists():
            self.video_panel.destroy()
        self.video_panel = None


    def run_detection_loop(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error de Cámara", "No se pudo acceder a la cámara.")
            self.detection_running = False
            return

        if self.video_panel is None or not self.video_panel.winfo_exists():
            self.video_panel = tk.Toplevel(self.window)
            self.video_panel.title("Detección en Vivo")
            self.video_label = ttk.Label(self.video_panel)
            self.video_label.pack()
            self.video_panel.protocol("WM_DELETE_WINDOW", self.stop_detection)

        last_spoken_objects = set()

        while self.detection_running:
            ret, frame = cap.read()
            if not ret:
                break

            annotated_frame, detected_objects = self.vision_service.detect_objects(frame)

            # Speak new objects
            new_objects = set(detected_objects) - last_spoken_objects
            if new_objects:
                self.voice_service.speak(f"Veo: {', '.join(new_objects)}")
                last_spoken_objects.update(new_objects)

            # Update GUI
            img = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img_pil)

            if self.video_label and self.video_label.winfo_exists():
                self.video_label.config(image=img_tk)
                self.video_label.image = img_tk

        cap.release()

    def start(self):
        self.voice_service.speak("Bienvenido a Visualiza")
        self.window.mainloop()