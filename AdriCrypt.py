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

init(autoreset=True) # Resetear colores automáticamente

# Manejo de señal de interrupción (Ctrl+C)
def signal_handler(sig, frame):
    clear()
    print(Fore.RED + "\n🚪 Saliendo del programa... Hasta pronto! 👋")
    time.sleep(1.5)
    clear()
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

    sys.stdout.write(f"\r{Fore.GREEN}✔ Listo!       \n")  

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
                    print()
                    print(Fore.YELLOW + "\n✅ Contraseña original:")
                    print(Fore.GREEN + descifrada)
                else:
                    print()
                    print(Fore.RED + "❌ Error: Clave maestra incorrecta o contraseña corrupta.")

                time.sleep(2)
                input(Fore.CYAN + "\nPresiona cualquier tecla para volver al menú principal...")

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
                time.sleep(1)
                clear()
                break

            else:
                print(Fore.RED + "❌ Opción no válida. Inténtalo de nuevo.")

    except KeyboardInterrupt:
        # Este bloque captura Ctrl+C dentro de la función menu por si acaso
        signal_handler(signal.SIGINT, None)

# Ejecutar el menú
menu()
