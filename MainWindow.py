import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar
import datetime
import os
import textwrap
import tempfile
import webbrowser
import pyperclip
from PIL import Image

# Ventana Principal
Receta = ctk.CTk()
Receta.geometry("600x600")
Receta.title("Generacion de Recetas")
Receta.resizable(1, 1)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

Receta.configure(fg_color="#ffffff") # Fuente para labels en negrita y negro

label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
label_instruccion = ctk.CTkFont(family="Arial", size=9, weight="bold")


def copiar_al_portapapeles():
    # Recopilar datos de los campos principales
    datos_paciente = {
        "Nombre": entry_nombre.get(),
        "Edad": entry_edad.get(),
        "Fecha": entry_fecha.get(),
        "Peso": entry_peso.get(),
        "Talla": entry_talla.get(),
    }
    
    # Determinar el modo (instrucciones o prosa)
    modo_prosa = checkbox_prosa.get()
    
    if modo_prosa:
        # En modo prosa, obtener el contenido del textbox
        texto_prosa = textbox_prosa.get("1.0", "end-1c").strip()
        
        # Formatear los datos para copiar al portapapeles
        texto_portapapeles = "DATOS DEL PACIENTE:\n"
        for clave, valor in datos_paciente.items():
            texto_portapapeles += f"{clave}: {valor}\n"
        
        texto_portapapeles += "\nTEXTO EN PROSA:\n"
        texto_portapapeles += texto_prosa
    else:
        # En modo instrucciones, recopilar las instrucciones
        instrucciones = []
        for i, widget in enumerate(instrucciones_widgets, 1):
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkTextbox):
                    texto = child.get("1.0", "end-1c").strip()
                    if texto:
                        instrucciones.append(f"INSTRUCCIÓN {i}: {texto}")
                    break
        
        # Formatear los datos para copiar al portapapeles
        texto_portapapeles = "DATOS DEL PACIENTE:\n"
        for clave, valor in datos_paciente.items():
            texto_portapapeles += f"{clave}: {valor}\n"
        
        texto_portapapeles += "\nINSTRUCCIONES:\n"
        for instruccion in instrucciones:
            texto_portapapeles += f"{instruccion}\n\n"
    
    # Copiar al portapapeles
    pyperclip.copy(texto_portapapeles)
    
    # Opcional: Puedes mostrar un mensaje de confirmación
    mensaje = ctk.CTkToplevel(Receta)
    mensaje.title("Éxito")
    mensaje.geometry("300x100")
    mensaje.resizable(0, 0)
    mensaje.grab_set()
    
    label = ctk.CTkLabel(mensaje, text="¡Datos copiados al portapapeles!", font=label_font)
    label.pack(pady=20)
    
    # Cerrar automáticamente el mensaje después de 2 segundos
    mensaje.after(2000, mensaje.destroy)

# Def calendario
def seleccionar_fecha():
    def set_date():
        fecha_seleccionada = cal.get_date()
        # Convertir string a objeto datetime
        fecha_obj = datetime.datetime.strptime(fecha_seleccionada, "%d/%m/%Y")
        # Formatear a dd/mm/aa
        fecha_formateada = fecha_obj.strftime("%d/%m/%y")
        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, fecha_formateada)
        top.destroy()
    
    top = ctk.CTkToplevel(Receta)
    top.title("Seleccionar Fecha")
    top.geometry("300x200")
    top.resizable(0, 0)
    top.grab_set()
    
    try:
        # Convertir fecha existente a objeto datetime para inicializar el calendario
        fecha_existente = datetime.datetime.strptime(entry_fecha.get(), "%d/%m/%y")
    except ValueError:
        fecha_existente = datetime.datetime.today()
    
    cal = Calendar(top,
                 selectmode='day',
                 year=fecha_existente.year,
                 month=fecha_existente.month,
                 day=fecha_existente.day,
                 date_pattern='dd/mm/yyyy')  # Patrón compatible con strptime
    cal.pack(pady=10)
    
    btn_aceptar = ctk.CTkButton(top, 
                               text="Seleccionar", 
                               command=set_date,
                               fg_color="#2CC985",
                               hover_color="#239561")
    btn_aceptar.pack(pady=5)

