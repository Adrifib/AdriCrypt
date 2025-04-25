from cryptography.fernet import Fernet
import base64
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import threading
import time
import pyperclip  # Para copiar al portapapeles

class PasswordDisplay:
    def __init__(self, password, duration=5):
        self.password = password
        self.duration = duration
        self.window = None
        
    def show(self):
        # Crear una nueva ventana para mostrar la contraseña
        self.window = tk.Toplevel()
        self.window.title("Contraseña Descifrada")
        self.window.geometry("500x200")
        self.window.configure(background="#1e1e1e")
        self.window.resizable(False, False)
        
        # Centrar la ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Etiqueta de título
        tk.Label(
            self.window, 
            text="Tu contraseña es:", 
            font=("Arial", 12), 
            bg="#1e1e1e", 
            fg="#e0e0e0"
        ).pack(pady=(20, 5))
        
        # Frame para la contraseña y el botón de copiar
        password_frame = tk.Frame(self.window, bg="#1e1e1e")
        password_frame.pack(pady=5)
        
        # Entrada de texto para mostrar la contraseña (permite copiar)
        password_entry = tk.Entry(
            password_frame,
            font=("Arial", 16, "bold"),
            width=30,
            bg="#2a2a2a",
            fg="#4CAF50",
            readonlybackground="#2a2a2a",
            relief=tk.FLAT
        )
        password_entry.insert(0, self.password)
        password_entry.config(state="readonly")
        password_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para copiar la contraseña
        copy_button = tk.Button(
            password_frame, 
            text="Copiar", 
            command=lambda: self.copy_to_clipboard(self.password),
            bg="#4CAF50", 
            fg="#ffffff"
        )
        copy_button.pack(side=tk.LEFT)
        
        # Etiqueta para el temporizador
        self.timer_label = tk.Label(
            self.window,
            text=f"Esta ventana se cerrará en {self.duration} segundos",
            font=("Arial", 10),
            bg="#1e1e1e", 
            fg="#e0e0e0"
        )
        self.timer_label.pack(pady=(10, 0))
        
        # Iniciar temporizador para cerrar la ventana
        self.remaining = self.duration
        self.update_timer()
    
    def update_timer(self):
        if self.remaining > 0:
            self.timer_label.config(text=f"Esta ventana se cerrará en {self.remaining} segundos")
            self.remaining -= 1
            self.window.after(1000, self.update_timer)
        else:
            self.window.destroy()
    
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        tk.Label(
            self.window,
            text="✓ Contraseña copiada al portapapeles",
            font=("Arial", 10),
            bg="#1e1e1e", 
            fg="#4CAF50"
        ).pack(pady=5)

class AdriCryptApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AdriCrypt - GUI")
        self.root.geometry("450x350")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        # Configurar estilo para los botones
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 11), padding=6)

        self.create_widgets()
    
    def create_widgets(self):
        # Marco principal
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título principal
        title_label = tk.Label(main_frame, text="🔐 AdriCrypt", font=("Arial", 24, "bold"), bg="#1e1e1e", fg="#e0e0e0")
        title_label.pack(pady=(10, 20))
        
        # Botones con mejor apariencia
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(fill=tk.X)
        
        # Estilos de botones
        button_styles = [
            {"text": "Cifrar Contraseña 🔒", "command": self.encrypt_password, "bg": "#4CAF50"},
            {"text": "Descifrar Contraseña 🔓", "command": self.decrypt_password, "bg": "#2196F3"},
            {"text": "Ayuda 📖", "command": self.show_help, "bg": "#FFC107"},
            {"text": "Salir 🚪", "command": self.root.quit, "bg": "#F44336"}
        ]
        
        for style in button_styles:
            button = tk.Button(
                button_frame,
                text=style["text"],
                command=style["command"],
                bg=style["bg"],
                fg="#ffffff",
                relief=tk.RAISED,
                borderwidth=1,
                padx=10,
                pady=8,
                font=("Arial", 11),
                width=25
            )
            button.pack(pady=8, fill=tk.X)
        
        # Información en la parte inferior
        footer_label = tk.Label(
            main_frame, 
            text="AdriCrypt - Protege tus contraseñas", 
            font=("Arial", 8), 
            bg="#1e1e1e", 
            fg="#888888"
        )
        footer_label.pack(side=tk.BOTTOM, pady=(20, 0))

    def generate_key(self, master_password):
        hashed = hashlib.sha256(master_password.encode()).digest()
        return base64.urlsafe_b64encode(hashed[:32])

    def encrypt_password(self):
        master_password = simpledialog.askstring("Clave Maestra", "Introduce tu clave maestra:", show='*')
        if not master_password:
            return
            
        password = simpledialog.askstring("Contraseña", "Introduce la contraseña a cifrar:")
        if not password:
            return
            
        key = self.generate_key(master_password)
        cipher = Fernet(key)
        encrypted_password = cipher.encrypt(password.encode()).decode()
        
        # Crear una ventana de resultado personalizada en lugar de messagebox
        result_window = tk.Toplevel(self.root)
        result_window.title("Contraseña Cifrada")
        result_window.geometry("550x200")
        result_window.configure(bg="#1e1e1e")
        result_window.resizable(False, False)
        
        # Centrar la ventana
        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (result_window.winfo_screenwidth() // 2) - (width // 2)
        y = (result_window.winfo_screenheight() // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Mensaje de éxito
        tk.Label(
            result_window,
            text="✅ Contraseña cifrada con éxito",
            font=("Arial", 12, "bold"),
            bg="#1e1e1e",
            fg="#4CAF50"
        ).pack(pady=(20, 15))
        
        # Frame para la contraseña cifrada y botón de copiar
        frame = tk.Frame(result_window, bg="#1e1e1e")
        frame.pack(pady=10, padx=20)
        
        # Campo de texto para mostrar la contraseña cifrada (permite seleccionar y copiar)
        entry = tk.Entry(frame, width=50, font=("Arial", 10), bg="#2a2a2a", fg="#e0e0e0", readonlybackground="#2a2a2a")
        entry.insert(0, encrypted_password)
        entry.config(state="readonly")
        entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para copiar
        copy_button = tk.Button(
            frame, 
            text="Copiar", 
            command=lambda: self.copy_to_clipboard(encrypted_password, result_window),
            bg="#4CAF50", 
            fg="#ffffff"
        )
        copy_button.pack(side=tk.LEFT)
        
        # Botón para cerrar
        close_button = tk.Button(
            result_window, 
            text="Cerrar", 
            command=result_window.destroy,
            bg="#F44336", 
            fg="#ffffff"
        )
        close_button.pack(pady=15)

    def decrypt_password(self):
        master_password = simpledialog.askstring("Clave Maestra", "Introduce tu clave maestra:", show='*')
        if not master_password:
            return
            
        encrypted_password = simpledialog.askstring("Contraseña Cifrada", "Introduce la contraseña cifrada:")
        if not encrypted_password:
            return
            
        try:
            key = self.generate_key(master_password)
            cipher = Fernet(key)
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            
            # Mostrar mensaje de éxito y opciones para ver la contraseña
            success_window = tk.Toplevel(self.root)
            success_window.title("Descifrado Exitoso")
            success_window.geometry("400x250")
            success_window.configure(bg="#1e1e1e")
            success_window.resizable(False, False)
            
            # Centrar la ventana
            success_window.update_idletasks()
            width = success_window.winfo_width()
            height = success_window.winfo_height()
            x = (success_window.winfo_screenwidth() // 2) - (width // 2)
            y = (success_window.winfo_screenheight() // 2) - (height // 2)
            success_window.geometry(f'{width}x{height}+{x}+{y}')
            
            # Mensaje de éxito
            tk.Label(
                success_window,
                text="✅ Contraseña descifrada con éxito",
                font=("Arial", 14, "bold"),
                bg="#1e1e1e",
                fg="#4CAF50"
            ).pack(pady=(20, 30))
            
            # Pregunta sobre cómo mostrar la contraseña
            tk.Label(
                success_window,
                text="¿Cómo deseas ver la contraseña descifrada?",
                font=("Arial", 11),
                bg="#1e1e1e",
                fg="#e0e0e0"
            ).pack(pady=(0, 20))
            
            # Botones de opciones
            buttons_frame = tk.Frame(success_window, bg="#1e1e1e")
            buttons_frame.pack(pady=10)
            
            # Opción 1: Mostrar en ventana segura
            secure_button = tk.Button(
                buttons_frame,
                text="Mostrar en ventana segura",
                command=lambda: [success_window.destroy(), PasswordDisplay(decrypted_password, 5).show()],
                bg="#2196F3",
                fg="#ffffff",
                width=25
            )
            secure_button.pack(side=tk.LEFT, padx=5)
            
            # Opción 2: Mostrar aquí
            show_button = tk.Button(
                buttons_frame,
                text="Mostrar aquí",
                command=lambda: self.show_password_here(success_window, decrypted_password),
                bg="#FFC107",
                fg="#ffffff",
                width=20
            )
            show_button.pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            messagebox.showerror("Error", "❌ Clave maestra incorrecta o contraseña corrupta.")

    def show_password_here(self, window, password):
        # Limpiar la ventana
        for widget in window.winfo_children():
            widget.destroy()
        
        # Titulo
        tk.Label(
            window,
            text="Tu contraseña descifrada",
            font=("Arial", 14, "bold"),
            bg="#1e1e1e",
            fg="#e0e0e0"
        ).pack(pady=(20, 15))
        
        # Frame para mostrar la contraseña y botón de copiar
        frame = tk.Frame(window, bg="#1e1e1e")
        frame.pack(pady=10, padx=20)
        
        # Campo para mostrar la contraseña con opción de seleccionar/copiar
        entry = tk.Entry(frame, width=30, font=("Arial", 12), bg="#2a2a2a", fg="#4CAF50", readonlybackground="#2a2a2a")
        entry.insert(0, password)
        entry.config(state="readonly")
        entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para copiar
        copy_button = tk.Button(
            frame, 
            text="Copiar", 
            command=lambda: self.copy_to_clipboard(password, window),
            bg="#4CAF50", 
            fg="#ffffff"
        )
        copy_button.pack(side=tk.LEFT)
        
        # Botón para cerrar
        close_button = tk.Button(
            window, 
            text="Cerrar", 
            command=window.destroy,
            bg="#F44336", 
            fg="#ffffff"
        )
        close_button.pack(pady=15)

    def copy_to_clipboard(self, text, window=None):
        pyperclip.copy(text)
        if window:
            copy_label = tk.Label(
                window,
                text="✓ Copiado al portapapeles",
                font=("Arial", 10),
                bg="#1e1e1e", 
                fg="#4CAF50"
            )
            copy_label.pack(pady=5)
            # Auto-eliminar el mensaje después de 2 segundos
            window.after(2000, copy_label.destroy)

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Ayuda - AdriCrypt")
        help_window.geometry("550x350")
        help_window.configure(bg="#1e1e1e")
        help_window.resizable(False, False)
        
        # Título
        tk.Label(
            help_window,
            text="📖 AYUDA - AdriCrypt 📖",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#2196F3"
        ).pack(pady=(20, 15))
        
        # Texto de ayuda
        help_text = (
            "Este programa te ayuda a cifrar y descifrar contraseñas o mensajes sensibles "
            "que no quieras mostrar en texto plano.\n\n"
            "🔒 Cifrar una contraseña:\n"
            "Selecciona 'Cifrar Contraseña' en el menú principal. Luego, introduce tu clave maestra "
            "y la contraseña que deseas cifrar. El programa generará una versión cifrada de tu "
            "contraseña que podrás copiar y guardar de forma segura.\n\n"
            "🔓 Descifrar una contraseña:\n"
            "Selecciona 'Descifrar Contraseña' en el menú principal. Luego, introduce tu clave maestra "
            "y la contraseña cifrada. El programa descifrará la contraseña y te mostrará el texto original "
            "en una ventana segura o directamente en la aplicación según prefieras.\n\n"
            "⚠️ IMPORTANTE: Asegúrate de recordar tu clave maestra, ya que es necesaria tanto para cifrar "
            "como para descifrar las contraseñas. Si pierdes tu clave maestra, no podrás recuperar tus "
            "contraseñas cifradas."
        )
        
        text_frame = tk.Frame(help_window, bg="#1e1e1e")
        text_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)
        
        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg="#2a2a2a",
            fg="#e0e0e0",
            font=("Arial", 10),
            padx=15,
            pady=15,
            height=12,
            borderwidth=0
        )
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Botón para cerrar
        close_button = tk.Button(
            help_window, 
            text="Cerrar", 
            command=help_window.destroy,
            bg="#F44336", 
            fg="#ffffff",
            width=10
        )
        close_button.pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdriCryptApp(root)
    root.mainloop()