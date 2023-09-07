import cv2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading

# Función para seleccionar un archivo de video
def seleccionar_archivo():
    archivo_video = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi *.mkv *.mov")])
    entrada_nombre_video.delete(0, tk.END)
    entrada_nombre_video.insert(0, archivo_video)

# Función para seleccionar una carpeta de destino
def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    entrada_carpeta.delete(0, tk.END)
    entrada_carpeta.insert(0, carpeta)

# Función para procesar el video en un hilo separado
def procesar_video():
    nombre_archivo_video = entrada_nombre_video.get()
    carpeta_destino = entrada_carpeta.get()

    if not os.path.isfile(nombre_archivo_video):
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "El archivo de video no existe.")
        return

    if not carpeta_destino:
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, "Debes seleccionar una carpeta de destino.")
        return

    os.makedirs(carpeta_destino, exist_ok=True)

    def procesar():
        cap = cv2.VideoCapture(nombre_archivo_video)

        if not cap.isOpened():
            resultado.delete(1.0, tk.END)
            resultado.insert(tk.END, "Error al abrir el archivo de video.")
            return

        frame_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            nombre_archivo_frame = os.path.join(carpeta_destino, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(nombre_archivo_frame, frame)

            frame_count += 1

            progreso.config(text=f'Frame {frame_count:04d}')

        cap.release()
        cv2.destroyAllWindows()

        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, f'Se han guardado {frame_count} frames en la carpeta "{carpeta_destino}".')

    # Iniciar un hilo para el procesamiento del video
    thread = threading.Thread(target=procesar)
    thread.start()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Extracción de Frames de Video")
ventana.configure(bg="#222")  # Fondo oscuro

# Estilo personalizado para los elementos de la interfaz gráfica
estilo = ttk.Style()
estilo.configure("TButton", foreground="#000", background="#333")  # Texto negro, fondo oscuro
estilo.configure("TLabel", foreground="#fff", background="#222")  # Texto blanco, fondo oscuro
estilo.configure("TText", foreground="#fff", background="#222")  # Texto blanco, fondo oscuro

# Crear elementos de la interfaz
etiqueta_nombre_video = ttk.Label(ventana, text="Archivo de Video:")
etiqueta_nombre_video.pack(pady=10)

entrada_nombre_video = ttk.Entry(ventana, width=40)
entrada_nombre_video.pack()

boton_seleccionar_video = ttk.Button(ventana, text="Seleccionar Archivo", command=seleccionar_archivo)
boton_seleccionar_video.pack(pady=10)

etiqueta_carpeta_destino = ttk.Label(ventana, text="Carpeta de Destino:")
etiqueta_carpeta_destino.pack(pady=10)

entrada_carpeta = ttk.Entry(ventana, width=40)
entrada_carpeta.pack()

boton_seleccionar_carpeta = ttk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar_carpeta.pack(pady=10)

boton_procesar = ttk.Button(ventana, text="Procesar Video", command=procesar_video)
boton_procesar.pack(pady=20)

progreso = ttk.Label(ventana, text="Frame 0000", foreground="#fff")  # Texto blanco
progreso.pack()

resultado = tk.Text(ventana, wrap=tk.WORD, height=5, width=50, foreground="#fff", background="#222")  # Texto blanco, fondo oscuro
resultado.pack()

ventana.mainloop()