# Cuadros de Texto Espacios
x_label = .015
x_entry = .2
al_nombre= .02
al_edad= .08
al_fecha= .14
al_peso = .20
al_talla= .26
al_ta= .32
al_instrucciones = .65
color_label = "white"

# Frame para el formulario con bordes redondeados
Cuadro1 = ctk.CTkFrame(
    Receta, 
    fg_color="#0799b6",  
    corner_radius=10,    
    border_width=3,      
    border_color="#0ab1d3"
)
Cuadro1.place(relx=0.01, rely=0.01, relwidth=0.8, relheight=0.99)

# Frame 2 
Cuadro3 = ctk.CTkFrame(
    Receta, 
    fg_color="#4a6eb0",  
    corner_radius=10,    
    border_width=6,      
    border_color="white"  
)
Cuadro3.place(relx=0.825, rely=0.66, relwidth=0.15, relheight=0.3)

# Frame desplazable para instrucciones
instrucciones_scrollable = ctk.CTkScrollableFrame(
    Cuadro1, 
    fg_color="#4a6eb0", 
    scrollbar_button_color="#ffffff"
)
instrucciones_scrollable.place(relx=0.05, rely=0.50, relwidth=0.9, relheight=0.45)

# Frame para el modo prosa (inicialmente oculto)
prosa_frame = ctk.CTkFrame(Cuadro1, fg_color="#4a6eb0")

# Textbox con scrollbar para prosa
textbox_prosa = ctk.CTkTextbox(
    prosa_frame,
    wrap="word",
    fg_color="white",
    border_color="white",
    border_width=1,
    text_color="black",
    height=300  # Altura inicial
)
textbox_prosa.pack(fill="both", expand=True, padx=10, pady=10)

# Botones
button_frame = ctk.CTkFrame(Cuadro1, fg_color="#4a6eb0")
button_frame.place(relx=0.05, rely=0.39, relwidth=0.9, relheight=0.1)

# Lista para mantener los widgets de instrucciones
instrucciones_widgets = []

