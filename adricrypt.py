#!/usr/bin/env python3

from cryptography.fernet import Fernet
import base64
import hashlib
import signal

import os # Limpiar pantalla 
import platform # Limpiar pantalla

import sys # Animación
import time # Animación
import itertools # Animación

from colorama import init, Fore, Style # Animaciones
from tqdm import tqdm # Animaciones

import tty
import termios
import getpass
import tkinter as tk
import threading

init(autoreset=True) # Resetear colores automáticamente

# Manejo de señal de interrupción (Ctrl+C)
def signal_handler(sig, frame):
    clear()
    print(Fore.RED + "\n🚪 Saliendo del programa... Hasta pronto! 👋")
    time.sleep(1.5)
    clear()  # Asegurar que la terminal se borra al salir
    sys.exit(0)

# Registrar el manejador de señal
signal.signal(signal.SIGINT, signal_handler)

# Detectar el sistema operativo y limpiar la pantalla

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Animación de carga

def animacion_carga(mensaje="Cargando", duracion=3):
    simbolos = itertools.cycle([Fore.CYAN + "-", Fore.YELLOW + "\\", Fore.GREEN + "|", Fore.RED + "/"])  
    fin = time.time() + duracion  

    while time.time() < fin:
        sys.stdout.write(f"\r{Style.BRIGHT + Fore.MAGENTA}{mensaje} {next(simbolos)}")  
        sys.stdout.flush()
        time.sleep(0.1)

    # Mensaje de finalización sin caracteres adicionales
    sys.stdout.write(f"\r{Fore.GREEN}✔ Listo!{' ' * 20}\n")  
    sys.stdout.flush()

def barra_carga():
    for _ in tqdm(range(15), desc=Fore.YELLOW + "⏳ Cargando", ncols=60, ascii=" █", leave=False):
        time.sleep(0.03)  # Velocidad de carga


# Input con asteriscos

def asteriscos(prompt=""):
    print(prompt, end="", flush=True)
    contraseña = ""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1)  # Leer un carácter
            if char == "\n" or char == "\r":  # Enter para finalizar
                print("")
                break
            elif char == "\x7f":  # Tecla Backspace
                if len(contraseña) > 0:
                    contraseña = contraseña[:-1]
                    print("\b \b", end="", flush=True)  # Borra el último *
            else:
                contraseña += char
                print("*", end="", flush=True)  # Muestra un asterisco

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return contraseña

