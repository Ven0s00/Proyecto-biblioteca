from tkinter import *
import customtkinter as ck # Modulo para mejorar la interfaz gráfica
import tkinter as tk # Modulo para crear la interfaz gráfica
from tkinter import messagebox # Modulo para mostrar mensajes en ventanas emergentes
from tkinter import ttk # Modulo para darle estilos a los widgets presentes en la app
from tkcalendar import DateEntry # Modulo para seleccionar una fecha median un calendario
from PIL import Image, ImageTk # Modulo para importar imágenes
import re # Modulo para poder validar si el correo electrónico es un correo electrónico
import random # Modulo para crear un código random
from twilio.rest import Client # Modulo para poder conectar con la API de mensajería
import time
from datetime import datetime, timedelta
import numpy as np
import cv2
from babel.numbers import format_currency # Modulo para que los DateEntrys funcionen

from model.conexion_db import BD
from client.barra import BarraProgreso

# Ventana Términos y Condiciones de Uso
class VentanaTerminosCondiciones(ck.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Términos y Condiciones de Uso")
        self.after(250, lambda: self.iconbitmap('img\libros.ico'))
        self.resizable(0,0)
        self.geometry("500x400")

        # Agregar un Text widget con Scrollbar para mostrar los Términos y Condiciones
        terminos_texto = ck.CTkTextbox(self, wrap="word", font=ck.CTkFont(size=12, weight="bold", family="Segoe UI Historic"))

        # Contenido de los Términos y Condiciones de Uso
        contenido_terminos = """TÉRMINOS Y CONDICIONES DE USO\nBienvenido/a a la aplicación "Biblioteca Virtual". Antes de utilizar esta aplicación, te pedimos que leas atentamente los siguientes Términos y Condiciones de Uso, ya que el acceso y uso de esta aplicación implican la aceptación plena y sin reservas de estos términos.\n\n1. Aceptación de los Términos:\nAl utilizar la aplicación "Biblioteca Virtual", aceptas estar legalmente vinculado por estos Términos y Condiciones de Uso. Si no estás de acuerdo con estos términos, por favor, no utilices la aplicación.\n\n2. Uso de la Aplicación:\nLa aplicación "Biblioteca Virtual" está diseñada para ser utilizada únicamente con fines personales y no comerciales.\nLos usuarios son responsables de cualquier contenido que compartan a través de la aplicación y deben asegurarse de que dicho contenido cumpla con las leyes aplicables y no infrinja los derechos de terceros.\nSe prohíbe el uso de la aplicación para actividades ilegales, ofensivas, dañinas o que puedan interferir con el funcionamiento normal de la aplicación o su infraestructura.\n\n3. Registro y Cuentas de Usuario:\nAlgunas funciones de la aplicación pueden requerir que los usuarios se registren y creen una cuenta. Los usuarios son responsables de mantener la confidencialidad de sus credenciales de acceso y de todas las actividades que ocurran en su cuenta.\n\n4. Privacidad:\nLa privacidad de los usuarios es importante para nosotros. Nuestra Política de Privacidad describe cómo recopilamos, utilizamos, almacenamos y protegemos la información personal de los usuarios. Al utilizar la aplicación, aceptas nuestra Política de Privacidad.\n\n5. Propiedad Intelectual:\nTodos los derechos de propiedad intelectual relacionados con la aplicación y su contenido (textos, imágenes, logotipos, etc.) son propiedad de sus respectivos propietarios y están protegidos por las leyes de propiedad intelectual aplicables.\n\n6. Modificaciones a los Términos:\nNos reservamos el derecho de modificar estos Términos y Condiciones en cualquier momento. Cualquier cambio será efectivo una vez publicado en la aplicación. Se recomienda a los usuarios revisar periódicamente los Términos y Condiciones para estar al tanto de las actualizaciones.\n\n7. Limitación de Responsabilidad:\nEl uso de la aplicación es bajo la responsabilidad del usuario. No nos hacemos responsables de cualquier daño, pérdida o perjuicio que pueda surgir del uso de la aplicación o del contenido compartido por los usuarios.\n\n8. Ley Aplicable y Jurisdicción:\nEstos Términos y Condiciones se rigen por las leyes del país en el que está registrada la entidad responsable de la aplicación. Cualquier disputa relacionada con la aplicación estará sujeta a la jurisdicción de los tribunales competentes de dicho país.\n\n9. Contacto:\nSi tienes alguna pregunta o inquietud sobre estos Términos y Condiciones de Uso, puedes ponerte en contacto con nosotros a través de biblioteca.virtual@gmail.com o +56 952458474.\n\nFecha de última actualización: 23-07-2023."""

        # Insertar el contenido en el Text widget
        terminos_texto.insert("1.0", contenido_terminos)

        # Deshabilitar la edición del Text widget
        terminos_texto.configure(state="disabled")

        terminos_texto.pack(side="left", fill="both", expand=True)

# Ventana de registro
class VentanaRegistro(ck.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Biblioteca Virtual")
        self.after(250, lambda: self.iconbitmap('img\libros.ico'))
        self.geometry("1240x650")
        self.resizable(0, 0)

        self.bd = BD()

        self.mostrar_contraseña = tk.BooleanVar(value=False)  # Variable para controlar la visibilidad de la contraseña
        
        self.terminos_condiciones = tk.BooleanVar()

        self.celular = ck.StringVar()
        self.celular.trace("w", self.validarEnTiempoReal)

        self.codigo_pais = ck.IntVar(value="+56 9")

        # ================Background Image ====================
        imagen_fondo = ck.CTkImage(Image.open("img\\image_1.png"), size=(1000, 600))
        bg_image = ck.CTkLabel(
            self,
            text="",
            image=imagen_fondo
        )
        bg_image.place(x=120, y=28)

        # ================ NOMBRE DE LA APP ====================
        logo_app = ck.CTkImage(Image.open("img\\libros.ico"), size=(80, 80))
        headerText_image_label1 = ck.CTkLabel(
            bg_image,
            image=logo_app,
            bg_color="#272A37"
        )
        headerText_image_label1.place(x=20, y=10)

        nombre_app_label = Label(
            bg_image,
            text="Biblioteca Virtual",
            fg="#FFFFFF",
            font=ck.CTkFont(size=25, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        nombre_app_label.place(x=110, y=32)

        # ================ HEADER CREAR CUENTA ====================
        crear_cuenta_label = Label(
            bg_image,
            text="Crear nueva cuenta",
            fg="#FFFFFF",
            font=ck.CTkFont(size=28, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        crear_cuenta_label.place(x=75, y=90)

        # ================ TEXTO YA TIENE CUENTA? ====================
        ya_registrado_label = Label(
            bg_image,
            text="¿Ya esta registrado?",
            fg="#FFFFFF",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        ya_registrado_label.place(x=75, y=150)

        # ================ IR A INICIAR SESIÓN ====================
        self.volver_login_button = Button(
            bg_image,
            text="Iniciar Sesión",
            fg="#206DB4",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37",
            bd=0,
            cursor="hand2",
            activebackground="#272A37",
            activeforeground="#ffffff",
            command=lambda: self.volverLogin()
        )
        self.volver_login_button.place(x=230, y=148, width=150, height=35)

        # ================ SECCIÓN NOMBRE ====================
        nombre_imagen = ck.CTkImage(Image.open("img\\input_img.png"), size=(190, 50))
        nombre_imagen_Label = ck.CTkLabel(
            bg_image,
            image=nombre_imagen,
            bg_color="#272A37"
        )
        nombre_imagen_Label.place(x=80, y=190)

        firstName_text = Label(
            nombre_imagen_Label,
            text="Nombre",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        firstName_text.place(x=25, y=0)

        self.nombre_entry = Entry(
            nombre_imagen_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=16, weight="bold", family="Segoe UI Historic"),
            fg="white"
        )
        self.nombre_entry.place(x=8, y=17, width=140, height=27)


        # ================ SECCIÓN APELLIDO ====================
        apellido_imagen = ck.CTkImage(Image.open("img\\input_img.png"), size=(190, 50))
        apellido_imagen_Label = ck.CTkLabel(
            bg_image,
            image=apellido_imagen,
            bg_color="#272A37"
        )
        apellido_imagen_Label.place(x=293, y=190)

        lastName_text = Label(
            apellido_imagen_Label,
            text="Apellido",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B",
            height=1
        )
        lastName_text.place(x=25, y=0)

        self.apellido_entry = Entry(
            apellido_imagen_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1),
            fg="white"
        )
        self.apellido_entry.place(x=8, y=17, width=140, height=27)

        # ================ SECCIÓN RUT ====================
        rut_imagen = ck.CTkImage(Image.open("img\\email.png"), size=(400, 50))
        rut_imagen_Label = ck.CTkLabel(
            bg_image,
            image=rut_imagen,
            bg_color="#272A37"
        )
        rut_imagen_Label.place(x=80, y=255)

        rut_text = Label(
            rut_imagen_Label,
            text="RUT",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13 * 1, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        rut_text.place(x=25, y=0)

        self.rut_entry = Entry(
            rut_imagen_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=14, weight="bold", family="Segoe UI Historic"),
            fg="white"
        )
        self.rut_entry.place(x=8, y=17, width=354, height=27)

       # ================ SECCIÓN EMAIL ====================
        email_imagen = ck.CTkImage(Image.open("img\\email.png"), size=(400, 50))
        email_imagen_Label = ck.CTkLabel(
            bg_image,
            text="",
            image=email_imagen,
            bg_color="#272A37"
        )
        email_imagen_Label.place(x=80, y=320)

        email_text = Label(
            email_imagen_Label,
            text="Email",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13 * 1, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        email_text.place(x=25, y=0)

        self.correo_entry = Entry(
            email_imagen_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=18, weight="bold", family="Segoe UI Historic"),
            fg="white"
        )
        self.correo_entry.place(x=8, y=17, width=354, height=27)

        # ================ SECCIÓN CÓDIGO CELULAR ====================
        codigo_celular_image = ck.CTkImage(Image.open("img\\input_img.png"), size=(195, 50))
        codigo_celular_image_Label = ck.CTkLabel(
            bg_image,
            image=codigo_celular_image,
            bg_color="#272A37",
            text=""
        )
        codigo_celular_image_Label.place(x=80, y=385)

        codigo_celular_text = Label(
            codigo_celular_image_Label,
            text="Código País",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13 * 1, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        codigo_celular_text.place(x=12, y=0)

        self.codigo_pais_entry = Entry(
            codigo_celular_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=18, weight="bold", family="Segoe UI Historic"),
            fg="white",
            textvariable=self.codigo_pais
        )
        self.codigo_pais_entry.place(x=8, y=17, width=354, height=27)

        # ================ SECCIÓN CELULAR ====================
        celular_image = ck.CTkImage(Image.open("img\\email.png"), size=(380, 50))
        celular_image_Label = ck.CTkLabel(
            bg_image,
            image=celular_image,
            bg_color="#272A37",
            text=""
        )
        celular_image_Label.place(x=280, y=385)

        celular_text = Label(
            celular_image_Label,
            text="Celular",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13 * 1, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        celular_text.place(x=12, y=0)

        self.celular_entry = Entry(
            celular_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=18, weight="bold", family="Segoe UI Historic"),
            fg="white"
        )
        self.celular_entry.place(x=8, y=17, width=354, height=27)

        # ================ SECCIÓN CONTRASEÑA ====================
        passwordName_image = ck.CTkImage(Image.open("img\\input_img.png"), size=(195, 50))
        passwordName_image_Label = ck.CTkLabel(
            bg_image,
            image=passwordName_image,
            bg_color="#272A37"
        )
        passwordName_image_Label.place(x=80, y=450)

        passwordName_text = Label(
            passwordName_image_Label,
            text="Password",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13 * -1),
            bg="#3D404B"
        )
        passwordName_text.place(x=25, y=0)

        self.contraseña_entry = Entry(
            passwordName_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1),
            fg="white"
        )
        self.contraseña_entry.place(x=8, y=17, width=140, height=20)

        # ================ SECCIÓN CONFIRMAR CONTRASEÑA ====================
        confirm_passwordName_image = ck.CTkImage(Image.open("img\\input_img.png"), size=(195, 50))
        confirm_passwordName_image_Label = ck.CTkLabel(
            bg_image,
            image=confirm_passwordName_image,
            bg_color="#272A37"
        )
        confirm_passwordName_image_Label.place(x=293, y=450)

        confirm_passwordName_text = Label(
            confirm_passwordName_image_Label,
            text="Confirm Password",
            fg="#FFFFFF",
            font=("yu gothic ui SemiBold", 13 * -1),
            bg="#3D404B"
        )
        confirm_passwordName_text.place(x=25, y=0)

        self.contraseña_entry_confirmar = Entry(
            confirm_passwordName_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=("yu gothic ui SemiBold", 16 * -1),
            fg="white"
        )
        self.contraseña_entry_confirmar.place(x=8, y=17, width=140, height=27)

        # =============== REGISTRARSE BUTTON ====================
        submit_button = ck.CTkButton(
            bg_image,
            text="Registrarse",
            font=ck.CTkFont(size=25, weight="bold", family="Segoe UI Historic"),
            width=350, 
            height=65,
            corner_radius=15,
            command=lambda: self.registrar()
        )
        submit_button .place(x=110, y=515)

        # ================ DESARROLLADORES HEADER ====================
        desarrolladores_image = ck.CTkImage(Image.open("img\\headerText_image.png"), size=(30, 30))
        desarrolladores_image_label = ck.CTkLabel(
            bg_image,
            image=desarrolladores_image,
            bg_color="#272A37",
            text=""
        )
        desarrolladores_image_label.place(x=710, y=505)

        headerText3 = Label(
            bg_image,
            text="Desarrollado por Aesir",
            fg="#FFFFFF",
            font=("yu gothic ui bold", 20 * -1),
            bg="#272A37"
        )
        headerText3.place(x=750, y=500)

        # Este es un checkbox para mostrar la contraseña que estamos ingresando
        self.mostrarContraseña_Registro = tk.BooleanVar()
        mostrar_contraseña_checkbox = ck.CTkCheckBox(self, 
            text="Mostrar contraseña", 
            variable=self.mostrarContraseña_Registro, 
            command=self.mostrarContraseñaRegistro, 
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg_color="#272A37"
        )
        mostrar_contraseña_checkbox.place(x=620, y=490)

        # ================ TÉRMINOS Y CONDICIONES DE USO ====================
        self.terminos_checkbox = ck.CTkCheckBox(self, 
            text="Acepto los Términos y Condiciones de Uso", 
            variable=self.terminos_condiciones, 
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg_color="#272A37"
        )
        self.terminos_checkbox.place(x=610, y=580)

        self.leer_mas_button = Button(
            bg_image,
            text="Leer más",
            fg="#206DB4",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37",
            bd=0,
            cursor="hand2",
            activebackground="#272A37",
            activeforeground="#ffffff",
            command=lambda: self.mostrarTerminosCondiciones()
        )
        self.leer_mas_button.place(x=820, y=548, width=150, height=35)

        # ================ VERSIÓN ====================
        version_label = Label(
            bg_image,
            text="Versión 1.0.0",
            fg="#FFFFFF",
            font=ck.CTkFont(size=12, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        version_label.place(x=15, y=572)


# Método para validar el correo electrónico
    def validarCorreo(self, correo):
        patron = r'^[\w\.-]+@\w+\.\w+$'

        if re.match(patron, correo):
            return True
        else:
            return False

# Método para validar el RUT ingresado
    def validarRut(self, rut):
        rut = rut.replace(".", "").replace("-", "")  # Remover puntos y guiones
        rut = rut.replace("k", "0")  # Reemplazar "k" por "0"
        rutSinDv = rut[:-1]  # Obtener el rut sin dígito verificador
        dv = rut[-1]  # Obtener el dígito verificador

        # Calcular el dígito verificador
        suma = 0
        multiplo = 2
        for i in reversed(rutSinDv):
            suma += int(i) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dvEsperado = str(11 - resto) if resto > 1 else "0"

        return dv == dvEsperado
        
# Método para mostrar la contraseña al presionar el Checkbox
    def mostrarContraseñaRegistro(self):
        # Cambia la visibilidad de la contraseña basado en el estado del checkbox
        if self.mostrarContraseña_Registro.get():
            self.contraseña_entry.configure(show="")
            self.contraseña_entry_confirmar.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
            self.contraseña_entry_confirmar.configure(show="*")

    # Método para registrar un Bibliotecario
    def registrar(self, event=None):
        # Obtiene los datos ingresados por el usuario
        nombre = self.nombre_entry.get()
        apellido = self.apellido_entry.get()
        rut = self.rut_entry.get()
        correo = self.correo_entry.get()
        codigo_pais = self.codigo_pais_entry.get()
        celular = codigo_pais + self.celular_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmarContraseña = self.contraseña_entry_confirmar.get()

        if nombre == "": # Comprobar que haya un nombre en el campo
            messagebox.showerror("Error de registro", "El campo 'nombre' no puede estar vacío.")
            return

        if apellido == "": # Comprobar que haya un apellido en el campo
            messagebox.showerror("Error de registro", "El campo 'apellido' no puede estar vacío.")

        if correo == "": #Comprobar que haya un correo en el campo
            messagebox.showerror("Error de registro", "Debe ingresar un correo.")
            return

        if not self.validarCorreo(correo):
            messagebox.showerror("Error de registro", f"Correo {correo} no válido.")
            return

        if contraseña != confirmarContraseña: #Validación de contraseña
            messagebox.showerror("Error de registro", "Las contraseñas no coinciden.")
            return

        if not self.validarRut(rut): # Validación del RUT
            messagebox.showerror("Error de registro", f"Rut {rut} no válido.")
            return
        
        # Verificar si el checkbox de términos y condiciones está marcado
        if not self.terminos_condiciones.get():
            messagebox.showwarning("Términos y Condiciones", "Debe aceptar los Términos y Condiciones de Uso para registrarse.")
            return

        if self.bd.registro(nombre, apellido, correo, contraseña, rut, celular):
            self.withdraw()  # Oculta la ventana de registro
        self.parent.deiconify()  # Muestra la ventana de login
        self.destroy()

    def validarEnTiempoReal(self, *args):
        # Validar número de celular
        entrada_celular = self.celular.get()
        if not entrada_celular.isdigit():
            self.celular_entry.delete(0, tk.END)
            self.celular_entry.insert(0, "".join(filter(str.isdigit, entrada_celular)))
            
    def volverLogin(self):
        self.destroy()
        self.parent.deiconify()

    def mostrarTerminosCondiciones(self):
        ventana_terminos = VentanaTerminosCondiciones(self)

# Ventana recuperar contraseña
class VentanaRecuperarContraseña(ck.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD()
        self.after(250, lambda: self.iconbitmap('img\libros.ico'))
        self.title("Biblioteca Virtual")
        self.geometry("600x700")
        self.resizable(0, 0)

        # Variables para obtener los datos de los entry´s
        self.celular_bibliotecario = ck.StringVar()
        self.celular_bibliotecario.trace("w", self.validarEnTiempoReal)
        self.codigo_ingresado = ck.StringVar()
        self.codigo_pais = ck.StringVar(value="+56 9")

        # Crear imagen de fondo como PhotoImage

        # Ruta de la imagen .ico
        ruta_icono = "img\\pattern.ico"

        # Abrir el archivo .ico
        ico_imagen = Image.open(ruta_icono)

        # Obtener el tamaño de la ventana
        ancho_ventana, alto_ventana = 600, 700

        # Escalar la imagen con el algoritmo LANCZOS para mejorar la calidad
        imagen_escalada = ico_imagen.resize((ancho_ventana, alto_ventana), Image.LANCZOS)

        # Crear el PhotoImage utilizando la imagen escalada
        imagen_fondo = ImageTk.PhotoImage(imagen_escalada)

        # Crear etiqueta para la imagen de fondo
        fondo = ck.CTkLabel(master=self, image=imagen_fondo, text="")
        fondo.pack()

        self.frame_recuperar_contraseña = ck.CTkFrame(master=fondo, corner_radius=15)
        self.frame_recuperar_contraseña.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.frame_recuperar_contraseña.configure(width=320, height=520)

        self.numero_celular_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese su numero de celular: ", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.numero_celular_label.place(x=25, y=0)

        self.codigo_pais_entry = ck.CTkEntry(self.frame_recuperar_contraseña, textvariable=self.codigo_pais, width=60, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"), state="disabled")
        self.codigo_pais_entry.place(x=25, y=40)

        self.numero_celular_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, textvariable=self.celular_bibliotecario, width=200, height=30, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.numero_celular_entry.place(x=90, y=40)

        self.button_celular = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.enviar_codigo_celular, text="Enviar código", font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.button_celular.place(x=90, y=80)

        self.codigo_celular_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese el código recibido: ", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.codigo_celular_label.place(x=40, y=120)

        self.codigo_celular_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, placeholder_text='Ingrese el código aquí ', textvariable=self.codigo_ingresado, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.codigo_celular_entry.place(x=35, y=160)

        self.codigo_celular_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.verificar_codigo_ingresado, text="Verificar codigo", font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.codigo_celular_button.place(x=90, y=200)

        self.volver_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.volverLogin, text="Volver", font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.volver_button.place(x=170, y=480)

    def validarEnTiempoReal(self, *args):
        # Validar número de celular
        entrada_celular = self.celular_bibliotecario.get()
        if not entrada_celular.isdigit():
            self.numero_celular_entry.delete(0, tk.END)
            self.numero_celular_entry.insert(0, "".join(filter(str.isdigit, entrada_celular)))

    # Método para generar un código único de 7 dígitos
    def generar_codigo_unico(self):
        codigo = random.randint(1000000, 9999999)  # Generar un código de 7 dígitos
        return str(codigo)
    
    # Método para enviar el código SMS
    def enviar_codigo_celular(self):
        celular = self.celular_bibliotecario.get()# Número de celular de destino
        if celular == "":
            messagebox.showerror("Recuperación de Contraseña", "Debe ingresar un numero de celular.")
            return
        codigo = self.generar_codigo_unico() # Generar el código único
        mensaje = f"Su código de recuperación de contraseña es: {codigo}"

        # Configurar las credenciales de Twilio
        account_sid = 'ACc5fcca03bf8e78a8d943d1e71c0099ed'
        auth_token = '8e549a03d607cdd90de517a898026b20'
        client = Client(account_sid, auth_token)

        try:
            # Enviar el mensaje de texto
            message = client.messages.create(
                body=mensaje,
                from_='+14178554277',
                to=celular
            )

            # Almacenar el código enviado por Twilio en una variable de instancia
            self.codigo_enviado_por_twilio = codigo

            messagebox.showinfo("Recuperación de Contraseña", "Mensaje enviado correctamente.")
            return codigo
        except Exception as e:
            messagebox.showerror("Recuperación de Contraseña", f"Error al enviar el mensaje: {str(e)}")
            return None
        
    # Método para verificar el codigo ingresado por el bibliotecario
    def verificar_codigo_ingresado(self):
        codigo_enviado = self.codigo_enviado_por_twilio
        codigo_ingresado = self.codigo_ingresado.get()
        if codigo_ingresado == codigo_enviado:
            messagebox.showinfo("Recuperación de Contraseña", "Los códigos coinciden")
            self.mostrar_actualizar_contraseña()
        else:
            messagebox.showerror("Recuperación de Contraseña", "Los códigos no coinciden")
    
    def mostrar_actualizar_contraseña(self):
        self.contraseña_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Ingrese su nueva contraseña: ", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.contraseña_label.place(x=25, y=240)

        self.contraseña_entry = ck.CTkEntry(master=self.frame_recuperar_contraseña, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.contraseña_entry.place(x=35, y=280)

        self.confirmar_contraseña_label = ck.CTkLabel(master=self.frame_recuperar_contraseña, text="Confirme su contraseña: ", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.confirmar_contraseña_label.place(x=40, y=320)

        self.contraseña_entry_confirmar = ck.CTkEntry(master=self.frame_recuperar_contraseña, width=250, height=30, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.contraseña_entry_confirmar.place(x=35, y=360)

        # Este es un checkbox para mostrar la contraseña que estamos ingresando
        self.mostrarContraseña_Registro = tk.BooleanVar()
        self.mostrar_contraseña_checkbox = ck.CTkCheckBox(master=self.frame_recuperar_contraseña, text="Mostrar contraseña", variable=self.mostrarContraseña_Registro, command=self.mostrarContraseñaRegistro, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.mostrar_contraseña_checkbox.place(x=75, y=400)

        self.actualizar_contraseña_button = ck.CTkButton(master = self.frame_recuperar_contraseña, command=self.actualizar_contraseña, text="Actualizar contraseña", font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"))
        self.actualizar_contraseña_button.place(x=75, y=440)
        
    def actualizar_contraseña(self):
        celular = self.numero_celular_entry.get()
        contraseña = self.contraseña_entry.get()
        confirmar_contraseña = self.contraseña_entry_confirmar.get()
        if contraseña != confirmar_contraseña:
            messagebox.showerror("Recuperación de contraseña", "Las contraseñas no coinciden.")
        if self.bd.actualizarContraseñaBibliotecario(str(celular), contraseña):
            self.withdraw()  # Oculta la ventana de registro 
        self.parent.deiconify()  # Muestra la ventana de login
        self.destroy()

    def volverLogin(self):
        self.destroy()
        self.parent.deiconify()

    # Método para mostrar la contraseña al presionar el Checkbox
    def mostrarContraseñaRegistro(self):
        # Cambia la visibilidad de la contraseña basado en el estado del checkbox
        if self.mostrarContraseña_Registro.get():
            self.contraseña_entry.configure(show="")
            self.contraseña_entry_confirmar.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")
            self.contraseña_entry_confirmar.configure(show="*")

# Ventana Login
class Frame(ck.CTkFrame):
    def __init__(self, root=None):
        super().__init__(root)
        self.root = root
        self.bd = BD()
        self.bd.conectar()

        self.correo_actual = None

        # ================ IMAGEN DE FONDO ====================
        imagen_fondo_login = ck.CTkImage(Image.open("img\\image_1.png"), size=(1000, 600))
        bg_imagenLogin = ck.CTkLabel(
            self,
            image=imagen_fondo_login,
            text=""
        )
        bg_imagenLogin.place(x=120, y=28)

        # ================ NOMBRE DE LA APP ====================
        Login_headerText_image_left = ck.CTkImage(Image.open("img\\libros.ico"), size=(80, 80))
        Login_headerText_image_label1 = ck.CTkLabel(
            bg_imagenLogin,
            text="",
            image=Login_headerText_image_left,
            bg_color="#272A37"
            #bg="#272A37"
        )
        Login_headerText_image_label1.place(x=30, y=20)

        Login_headerText1 = Label(
            bg_imagenLogin,
            text="Biblioteca Virtual",
            fg="#FFFFFF",
            font=ck.CTkFont(size=26, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        Login_headerText1.place(x=110, y=42)

        # ================ LOGIN TO ACCOUNT HEADER ====================
        loginAccount_header = Label(
            bg_imagenLogin,
            text="Inicia Sesión para continuar",
            fg="#FFFFFF",
            font=ck.CTkFont(size=18, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        loginAccount_header.place(x=75, y=121)

        # ================ NO ESTA REGISTRADO? ====================
        self.login_label = Label(
            bg_imagenLogin,
            text="¿No estás registrado?",
            fg="#FFFFFF",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        self.login_label.place(x=75, y=187)

        # ================ REGISTRARSE ====================
        self.registrarse_button = Button(
            bg_imagenLogin,
            text="Registrarse",
            fg="#206DB4",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37",
            bd=0,
            cursor="hand2",
            activebackground="#272A37",
            activeforeground="#ffffff",
            command=lambda: self.abrir_ventana_registro()
        )
        self.registrarse_button.place(x=260, y=185, width=85, height=35)

        # ================ Sección Email ====================
        Login_rut_imagen = ck.CTkImage(Image.open("img\\email.png"), size=(400, 50))
        Login_rut_imagen_Label = ck.CTkLabel(
            bg_imagenLogin,
            image=Login_rut_imagen,
            bg_color="#272A37",
            text=""
        )
        Login_rut_imagen_Label.place(x=76, y=242)

        Login_emailName_text = Label(
            Login_rut_imagen_Label,
            text="Email account: ",
            fg="white",
            font=ck.CTkFont(size=13, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        Login_emailName_text.place(x=25, y=0)

        self.correo = Entry(
            Login_rut_imagen_Label,
            bd=0,
            bg="#3D404B",
            fg="white",
            highlightthickness=0,
            font=ck.CTkFont(size=16, weight="bold", family="Segoe UI Historic"),
        )
        self.correo.place(x=8, y=17, width=354, height=27)

        # ================ Sección Contraseña ====================
        Login_passwordName_image = ck.CTkImage(Image.open("img\\email.png"), size=(400, 50))
        Login_passwordName_image_Label = ck.CTkLabel(
            bg_imagenLogin,
            image=Login_passwordName_image,
            bg_color="#272A37",
            text=""
        )
        Login_passwordName_image_Label.place(x=80, y=330)

        Login_passwordName_text = Label(
            Login_passwordName_image_Label,
            text="Contraseña",
            fg="#FFFFFF",
            font=ck.CTkFont(size=13, weight="bold", family="Segoe UI Historic"),
            bg="#3D404B"
        )
        Login_passwordName_text.place(x=25, y=0)

        self.contraseña_entry = Entry(
            Login_passwordName_image_Label,
            bd=0,
            bg="#3D404B",
            highlightthickness=0,
            font=ck.CTkFont(size=16, weight="bold", family="Segoe UI Historic"),
            fg="white"
        )
        self.contraseña_entry.place(x=8, y=17, width=354, height=27)
        self.contraseña_entry.bind("<Return>", self.login)

        # Checkbox para mostrar/ocultar la contraseña
        self.mostrar_contraseña = tk.BooleanVar()
        self.checkbox_mostrar_contraseña = ck.CTkCheckBox(master=self, 
            text="Mostrar contraseña", 
            variable=self.mostrar_contraseña, 
            command=self.mostrarContraseña, 
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg_color="#272A37"
        )
        self.checkbox_mostrar_contraseña.place(x=610, y=370)

        # =============== INICIAR SESIÓN BUTTON ====================
        self.login_button = ck.CTkButton(
            bg_imagenLogin,
            text="Iniciar Sesión",
            font=ck.CTkFont(size=25, weight="bold", family="Segoe UI Historic"),
            width=350, 
            height=65,
            corner_radius=15,
            command=lambda: self.login()
        )
        self.login_button.place(x=100, y=445)

        # ================ Desarrolladores ====================
        desarrolladores_image = ck.CTkImage(Image.open("img\\headerText_image.png"), size=(30, 30))
        desarrolladores_image_label = ck.CTkLabel(
            bg_imagenLogin,
            image=desarrolladores_image,
            bg_color="#272A37",
            text=""
        )
        desarrolladores_image_label.place(x=660, y=535)

        desarrolladores_label = Label(
            bg_imagenLogin,
            text="Desarrollado por Aesir",
            fg="#FFFFFF",
            font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        desarrolladores_label.place(x=700, y=530)

        # ================ Olvido su contraseña? ====================
        self.recuperar_contraseña_button = Button(
            bg_imagenLogin,
            text="¿Olvidaste tu contraseña?",
            fg="#206DB4",
            font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"),
            bg="#272A37",
            bd=0,
            activebackground="#272A37",
            activeforeground="#ffffff",
            cursor="hand2",
            command=lambda: self.abrir_ventana_recuperar_contraseña(),
        )
        self.recuperar_contraseña_button.place(x=190, y=400, width=190, height=35)

        # ================ VERSIÓN ====================
        version_label = Label(
            bg_imagenLogin,
            text="Versión 1.0.0",
            fg="#FFFFFF",
            font=ck.CTkFont(size=12, weight="bold", family="Segoe UI Historic"),
            bg="#272A37"
        )
        version_label.place(x=15, y=572)

    def login(self, event=None):
        correo = self.correo.get()
        contraseña = self.contraseña_entry.get()

        if not correo:
            messagebox.showerror("Error de inicio de sesión", "Debe ingresar un correo.")
            return

        # Verifica si el correo existe en la base de datos
        if self.bd.login(correo, contraseña):
            self.root.withdraw()
            ventana_principal = VentanaPrincipal(self.root, correo)
            self.root.wait_window(ventana_principal)
            self.limparCampos()

    def mostrarContraseña(self):
        if self.mostrar_contraseña.get():
            self.contraseña_entry.configure(show="")
        else:
            self.contraseña_entry.configure(show="*")

    def abrir_ventana_registro(self):
        self.root.withdraw()
        ventana_registro = VentanaRegistro(self.root)
        self.root.wait_window(ventana_registro)

    def abrir_ventana_recuperar_contraseña(self):
        self.root.withdraw()
        ventana_recuperar_contraseña = VentanaRecuperarContraseña(self.root)
        self.root.wait_window(ventana_recuperar_contraseña)

    def limparCampos(self):
        self.correo.delete(0, 'end')
        self.contraseña_entry.delete(0, 'end')
        
# Ventana principal de la aplicación
class VentanaPrincipal(ck.CTkToplevel):
    def __init__(self, parent, correo_actual = None):
        super().__init__(parent)
        self.parent = parent
        self.bd = BD() #Conexión a la base de datos
        self.correo_actual = correo_actual # Obtener el correo del bibliotecario logeado
        self.after(250, lambda: self.iconbitmap('img\libros.ico'))
        self.title("Biblioteca Virtual")
        self.resizable(0, 0)

        self.prestamo_seleccionado = None

        # Variables para el Frame de stock
        self.stockLibro = ck.IntVar(value="")
        self.numero_paginas = ck.IntVar(value="")
        self.titulo = ck.StringVar()
        self.isbn = ck.StringVar()
        self.buscar_actualiza = ck.StringVar()

        # Variables para el Frame Realizar Préstamo
        self.rut_usuario = ck.StringVar()
        self.tipo_usuario = ck.StringVar()

        # Variables para el Frame Registrar Usuario
        self.nombre_usuario = ck.StringVar()
        self.apellido_ususario = ck.StringVar()
        self.direccion_usuario = ck.StringVar()
        self.codigo_pais = ck.IntVar(value="+56 9")
        self.celular_usuario = ck.StringVar()
        self.celular_usuario.trace("w", self.validarEnTiempoReal)
        self.correo_usuario = ck.StringVar()

        # Variables para el Frame Pagar Multa
        self.multa_nombre_usuario = ck.StringVar()
        self.multa_apellido_usuario = ck.StringVar()
        self.multa_rut_usuario = ck.StringVar()
        self.multa_celular_usuario = ck.StringVar()
        self.multa_correo_usuario = ck.StringVar()
        self.multa_tipo_usuario = ck.StringVar()
        self.multa_multa_usuario = ck.StringVar()
        self.multa_monto_usuario = ck.StringVar()
        self.multa_isbn_usuario = ck.StringVar()

        # Crear Frame lateral izquierdo para la navegación
        self.frameNavegacion = ck.CTkFrame(self, corner_radius=0)
        self.frameNavegacion.grid(row=0, column=0, sticky="nsew")
        self.frameNavegacion.grid_rowconfigure(8, weight=1)

        # Imágenes para el menu de navegación
        logo_imagen = ck.CTkImage(Image.open("img\\libros.ico"), size=(30, 30))
        inicio_imagen = ck.CTkImage(Image.open("img\\home.ico"), size=(28, 28))
        cerrar_sesion_imagen = ck.CTkImage(Image.open("img\\cerrar_sesion.ico"))
        inicio_imagen_frame = ck.CTkImage(Image.open("img\\retrasos_en_prestamo.ico"), size=(450, 120))
        catalogo_libro_icono = ck.CTkImage(Image.open("img\\catalogo_libros.ico"), size=(28, 28))
        catalogo_imagen = ck.CTkImage(Image.open("img\\catalogo_de_libros.ico"), size=(450, 120))
        stock_imagen_icono = ck.CTkImage(Image.open("img\\stock.ico"), size=(28, 28))
        actualizar_stock_imagen = ck.CTkImage(Image.open("img\\actualizar_stock.ico"), size=(450, 120))
        realizar_prestamo_imagen = ck.CTkImage(Image.open("img\\realizar_prestamo.ico"), size=(450, 120))
        realizar_prestamo_icono = ck.CTkImage(Image.open("img\\realizar_prestamo_icono.ico"), size=(28, 28))
        libros_en_prestamo_image = ck.CTkImage(Image.open("img\\libros_en_prestamo.ico"), size=(450, 120))
        libros_en_prestamo_icono = ck.CTkImage(Image.open("img\\libros_prestamo.ico"), size=(28, 28))
        prestamos_por_usuario_image = ck.CTkImage(Image.open("img\\prestamos_por_usuario.ico"), size=(450, 120))
        prestamos_por_usuario_image_icon = ck.CTkImage(Image.open("img\\prestamos_por_usuario_icono.ico"), size=(28, 28))
        renovar_libro_icono = ck.CTkImage(Image.open("img\\renovar_libro.ico"), size=(28, 28))
        renovar_libro_image_titulo = ck.CTkImage(Image.open("img\\renovar_libro_titulo.ico"), size=(450, 120))
        registrar_usuario_icono = ck.CTkImage(Image.open("img\\registrarse.ico"), size=(28, 28))
        usuario_image = ck.CTkImage(Image.open("img\\usuarios.ico"), size=(28, 28))
        usuarios_registrados_image = ck.CTkImage(Image.open("img\\usuarios_registrados.ico"), size=(450, 120))
        registrar_usuario_imagen = ck.CTkImage(Image.open("img\\registrar_usuario.ico"), size=(450, 120))
        pagar_multa_icono = ck.CTkImage(Image.open("img\\pagar_multa.ico"), size=(28, 28))
        pagar_multa_imagen = ck.CTkImage(Image.open("img\\pagar_multa_imagen.ico"), size=(450, 120))
        devolver_libros_imagen = ck.CTkImage(Image.open("img\\devolver_libros_imagen.ico"), size=(450, 120))
        devolver_libros_icono = ck.CTkImage(Image.open("img\\devolver_libros_icono.ico"), size=(28, 28))

        # Crear icono en frame lateral
        self.frameNavegacion_label = ck.CTkLabel(self.frameNavegacion, text="  Biblioteca Virtual", image=logo_imagen,
                                                  compound="left", font=ck.CTkFont(size=30, weight="bold", family="Segoe UI Historic"))
        self.frameNavegacion_label.grid(row=0, column=0, padx=20, pady=20)

        # Botón de Inicio en navegación
        self.inicio_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Inicio",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=inicio_imagen, anchor="w",
                                        command=self.inicio_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.inicio_button.grid(row=1, column=0, sticky="ew")

        # Botón de Catalogo en navegación
        self.catalogo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Catalogo",
                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                        hover_color=("gray70", "gray30"), image=catalogo_libro_icono, anchor="w",
                                        command=self.catalogo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.catalogo_button.grid(row=2, column=0, sticky="ew")

        # Botón de Stock en navegación
        self.stock_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Actualizar Stock",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"), image=stock_imagen_icono, anchor="w",
                                         command=self.stock_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.stock_button.grid(row=3, column=0, sticky="ew")

        # Botón de Realizar prestamos en navegación
        self.realizar_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Realizar Prestamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=realizar_prestamo_icono, anchor="w",
                                           command=self.realizarPrestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.realizar_prestamo_button.grid(row=4, column=0, sticky="ew")

        # Botón de Frame Libros en Préstamo
        self.frame_libros_en_prestamo_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Libros en Préstamo", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=libros_en_prestamo_icono, anchor="w",
                                           command=self.frame_libros_en_prestamo_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.frame_libros_en_prestamo_button.grid(row=5, column=0, sticky="ew")

        # Botón de frame Prestamos por Usuario
        self.prestamos_por_usuario_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Préstamos por Usuario", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=prestamos_por_usuario_image_icon, anchor="w",
                                           command=self.frame_prestamos_por_usuario_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.prestamos_por_usuario_button.grid(row=6, column=0, sticky="ew")

        # Botón de Frame Renovar Libro
        self.frame_renovar_libro_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Renovación de Días para Libro", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=renovar_libro_icono, anchor="w",
                                           command=self.frame_renovar_libro_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.frame_renovar_libro_button.grid(row=7, column=0, sticky="ew")

        # Botón de Frame Registrar Usuario
        self.frame_registrar_usuario_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10,
                                           text="Registrar Usuario", fg_color="transparent", text_color=("gray10", "gray90"),
                                           hover_color=("gray70", "gray30"), image=registrar_usuario_icono, anchor="w",
                                           command=self.frame_registrar_usuario_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.frame_registrar_usuario_button.grid(row=8, column=0, sticky="ew")

        # Botón de Frame Usuarios en navegación
        self.usuarios_registrados_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Usuarios Registrados",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=usuario_image, anchor="w",command=self.usuarios_registrados_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.usuarios_registrados_button.grid(row=10, column=0, sticky="ew")

        # Botón de Frame Pagar Multa
        self.frame_pagar_multa_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Pagar Multas",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=pagar_multa_icono, anchor="w",command=self.pagar_multa_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.frame_pagar_multa_button.grid(row=11, column=0, sticky="ew")

        self.frame_devolver_libro_button = ck.CTkButton(self.frameNavegacion, corner_radius=0, height=40, border_spacing=10, text="Devolver Libros",
                                           fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           image=devolver_libros_icono, anchor="w",command=self.devolver_libro_button_evento, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.frame_devolver_libro_button.grid(row=12, column=0, sticky="ew")

        # Menu de opciones para cambiar de apariencia la app
        self.menu_apariencia = ck.CTkOptionMenu(self.frameNavegacion, font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"), values=["Dark", "Light"], command=self.evento_cambiar_apariencia)
        self.menu_apariencia.grid(row=13, column=0, padx=20, pady=20, sticky="s")

        # Botón para cerrar sesión
        self.button_cerrarSesion = ck.CTkButton(self.frameNavegacion, font=ck.CTkFont(size=18, weight="bold", family="Segoe UI Historic"), text="Cerrar sesión", image=cerrar_sesion_imagen, command=self.cerrar_sesion)
        self.button_cerrarSesion.grid(row=14, column=0, padx=20, pady=20, sticky="s")

        # Contenedor main para los frames
        self.main_frame = ck.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # ******************FRAME INICIO APP******************
        self.inicio_frame = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.inicio_frame.grid(row=0, column=0, sticky="nsew")
        self.inicio_frame.grid_columnconfigure(0, weight=1)
        self.inicio_frame.grid_rowconfigure(1, weight=1)

        self.inicio_label_image = ck.CTkLabel(self.inicio_frame, text="", image=inicio_imagen_frame)
        self.inicio_label_image.grid(row=0, columnspan=1, padx=20)

        # Crear el DateEntry con el date_pattern en año/mes/día
        self.date_entry = DateEntry(self.inicio_frame, width=11,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.date_entry.place(x=50, y=80)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Crear el Frame contenedor del Treeview y el Scrollbar
        self.treeview_frame_inicio = ck.CTkFrame(self.inicio_frame)
        self.treeview_frame_inicio.grid(row=1, columnspan=3, padx=20, pady=5, sticky="nsew")

        self.tabla_inicio = ttk.Treeview(self.treeview_frame_inicio)
        self.tabla_inicio.grid(row=0, column=0, sticky="nsew")

        ladoy = ttk.Scrollbar(self.treeview_frame_inicio, orient='vertical', command=self.tabla_inicio.yview)
        ladoy.grid(row=0, column=1, sticky='ns')

        self.treeview_frame_inicio.grid_rowconfigure(0, weight=1)
        self.treeview_frame_inicio.grid_columnconfigure(0, weight=1)
        
        # Columnas que se mostrarán en la tabla
        self.tabla_inicio.grid(sticky="nsew")
        self.tabla_inicio['columns'] = ('Nombre', 'Apellido', 'RUT', 'Tipo de usuario', 'F. Devolución', 'ISBN', 'Titulo', 'Multa', 'Monto')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_inicio.column('#0', minwidth=60, width=70, anchor='center')
        self.tabla_inicio.column('Nombre', minwidth=100, width=130, anchor='center')
        self.tabla_inicio.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_inicio.column('RUT', minwidth=100, width=120, anchor='center')
        self.tabla_inicio.column('Tipo de usuario', minwidth=130, width=105, anchor='center')
        self.tabla_inicio.column('F. Devolución', minwidth=130, width=105, anchor='center')
        self.tabla_inicio.column('ISBN', minwidth=60, width=70, anchor='center')
        self.tabla_inicio.column('Titulo', minwidth=100, width=120, anchor='center')
        self.tabla_inicio.column('Multa', minwidth=100, width=120, anchor='center')
        self.tabla_inicio.column('Monto', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_inicio.heading('#0', text='Id', anchor='center')
        self.tabla_inicio.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_inicio.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_inicio.heading('RUT', text='RUT', anchor='center')
        self.tabla_inicio.heading('Tipo de usuario', text='Tipo de usuario', anchor='center')
        self.tabla_inicio.heading('F. Devolución', text='F. Devolución', anchor='center')
        self.tabla_inicio.heading('ISBN', text='ISBN', anchor='center')
        self.tabla_inicio.heading('Titulo', text='Titulo', anchor='center')
        self.tabla_inicio.heading('Multa', text='Multa', anchor='center')
        self.tabla_inicio.heading('Monto', text='Monto', anchor='center')

        self.actualizar_button = ck.CTkButton(self.inicio_frame, text='ACTUALIZAR TABLA', font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"), command=self.mostrarDatosPrestamo) # 
        self.actualizar_button.grid(columnspan=1, row=2, pady=5)

        # ******************FRAME MODIFICAR CATALOGO******************
        self.catalogo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.catalogo.grid(row=0, column=0, sticky="nsew")
        self.catalogo.grid_columnconfigure(5, weight=1)
        self.catalogo.grid_rowconfigure(2, weight=2)

        self.catalogo_image_label = ck.CTkLabel(self.catalogo, text="", image=catalogo_imagen)
        self.catalogo_image_label.grid(row=0, column=0, columnspan=6, padx=20)

        self.buscar_categoria_label = ck.CTkLabel(self.catalogo, text="Seleccione categoría:",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_categoria_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Obtener todas las categorías de la base de datos
        categorias = self.bd.obtenerCategorias()
        if categorias is None:
            categorias = []
        categorias.insert(0, "Mostrar Todos")

        self.categoria = ttk.Combobox(self.catalogo, values=categorias,
                                    font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.categoria.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Configurar evento de selección de categoría
        self.categoria.bind("<<ComboboxSelected>>", self.seleccionarCategoria)

        self.buscar_nombre_libro_label = ck.CTkLabel(self.catalogo, text="Ingrese el nombre del libro:",
                                                    font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_nombre_libro_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.buscar_nombre_libro_entry = ck.CTkEntry(self.catalogo, placeholder_text="Con mayus y minus", width=200,
                                                    font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_nombre_libro_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        self.buscar_nombre_libro_entry.bind("<Return>", self.buscarLibroNombre)

        self.buscar_isbn_libro_label = ck.CTkLabel(self.catalogo, text="Ingrese el ISBN del libro:",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_isbn_libro_label.grid(row=1, column=4, padx=10, pady=10, sticky="w")

        self.buscar_isbn_libro_entry = ck.CTkEntry(self.catalogo, placeholder_text="Ej: l-001", width=100,
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_isbn_libro_entry.grid(row=1, column=5, padx=10, pady=10, sticky="w")
        self.buscar_isbn_libro_entry.bind("<Return>", self.buscarLibroIsbn)

        self.frame_imagenes_catalogo = ck.CTkFrame(self.catalogo, corner_radius=0, fg_color="transparent")
        self.frame_imagenes_catalogo.grid(row=2, column=0, padx=10, pady=3, columnspan=6, sticky="nsew")

        self.canvas = tk.Canvas(self.frame_imagenes_catalogo, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        ladox = ttk.Scrollbar(self.frame_imagenes_catalogo, orient="horizontal", command=self.canvas.xview)
        ladox.grid(row=1, column=0, sticky="ew")

        ladoy = ttk.Scrollbar(self.frame_imagenes_catalogo, orient="vertical", command=self.canvas.yview)
        ladoy.grid(row=0, column=1, sticky="ns")

        self.canvas.grid_rowconfigure(0, weight=2)
        self.canvas.grid_columnconfigure(0, weight=1)
        self.canvas.grid(sticky="nsew")
        
        self.frame_imagenes = ck.CTkFrame(self.canvas, corner_radius=0, fg_color="transparent")
        self.canvas.create_window((0, 0), window=self.frame_imagenes, anchor="center")

        libros = self.bd.obtenerLibrosCatalogo() # Obtener los libros desde la base de datos

        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 8, column=i % 8, padx=10, pady=10, sticky="nsew")
                self.frame_imagenes.grid_rowconfigure(i // 8, weight=2)  # Expansión vertical
                self.frame_imagenes.grid_columnconfigure(i % 8, weight=1)  # Expansión horizontal

        self.canvas.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.mostar_libros_button = ck.CTkButton(self.catalogo, text="MOSTRAR TODO",
                                                font=ck.CTkFont(size=13, weight="bold", family="Segoe UI Historic"),
                                                command=self.mostrarTodosLosLibros)
        self.mostar_libros_button.grid(row=3, columnspan=6, padx=10, pady=10, sticky="se")

        # ******************FRAME ACTUALIZAR STOCK******************
        self.frame_stock = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_stock.grid(row=0, column=0, sticky="nsew")
        self.frame_stock.grid_rowconfigure(8, weight=1)
        self.frame_stock.grid_columnconfigure(8, weight=1)

        self.frame_imagen_stock = ck.CTkFrame(self.frame_stock, corner_radius=0, fg_color="transparent")
        self.frame_imagen_stock.grid(row=0, column=0, sticky="nsew")
        self.frame_imagen_stock.grid_columnconfigure(3, weight=1)

        self.actualizar_stock_label_image = ck.CTkLabel(self.frame_imagen_stock, text="", image=actualizar_stock_imagen)
        self.actualizar_stock_label_image.grid(row=0, column=3, columnspan=2)

        self.buscar_libro_isbn_label = ck.CTkLabel(self.frame_stock, text="Ingrese el ISBN del libro para actualizar stock: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_libro_isbn_label.grid(row=1, column=0, padx=10, pady=0)

        self.buscar_libro_isbn_entry = ck.CTkEntry(self.frame_stock, width=140, textvariable=self.buscar_actualiza, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_libro_isbn_entry.grid(row=1, column=1, padx=10)
        self.buscar_libro_isbn_entry.bind("<Return>", self.buscarLibroStock) # Al presionar enter, me devuelve el dato solicitado

        # Botón para buscar el libro
        self.buscar_libro_isbn_button = ck.CTkButton(self.frame_stock, command=self.buscarLibroStock, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_libro_isbn_button.grid(row=1, column=2, padx=3)

        # Widgets del frame stock a mostrar
        self.isbn_label = ck.CTkLabel(self.frame_stock, text="ISBN: ",
                        font=ck.CTkFont(size=20, weight="bold"))
        self.isbn_label.grid(row=2, column=0, pady=5)

        self.isbn_entry = ck.CTkEntry(self.frame_stock, width=140, textvariable=self.isbn, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"), state="disabled")
        self.isbn_entry.grid(row=2, columnspan=7, padx=10, pady=5)
        
        self.titulo_label = ck.CTkLabel(self.frame_stock, text="Titulo: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.titulo_label.grid(row=4, column=0, pady=5)

        self.titulo_entry = ck.CTkEntry(self.frame_stock, width=200, textvariable=self.titulo, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"), state="disabled")
        self.titulo_entry.grid(row=4, columnspan=7, padx=10, pady=5)

        self.numero_paginas_label = ck.CTkLabel(self.frame_stock, text="N° de Paginas: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.numero_paginas_label.grid(row=6, column=0, pady=5)

        self.numero_paginas_entry = ck.CTkEntry(self.frame_stock, width=140, textvariable=self.numero_paginas, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"), state="disabled")
        self.numero_paginas_entry.grid(row=6, columnspan=7, padx=10, pady=5)

        # Campo que se va a actualizar
        self.stock_label = ck.CTkLabel(self.frame_stock, text="Stock: ",
                        font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.stock_label.grid(row=7, column=0, pady=5)

        self.stock_entry = ck.CTkEntry(self.frame_stock, width=140, textvariable=self.stockLibro, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.stock_entry.grid(row=7, columnspan=7, padx=10, pady=5)
        self.stock_entry.bind("<Return>", self.actualizarStock)

        # Botón para actualizar el stock del libro
        self.actualizar_stock_button = ck.CTkButton(self.frame_stock, command=self.actualizarStock, text="ACTUALIZAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.actualizar_stock_button.grid(row=27, column=2, columnspan=4, padx=10, pady=10)

        # ******************FRAME REALIZAR PRESTAMO******************
        self.frame_realizar_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_realizar_prestamo.grid(row=0, column=0, sticky="nsew")

        self.realizar_prestamo_label_image = ck.CTkLabel(self.frame_realizar_prestamo, text="", image=realizar_prestamo_imagen)
        self.realizar_prestamo_label_image.grid(row=0, columnspan=3, padx=20)

        self.rut_usuario_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Ingrese el RUT del Usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.rut_usuario_label.grid(row=10, column=0, pady=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.rut_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.rut_usuario_entry.grid(row=10, column=1, pady=5)
        self.rut_usuario_entry.bind("<Return>", self.obtenerTipoUsuario) # Al presionar enter, me devuelve el dato solicitado

        # Botón para buscar al usuario por el rut
        self.buscar_usuario_rut = ck.CTkButton(self.frame_realizar_prestamo, command=self.obtenerTipoUsuario, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.buscar_usuario_rut.grid(row=10, column=2, padx=3)

        self.isbn_libro_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Ingrese el ISBN del Libro: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.isbn_libro_label.grid(row=11, column=0, pady=5)

        self.isbn_libro_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.isbn, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.isbn_libro_entry.grid(row=11, column=1, padx=5)

        self.fecha_inicio_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Inicio de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.fecha_inicio_label.grid(row=12, column=0, pady=5)

        self.fecha_inicio = DateEntry(self.frame_realizar_prestamo, width=11,
                        date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"),
                        highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_inicio.grid(row=12, column=1, pady=5)

        self.fecha_devolucion_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Fecha Devolución de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.fecha_devolucion_label.grid(row=13, column=0, pady=5)

        self.fecha_devolucion = DateEntry(self.frame_realizar_prestamo, width=11,
                        date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"),
                        highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_devolucion.grid(row=13, column=1, pady=5)

        self.tipo_usuario_label = ck.CTkLabel(self.frame_realizar_prestamo, text="Tipo de Usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.tipo_usuario_label.grid(row=14, column=0, pady=5)

        self.tipo_usuario_entry = ck.CTkEntry(self.frame_realizar_prestamo, textvariable=self.tipo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.tipo_usuario_entry.grid(row=14, column=1, padx=5)

        # Crear el Frame contenedor del Treeview y el Scrollbar
        treeview_frame = ck.CTkFrame(self.frame_realizar_prestamo)
        treeview_frame.grid(row=15, columnspan=3, padx=20, pady=5)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Crear el Treeview dentro del Frame
        self.treeview_prestamos = ttk.Treeview(treeview_frame, columns=("rut", "isbn", "f.inicio", "f.devolución", "tipo de usuario"), show="headings")
        self.treeview_prestamos.heading("rut", text="RUT")
        self.treeview_prestamos.heading("isbn", text="ISBN")
        self.treeview_prestamos.heading("f.inicio", text="F.inicio")
        self.treeview_prestamos.heading("f.devolución", text="F.devolución")
        self.treeview_prestamos.heading("tipo de usuario", text="Tipo de Usuario")
        self.treeview_prestamos.pack(side="left", fill="both", expand=True)

        # Crear el Scrollbar vertical
        scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical", command=self.treeview_prestamos.yview)
        scrollbar.pack(side="right", fill="y")

        # Configurar el Scrollbar en el Treeview
        self.treeview_prestamos.configure(yscrollcommand=scrollbar.set)

        # Centrar los datos en cada columna
        columns = ("rut", "isbn", "f.inicio", "f.devolución", "tipo de usuario")
        for column in columns:
            self.treeview_prestamos.column(column, anchor="center")

        # Botón que agregará el libro a la tabla
        self.agregar_libro_button = ck.CTkButton(self.frame_realizar_prestamo, command=self.agregarLibro, text="Agregar", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.agregar_libro_button.grid(row=16, column=0, pady=5)

        #Botón que eliminará el libro de la tabla
        self.eliminar_libro_button = ck.CTkButton(self.frame_realizar_prestamo, command=self.eliminarLibro, text="Eliminar", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.eliminar_libro_button.grid(row=16, column=1, pady=5)

        # Botón que realizara el préstamo
        self.completar_prestamo_button = ck.CTkButton(self.frame_realizar_prestamo, command=self.realizarPrestamo, text="REALIZAR PRÉSTAMO", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"))
        self.completar_prestamo_button.grid(row=17, column=2, padx=5, pady=5)

        # ******************FRAME LIBROS EN PRÉSTAMO******************
        self.frame_libros_en_prestamo = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")
        self.frame_libros_en_prestamo.grid_columnconfigure(0, weight=1) # Expansión horizontal
        self.frame_libros_en_prestamo.grid_rowconfigure(1, weight=1) # Expansión vertical

        self.librosPrestamos_label_image = ck.CTkLabel(self.frame_libros_en_prestamo, text="", image=libros_en_prestamo_image)
        self.librosPrestamos_label_image.grid(row=0, columnspan=1, padx=20)

        actualizar_librosPrestamo_button = ck.CTkButton(self.frame_libros_en_prestamo, text='ACTUALIZAR TABLA LIBROS EN PRÉSTAMO', font=ck.CTkFont(size=15, weight="bold", family="Segoe UI Historic"), command=self.mostrarDatosLibros)
        actualizar_librosPrestamo_button.grid(columnspan=1, row=2, pady=5)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Mostrar la tabla en el frame libros en prestamo
        self.frame_tabla_dos = ck.CTkFrame(self.frame_libros_en_prestamo, corner_radius=0, fg_color="transparent")
        self.frame_tabla_dos.grid(column=0, row=1, sticky='nsew', padx=10, pady=5)

        self.tabla_dos = ttk.Treeview(self.frame_tabla_dos)
        self.tabla_dos.grid(column=0, row=0, sticky='nsew')

        ladoy = ttk.Scrollbar(self.frame_tabla_dos, orient='vertical', command=self.tabla_dos.yview)
        ladoy.grid(column=1, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame y la tabla
        self.frame_tabla_dos.grid_rowconfigure(0, weight=1)
        self.frame_tabla_dos.grid_columnconfigure(0, weight=1)
        
        # Columnas que se mostrarán en la tabla
        self.tabla_dos.grid(sticky='nsew')
        self.tabla_dos['columns'] = ('Titulo', 'Estado')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_dos.column('#0', minwidth=60, width=70, anchor='center')
        self.tabla_dos.column('Titulo', minwidth=100, width=130, anchor='center')
        self.tabla_dos.column('Estado', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_dos.heading('#0', text='ISBN', anchor='center')
        self.tabla_dos.heading('Titulo', text='Titulo', anchor='center')
        self.tabla_dos.heading('Estado', text='Estado', anchor='center')

        self.tabla_dos.bind("<<TreeviewSelect>>", self.obtener_filaLibros)

        # ******************FRAME PRESTAMOS POR USUARIO******************
        self.frame_prestamos_por_usuario = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_prestamos_por_usuario.grid(row=0, column=0, sticky="nsew")

        self.frame_prestamos_por_usuario_image = ck.CTkLabel(self.frame_prestamos_por_usuario, text="", image=prestamos_por_usuario_image)
        self.frame_prestamos_por_usuario_image.grid(row=0, columnspan=3, padx=20)

        self.rut_usuario_prestamos_label = ck.CTkLabel(self.frame_prestamos_por_usuario, text="Ingrese el RUT del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_prestamos_label.grid(row=1, column=0, pady=5, padx=5, sticky="e")

        self.rut_usuario_prestamos_entry = ck.CTkEntry(self.frame_prestamos_por_usuario, width=200, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_prestamos_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.rut_usuario_prestamos_entry.bind("<Return>", self.mostrarDatosPrestamoPorRut)

        self.buscar_usuario_prestamo_button = ck.CTkButton(self.frame_prestamos_por_usuario, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.mostrarDatosPrestamoPorRut)
        self.buscar_usuario_prestamo_button.grid(row=1, column=2, pady=5, padx=5)
        
        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Mostrar la tabla en el frame prestamos por usuario
        self.frame_tabla_tres = ck.CTkFrame(self.frame_prestamos_por_usuario)
        self.frame_tabla_tres.grid(column=0, row=2, columnspan=3, sticky='nsew', padx=10, pady=10)

        self.tabla_tres = ttk.Treeview(self.frame_tabla_tres)
        self.tabla_tres.grid(column=0, row=0, sticky="nsew")

        ladoy = ttk.Scrollbar(self.frame_tabla_tres, orient='vertical', command=self.tabla_tres.yview)
        ladoy.grid(column=2, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame
        self.frame_prestamos_por_usuario.grid_rowconfigure(2, weight=1)
        self.frame_prestamos_por_usuario.grid_columnconfigure(0, weight=1)

        # Configurar expansión en todas las direcciones para el frame de la tabla
        self.frame_tabla_tres.grid_rowconfigure(0, weight=1)
        self.frame_tabla_tres.grid_columnconfigure(0, weight=1)

        # Configurar expansión en todas las direcciones para el treeview
        self.tabla_tres.grid(sticky='nsew')
        self.tabla_tres['columns'] = ('ISBN', 'Titulo', 'Nombre', 'Apellido', 'RUT')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_tres.column('#0', stretch=tk.NO, width=0)  # Eliminar la columna del ID
        self.tabla_tres.column('ISBN', minwidth=60, width=70, anchor='center')
        self.tabla_tres.column('Titulo', minwidth=100, width=130, anchor='center')
        self.tabla_tres.column('Nombre', minwidth=100, width=120, anchor='center')
        self.tabla_tres.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_tres.column('RUT', minwidth=100, width=105, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_tres.heading('#0', text='ID', anchor='center')
        self.tabla_tres.heading('ISBN', text='ISBN', anchor='center')
        self.tabla_tres.heading('Titulo', text='Titulo', anchor='center')
        self.tabla_tres.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_tres.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_tres.heading('RUT', text='RUT', anchor='center')

        # ******************FRAME RENOVAR LIBRO******************
        self.frame_renovar_libro = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_renovar_libro.grid(row=0, column=0, sticky="nsew")

        self.renovar_libro_image = ck.CTkLabel(self.frame_renovar_libro, text="", image=renovar_libro_image_titulo)
        self.renovar_libro_image.grid(row=0, columnspan=3, padx=20)

        self.rut_usuario_label = ck.CTkLabel(self.frame_renovar_libro, text="Ingrese el rut del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_label.grid(row=3, column=0, pady=5, padx=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_renovar_libro, textvariable=self.rut_usuario, width=200, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_entry.grid(row=3, column=1, pady=5, padx=5)

        self.isbn_label = ck.CTkLabel(self.frame_renovar_libro, text="Ingrese el ISBN del libro: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.isbn_label.grid(row=4, column=0, pady=5, padx=5)

        self.isbn_entry = ck.CTkEntry(self.frame_renovar_libro, textvariable=self.isbn, width=200, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.isbn_entry.grid(row=4, column=1, pady=5, padx=5)

        self.buscar_usuario = ck.CTkButton(self.frame_renovar_libro, text="BUSCAR USUARIO", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.obtenerFechaDevolucion)
        self.buscar_usuario.grid(row=4, column=2, pady=5, padx=5)

        self.fecha_devolucion_label = ck.CTkLabel(self.frame_renovar_libro, text="Fecha Devolución de Préstamo: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.fecha_devolucion_label.grid(row=7, column=0, pady=5, padx=5)

        self.fecha_devolucion_renovar = DateEntry(self.frame_renovar_libro, width=16,
                          date_pattern='yyyy/mm/dd', font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"),
                          highlightbackground="deep sky blue", highlightthickness=1, corner_radius=10)
        self.fecha_devolucion_renovar.grid(row=7, column=1, pady=5, padx=5)

        self.sumar_dias = ck.CTkButton(self.frame_renovar_libro, text="SUMAR DÍAS", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.sumarDiasRenovacion)
        self.sumar_dias.grid(row=7, column=2, pady=5, padx=5)

        self.renovar_libro_button = ck.CTkButton(self.frame_renovar_libro, text="RENOVAR LIBRO", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.renovarLibro)
        self.renovar_libro_button.place(x=330, y=260)

        # ******************FRAME REGISTRAR USUARIO******************
        self.frame_registrar_usuario = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_registrar_usuario.grid(row=0, column=0, sticky="nsew")

        self.registrar_usuario_image_label = ck.CTkLabel(self.frame_registrar_usuario, text="", image=registrar_usuario_imagen)
        self.registrar_usuario_image_label.grid(row=0, columnspan=2, padx=20)

        self.nombre_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el nombre del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.nombre_usuario_label.grid(row=10, column=0, pady=5, padx=5)

        self.nombre_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.nombre_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.nombre_usuario_entry.grid(row=10, column=1, pady=10, padx=5)

        self.apellido_ususario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el apellido del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.apellido_ususario_label.grid(row=11, column=0, pady=5, padx=5)

        self.apellido_ususario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.apellido_ususario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.apellido_ususario_entry.grid(row=11, column=1, pady=10, padx=5)

        self.direccion_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese la dirección del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.direccion_usuario_label.grid(row=12, column=0, pady=5, padx=5)

        self.direccion_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.direccion_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.direccion_usuario_entry.grid(row=12, column=1, pady=10, padx=5)

        self.rut_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el RUT del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_label.grid(row=13, column=0, pady=5, padx=5)

        self.rut_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.rut_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.rut_usuario_entry.grid(row=13, column=1, pady=10, padx=5)

        self.celular_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el celular del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.celular_usuario_label.grid(row=14, column=0, pady=5, padx=5)

        self.codigo_pais_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.codigo_pais, width=70, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled")
        self.codigo_pais_entry.place(x=338, y=350)

        self.celular_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.celular_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.celular_usuario_entry.grid(row=14, column=1, pady=10, padx=5)

        self.correo_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el correo electrónico del usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.correo_usuario_label.grid(row=15, column=0, pady=5, padx=5)

        self.correo_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.correo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.correo_usuario_entry.grid(row=15, column=1, pady=10, padx=5)

        self.tipo_usuario_label = ck.CTkLabel(self.frame_registrar_usuario, text="Ingrese el tipo de usuario: ",
                                                font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.tipo_usuario_label.grid(row=16, column=0, pady=5, padx=5)

        self.tipo_usuario_entry = ck.CTkEntry(self.frame_registrar_usuario, textvariable=self.tipo_usuario, width=140, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.tipo_usuario_entry.grid(row=16, column=1, pady=10, padx=5)

        self.registrar_usuario_button = ck.CTkButton(self.frame_registrar_usuario, text="REGISTRAR USUARIO", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.registrarUsuario)
        self.registrar_usuario_button.place(x=330, y=530)

        # ******************FRAME MOSTRAR USUARIOS REGISTRADOS******************
        self.frame_usuarios_registrados = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_usuarios_registrados.grid(row=0, column=0, sticky="nsew")
        self.frame_usuarios_registrados.grid_columnconfigure(0, weight=1)  # Expansión horizontal
        self.frame_usuarios_registrados.grid_rowconfigure(1, weight=1)  # Expansión vertical

        self.usuarios_registrados_label_image = ck.CTkLabel(self.frame_usuarios_registrados, text="", image=usuarios_registrados_image)
        self.usuarios_registrados_label_image.grid(row=0, columnspan=1, padx=20)

        self.actualizar_button = ck.CTkButton(self.frame_usuarios_registrados, text='ACTUALIZAR TABLA', font=ck.CTkFont(size=15, weight="bold", family="Segoe UI"), command=self.mostrarDatosUsuario)
        self.actualizar_button.grid(columnspan=1, row=2, pady=5)
        
        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Mostrar la tabla en el frame usuario
        self.frame_tabla_uno = ck.CTkFrame(self.frame_usuarios_registrados)
        self.frame_tabla_uno.grid(column=0, row=1, sticky='nsew', padx=10)

        self.tabla_uno = ttk.Treeview(self.frame_tabla_uno)
        self.tabla_uno.grid(column=0, row=0, sticky='nsew')

        ladoy = ttk.Scrollbar(self.frame_tabla_uno, orient='vertical', command=self.tabla_uno.yview)
        ladoy.grid(column=1, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame y la tabla
        self.frame_tabla_uno.grid_rowconfigure(0, weight=1)
        self.frame_tabla_uno.grid_columnconfigure(0, weight=1)
        self.tabla_uno.grid(sticky='nsew')

        # Columnas que se mostrarán en la tabla
        self.tabla_uno['columns'] = ('Nombre', 'Apellido', 'Dirección', 'RUT', 'Celular', 'Correo electrónico', 'Tipo de usuario')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_uno.column('#0', minwidth=60, width=70, anchor='center')
        self.tabla_uno.column('Nombre', minwidth=100, width=130, anchor='center')
        self.tabla_uno.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_uno.column('Dirección', minwidth=100, width=140, anchor='center')
        self.tabla_uno.column('RUT', minwidth=100, width=105, anchor='center')
        self.tabla_uno.column('Celular', minwidth=100, width=105, anchor='center')
        self.tabla_uno.column('Correo electrónico', minwidth=100, width=170, anchor='center')
        self.tabla_uno.column('Tipo de usuario', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_uno.heading('#0', text='Id', anchor='center')
        self.tabla_uno.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_uno.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_uno.heading('Dirección', text='Dirección', anchor='center')
        self.tabla_uno.heading('RUT', text='RUT', anchor='center')
        self.tabla_uno.heading('Celular', text='Celular', anchor='center')
        self.tabla_uno.heading('Correo electrónico', text='Correo electrónico', anchor='center')
        self.tabla_uno.heading('Tipo de usuario', text='Tipo de usuario', anchor='center')

        self.tabla_uno.bind("<<TreeviewSelect>>", self.obtener_filaUsuario)

        # ******************FRAME PAGAR MULTA******************
        self.frame_pagar_multa = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_pagar_multa.grid(row=0, column=0, sticky="nsew")
        self.frame_pagar_multa.grid_columnconfigure(0, weight=1)

        self.pagar_multa_imagen_label = ck.CTkLabel(self.frame_pagar_multa, text="", image=pagar_multa_imagen)
        self.pagar_multa_imagen_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.buscar_rut_multa_label = ck.CTkLabel(self.frame_pagar_multa, text="Ingrese el RUT del usuario: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.buscar_rut_multa_label.grid(row=1, columnspan=2, pady=5, padx=10, sticky="w")

        self.buscar_rut_multa_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.buscar_rut_multa_entry.place(x=330, y=148)

        self.buscar_rut_multa_button = ck.CTkButton(self.frame_pagar_multa, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.cargarDatosTablaMultas) # command=self.mostrarDatosPrestamoPorRut
        self.buscar_rut_multa_button.place(x=490, y=148)

        # Frame para el Treeview
        self.frame_tabla_multa = ck.CTkFrame(self.frame_pagar_multa)
        self.frame_tabla_multa.grid(column=0, row=2, sticky='nsew', padx=10)

        self.tabla_multa = ttk.Treeview(self.frame_tabla_multa)
        self.tabla_multa.grid(column=0, row=0, sticky='nsew')

        ladoy = ttk.Scrollbar(self.frame_tabla_multa, orient='vertical', command=self.tabla_multa.yview)
        ladoy.grid(column=1, row=0, sticky='ns')

        # Configurar expansión en todas las direcciones para el frame y la tabla
        self.frame_tabla_multa.grid_rowconfigure(1, weight=1)
        self.frame_tabla_multa.grid_columnconfigure(0, weight=1)
        self.tabla_multa.grid(sticky="nsew")

        # Columnas que se mostrarán en la tabla
        self.tabla_multa['columns'] = ('ISBN Libro', 'Nombre', 'Apellido', 'Dirección', 'RUT', 'Celular', 'Correo electrónico', 'Tipo de usuario', 'Multa', 'Monto')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_multa.column('#0', minwidth=60, width=0, anchor='center', stretch=False)
        self.tabla_multa.column('ISBN Libro', minwidth=100, width=130, anchor='center')
        self.tabla_multa.column('Nombre', minwidth=100, width=130, anchor='center')
        self.tabla_multa.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_multa.column('Dirección', minwidth=100, width=140, anchor='center')
        self.tabla_multa.column('RUT', minwidth=100, width=105, anchor='center')
        self.tabla_multa.column('Celular', minwidth=100, width=105, anchor='center')
        self.tabla_multa.column('Correo electrónico', minwidth=100, width=170, anchor='center')
        self.tabla_multa.column('Tipo de usuario', minwidth=100, width=120, anchor='center')
        self.tabla_multa.column('Multa', minwidth=100, width=120, anchor='center')
        self.tabla_multa.column('Monto', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_multa.heading('#0', text='Id', anchor='center')
        self.tabla_multa.heading('ISBN Libro', text='ISBN Libro', anchor='center')
        self.tabla_multa.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_multa.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_multa.heading('Dirección', text='Dirección', anchor='center')
        self.tabla_multa.heading('RUT', text='RUT', anchor='center')
        self.tabla_multa.heading('Celular', text='Celular', anchor='center')
        self.tabla_multa.heading('Correo electrónico', text='Correo electrónico', anchor='center')
        self.tabla_multa.heading('Tipo de usuario', text='Tipo de usuario', anchor='center')
        self.tabla_multa.heading('Multa', text='Multa', anchor='center')
        self.tabla_multa.heading('Monto', text='Monto', anchor='center')

        self.multa_nombre_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Nombre: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_nombre_usuario_label.place(x=30, y=450)

        self.multa_nombre_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_nombre_usuario)
        self.multa_nombre_usuario_entry.place(x=140, y=455)

        self.multa_apellido_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Apellido: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_apellido_usuario_label.place(x=320, y=450)

        self.multa_apellido_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_apellido_usuario)
        self.multa_apellido_usuario_entry.place(x=430, y=455)

        self.multa_rut_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="RUT: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_rut_usuario_label.place(x=610, y=450)

        self.multa_rut_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_rut_usuario)
        self.multa_rut_usuario_entry.place(x=670, y=452)

        self.multa_celular_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Celular: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_celular_usuario_label.place(x=850, y=450)

        self.multa_celular_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_celular_usuario)
        self.multa_celular_usuario_entry.place(x=950, y=452)

        self.multa_correo_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Correo electrónico: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_correo_usuario_label.place(x=30, y=550)

        self.multa_correo_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_correo_usuario)
        self.multa_correo_usuario_entry.place(x=264, y=555)

        self.multa_tipo_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Tipo de usuario: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_tipo_usuario_label.place(x=450, y=550)

        self.multa_tipo_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_tipo_usuario)
        self.multa_tipo_usuario_entry.place(x=650, y=555)

        self.multa_multa_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Multa: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_multa_usuario_label.place(x=850, y=550)

        self.multa_multa_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_multa_usuario)
        self.multa_multa_usuario_entry.place(x=930, y=555)

        self.multa_monto_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="Monto: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_monto_usuario_label.place(x=700, y=690)

        self.multa_monto_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_monto_usuario)
        self.multa_monto_usuario_entry.place(x=800, y=695)

        self.multa_isbn_usuario_label = ck.CTkLabel(self.frame_pagar_multa, text="ISBN: ",
                                                font=ck.CTkFont(size=25, weight="bold", family="Segoe UI"))
        self.multa_isbn_usuario_label.place(x=400, y=690)

        self.multa_isbn_usuario_entry = ck.CTkEntry(self.frame_pagar_multa, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), state="disabled", textvariable=self.multa_isbn_usuario)
        self.multa_isbn_usuario_entry.place(x=480, y=695)

        self.pagar_multa_button = ck.CTkButton(self.frame_pagar_multa, text="PAGAR MULTA", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.pagarMulta)
        self.pagar_multa_button.place(x=1005, y=690)

        # ******************FRAME DEVOLVER LIBROS******************
        self.frame_devolver_libro = ck.CTkFrame(self.main_frame, corner_radius=0, fg_color="transparent")
        self.frame_devolver_libro.grid(row=0, column=0, sticky="nsew")
        self.frame_devolver_libro.grid_columnconfigure(0, weight=1)
        self.frame_devolver_libro.grid_rowconfigure(1, weight=6)
        self.frame_devolver_libro.grid_rowconfigure(0, weight=1)

        self.devolver_libro_label_imagen = ck.CTkLabel(self.frame_devolver_libro, text="", image=devolver_libros_imagen)
        self.devolver_libro_label_imagen.grid(row=0, columnspan=1, padx=20)

        self.buscar_rut_devolver_libro_label = ck.CTkLabel(self.frame_devolver_libro, text="Ingrese el RUT del usuario: ",
                                                font=ck.CTkFont(size=23, weight="bold", family="Segoe UI"))
        self.buscar_rut_devolver_libro_label.place(x=18, y=146)

        self.buscar_rut_devolver_libro_entry = ck.CTkEntry(self.frame_devolver_libro, width=150, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.buscar_rut_devolver_libro_entry.place(x=320, y=148)

        self.buscar_rut_devolver_libro_button = ck.CTkButton(self.frame_devolver_libro, text="BUSCAR", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.buscarPrestamosPorRut) # command=self.mostrarDatosPrestamoPorRut
        self.buscar_rut_devolver_libro_button.place(x=480, y=148)

        self.actualizar_tabla_devolver_button = ck.CTkButton(self.frame_devolver_libro, text="ACTUALIZAR TABLA", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.cargarDatosTablaDevolverLibro) # command=self.mostrarDatosPrestamoPorRut
        self.actualizar_tabla_devolver_button.place(x=845, y=148)

        # Estilo de la tabla para mostrar los datos
        estilo_tabla = ttk.Style()
        estilo_tabla.configure("Treeview", font=ck.CTkFont(size=10, weight="bold", family="Segoe UI"), foreground='black', background='white')
        estilo_tabla.map('Treeview', background=[('selected', 'green')], foreground=[('selected', 'black')])
        estilo_tabla.configure('Heading', background='white', foreground='navy', padding=3, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"))
        estilo_tabla.configure('Item', foreground='transparent', focuscolor='DarkOrchid1')
        estilo_tabla.configure('TScrollbar', arrowcolor='DarkOrchid1', bordercolor='black', troughcolor='DarkOrchid1', background='white')

        # Crear el Frame contenedor del Treeview y el Scrollbar
        self.frame_tabla_devolver_libro = ck.CTkFrame(self.frame_devolver_libro)
        self.frame_tabla_devolver_libro.grid(row=1, columnspan=3, padx=20, pady=15, sticky="nsew")

        self.tabla_devolver_libro = ttk.Treeview(self.frame_tabla_devolver_libro)
        self.tabla_devolver_libro.grid(row=0, column=0, sticky="nsew")

        ladoy = ttk.Scrollbar(self.frame_tabla_devolver_libro, orient='vertical', command=self.tabla_devolver_libro.yview)
        ladoy.grid(row=0, column=1, sticky='ns')

        self.frame_tabla_devolver_libro.grid_rowconfigure(0, weight=1)
        self.frame_tabla_devolver_libro.grid_columnconfigure(0, weight=1)
        
        # Columnas que se mostrarán en la tabla
        self.tabla_devolver_libro.grid(sticky="nsew")
        self.tabla_devolver_libro['columns'] = ('Nombre', 'Apellido', 'RUT', 'Tipo de usuario', 'F. Devolución', 'ISBN', 'Titulo', 'Multa', 'Monto')

        # Ajustar ancho mínimo y ancho de cada columna de encabezado
        self.tabla_devolver_libro.column('#0', minwidth=60, width=0, anchor='center', stretch=False)
        self.tabla_devolver_libro.column('Nombre', minwidth=100, width=130, anchor='center')
        self.tabla_devolver_libro.column('Apellido', minwidth=100, width=120, anchor='center')
        self.tabla_devolver_libro.column('RUT', minwidth=100, width=120, anchor='center')
        self.tabla_devolver_libro.column('Tipo de usuario', minwidth=130, width=105, anchor='center')
        self.tabla_devolver_libro.column('F. Devolución', minwidth=130, width=105, anchor='center')
        self.tabla_devolver_libro.column('ISBN', minwidth=60, width=70, anchor='center')
        self.tabla_devolver_libro.column('Titulo', minwidth=100, width=120, anchor='center')
        self.tabla_devolver_libro.column('Multa', minwidth=100, width=120, anchor='center')
        self.tabla_devolver_libro.column('Monto', minwidth=100, width=120, anchor='center')

        # Configurar el texto de encabezado para que se muestre completo
        self.tabla_devolver_libro.heading('#0', text='Id', anchor='center')
        self.tabla_devolver_libro.heading('Nombre', text='Nombre', anchor='center')
        self.tabla_devolver_libro.heading('Apellido', text='Apellido', anchor='center')
        self.tabla_devolver_libro.heading('RUT', text='RUT', anchor='center')
        self.tabla_devolver_libro.heading('Tipo de usuario', text='Tipo de usuario', anchor='center')
        self.tabla_devolver_libro.heading('F. Devolución', text='F. Devolución', anchor='center')
        self.tabla_devolver_libro.heading('ISBN', text='ISBN', anchor='center')
        self.tabla_devolver_libro.heading('Titulo', text='Titulo', anchor='center')
        self.tabla_devolver_libro.heading('Multa', text='Multa', anchor='center')
        self.tabla_devolver_libro.heading('Monto', text='Monto', anchor='center')

        self.tabla_devolver_libro.bind("<ButtonRelease-1>", self.seleccionarFilaPrestamo)

        self.devolver_libro_button = ck.CTkButton(self.frame_devolver_libro, text="DEVOLVER LIBRO", font=ck.CTkFont(size=20, weight="bold", family="Segoe UI"), command=self.devolverLibro) # command=self.mostrarDatosPrestamoPorRut
        self.devolver_libro_button.grid(row=2, columnspan=2, padx=20, pady=10)

        # FRAME SELECCIONADO POR DEFECTO
        self.seleccion_frame_nombre("inicio")

    # Método para buscar el frame por el nombre
    def seleccion_frame_nombre(self, nombre):
        self.inicio_button.configure(fg_color=("gray75", "gray25") if nombre == "inicio" else "transparent")
        self.catalogo.configure(fg_color=("gray75", "gray25") if nombre == "catalogo" else "transparent")
        self.frame_stock.configure(fg_color=("gray75", "gray25") if nombre == "stock" else "transparent")
        self.frame_realizar_prestamo.configure(fg_color=("gray75", "gray25") if nombre == "realizar_prestamo" else "transparent")
        self.frame_libros_en_prestamo.configure(fg_color=("gray75", "gray25") if nombre == "libros_prestamo" else "transparent")
        self.frame_prestamos_por_usuario.configure(fg_color=("gray75", "gray25") if nombre == "prestamos_por_usuario" else "transparent")
        self.frame_renovar_libro.configure(fg_color=("gray75", "gray25") if nombre == "renovar_libro" else "transparent")
        self.frame_registrar_usuario.configure(fg_color=("gray75", "gray25") if nombre == "registrar_usuario" else "transparent")
        self.frame_usuarios_registrados.configure(fg_color=("gray75", "gray25") if nombre == "usuarios_registrados" else "transparent")
        self.frame_pagar_multa.configure(fg_color=("gray75", "gray25") if nombre == "pagar_multa" else "transparent")
        self.frame_devolver_libro.configure(fg_color=("gray75", "gray25") if nombre == "devolver_libro" else "transparent")
        
        # Mostrar frame seleccionado
        if nombre == "inicio":
            self.inicio_frame.grid(row=0, column=0, sticky="nsew")
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "catalogo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid(row=0, column=0, sticky="nsew")
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "stock":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid(row=0, column=0, sticky="nsew")
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "realizar_prestamo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid(row=0, column=0, sticky="nsew")
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "libros_en_prestamo":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid(row=0, column=0, sticky="nsew")
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "prestamos_por_usuario":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid(row=0, column=0, sticky="nsew")
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "renovar_libro":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid(row=0, column=0, sticky="nsew")
            self.frame_registrar_usuario.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "registrar_usuario":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_registrar_usuario.grid(row=0, column=0, sticky="nsew")
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "usuarios_registrados":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_usuarios_registrados.grid(row=0, column=0, sticky="nsew")
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid_forget()
        elif nombre == "pagar_multa":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid(row=0, column=0, sticky="nsew")
            self.frame_devolver_libro.grid_forget()
        elif nombre == "devolver_libro":
            self.inicio_frame.grid_forget()
            self.catalogo.grid_forget()
            self.frame_stock.grid_forget()
            self.frame_realizar_prestamo.grid_forget()
            self.frame_libros_en_prestamo.grid_forget()
            self.frame_prestamos_por_usuario.grid_forget()
            self.frame_renovar_libro.grid_forget()
            self.frame_usuarios_registrados.grid_forget()
            self.frame_pagar_multa.grid_forget()
            self.frame_devolver_libro.grid(row=0, column=0, sticky="nsew")
            

    # Métodos para mostrar el frame cuando se pulse el botón
    def inicio_button_evento(self):
        self.seleccion_frame_nombre("inicio")
    
    def catalogo_button_evento(self):
        self.seleccion_frame_nombre("catalogo")

    def stock_button_evento(self):
        self.seleccion_frame_nombre("stock")

    def realizarPrestamo_button_evento(self):
        self.seleccion_frame_nombre("realizar_prestamo")

    def frame_libros_en_prestamo_button_evento(self):
        self.seleccion_frame_nombre("libros_en_prestamo")

    def frame_prestamos_por_usuario_button_evento(self):
        self.seleccion_frame_nombre("prestamos_por_usuario")

    def frame_renovar_libro_button_evento(self):
        self.seleccion_frame_nombre("renovar_libro")

    def frame_registrar_usuario_button_evento(self):
        self.seleccion_frame_nombre("registrar_usuario")

    def usuarios_registrados_button_evento(self):
        self.seleccion_frame_nombre("usuarios_registrados")

    def pagar_multa_button_evento(self):
        self.seleccion_frame_nombre("pagar_multa")
    
    def devolver_libro_button_evento(self):
        self.seleccion_frame_nombre("devolver_libro")

    # Método para cambiar la apariencia de la app
    def evento_cambiar_apariencia(self, new_appearance_mode):
        ck.set_appearance_mode(new_appearance_mode)

    # MÉTODOS PARA EL FRAME INICIO
    def mostrarDatosPrestamo(self):
        datos = self.bd.obtenerPrestamosConRetraso()
        self.tabla_inicio.delete(*self.tabla_inicio.get_children())
        i = -1
        for dato in datos:
            i += 1
            id_prestamo = datos[i][0]
            rut_usuario = datos[i][3]
            f_devolucion = datetime.strptime(datos[i][5], "%Y-%m-%d")
            titulo_libro = datos[i][7]
            multa = datos[i][8]
            monto = datos[i][9]

            # Calcular días de retraso
            fecha_actual = datetime.today()
            dias_retraso = (fecha_actual - f_devolucion).days

            # Verificar si hay retraso y asignar la etiqueta de estilo correspondiente
            if dias_retraso > 0 and monto is not None and monto > 0:
                self.tabla_inicio.insert('', i, text=id_prestamo, values=datos[i][1:10], tags='retraso')
            else:
                self.tabla_inicio.insert('', i, text=id_prestamo, values=datos[i][1:10])

            # Verificar si hay un monto que pagar y aún no ha sido pagado
            if monto is not None and monto > 0 and multa == 0:
                self.tabla_inicio.set(id_prestamo, 'Multa', 'no pagado')

        # Configurar estilo para las filas con retraso
        self.tabla_inicio.tag_configure('retraso', background='yellow')

        messagebox.showinfo("Devoluciones retrasadas", "La tabla ha sido actualizada.")

    # MÉTODOS PARA FRAME CATALOGO
    def crear_imagen_flip(self, imagen_bytes, titulo, detalle):
        imagen_np = np.frombuffer(imagen_bytes, np.uint8)
        imagen_cv2 = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

        if imagen_cv2.shape[2] == 3:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
        else:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_GRAY2RGB)

        imagen_pil = Image.fromarray(imagen_cv2_rgb)

        imagen = ck.CTkImage(imagen_pil, size=(150, 200))
        imagen_label = ck.CTkLabel(self.canvas, text="", image=imagen, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"), text_color="black")
        imagen_label.image = imagen
        imagen_label.bind("<Button-1>", lambda event: self.mostrar_detalle(imagen_label, titulo, detalle))

        return imagen_label

    def mostrar_detalle(self, imagen_label, titulo, detalle):
        imagen_label.configure(text=f"{titulo}\n {detalle}")
        self.frame_imagenes_catalogo.after(5000, lambda: self.ocultar_detalle(imagen_label))

    def ocultar_detalle(self, imagen_label):
        imagen_label.configure(text="")

    def seleccionarCategoria(self, event = None):
        categoria_seleccionada = self.categoria.get()

        # Verificar si se seleccionó la opción "Mostrar Todos"
        if categoria_seleccionada == "Mostrar Todos":
            # Obtener todos los libros desde la base de datos
            libros = self.bd.obtenerLibrosCatalogo()
        else:
            # Obtener los libros de la categoría seleccionada desde la base de datos
            libros = self.bd.obtenerLibroCategoria(categoria_seleccionada)

        # Limpiar el frame de imágenes antes de mostrar los nuevos libros
        for widget in self.canvas.winfo_children():
            widget.destroy()

        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 8, column=i % 8, padx=10, pady=10, sticky="nsew")
                self.frame_imagenes_catalogo.grid_rowconfigure(i // 8, weight=1)  # Expansión vertical
                self.frame_imagenes_catalogo.grid_columnconfigure(i % 8, weight=1)  # Expansión horizontal

    def buscarLibroNombre(self, event = None):
        nombre_libro = self.buscar_nombre_libro_entry.get()
        if nombre_libro:
            libro = self.bd.obtenerLibroNombre(nombre_libro)
            # Limpiar el frame de imágenes antes de mostrar los nuevos libros
            for widget in self.canvas.winfo_children():
                widget.destroy()

            if libro:
                # Obtener los datos del libro
                nombre = libro[0]
                apellido = libro[1]
                nacionalidad = libro[2]
                titulo = libro[3]
                imagen_bytes = libro[4]
                isbn = libro[5]

                if imagen_bytes is not None:
                    imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                    imagen_flip.grid(row=4, column=8, padx=10, pady=10, sticky="nsew")
                    self.frame_imagenes_catalogo.grid_rowconfigure( 8, weight=1)  # Expansión vertical
                    self.frame_imagenes_catalogo.grid_columnconfigure( 8, weight=1)  # Expansión horizontal

                # Restablecer el campo de búsqueda
                self.buscar_nombre_libro_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Búsqueda de libro", f"No se encontró ningún libro con el nombre '{nombre_libro}'.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un nombre de libro para realizar la búsqueda.")

    def buscarLibroIsbn(self, event = None):
        isbn_libro = self.buscar_isbn_libro_entry.get()
        if isbn_libro:
            libro = self.bd.obtenerLibroIsbn(isbn_libro)
            # Limpiar el frame de imágenes antes de mostrar los nuevos libros
            for widget in self.canvas.winfo_children():
                widget.destroy()

            if libro:
                # Obtener los datos del libro
                nombre = libro[0]
                apellido = libro[1]
                nacionalidad = libro[2]
                titulo = libro[3]
                imagen_bytes = libro[4]
                isbn = libro[5]

                if imagen_bytes is not None:
                    imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                    imagen_flip.grid(row=4, column=8, padx=10, pady=10, sticky="nsew")
                    self.frame_imagenes_catalogo.grid_rowconfigure( 8, weight=1)  # Expansión vertical
                    self.frame_imagenes_catalogo.grid_columnconfigure( 8, weight=1)  # Expansión horizontal

                # Restablecer el campo de búsqueda
                self.buscar_isbn_libro_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Búsqueda de libro", f"No se encontró ningún libro con el ISBN: '{isbn_libro}'.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un ISBN de libro para realizar la búsqueda.")

    def mostrarTodosLosLibros(self):
    # Obtener nuevamente todos los libros desde la base de datos
        libros = self.bd.obtenerLibrosCatalogo()

        # Eliminar las imágenes existentes en el frame de imágenes del catálogo
        for widget in self.canvas.winfo_children():
            widget.destroy()

        # Mostrar las imágenes de los libros nuevamente en el catálogo
        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 8, column=i % 8, padx=10, pady=10, sticky="nsew")
                self.frame_imagenes_catalogo.grid_rowconfigure(i // 8, weight=1)  # Expansión vertical
                self.frame_imagenes_catalogo.grid_columnconfigure(i % 8, weight=1)  # Expansión horizontal

    # METODOS PARA EL FRAME STOCK
    # Método para buscar un libro
    def buscarLibroStock(self, event = None):
        isbn = self.buscar_actualiza.get()  # Obtener el ISBN ingresado
        if isbn == "":
            messagebox.showerror("Stock", "Debe de ingresar un ISBN para realizar la busqueda.")
            self.limpiarCamposStock()
        libros = self.bd.buscarLibro(isbn)  # Buscar el libro en la base de datos
        if libros:
            isbn, titulo, num_paginas, stock = libros[0][1:5]  # Tomar los elementos del índice 1 al 4
            self.isbn.set(str(isbn))  # Actualizar el valor del campo ISBN
            self.titulo.set(str(titulo))  # Actualizar el valor del campo Título
            self.numero_paginas.set(int(num_paginas))  # Actualizar el valor del campo Número de Páginas
            self.stockLibro.set(int(stock))  # Actualizar el valor del campo Stock
        else:
            messagebox.showerror("Stock", f"El libro con el ISBN {isbn} no existe.")
            self.limpiarCamposStock()

    # Método para actualizar el stock de un libro
    def actualizarStock(self, event = None):
        isbn = self.isbn.get()
        stock = self.stockLibro.get()
        titulo = self.titulo.get()

        if not isbn:
            messagebox.showerror("Modificar Stock", "El campo ISBN no puede estar vació")
            return
        if stock < 0:
            messagebox.showerror("Modificar Stock", "Ingrese un stock valido.")
            return

        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Nostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.frame_stock, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Segoe UI Historic"))
        self.barra_progreso_label.place(x=40, y=430)

        # Realizar el préstamo
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_realizar_prestamo.update() # Actualizar la ventana
            time.sleep(0.003)

        self.bd.actualizarStock(stock, isbn)
        self.limpiarCamposStock()

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_realizar_prestamo.update() # Actualizar la ventana

    # METODOS PARA EL FRAME USUARIOS REGISTRADOS
    # Método para mostrar los datos en la tabla de usuarios
    def mostrarDatosUsuario(self):
        datos = self.bd.mostrarUsuarios()
        self.tabla_uno.delete(*self.tabla_uno.get_children())
        i = - 1
        for dato in datos:
            i += 1
            self.tabla_uno.insert('', i, text=datos[i][0], values=datos[i][1:8])
        messagebox.showinfo("Usuarios registrados", "La tabla ha sido actualizada.")

    # Método para poder seleccionar la fila en la tabla de usuarios
    def obtener_filaUsuario(self, event = None):
        current_item = self.tabla_uno.focus()
        if not current_item:
            return
        data = self.tabla_uno.item(current_item)
        self.nombre_borrar = data['values'][0]

    # METODOS PARA EL FRAME LIBROS EN PRESTAMO
    # Método para mostrar los datos en la tabla libros en préstamo
    def mostrarDatosLibros(self):
        datos = self.bd.mostrarLibrosPrestamo()
        self.tabla_dos.delete(*self.tabla_dos.get_children())
        i = - 1
        for dato in datos:
            i += 1
            self.tabla_dos.insert('', i, text=datos[i][0], values=datos[i][1:3])
        messagebox.showinfo("Libros en préstamo", "La tabla ha sido actualizada.")

    # Método para poder seleccionar la fila en la tabla de libros en préstamo
    def obtener_filaLibros(self, event = None):
        current_item = self.tabla_dos.focus()
        if not current_item:
            return
        data = self.tabla_dos.item(current_item)
        self.nombre_borrar = data['values'][0]

    # METODOS PARA EL FRAME REALIZAR PRESTAMO
    # Método para obtener el tipo de usuario mediante su RUT
    def obtenerTipoUsuario(self, event=None):
        rut = self.rut_usuario.get()
        isbn = self.isbn.get()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)
        self.fecha_devolucion.get_date()

        if not rut:
            messagebox.showerror("Realizar Préstamo", "El campo RUT no puede estar vacío.")
            return

        if self.validarRut(rut):
            if tipo_usuario:
                self.tipo_usuario.set(tipo_usuario)
                if tipo_usuario == "Alumno":
                    fecha_devolucion = self.calcularFechaDevolucion(7)
                    messagebox.showinfo("Realizar Préstamo", f"Se han sumado 7 días por ser {tipo_usuario}")
                    if fecha_devolucion:
                        self.fecha_devolucion.delete(0, 'end')
                        self.fecha_devolucion.set_date(fecha_devolucion)
                elif tipo_usuario == "Docente":
                    fecha_devolucion = self.calcularFechaDevolucion(20)
                    messagebox.showinfo("Realizar Préstamo", f"Se han sumado 20 días por ser {tipo_usuario}")
                    if fecha_devolucion:
                        self.fecha_devolucion.delete(0, 'end')
                        self.fecha_devolucion.set_date(fecha_devolucion)
                else:
                    self.fecha_devolucion.configure(state="disabled")
            else:
                messagebox.showerror("Realizar Prestamo", f"El RUT {rut} no existe en la base de datos.")
        else:
            messagebox.showerror("Realizar Prestamo", f"El RUT {rut} no es válido.")

    def realizarPrestamo(self):
        # Verificar la cantidad de préstamos pendientes y el límite máximo de préstamos permitidos
        cantidad_prestamos = len(self.treeview_prestamos.get_children())
        rut = self.rut_usuario.get()
        isbn = self.isbn_libro_entry.get()
        f_prestamo = self.fecha_inicio.get_date()
        f_devolucion = self.fecha_devolucion.get_date()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)
        id_bibliotecario = self.bd.obtenerUsuarioLog(self.correo_actual)
        
        if self.bd.retrasoDeFecha(rut):
            messagebox.showwarning("Realizar Préstamo", f"El usuario con RUT: {rut} tiene libros pendientes para devolución.")
            return
        
        # Verificar la cantidad de libros en préstamo del usuario
        cantidad_prestamos = self.bd.obtenerCantidadLibrosPrestamo(rut)

        if tipo_usuario == "Alumno" and cantidad_prestamos >= 4:
            messagebox.showwarning("Límite de préstamos alcanzado", "El alumno ha alcanzado el límite máximo de préstamos (4 libros).")
            return
        
        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Mostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.frame_realizar_prestamo, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Segoe UI Historic"))
        self.barra_progreso_label.place(x=65, y=620)

        # Realizar el préstamo
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_realizar_prestamo.update() # Actualizar la ventana
            time.sleep(0.003)

        # Iterar sobre los préstamos pendientes y registrar cada uno en la base de datos
        for child in self.treeview_prestamos.get_children():
            rut = self.treeview_prestamos.item(child)["values"][0]
            isbn = self.treeview_prestamos.item(child)["values"][1]
            f_prestamo = self.treeview_prestamos.item(child)["values"][2]
            f_devolucion = self.treeview_prestamos.item(child)["values"][3]
            tipo_usuario = self.treeview_prestamos.item(child)["values"][4]

            # Registrar el préstamo en la base de datos
            self.bd.registrarPrestamo(id_bibliotecario, rut, isbn, f_prestamo, f_devolucion, tipo_usuario)

        # Limpiar el Treeview de préstamos pendientes
        self.treeview_prestamos.delete(*self.treeview_prestamos.get_children())

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_realizar_prestamo.update() # Actualizar la ventana
            
    def calcularFechaDevolucion(self, dias):
        fecha_actual = datetime.now()
        fecha_devolucion = fecha_actual + timedelta(days=dias)
        return fecha_devolucion

    def agregarLibro(self):
        rut = self.rut_usuario_entry.get()
        isbn = self.isbn_libro_entry.get()
        f_prestamo = self.fecha_inicio.get_date()
        f_devolucion = self.fecha_devolucion.get_date()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)

        # Verificar si el ISBN ya está agregado en el Treeview
        for child in self.treeview_prestamos.get_children():
            if self.treeview_prestamos.item(child)["values"][1] == isbn:
                messagebox.showerror("Agregar libro", f"El ISBN {isbn} ya está agregado.")
                return
            
        # Verificar si se completo el campo Rut
        if not rut:
            messagebox.showerror("Agregar libro", "El campo RUT no puede estar vacio.")
            return
        
        # Verificar si se completo el campo ISBN
        if not isbn:
            messagebox.showerror("Agregar libro", "El campo ISBN no puede estar vacio.")
            return
        
            
        # Verificar si el ISBN existe en la base de datos
        if not self.bd.verificarISBN(isbn):
            messagebox.showerror("Agregar libro", f"El ISBN {isbn} no existe en la base de datos.")
            return

        # Verificar si se han ingresado todos los campos
        if rut and isbn and f_prestamo and f_devolucion and tipo_usuario:
            if tipo_usuario == "Alumno":
                # Verificar la cantidad de préstamos del alumno
                cantidad_prestamos_alumno = len(self.treeview_prestamos.get_children())
                if cantidad_prestamos_alumno >= 4:
                    messagebox.showwarning("Agregar libro", "El alumno ha alcanzado el límite máximo de préstamos (4 libros).")
                    return
                
            # Agregar el libro al Treeview de préstamos pendientes
            self.treeview_prestamos.insert("", "end", values=(rut, isbn, f_prestamo, f_devolucion, tipo_usuario))
            # Limpiar los campos de entrada de datos del libro
            self.isbn_libro_entry.delete(0, "end")
            self.tipo_usuario_entry.delete(0, "end")
            self.fecha_inicio.set_date(datetime.today())
            self.fecha_devolucion.set_date(datetime.today())
        else:
            messagebox.showerror("Agregar Libro", "Por favor, complete todos los campos.")

    def eliminarLibro(self):
        # Obtener el índice del libro seleccionado en el Treeview
        selected_item = self.treeview_prestamos.selection()
        if selected_item:
            self.treeview_prestamos.delete(selected_item)
        else:
            messagebox.showerror("Eliminar Libro", "Por favor, seleccione un libro para eliminar.")

    # MÉTODOS PARA EL FRAME REGISTRAR USUARIO
    # Método para registrar usuario
    def registrarUsuario(self):
        nombre = self.nombre_usuario.get()
        apellido = self.apellido_ususario.get()
        direccion = self.direccion_usuario.get()
        rut = self.rut_usuario.get()
        celular = self.codigo_pais_entry.get() + self.celular_usuario.get()
        correo = self.correo_usuario.get()
        tipo = self.tipo_usuario.get()

        if rut == "":
            messagebox.showerror("Registrar Usuario", "Debe de ingresar un rut.")

        if self.validarRut(rut):
                if self.validarCorreo(correo):
                    # Crear instancia de BarraProgreso
                    total_elementos = 100
                    barra = BarraProgreso(total_elementos)

                    # Nostrar barra de progreso en el Frame
                    self.barra_progreso_label = ck.CTkLabel(self.frame_registrar_usuario, text="",
                                                            font=ck.CTkFont(size=14, weight="bold", family="Segoe UI Historic"))
                    self.barra_progreso_label.place(x=30, y=570)

                    # Realizar el préstamo
                    for i in range(total_elementos):
                        mensaje_progreso = barra.actualizar()
                        self.barra_progreso_label.configure(text=mensaje_progreso)
                        self.frame_registrar_usuario.update() # Actualizar la ventana
                        time.sleep(0.003)

                    self.bd.registrarUsuario(nombre, apellido, direccion, rut, celular, correo, tipo)
                    self.limpiarCamposUsuario()
                    # Restablecer el estado de la barra de progreso
                    self.barra_progreso_label.configure(text="")
                    self.frame_registrar_usuario.update() # Actualizar la ventana
                else:
                    messagebox.showerror("Registrar Usuario", f"El correo {correo} no es valido.")
        else:
            messagebox.showerror("Registrar Usuario", f"El RUT {rut} ingresado no es valido.")

    # METODO PARA EL FRAME RENOVAR PRÉSTAMO
    def renovarLibro(self):
        # Obtener los datos necesarios
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        id_bibliotecario = self.bd.obtenerUsuarioLog(self.correo_actual)
        nueva_fecha_devolucion = self.fecha_devolucion_renovar.get_date()

        if not rut:
            messagebox.showerror("Renovación de libro", "El campo RUT no debe estar vacío")
            return

        if not isbn:
            messagebox.showerror("Renovación de libro", "El campo ISBN no debe estar vacío")
            return

        # Crear instancia de BarraProgreso
        total_elementos = 100
        barra = BarraProgreso(total_elementos)

        # Mostrar barra de progreso en el Frame
        self.barra_progreso_label = ck.CTkLabel(self.frame_renovar_libro, text="",
                                                font=ck.CTkFont(size=14, weight="bold", family="Segoe UI Historic"))
        self.barra_progreso_label.grid(row=4, column=0, padx=10, pady=10)

        # Realizar la renovación del libro
        for i in range(total_elementos):
            mensaje_progreso = barra.actualizar()
            self.barra_progreso_label.configure(text=mensaje_progreso)
            self.frame_renovar_libro.update()  # Actualizar la ventana
            time.sleep(0.003)

        # Registrar la renovación del libro
        if self.bd.registrarRenovacion(rut, isbn):
            # Actualizar la fecha de devolución en la base de datos
            if self.bd.actualizarPrestamo(rut, isbn, nueva_fecha_devolucion, id_bibliotecario):
                messagebox.showinfo("Renovación de libro", "El libro ha sido renovado exitosamente.")
                self.limpiarCamposRenovacion()
            else:
                messagebox.showerror("Renovación de libro", "Error al actualizar la fecha de devolución del préstamo.")
        else:
            messagebox.showerror("Renovación de libro", "Error al registrar la renovación del libro.")

        # Restablecer el estado de la barra de progreso
        self.barra_progreso_label.configure(text="")
        self.frame_renovar_libro.update()  # Actualizar la ventana

    def obtenerFechaDevolucion(self):
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        tipo_usuario = self.bd.obtenerTipoUsuario(rut)

        if rut == "" and isbn == "":
            messagebox.showerror("Renovación de libro", "Debe de ingresar un RUT.")

        # Verificar si el usuario es "Alumno"
        if tipo_usuario == "Alumno":
            # Verificar si el alumno ya ha realizado una renovación
            if self.bd.haRealizadoRenovacion(rut):
                messagebox.showinfo("Renovación de libro", "El alumno ya ha realizado una renovación y no puede renovar más libros.")
                return

        # Obtener la fecha de devolución actual del préstamo
        fecha_devolucion_actual = self.bd.obtenerFechaDevolucionPrestamo(rut, isbn)
        if fecha_devolucion_actual is None:
            messagebox.showerror("Renovación de libro", "No se encontró un préstamo vigente para el usuario y el libro especificados.")
            return
        
        # Establecer la fecha de devolución actual en el DateEntry
        self.fecha_devolucion_renovar.set_date(datetime.strptime(fecha_devolucion_actual, "%Y-%m-%d"))
        messagebox.showinfo("Renovación de libro", f"La fecha de devolución establecida para el alumno por este libro es: {self.fecha_devolucion_renovar.get_date()}")

    def sumarDiasRenovacion(self):
        rut = self.rut_usuario.get()
        isbn = self.isbn_entry.get()
        # Obtener la fecha de devolución actual del préstamo
        fecha_devolucion_actual = self.bd.obtenerFechaDevolucionPrestamo(rut, isbn)
        if fecha_devolucion_actual is None:
            messagebox.showerror("Renovación de libro", "No se encontró un préstamo vigente para el usuario y el libro especificados.")
            return
        # Calcular la nueva fecha de devolución sumando 3 días a la fecha actual
        nueva_fecha_devolucion = datetime.strptime(fecha_devolucion_actual, "%Y-%m-%d").date() + timedelta(days=3)
        self.fecha_devolucion_renovar.set_date(nueva_fecha_devolucion)
        messagebox.showinfo("Renovación de libro", f"Se han sumado 3 dias a la fecha de devolución, ahora la nueva fecha es: {nueva_fecha_devolucion}") 

    # MÉTODOS PARA FRAME CATALOGO
    def crear_imagen_flip(self, imagen_bytes, titulo, detalle):
        imagen_np = np.frombuffer(imagen_bytes, np.uint8)
        imagen_cv2 = cv2.imdecode(imagen_np, cv2.IMREAD_COLOR)

        if imagen_cv2.shape[2] == 3:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
        else:
            imagen_cv2_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_GRAY2RGB)

        imagen_pil = Image.fromarray(imagen_cv2_rgb)

        imagen = ck.CTkImage(imagen_pil, size=(150, 200))
        imagen_label = ck.CTkLabel(self.canvas, text="", image=imagen, font=ck.CTkFont(size=20, weight="bold", family="Segoe UI Historic"), text_color="black")
        imagen_label.image = imagen
        imagen_label.bind("<Button-1>", lambda event: self.mostrar_detalle(imagen_label, titulo, detalle))

        return imagen_label

    def mostrar_detalle(self, imagen_label, titulo, detalle):
        imagen_label.configure(text=f"{titulo}\n {detalle}")
        self.frame_imagenes_catalogo.after(5000, lambda: self.ocultar_detalle(imagen_label))

    def ocultar_detalle(self, imagen_label):
        imagen_label.configure(text="")

    def seleccionarCategoria(self, event = None):
        categoria_seleccionada = self.categoria.get()

        # Verificar si se seleccionó la opción "Mostrar Todos"
        if categoria_seleccionada == "Mostrar Todos":
            # Obtener todos los libros desde la base de datos
            libros = self.bd.obtenerLibrosCatalogo()
        else:
            # Obtener los libros de la categoría seleccionada desde la base de datos
            libros = self.bd.obtenerLibroCategoria(categoria_seleccionada)

        # Limpiar el frame de imágenes antes de mostrar los nuevos libros
        for widget in self.canvas.winfo_children():
            widget.destroy()

        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 8, column=i % 8, padx=10, pady=10, sticky="nsew")
                self.frame_imagenes_catalogo.grid_rowconfigure(i // 8, weight=1)  # Expansión vertical
                self.frame_imagenes_catalogo.grid_columnconfigure(i % 8, weight=1)  # Expansión horizontal

    def buscarLibroNombre(self, event = None):
        nombre_libro = self.buscar_nombre_libro_entry.get()
        if nombre_libro:
            libro = self.bd.obtenerLibroNombre(nombre_libro)
            # Limpiar el frame de imágenes antes de mostrar los nuevos libros
            for widget in self.canvas.winfo_children():
                widget.destroy()

            if libro:
                # Obtener los datos del libro
                nombre = libro[0]
                apellido = libro[1]
                nacionalidad = libro[2]
                titulo = libro[3]
                imagen_bytes = libro[4]
                isbn = libro[5]

                if imagen_bytes is not None:
                    imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                    imagen_flip.grid(row=4, column=8, padx=10, pady=10, sticky="nsew")
                    self.frame_imagenes_catalogo.grid_rowconfigure( 8, weight=1)  # Expansión vertical
                    self.frame_imagenes_catalogo.grid_columnconfigure( 8, weight=1)  # Expansión horizontal

                # Restablecer el campo de búsqueda
                self.buscar_nombre_libro_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Búsqueda de libro", f"No se encontró ningún libro con el nombre '{nombre_libro}'.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un nombre de libro para realizar la búsqueda.")

    def buscarLibroIsbn(self, event = None):
        isbn_libro = self.buscar_isbn_libro_entry.get()
        if isbn_libro:
            libro = self.bd.obtenerLibroIsbn(isbn_libro)
            # Limpiar el frame de imágenes antes de mostrar los nuevos libros
            for widget in self.canvas.winfo_children():
                widget.destroy()

            if libro:
                # Obtener los datos del libro
                nombre = libro[0]
                apellido = libro[1]
                nacionalidad = libro[2]
                titulo = libro[3]
                imagen_bytes = libro[4]
                isbn = libro[5]

                if imagen_bytes is not None:
                    imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                    imagen_flip.grid(row=4, column=8, padx=10, pady=10, sticky="nsew")
                    self.frame_imagenes_catalogo.grid_rowconfigure( 8, weight=1)  # Expansión vertical
                    self.frame_imagenes_catalogo.grid_columnconfigure( 8, weight=1)  # Expansión horizontal

                # Restablecer el campo de búsqueda
                self.buscar_isbn_libro_entry.delete(0, tk.END)
            else:
                messagebox.showinfo("Búsqueda de libro", f"No se encontró ningún libro con el ISBN: '{isbn_libro}'.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un ISBN de libro para realizar la búsqueda.")

    def mostrarTodosLosLibros(self):
    # Obtener nuevamente todos los libros desde la base de datos
        libros = self.bd.obtenerLibrosCatalogo()

        # Eliminar las imágenes existentes en el frame de imágenes del catálogo
        for widget in self.canvas.winfo_children():
            widget.destroy()

        # Mostrar las imágenes de los libros nuevamente en el catálogo
        for i, libro in enumerate(libros):
            nombre = libro[0]
            apellido = libro[1]
            nacionalidad = libro[2]
            titulo = libro[3]
            imagen_bytes = libro[4]
            isbn = libro[5]

            if imagen_bytes is not None:
                imagen_flip = self.crear_imagen_flip(imagen_bytes, titulo, f"ISBN: {isbn}\nAutor: {nombre} {apellido}\nNacionalidad: {nacionalidad}")
                imagen_flip.grid(row=i // 8, column=i % 8, padx=10, pady=10, sticky="nsew")
                self.frame_imagenes_catalogo.grid_rowconfigure(i // 8, weight=1)  # Expansión vertical
                self.frame_imagenes_catalogo.grid_columnconfigure(i % 8, weight=1)  # Expansión horizontal

    # MÉTODOS PARA FRAME PAGAR MULTAS
    # Método para mostrar los prestamos por usuario
    def mostrarDatosPrestamoPorRut(self, event=None):
        rut_usuario = self.rut_usuario_prestamos_entry.get()

        if rut_usuario:
            # Validar el RUT ingresado
            if self.validarRut(rut_usuario):
                # Obtener datos del préstamo por el RUT del usuario
                datos_prestamo = self.bd.obtenerPrestamoUsuarioRut(rut_usuario)

                if datos_prestamo is not None:
                    if datos_prestamo:  # Si la lista no está vacía
                        # Eliminar cualquier dato previo en la tabla
                        self.tabla_tres.delete(*self.tabla_tres.get_children())

                        # Insertar los datos en la tabla
                        for prestamo in datos_prestamo:
                            self.tabla_tres.insert('', 'end', values=prestamo)
                    else:
                        messagebox.showinfo("Búsqueda de préstamo", f"No se encontraron préstamos para el RUT: {rut_usuario}.")
                else:
                    messagebox.showerror("Búsqueda de préstamo", f"El RUT {rut_usuario} no se encuentra en la base de datos.")
            else:
                messagebox.showerror("RUT inválido", "El RUT ingresado no es válido. Por favor, ingrese un RUT válido.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un RUT de usuario para realizar la búsqueda.")

    # MÉTODOS PARA FRAME PAGAR MULTAS
    def cargarDatosTablaMultas(self):
        rut_usuario = self.buscar_rut_multa_entry.get()

        if rut_usuario:
            # Validar el RUT ingresado
            if self.validarRut(rut_usuario):
                # Obtener datos de las multas por el RUT del usuario
                datos_multas = self.bd.obtenerUsuarioMulta(rut_usuario)

                if datos_multas:  # Si la lista no está vacía
                    # Limpiar la tabla
                    self.tabla_multa.delete(*self.tabla_multa.get_children())

                    # Insertar los datos en la tabla
                    for multa in datos_multas:
                        self.tabla_multa.insert('', 'end', values=multa)
                else:
                    messagebox.showinfo("Búsqueda de multas", f"No se encontraron multas para el RUT: {rut_usuario}.")
            else:
                messagebox.showerror("RUT inválido", "El RUT ingresado no es válido. Por favor, ingrese un RUT válido.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un RUT de usuario para realizar la búsqueda.")
        # Vincular el evento de selección a la función actualizarDatosUsuario
        self.tabla_multa.bind("<ButtonRelease-1>", self.actualizarDatosUsuario)

    def actualizarDatosUsuario(self, event):
        # Obtener el índice seleccionado de la tabla
        selected_item = self.tabla_multa.selection()[0]
        values = self.tabla_multa.item(selected_item, "values")

        # Actualizar los Entry con los datos del usuario seleccionado
        self.multa_nombre_usuario_entry.configure(state="normal")
        self.multa_nombre_usuario_entry.delete(0, tk.END)
        self.multa_nombre_usuario_entry.insert(0, values[1])  # Nombre

        self.multa_apellido_usuario_entry.configure(state="normal")
        self.multa_apellido_usuario_entry.delete(0, tk.END)
        self.multa_apellido_usuario_entry.insert(0, values[2])  # Apellido

        self.multa_rut_usuario_entry.configure(state="normal")
        self.multa_rut_usuario_entry.delete(0, tk.END)
        self.multa_rut_usuario_entry.insert(0, values[4])  # RUT

        self.multa_celular_usuario_entry.configure(state="normal")
        self.multa_celular_usuario_entry.delete(0, tk.END)
        self.multa_celular_usuario_entry.insert(0, values[5])  # Celular

        self.multa_correo_usuario_entry.configure(state="normal")
        self.multa_correo_usuario_entry.delete(0, tk.END)
        self.multa_correo_usuario_entry.insert(0, values[6])  # Correo electrónico

        self.multa_tipo_usuario_entry.configure(state="normal")
        self.multa_tipo_usuario_entry.delete(0, tk.END)
        self.multa_tipo_usuario_entry.insert(0, values[7])  # Tipo de usuario

        self.multa_multa_usuario_entry.configure(state="normal")
        self.multa_multa_usuario_entry.delete(0, tk.END)
        self.multa_multa_usuario_entry.insert(0, values[8])  # Multa

        self.multa_monto_usuario_entry.configure(state="normal")
        self.multa_monto_usuario_entry.delete(0, tk.END)
        self.multa_monto_usuario_entry.insert(0, values[9])  # Monto

        self.multa_isbn_usuario_entry.configure(state="normal")
        self.multa_isbn_usuario_entry.delete(0, tk.END)
        self.multa_isbn_usuario_entry.insert(0, values[0])  # Monto

        # Bloquear los Entry para que no se puedan editar
        self.multa_nombre_usuario_entry.configure(state="disabled")
        self.multa_apellido_usuario_entry.configure(state="disabled")
        self.multa_rut_usuario_entry.configure(state="disabled")
        self.multa_celular_usuario_entry.configure(state="disabled")
        self.multa_correo_usuario_entry.configure(state="disabled")
        self.multa_tipo_usuario_entry.configure(state="disabled")
        self.multa_multa_usuario_entry.configure(state="disabled")
        self.multa_monto_usuario_entry.configure(state="disabled")
        self.multa_isbn_usuario_entry.configure(state="disabled")

    def pagarMulta(self):
        rut_usuario = self.buscar_rut_multa_entry.get()
        monto = self.multa_monto_usuario_entry.get()
        isbn = self.multa_isbn_usuario_entry.get()

        if rut_usuario:
            # Validar el RUT ingresado
            if self.validarRut(rut_usuario):
                # Marcar la multa como pagada en la tabla "usuario"
                self.bd.marcarMultaPagada(rut_usuario, isbn)
                self.limpiarCamposPagarMulta()

                # Actualizar la tabla de multas para reflejar los cambios
                self.cargarDatosTablaMultas()
                
                messagebox.showinfo("Pagar multa", f"La multa con RUT: {rut_usuario} ha sido pagada, monto total: {monto}")
            else:
                messagebox.showerror("RUT inválido", "El RUT ingresado no es válido. Por favor, ingrese un RUT válido.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un RUT de usuario para realizar el pago de la multa.")

    # MÉTODOS PARA FRAME DEVOLVER LIBROS
    # Método para buscar el prestamo por el RUT del usuario
    def buscarPrestamosPorRut(self):
        rut_usuario = self.buscar_rut_devolver_libro_entry.get()

        if rut_usuario:
            # Validar el RUT ingresado
            if self.validarRut(rut_usuario):
                # Obtener datos de los préstamos por el RUT del usuario
                datos_prestamos = self.bd.obtenerDevolverLibroRut(rut_usuario)

                if datos_prestamos:  # Si la lista no está vacía
                    # Limpiar la tabla
                    self.tabla_devolver_libro.delete(*self.tabla_devolver_libro.get_children())

                    # Insertar los datos en la tabla
                    for prestamo in datos_prestamos:
                        self.tabla_devolver_libro.insert('', 'end', values=prestamo)
                else:
                    messagebox.showinfo("Búsqueda de préstamos", f"No se encontraron préstamos para el RUT: {rut_usuario}.")
            else:
                messagebox.showerror("RUT inválido", "El RUT ingresado no es válido. Por favor, ingrese un RUT válido.")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, ingrese un RUT de usuario para realizar la búsqueda.")

    # Método para seleccionar la fila de la tabla
    def seleccionarFilaPrestamo(self, event):
        selected_item = self.tabla_devolver_libro.selection()
        if selected_item:
            prestamo_seleccionado = self.tabla_devolver_libro.item(selected_item[0], "values")
            self.prestamo_seleccionado = prestamo_seleccionado  # Almacenar la información del préstamo seleccionado
        else:
            self.prestamo_seleccionado = None

    def devolverLibro(self):
        selected_item = self.tabla_devolver_libro.selection()
        if not selected_item:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un préstamo de la tabla para devolver el libro.")
            return

        isbn = self.tabla_devolver_libro.item(selected_item, "values")[5]  # Obtener el ISBN seleccionado

        # Obtener el estado de la multa utilizando el ISBN seleccionado
        multa_estado = self.bd.obtenerEstadoMultaPorISBN(isbn)

        if multa_estado == "No pagado":
            messagebox.showerror("Devolución de Libros", "El usuario tiene una multa impaga. Debe pagar la multa antes de devolver un libro.")
        else:
            # Devolver el libro utilizando el ISBN seleccionado
            self.bd.devolverLibro(isbn)

            # Actualizar la tabla de préstamos
            self.buscarPrestamosPorRut()

            messagebox.showinfo("Devolución de Libros", "Libro devuelto con éxito.")

    def cargarDatosTablaDevolverLibro(self):
        try:
            # Obtener el RUT del usuario ingresado en el campo de búsqueda
            rut_usuario = self.buscar_rut_devolver_libro_entry.get()

            if not rut_usuario:
                messagebox.showwarning("Campo vacío", "Por favor, ingrese un RUT de usuario para realizar la búsqueda.")
                return

            # Validar el RUT ingresado
            if not self.validarRut(rut_usuario):
                messagebox.showerror("RUT inválido", "El RUT ingresado no es válido. Por favor, ingrese un RUT válido.")
                return

            # Obtener los datos de los préstamos por el RUT del usuario
            datos_prestamos = self.bd.obtenerDevolverLibroRut(rut_usuario)
            messagebox.showinfo("Busqueda de préstamos", "Tabla actualizada.")

            if not datos_prestamos:
                messagebox.showinfo("Búsqueda de préstamos", f"No se encontraron préstamos para el RUT: {rut_usuario}.")
                return

            # Limpiar la tabla
            self.tabla_devolver_libro.delete(*self.tabla_devolver_libro.get_children())

            # Insertar los datos en la tabla
            for prestamo in datos_prestamos:
                self.tabla_devolver_libro.insert('', 'end', values=prestamo)
        except Exception as e:
            messagebox.showerror("Error al cargar datos en la tabla", f"{str(e)}")

    # MÉTODOS ADICIONALES
    def validarEnTiempoReal(self, *args):
        # Validar número de celular
        entrada_celular = self.celular_usuario.get()
        if not entrada_celular.isdigit():
            self.celular_usuario_entry.delete(0, tk.END)
            self.celular_usuario_entry.insert(0, "".join(filter(str.isdigit, entrada_celular)))

        # Método para validar el correo electrónico
    
    # Métodos para validad el correo ingresado
    def validarCorreo(self, correo):
        patron = r'^[\w\.-]+@\w+\.\w+$'

        if re.match(patron, correo):
            return True
        else:
            return False

    # Método para validar el RUT ingresado
    def validarRut(self, rut):
        rut = rut.replace(".", "").replace("-", "")  # Remover puntos y guiones
        rut = rut.replace("k", "0")  # Reemplazar "k" por "0"
        rutSinDv = rut[:-1]  # Obtener el rut sin dígito verificador
        dv = rut[-1]  # Obtener el dígito verificador

        # Calcular el dígito verificador
        suma = 0
        multiplo = 2
        for i in reversed(rutSinDv):
            suma += int(i) * multiplo
            multiplo += 1
            if multiplo > 7:
                multiplo = 2

        resto = suma % 11
        dvEsperado = str(11 - resto) if resto > 1 else "0"

        return dv == dvEsperado

    # Método para limpiar los valores en los entry's
    def limpiarCamposRenovacion(self):
        self.rut_usuario.set('')
        self.isbn.set('')
        self.fecha_devolucion.set_date(datetime.now().date())

    # Método para limpiar los valores en los entry's    
    def limpiarCamposUsuario(self):
        self.nombre_usuario.set('')
        self.apellido_ususario.set('')
        self.direccion_usuario.set('')
        self.rut_usuario.set('')
        self.celular_usuario.set('')
        self.correo_usuario.set('')
        self.tipo_usuario.set('')
    
    # Método para limpiar los valores en los entry's
    def limpiarCamposPrestamo(self):
        self.rut_usuario.set('')
        self.isbn.set('')
        self.fecha_inicio.set_date(datetime.now().date())
        self.fecha_devolucion.set_date(datetime.now().date())
        self.tipo_usuario.set('')

    # Método para limpiar los valores en los entry's
    def limpiarCamposStock(self):
        self.buscar_actualiza.set('')
        self.isbn.set('')
        self.titulo.set('')
        self.numero_paginas.set('')
        self.stockLibro.set('')

    # Método para limpiar los valores en los entry´s
    def limpiarCamposPagarMulta(self):
        self.multa_nombre_usuario.set('')
        self.multa_apellido_usuario.set('')
        self.multa_rut_usuario.set('')
        self.multa_celular_usuario.set('')
        self.multa_correo_usuario.set('')
        self.multa_tipo_usuario.set('')
        self.multa_multa_usuario.set('')
        self.multa_monto_usuario.set('')
        self.multa_isbn_usuario.set('')

    # Método para cerrar sesion en la app
    def cerrar_sesion(self):
        self.destroy()
        self.parent.deiconify()