def agregar_instruccion():
    # Crear nuevo frame para cada instrucción
    frame = ctk.CTkFrame(instrucciones_scrollable, fg_color="#61461F")
    
    # Número de instrucción
    num_inst = len(instrucciones_widgets) + 1
    label = ctk.CTkLabel(frame, text=f" INSTRUCCIÓN {num_inst}:", 
                        font=label_instruccion, text_color=color_label)
    label.pack(side="left", padx=(0, 5))
    
    # Textbox con scrollbar
    textbox = ctk.CTkTextbox(frame, 
                         height=50,  # Altura inicial en píxeles
                         wrap="word",
                         fg_color="white",
                         border_color="white",
                         border_width=1,
                         text_color="black")
    
    textbox.pack(side="left", fill="both", expand=True, padx=(0, 5))
    
    # Función mejorada para ajustar altura
    def ajustar_altura(event=None):
        # Asegurar que el widget tenga tiempo para actualizarse
        textbox.update_idletasks()
        
        # Obtener el contenido actual
        contenido = textbox.get("1.0", "end-1c")
        
        # Contar las líneas reales (incluyendo saltos de línea)
        lineas = contenido.count('\n') + 1
        
        # Para textos largos sin saltos, calcular líneas adicionales basadas en el ancho
        ancho_textbox = textbox.winfo_width()
        if ancho_textbox > 10:  # Asegurarse de que el widget ya tiene un ancho
            # Estimar caracteres por línea (aproximadamente)
            chars_por_linea = max(30, ancho_textbox // 8)  # 8 píxeles por carácter es una aproximación
            
            # Añadir líneas adicionales para texto largo sin saltos
            for parrafo in contenido.split('\n'):
                if len(parrafo) > chars_por_linea:
                    lineas_adicionales = len(parrafo) // chars_por_linea
                    lineas += lineas_adicionales
        
        # Calcular nueva altura (mínimo 50px)
        # Altura aproximada por línea (depende de la fuente)
        altura_por_linea = 20
        altura_minima = 50
        altura_maxima = 300  # Aumentado para textos más largos
        
        nueva_altura = max(altura_minima, min(altura_maxima, lineas * altura_por_linea + 10))
        
        # Actualizar la altura solo si cambió significativamente
        altura_actual = textbox.winfo_height()
        if abs(altura_actual - nueva_altura) > 10:
            textbox.configure(height=nueva_altura)
            frame.update_idletasks()  # Forzar actualización del layout
    
    # Configurar eventos
    textbox.bind("<KeyRelease>", ajustar_altura)
    textbox.bind("<FocusOut>", ajustar_altura)  # Ajustar también al perder el foco
    
    # Programa un ajuste inicial después de 100ms (para dar tiempo a que el widget se dibuje)
    textbox.after(100, ajustar_altura)
    
    frame.pack(fill="x", pady=3)
    instrucciones_widgets.append(frame)

def eliminar_instruccion():
    if len(instrucciones_widgets) > 1:
        # Eliminar el último widget
        instrucciones_widgets.pop().destroy()

# Función para alternar entre modo prosa e instrucciones
def toggle_modo_prosa():
    modo_prosa = checkbox_prosa.get()
    
    if modo_prosa:
        # Ocultar modo instrucciones
        instrucciones_scrollable.place_forget()
        button_frame.place_forget()
        
        # Mostrar modo prosa
        prosa_frame.place(relx=0.05, rely=0.39, relwidth=0.9, relheight=0.56)
    else:
        # Ocultar modo prosa
        prosa_frame.place_forget()
        
        # Mostrar modo instrucciones
        instrucciones_scrollable.place(relx=0.05, rely=0.50, relwidth=0.9, relheight=0.45)
        button_frame.place(relx=0.05, rely=0.39, relwidth=0.9, relheight=0.1)

# Botones de control
btn_agregar = ctk.CTkButton(button_frame, 
                           text="➕ Añadir Instrucción",
                           command=agregar_instruccion,
                           width=120,
                           fg_color="#2CC985",
                           hover_color="#239561")
btn_agregar.pack(side="left", padx=10)

btn_eliminar = ctk.CTkButton(button_frame, 
                            text="➖ Eliminar Instrucción",
                            command=eliminar_instruccion,
                            width=120,
                            fg_color="#FF4D4D",
                            hover_color="#CC3E3E")
btn_eliminar.pack(side="right", padx=10)

# Agregar primera instrucción por defecto
agregar_instruccion()

# Caja 1 textos
label_nombre = ctk.CTkLabel(Cuadro1, text="👤 Nombre:", font=label_font, text_color=color_label)
label_nombre.place(relx=x_label, rely=al_nombre, relwidth=0.2)
entry_nombre = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black"
)
entry_nombre.place(relx=x_entry, rely=al_nombre, relwidth=0.7)

label_edad = ctk.CTkLabel(Cuadro1, text="🎂 Edad:", font=label_font, text_color=color_label)
label_edad.place(relx=x_label, rely=al_edad, relwidth=0.2)
entry_edad = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black"
)
entry_edad.place(relx=x_entry, rely=al_edad, relwidth=0.2)

label_fecha = ctk.CTkLabel(Cuadro1, text="📅 Fecha:", font=label_font, text_color=color_label)
label_fecha.place(relx=x_label, rely=al_fecha, relwidth=0.2)
entry_fecha = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black",
    width=100
)
entry_fecha.place(relx=x_entry, rely=al_fecha, relwidth=0.15)

btn_calendario = ctk.CTkButton(
    Cuadro1,
    text="📅",
    command=seleccionar_fecha,
    width=30,
    height=28,
    fg_color="#0799b6",
    hover_color="#0ab1d3",
    font=ctk.CTkFont(size=14)
)
btn_calendario.place(relx=x_entry + 0.16, rely=al_fecha)

label_peso = ctk.CTkLabel(Cuadro1, text="⚖️ Peso:", font=label_font, text_color=color_label)
label_peso.place(relx=x_label, rely=al_peso, relwidth=0.2)
entry_peso = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black"
)
entry_peso.place(relx=x_entry, rely=al_peso, relwidth=0.2)

label_talla = ctk.CTkLabel(Cuadro1, text="📏 Talla:", font=label_font, text_color=color_label)
label_talla.place(relx=x_label, rely=al_talla, relwidth=0.2)
entry_talla = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black"
)
entry_talla.place(relx=x_entry, rely=al_talla, relwidth=0.2)

label_ta = ctk.CTkLabel(Cuadro1, text="💓 TA:", font=label_font, text_color=color_label)
label_ta.place(relx=x_label, rely=al_ta, relwidth=0.2)
entry_ta = ctk.CTkEntry(
    Cuadro1, 
    fg_color="white", 
    border_color="white", 
    border_width=.5,
    text_color="black"
)
entry_ta.place(relx=x_entry, rely=al_ta, relwidth=0.2)