# Función para generar clave a partir de la clave maestra
def generar_clave(password_maestra):
    hashed = hashlib.sha256(password_maestra.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

# Función para cifrar una contraseña
def cifrar_contraseña(contraseña, password_maestra):
    clave = generar_clave(password_maestra)
    cipher = Fernet(clave)
    return cipher.encrypt(contraseña.encode()).decode()

# Función para descifrar una contraseña
def descifrar_contraseña(contraseña_cifrada, password_maestra):
    try:
        clave = generar_clave(password_maestra)
        cipher = Fernet(clave)
        return cipher.decrypt(contraseña_cifrada.encode()).decode()
    except:
        return None

# Función para mostrar la contraseña en una ventana emergente cuando el usuario lo solicita
def mostrar_contraseña_en_ventana(contraseña, tiempo_mostrar=5):
    def abrir_ventana():
        # Crear la ventana
        ventana = tk.Tk()
        ventana.title("Contraseña Descifrada")
        ventana.geometry("500x150")
        ventana.configure(background="#1e1e1e")
        
        # Variable para controlar si la ventana sigue activa
        ventana_activa = True
        
        # Función para manejar el cierre de la ventana
        def on_closing():
            nonlocal ventana_activa
            ventana_activa = False
            ventana.destroy()
        
        # Asociar el manejador de eventos al cierre de la ventana
        ventana.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Centrar la ventana en la pantalla
        ancho_ventana = ventana.winfo_reqwidth()
        alto_ventana = ventana.winfo_reqheight()
        pos_x = int(ventana.winfo_screenwidth() / 2 - ancho_ventana / 2)
        pos_y = int(ventana.winfo_screenheight() / 2 - alto_ventana / 2)
        ventana.geometry(f"+{pos_x}+{pos_y}")
        
        # Crear etiqueta con la contraseña
        tk.Label(
            ventana, 
            text="Tu contraseña es:", 
            font=("Arial", 12), 
            background="#1e1e1e", 
            foreground="#e0e0e0"
        ).pack(pady=(20, 5))
        
        tk.Label(
            ventana, 
            text=contraseña, 
            font=("Arial", 16, "bold"), 
            background="#1e1e1e", 
            foreground="#4CAF50"
        ).pack(pady=5)
        
        # Etiqueta de tiempo restante
        lbl_tiempo = tk.Label(
            ventana, 
            text=f"Esta ventana se cerrará en {tiempo_mostrar} segundos", 
            font=("Arial", 10), 
            background="#1e1e1e", 
            foreground="#e0e0e0"
        )
        lbl_tiempo.pack(pady=(5, 10))
        
        # Usamos after en lugar de un hilo para el contador
        tiempo_restante = [tiempo_mostrar]  # Usamos lista para poder modificarla
        
        def actualizar_contador():
            # Si la ventana ya no está activa, no hacemos nada
            if not ventana_activa:
                return
                
            tiempo_restante[0] -= 1
            if tiempo_restante[0] > 0:
                # Verificamos si la ventana sigue existiendo antes de actualizar
                try:
                    lbl_tiempo.config(text=f"Esta ventana se cerrará en {tiempo_restante[0]} segundos")
                    # Programamos la siguiente actualización solo si la ventana sigue activa
                    ventana.after(1000, actualizar_contador)
                except tk.TclError:
                    # La ventana fue cerrada, no hacemos nada
                    pass
            else:
                # Cuando llegue a cero, cerramos la ventana si sigue activa
                if ventana_activa:
                    try:
                        ventana.destroy()
                    except tk.TclError:
                        # La ventana ya fue cerrada, no hacemos nada
                        pass
        
        # Iniciamos el contador usando el propio sistema de eventos de tkinter
        ventana.after(1000, actualizar_contador)
        
        # Ejecutar la ventana
        ventana.mainloop()
    
    return abrir_ventana

# Menú principal

clear()

animacion_carga("Cargando AdriCrypt, por favor, espere", 3) # Aumentar a 2


def menu():
    try:
        while True:
            clear()
            print(Style.BRIGHT + Fore.BLUE + "\n🔐 MENÚ PRINCIPAL - AdriCrypt 🔐")
            print()
            print(Fore.YELLOW + "1️⃣ Cifrar contraseña 🔒")
            print(Fore.GREEN + "2️⃣ Descifrar contraseña 🔓")
            print(Fore.BLUE + "3️⃣ Ayuda 📖")
            print(Fore.RED + "4️⃣ Salir 🚪")
            
            opcion = input(Fore.CYAN + "\n👉 Elige una opción: ")

            if opcion == "1":
                clear()
                barra_carga()
                print(Fore.YELLOW + "\n🔒 Cifrar una contraseña")
                print()
                password_maestra = asteriscos(Fore.CYAN + "🔑 Introduce tu clave maestra: ")
                print()
                contraseña = input(Fore.CYAN + "🔏 Introduce la contraseña a cifrar: " + Fore.WHITE)
                print()
                animacion_carga("🔐 Cifrando...", 3)
                cifrada = cifrar_contraseña(contraseña, password_maestra)
                
                print(Fore.GREEN + "\n✅ Contraseña cifrada:")
                print(Fore.CYAN + cifrada)
                time.sleep(2)
                input(Fore.CYAN + "\nPresiona cualquier tecla para volver al menú principal...")

            elif opcion == "2":
                clear()
                print(Fore.GREEN + "\n🔓 Descifrar una contraseña")
                print()
                password_maestra = asteriscos(Fore.CYAN + "🔑 Introduce tu clave maestra: ")
                print()
                cifrada = input(Fore.CYAN + "🔏 Introduce la contraseña cifrada: " + Fore.WHITE)
                print()
                animacion_carga("🔓 Descifrando...", 3)
                descifrada = descifrar_contraseña(cifrada, password_maestra)
                
                if descifrada is not None:
                    clear()  # Borramos la terminal antes de mostrar nuevos mensajes

                    print(Fore.GREEN + "✅ Contraseña descifrada con éxito!")

                    # Preguntar al usuario si desea ver la contraseña en una ventana segura
                    print(Fore.CYAN + "\n¿Cómo deseas ver la contraseña descifrada?")
                    print(Fore.YELLOW + "1. Mostrar en ventana segura")
                    print(Fore.MAGENTA + "2. Mostrar aquí en la terminal")
                    
                    opcion_ventana = input(Fore.CYAN + "\n👉 Elige una opción (1/2): ")
                    
                    if opcion_ventana == "1":
                        # Mostrar la contraseña en una ventana emergente
                        print(Fore.GREEN + "\nAbriendo ventana segura...")
                        func_ventana = mostrar_contraseña_en_ventana(descifrada)
                        func_ventana()  # Ejecutar la función para abrir la ventana
                        # Limpiamos la pantalla después de que la ventana se cierre
                        clear()
                    else:
                        # Mostrar la contraseña en la terminal
                        print(Fore.YELLOW + "\n✅ Contraseña original:")
                        print(Fore.GREEN + descifrada)
                else:
                    print()
                    print(Fore.RED + "❌ Error: Clave maestra incorrecta o contraseña corrupta.")
                
                print()  # Agregamos una línea en blanco
                input(Fore.CYAN + "Presiona cualquier tecla para volver al menú principal...")

            elif opcion == "3":
                clear()
                print(Style.BRIGHT + Fore.BLUE + "\n📖 AYUDA - AdriCrypt 📖")
                print()
                print(Fore.YELLOW + "Este programa te ayuda a cifrar y descifrar contraseñas o mensajes sensibles que no quieras mostrar en texto plano.")
                print()
                print(Fore.CYAN + "🔒 Cifrar una contraseña:")
                print(Fore.WHITE + "Selecciona la opción 'Cifrar contraseña' en el menú principal. Luego, introduce tu clave maestra y la contraseña que deseas cifrar.")
                print("El programa generará una versión cifrada de tu contraseña que podrás guardar de forma segura.")
                print()
                print(Fore.CYAN + "🔓 Descifrar una contraseña:")
                print(Fore.WHITE + "Selecciona la opción 'Descifrar contraseña' en el menú principal. Luego, introduce tu clave maestra y la contraseña cifrada.")
                print("El programa descifrará la contraseña y te mostrará el texto original.")
                print()
                print(Fore.GREEN + "Nota: Asegúrate de recordar tu clave maestra, ya que es necesaria tanto para cifrar como para descifrar las contraseñas.")
                print(Fore.RED + "⚠️ Si pierdes tu clave maestra, no podrás recuperar tus contraseñas cifradas.")
                input(Fore.CYAN + "\nPresiona cualquier tecla para volver al menú principal...")

            elif opcion == "4":
                clear()
                print(Fore.RED + "\n🚪 Saliendo del programa... Hasta pronto! 👋")
                time.sleep(1.5)
                clear()  # Asegurar que la terminal se borra al salir
                break

            else:
                print(Fore.RED + "❌ Opción no válida. Inténtalo de nuevo.")

    except KeyboardInterrupt:
        # Este bloque captura Ctrl+C dentro de la función menu por si acaso
        signal_handler(signal.SIGINT, None)

# Ejecutar el menú
menu()