# Logo en el formulario
ruta_logo = os.path.join(os.path.dirname(__file__), "Logo.jpg")
logo_image = ctk.CTkImage(
    light_image=Image.open(ruta_logo), 
    dark_image=Image.open(ruta_logo), 
    size=(100, 125)  # Ajusta el tamaño según tus necesidades
)
logo_label = ctk.CTkLabel(
    Receta, 
    image=logo_image, 
    text="",
    # Sin texto
)
logo_label.place(relx=0.83, rely=0.35, relwidth=0.15)

# Frame para controles de formato
format_frame = ctk.CTkFrame(Cuadro1, fg_color="#4a6eb0")
format_frame.place(relx=0.05, rely=0.32, relwidth=0.9, relheight=0.06)

# Tamaño de fuente
label_fuente = ctk.CTkLabel(
    format_frame,
    text="Tamaño Fuente:",
    font=label_font,
    text_color="white"
)
label_fuente.pack(side="left", padx=10)

entry_fuente = ctk.CTkEntry(
    format_frame,
    justify="center",
    validate="key",
    validatecommand=(Receta.register(lambda text: text.isdigit() or text == ""), '%P'),
    width=60
)
entry_fuente.pack(side="left", padx=5)
entry_fuente.insert(0, "60")  # Valor por defecto

# Control de interlineado
label_interlineado = ctk.CTkLabel(
    format_frame,
    text="Interlineado:",
    font=label_font,
    text_color="white"
)
label_interlineado.pack(side="left", padx=10)

entry_interlineado = ctk.CTkEntry(
    format_frame,
    justify="center",
    validate="key",
    validatecommand=(Receta.register(lambda text: text.isdigit() or text == ""), '%P'),
    width=60
)
entry_interlineado.pack(side="left", padx=5)
entry_interlineado.insert(0, "20")  # Valor por defecto - 15 pixeles

# Añadir checkbox para alternar entre formato y sin formato
checkbox_formato = ctk.CTkCheckBox(
    Cuadro1,
    text="Formato",
    font=label_font,
    text_color=color_label,
    fg_color="#2CC985",
    hover_color="#239561",
    checkbox_height=20,
    checkbox_width=20
)
checkbox_formato.place(relx=0.5, rely=0.2, relwidth=0.4)

# Añadir checkbox para alternar entre modo instrucciones y prosa
checkbox_prosa = ctk.CTkCheckBox(
    Cuadro1,
    text="Prosa",
    font=label_font,
    text_color=color_label,
    fg_color="#2CC985",
    hover_color="#239561",
    checkbox_height=20,
    checkbox_width=20,
    command=toggle_modo_prosa
)
checkbox_prosa.place(relx=0.5, rely=0.26, relwidth=0.4)

def vaciar_campos():
    # Limpiar campos de Cuadro1
    entry_nombre.delete(0, 'end')
    entry_edad.delete(0, 'end')
    entry_fecha.delete(0, 'end')
    entry_peso.delete(0, 'end')
    entry_talla.delete(0, 'end')
    entry_ta.delete(0, 'end')
    
    # Limpiar textbox de prosa
    textbox_prosa.delete("1.0", "end")
    
    # Limpiar instrucciones
    for widget in instrucciones_widgets:
        widget.destroy()
    instrucciones_widgets.clear()
    agregar_instruccion()

# Función para determinar el ancho máximo de texto según el tamaño de fuente
def obtener_ancho_maximo(tamano_fuente):
    # AQUÍ PUEDES PERSONALIZAR LOS VALORES PARA CADA TAMAÑO DE FUENTE
    # Estas condiciones determinan cuántos caracteres pueden caber en una línea
    # para diferentes tamaños de fuente
    tamano = int(tamano_fuente)
    
    # Valores personalizados para distintos rangos de tamaño de fuente
    if tamano <= 20:
        return 200  # Muchos caracteres para fuentes muy pequeñas
    elif tamano <= 25:
        return 170
    elif tamano <= 30:
        return 150
    elif tamano <= 35:
        return 140
    elif tamano <= 40:
        return 120
    elif tamano <= 45:
        return 100
    elif tamano <= 50:
        return 90
    elif tamano <= 60:
        return 70
    elif tamano <= 65:
        return 65
    elif tamano <= 70:
        return 60
    elif tamano <= 75:
        return 55
    else:
        return 60  # Pocos caracteres para fuentes muy grandes

def Generar_Imagen_Con_Formato():
    """
    Genera una imagen de receta con formato completo (con logotipos, datos de contacto,
    y todos los elementos de diseño). Soporta tanto el modo de instrucciones como el modo prosa.
    """
    imagen = Image.new("RGB", (2550, 3300), color="white")
    draw = ImageDraw.Draw(imagen)

    try:
        ESPACIO_ENTRE_LINEAS = int(entry_interlineado.get())
        if ESPACIO_ENTRE_LINEAS <= 0:
            ESPACIO_ENTRE_LINEAS = 15  # Valor predeterminado si es negativo o cero
    except:
        ESPACIO_ENTRE_LINEAS = 15  # Valor predeterminado si no es un número válido
    
    # Configuración para texto de una sola columna ancha
    Y_MAX = 2750  # Ajustado para dar más espacio vertical
    X_INICIAL = 200
    y_actual = 1100  # Y_INICIAL
    
    # Almacen de inputs
    datos = {
        "Nombre": entry_nombre.get(),
        "Edad": entry_edad.get(),
        "Fecha": entry_fecha.get(),
        "Peso": entry_peso.get(),
        "Talla": entry_talla.get(),
        "TA": entry_ta.get()
    }
    
    # Fuentes
    Fuente1 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 50)
    Fuente2 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 30)
    
    # Creacion de imagenes 
    ruta_mitad = os.path.join(os.path.dirname(__file__), "mitad.jpg")
    mitad = Image.open(ruta_mitad)
    anchomitad, altomitad = 1100, 2400  
    mitad = mitad.resize((anchomitad, altomitad))
    imagen.paste(mitad, (1460, 600))
   
    # Mancha
    ruta_mancha = os.path.join(os.path.dirname(__file__), "Mancha.png")
    mancha = Image.open(ruta_mancha)
    anchomancha, altomancha = 1600, 500  
    mancha = mancha.resize((anchomancha, altomancha))
    imagen.paste(mancha, (0, 2800))
   
    # Logo
    ruta_logo = os.path.join(os.path.dirname(__file__), "Logo.jpg")
    logo = Image.open(ruta_logo)
    anchologo, altologo = 400, 500  
    logo = logo.resize((anchologo, altologo))
    imagen.paste(logo, (200, 70))
   
    # Encabezado1 arriba a la derecha
    texto1 = "Dra. Mónica Reyes Berlanga"
    draw.text((2450, 70), texto1, font=Fuente1, fill=(50, 50, 50), spacing=1.5, anchor="rt")
    texto2 = "Infectóloga"
    draw.text((2450, 125), texto2, font=Fuente1, fill=(50, 50, 50), anchor="rt")
    texto3 = "CED. PROF. 1826231 CED. PED. AE-007858 CED. INFECTÓLOGA 5988060"
    draw.text((2450, 195), texto3, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto4 = "CED. MIAC. 8402586 CED. DAEO. 00022662 CERT. PED. 6344"
    draw.text((2450, 235), texto4, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto5 = "CERTIFICACIÓN INFECTOLOGÍA 2044"
    draw.text((2450, 265), texto5, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto6 = "Academia Mexicana de Pediatría"
    draw.text((2450, 325), texto6, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto7 = "Académico Numerario"
    draw.text((2450, 365), texto7, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto8 = "Asociación Mexicana de Infectología Pediátrica"
    draw.text((2450, 430), texto8, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto9 = "Vicepresidenta"
    draw.text((2450, 470), texto9, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto10 = "American Academy of Pediatrics"
    draw.text((2450, 535), texto10, font=Fuente2, fill=(50, 50, 50), anchor="rt")
    texto11 = "International Member"
    draw.text((2450, 575), texto11, font=Fuente2, fill=(50, 50, 50), anchor="rt")

    # Encabezado 2 Abajo de la derecha
    ruta_whatsapp = os.path.join(os.path.dirname(__file__), "Whatsapp.jpg")
    whatsapp = Image.open(ruta_whatsapp)
    anchowhat, altowhat = 55, 55  
    whatsapp = whatsapp.resize((anchowhat, altowhat))
    texto21 = "WhatsApp: 462 146 3202"
    draw.text((1700, 3000), texto21, font=Fuente1, fill=(50, 50, 50))
    imagen.paste(whatsapp, (1635, 3000))

    ruta_facebook = os.path.join(os.path.dirname(__file__), "Facebook.jpg") 
    facebook = Image.open(ruta_facebook)
    ancho_facebook, alto_facebook = 55, 55  
    facebook = facebook.resize((ancho_facebook, alto_facebook))
    texto22 = "Infectología Berlanga"
    draw.text((1700, 3075), texto22, font=Fuente1, fill=(50, 50, 50))
    imagen.paste(facebook, (1635, 3075))

    ruta_sobre = os.path.join(os.path.dirname(__file__), "Sobre.jpg") 
    sobre = Image.open(ruta_sobre)
    ancho_sobre, alto_sobre = 55, 55 
    sobre = sobre.resize((ancho_sobre, alto_sobre))
    texto23 = r"reyesberlanga@yahoo.com.mx"
    draw.text((1700, 3150), texto23, font=Fuente1, fill=(50, 50, 50))
    imagen.paste(sobre, (1635, 3150))
    
    # Encabezado 3 abajo a la izquierda
    ruta_gps = os.path.join(os.path.dirname(__file__), "GPS.png") 
    gps = Image.open(ruta_gps).convert("RGBA")  # Asegurar modo RGBA
    ancho_gps, alto_gps = 55, 55 

    # Redimensionar manteniendo la transparencia
    gps = gps.resize((ancho_gps, alto_gps), Image.Resampling.LANCZOS)

    # Crear máscara de transparencia
    mask = gps.split()[3] if gps.mode == 'RGBA' else None

    # Pegar la imagen conservando la transparencia
    imagen.paste(gps, (135, 2925), mask)

    texto30 = r"HOSPITAL MAC IRAPUATO"
    draw.text((200, 2925), texto30, font=Fuente1, fill='white')    
    texto31 = r"Consultorio #303 3er. Piso"
    draw.text((200, 3000), texto31, font=Fuente1, fill='white')
    texto32 = r"Calle Dr. Javier Castellanos #564"
    draw.text((200, 3075), texto32, font=Fuente1, fill='white')
    texto33 = r"CP. 36520 Irapuato, Gto"
    draw.text((200, 3150), texto33, font=Fuente1, fill='white')
    
    # Datos del Paciente
    draw.text((200, 800), f"Nombre: {datos['Nombre']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((2000, 800), f"Edad: {datos['Edad']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((200, 900), f"Fecha: {datos['Fecha']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((800, 900), f"Peso: {datos['Peso']} kg", font=Fuente1, fill=(50, 50, 50))
    draw.text((1400, 900), f"Talla: {datos['Talla']} cm", font=Fuente1, fill=(50, 50, 50))
    draw.text((2000, 900), f"TA: {datos['TA']} mmHg", font=Fuente1, fill=(50, 50, 50))
    
    # Configuración para el texto
    tamano_fuente = int(entry_fuente.get()) if entry_fuente.get().isdigit() and int(entry_fuente.get()) > 0 else 30
    # Obtener el ancho máximo de texto según el tamaño de fuente
    max_caracteres = obtener_ancho_maximo(tamano_fuente)
    FuenteInstrucciones = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', tamano_fuente)
    
    # Verificar si estamos en modo prosa o instrucciones
    if checkbox_prosa.get():
        # Modo prosa: obtener texto del textbox_prosa
        texto_prosa = textbox_prosa.get("1.0", "end-1c").strip()
        
        # Procesar el texto con saltos de línea y ajuste de texto
        lineas_brutas = texto_prosa.split('\n')
        todas_lineas = []
        
        for segmento in lineas_brutas:
            # Ajustar el texto al ancho máximo
            lineas_envueltas = textwrap.wrap(segmento, width=max_caracteres)
            todas_lineas.extend(lineas_envueltas if lineas_envueltas else [''])  # Asegurar que las líneas vacías se preserven
        
        # Dibujar todas las líneas del texto en prosa
        for linea in todas_lineas:
            if y_actual > Y_MAX:
                break
                
            draw.text((X_INICIAL, y_actual), linea, font=FuenteInstrucciones, fill=(50, 50, 50))
            bbox = draw.textbbox((0, 0), linea, font=FuenteInstrucciones)
            y_actual += (bbox[3] - bbox[1]) + ESPACIO_ENTRE_LINEAS
    else:
        # Modo instrucciones: obtener instrucciones numeradas
        instrucciones = []
        for widget in instrucciones_widgets:
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkTextbox):
                    texto = child.get("1.0", "end-1c").strip()
                    if texto:
                        instrucciones.append(texto)
                    break

        # Calcular el espacio entre instrucciones basado en el interlineado
        espacio_entre_instrucciones = ESPACIO_ENTRE_LINEAS * 2

        for i, instruccion in enumerate(instrucciones, 1):
            # Procesar saltos manuales y automáticos
            lineas_brutas = instruccion.split('\n')
            todas_lineas = []
            
            for segmento in lineas_brutas:
                # Usar el ancho definido por la función
                lineas_envueltas = textwrap.wrap(segmento, width=max_caracteres)
                todas_lineas.extend(lineas_envueltas if lineas_envueltas else [''])  # Preservar líneas vacías
            
            for j, linea in enumerate(todas_lineas):
                if y_actual > Y_MAX:
                    # Si se supera el límite vertical, no se dibuja más texto
                    break
                
                texto = f"{i}. {linea}" if j == 0 else f"    {linea}"
                draw.text((X_INICIAL, y_actual), texto, font=FuenteInstrucciones, fill=(50, 50, 50))
                bbox = draw.textbbox((0, 0), texto, font=FuenteInstrucciones)
                y_actual += (bbox[3] - bbox[1]) + ESPACIO_ENTRE_LINEAS
            
            # Añadir espacio extra entre instrucciones
            y_actual += espacio_entre_instrucciones
    
    # Guardar la imagen como PDF
    crear_pdf(imagen)

def Generar_Imagen_Sin_Formato():
    """
    Genera una imagen de receta sin formato (sin elementos decorativos, solo contenido principal).
    Soporta tanto el modo de instrucciones como el modo prosa.
    """
    imagen = Image.new("RGB", (2550, 3300), color="white")
    draw = ImageDraw.Draw(imagen)

    try:
        ESPACIO_ENTRE_LINEAS = int(entry_interlineado.get())
        if ESPACIO_ENTRE_LINEAS <= 0:
            ESPACIO_ENTRE_LINEAS = 15  # Valor predeterminado si es negativo o cero
    except:
        ESPACIO_ENTRE_LINEAS = 15  # Valor predeterminado si no es un número válido
    
    # Configuración para texto de una sola columna ancha
    Y_MAX = 2750  # Ajustado para dar más espacio vertical
    X_INICIAL = 200
    y_actual = 1100  # Y_INICIAL
    
    # Almacen de inputs
    datos = {
        "Nombre": entry_nombre.get(),
        "Edad": entry_edad.get(),
        "Fecha": entry_fecha.get(),
        "Peso": entry_peso.get(),
        "Talla": entry_talla.get(),
        "TA": entry_ta.get()
    }
    
    # Fuentes
    Fuente1 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 50)
    
    # Datos del Paciente
    draw.text((200, 800), f"Nombre: {datos['Nombre']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((2000, 800), f"Edad: {datos['Edad']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((200, 900), f"Fecha: {datos['Fecha']}", font=Fuente1, fill=(50, 50, 50))
    draw.text((800, 900), f"Peso: {datos['Peso']} kg", font=Fuente1, fill=(50, 50, 50))
    draw.text((1400, 900), f"Talla: {datos['Talla']} cm", font=Fuente1, fill=(50, 50, 50))
    draw.text((2000, 900), f"TA: {datos['TA']} mmHg", font=Fuente1, fill=(50, 50, 50))
    
    # Configuración para el texto
    tamano_fuente = int(entry_fuente.get()) if entry_fuente.get().isdigit() and int(entry_fuente.get()) > 0 else 30
    max_caracteres = obtener_ancho_maximo(tamano_fuente)
    FuenteInstrucciones = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', tamano_fuente)

    # Verificar si estamos en modo prosa o instrucciones
    if checkbox_prosa.get():
        # Modo prosa: obtener texto del textbox_prosa
        texto_prosa = textbox_prosa.get("1.0", "end-1c").strip()
        
        # Procesar el texto con saltos de línea y ajuste de texto
        lineas_brutas = texto_prosa.split('\n')
        todas_lineas = []
        
        for segmento in lineas_brutas:
            # Ajustar el texto al ancho máximo
            lineas_envueltas = textwrap.wrap(segmento, width=max_caracteres)
            todas_lineas.extend(lineas_envueltas if lineas_envueltas else [''])  # Preservar líneas vacías
        
        # Dibujar todas las líneas del texto en prosa
        for linea in todas_lineas:
            if y_actual > Y_MAX:
                break
                
            draw.text((X_INICIAL, y_actual), linea, font=FuenteInstrucciones, fill=(50, 50, 50))
            bbox = draw.textbbox((0, 0), linea, font=FuenteInstrucciones)
            y_actual += (bbox[3] - bbox[1]) + ESPACIO_ENTRE_LINEAS
    else:
        # Modo instrucciones: obtener instrucciones numeradas
        instrucciones = []
        for widget in instrucciones_widgets:
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkTextbox):
                    texto = child.get("1.0", "end-1c").strip()
                    if texto:
                        instrucciones.append(texto)
                    break

        # Calcular el espacio entre instrucciones basado en el interlineado
        espacio_entre_instrucciones = ESPACIO_ENTRE_LINEAS * 2

        for i, instruccion in enumerate(instrucciones, 1):
            # Procesar saltos manuales y automáticos
            lineas_brutas = instruccion.split('\n')
            todas_lineas = []
            
            for segmento in lineas_brutas:
                # Usar el ancho definido por la función
                lineas_envueltas = textwrap.wrap(segmento, width=max_caracteres)
                todas_lineas.extend(lineas_envueltas if lineas_envueltas else [''])  # Preservar líneas vacías
            
            for j, linea in enumerate(todas_lineas):
                if y_actual > Y_MAX:
                    # Si se supera el límite vertical, no se dibuja más texto
                    break
                
                texto = f"{i}. {linea}" if j == 0 else f"    {linea}"
                draw.text((X_INICIAL, y_actual), texto, font=FuenteInstrucciones, fill=(50, 50, 50))
                bbox = draw.textbbox((0, 0), texto, font=FuenteInstrucciones)
                y_actual += (bbox[3] - bbox[1]) + ESPACIO_ENTRE_LINEAS
            
            # Añadir espacio extra entre instrucciones
            y_actual += espacio_entre_instrucciones
    
    # Guardar la imagen como PDF
    crear_pdf(imagen)

def crear_pdf(imagen):
    try:
        # Crear un archivo temporal para el PDF
        pdf_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = pdf_temp.name
        pdf_temp.close()
        
        # Guardar la imagen como PDF
        imagen.save(pdf_path, "PDF", resolution=100.0)
        
        # Abrir el PDF con el visor predeterminado
        webbrowser.open(pdf_path)
    except Exception as e:
        print(f"Error al crear el PDF: {e}")

def generar_receta():
    # Comprobar el estado del checkbox y llamar a la función correspondiente
    if checkbox_formato.get():
        Generar_Imagen_Con_Formato()
    else:
        Generar_Imagen_Sin_Formato()

# Actualizar el botón para utilizar la nueva función
boton_imagen = ctk.CTkButton(
    Cuadro3, 
    text="Generar Receta", 
    command=generar_receta, 
    font=ctk.CTkFont(family="Arial", size=8)
)
boton_imagen.place(relx=0.1, rely=0.2, relwidth=0.8)

btn_copiar = ctk.CTkButton(
    Cuadro3,
    text="Copiar Datos",
    command=copiar_al_portapapeles, 
    fg_color="#2C85CC",
    hover_color="#23619C",
    font=ctk.CTkFont(family="Arial", size=8)
)
btn_copiar.place(relx=0.1, rely=0.7, relwidth=0.8)

btn_vaciar = ctk.CTkButton(
    Cuadro3,
    text="Vaciar Campos",
    command=vaciar_campos, 
    fg_color="#FF4D4D",
    hover_color="#CC3E3E",
    font=ctk.CTkFont(family="Arial", size=8)
)
btn_vaciar.place(relx=0.1, rely=0.45, relwidth=0.8)

Receta.mainloop()