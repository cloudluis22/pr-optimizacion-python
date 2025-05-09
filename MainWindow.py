import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar
import os
import tempfile
import webbrowser
import pyperclip
# Eliminar importación duplicada de PIL.Image
# from PIL import Image

from seleccionar_fecha import SeleccionarFecha
from gestionar_instrucciones import GestorInstrucciones
from generador_imagen import GeneradorImagen


# Definir constantes para colores y posiciones
COLORS = {
    "white": "#ffffff",
    "primary": "#0799b6",
    "primary_hover": "#0ab1d3",
    "secondary": "#4a6eb0",
    "success": "#2CC985",
    "success_hover": "#239561",
    "danger": "#FF4D4D",
    "danger_hover": "#CC3E3E"
}

# Ventana Principal
Receta = ctk.CTk()
Receta.geometry("600x600")
Receta.title("Generacion de Recetas")
Receta.resizable(1, 1)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

Receta.configure(fg_color=COLORS["white"])

# Fuentes
label_font = ctk.CTkFont(family="Arial", size=14, weight="bold")
label_instruccion = ctk.CTkFont(family="Arial", size=9, weight="bold")
button_font = ctk.CTkFont(family="Arial", size=8)

# Función para crear etiquetas y entradas estándar
def crear_label_entry(parent, texto, relx_label, rely, relx_entry, relwidth_label=0.2, relwidth_entry=0.7, emoji=""):
    label = ctk.CTkLabel(
        parent, 
        text=f"{emoji} {texto}:", 
        font=label_font, 
        text_color="white"
    )
    label.place(relx=relx_label, rely=rely, relwidth=relwidth_label)
    
    entry = ctk.CTkEntry(
        parent, 
        fg_color="white", 
        border_color="white", 
        border_width=0.5,
        text_color="black"
    )
    entry.place(relx=relx_entry, rely=rely, relwidth=relwidth_entry)
    return label, entry

def copiar_al_portapapeles():
    # Recopilar datos de los campos principales
    datos_paciente = {
        "Nombre": entry_nombre.get(),
        "Edad": entry_edad.get(),
        "Fecha": entry_fecha.get(),
        "Peso": entry_peso.get(),
        "Talla": entry_talla.get(),
        "TA": entry_ta.get()  # Añadido TA que faltaba en el dict original
    }
    
    # Determinar el modo (instrucciones o prosa)
    modo_prosa = checkbox_prosa.get()
    
    # Preparar encabezado de datos del paciente
    texto_portapapeles = "DATOS DEL PACIENTE:\n"
    for clave, valor in datos_paciente.items():
        texto_portapapeles += f"{clave}: {valor}\n"
    
    if modo_prosa:
        # En modo prosa, obtener el contenido del textbox
        texto_prosa = textbox_prosa.get("1.0", "end-1c").strip()
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
        
        texto_portapapeles += "\nINSTRUCCIONES:\n"
        texto_portapapeles += "\n\n".join(instrucciones)
    
    # Copiar al portapapeles
    pyperclip.copy(texto_portapapeles)
    
    # Mostrar mensaje de confirmación
    mostrar_mensaje(Receta, "¡Datos copiados al portapapeles!", 2000)

def mostrar_mensaje(parent, texto, tiempo_ms=2000):
    """Función reutilizable para mostrar mensajes temporales"""
    mensaje = ctk.CTkToplevel(parent)
    mensaje.title("Mensaje")
    mensaje.geometry("300x100")
    mensaje.resizable(0, 0)
    mensaje.grab_set()
    
    label = ctk.CTkLabel(mensaje, text=texto, font=label_font)
    label.pack(pady=20)
    
    # Cerrar automáticamente el mensaje después del tiempo especificado
    mensaje.after(tiempo_ms, mensaje.destroy)

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
    fg_color=COLORS["primary"],  
    corner_radius=10,    
    border_width=3,      
    border_color=COLORS["primary_hover"]
)
Cuadro1.place(relx=0.01, rely=0.01, relwidth=0.8, relheight=0.99)

# Frame 2 - para botones laterales
Cuadro3 = ctk.CTkFrame(
    Receta, 
    fg_color=COLORS["secondary"],  
    corner_radius=10,    
    border_width=6,      
    border_color="white"  
)
Cuadro3.place(relx=0.825, rely=0.66, relwidth=0.15, relheight=0.3)

# Frame desplazable para instrucciones
instrucciones_scrollable = ctk.CTkScrollableFrame(
    Cuadro1,
    fg_color=COLORS["secondary"],
    scrollbar_button_color=COLORS["white"]
)
instrucciones_scrollable.place(relx=0.05, rely=0.50, relwidth=0.9, relheight=0.45)

# Frame para el modo prosa (inicialmente oculto)
prosa_frame = ctk.CTkFrame(Cuadro1, fg_color=COLORS["secondary"])

# Textbox con scrollbar para prosa
textbox_prosa = ctk.CTkTextbox(
    prosa_frame,
    wrap="word",
    fg_color="white",
    border_color="white",
    border_width=1,
    text_color="black",
    height=300
)
textbox_prosa.pack(fill="both", expand=True, padx=10, pady=10)

# Botones
button_frame = ctk.CTkFrame(Cuadro1, fg_color=COLORS["secondary"])
button_frame.place(relx=0.05, rely=0.39, relwidth=0.9, relheight=0.1)

# Lista para mantener los widgets de instrucciones
instrucciones_widgets = []

# Función para abrir el selector de fecha
def abrir_selector_fecha():
    SeleccionarFecha(Receta, entry_fecha)

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

# Configurar gestor de instrucciones
gestor_inst = GestorInstrucciones(instrucciones_scrollable)

# Crear botón con apariencia estándar
def crear_boton(parent, texto, comando, fg_color, hover_color, side="left", padx=10, font=None):
    btn = ctk.CTkButton(
        parent,
        text=texto,
        command=comando,
        width=120,
        fg_color=fg_color,
        hover_color=hover_color,
        font=font if font else button_font
    )
    btn.pack(side=side, padx=padx)
    return btn

# Botones de control para instrucciones
btn_agregar = crear_boton(
    button_frame,
    "➕ Añadir Instrucción",
    gestor_inst.agregar,
    COLORS["success"],
    COLORS["success_hover"]
)

btn_eliminar = crear_boton(
    button_frame,
    "➖ Eliminar Instrucción",
    gestor_inst.eliminar,
    COLORS["danger"],
    COLORS["danger_hover"],
    side="right"
)

# Campos de texto (usando la función crear_label_entry)
_, entry_nombre = crear_label_entry(Cuadro1, "Nombre", x_label, al_nombre, x_entry, relwidth_entry=0.7, emoji="👤")
_, entry_edad = crear_label_entry(Cuadro1, "Edad", x_label, al_edad, x_entry, relwidth_entry=0.2, emoji="🎂")

# Para el campo fecha con botón especial
label_fecha, entry_fecha = crear_label_entry(Cuadro1, "Fecha", x_label, al_fecha, x_entry, relwidth_entry=0.15, emoji="📅")

# Botón calendario
btn_calendario = ctk.CTkButton(
    Cuadro1,
    text="📅",
    command=abrir_selector_fecha,
    width=30,
    height=28,
    fg_color=COLORS["primary"],
    hover_color=COLORS["primary_hover"],
    font=ctk.CTkFont(size=14)
)
btn_calendario.place(relx=x_entry + 0.16, rely=al_fecha)

# Resto de campos
_, entry_peso = crear_label_entry(Cuadro1, "Peso", x_label, al_peso, x_entry, relwidth_entry=0.2, emoji="⚖️")
_, entry_talla = crear_label_entry(Cuadro1, "Talla", x_label, al_talla, x_entry, relwidth_entry=0.2, emoji="📏")
_, entry_ta = crear_label_entry(Cuadro1, "TA", x_label, al_ta, x_entry, relwidth_entry=0.2, emoji="💓")

# Logo en el formulario - Optimización de la carga de imagen
RUTA_LOGO = os.path.join(os.path.dirname(__file__), "Logo.jpg")
logo_image = ctk.CTkImage(
    light_image=Image.open(RUTA_LOGO), 
    dark_image=Image.open(RUTA_LOGO), 
    size=(100, 125)
)
logo_label = ctk.CTkLabel(
    Receta, 
    image=logo_image, 
    text=""
)
logo_label.place(relx=0.83, rely=0.35, relwidth=0.15)

# Frame para controles de formato
format_frame = ctk.CTkFrame(Cuadro1, fg_color=COLORS["secondary"])
format_frame.place(relx=0.05, rely=0.32, relwidth=0.9, relheight=0.06)

# Función para validar entrada numérica
def validar_numero(text):
    return text.isdigit() or text == ""

# Función para crear campo de entrada de configuración
def crear_campo_config(parent, texto, valor_defecto, validacion=None, width=60):
    label = ctk.CTkLabel(
        parent,
        text=texto,
        font=label_font,
        text_color="white"
    )
    label.pack(side="left", padx=10)
    
    validate_cmd = None
    if validacion:
        validate_cmd = (Receta.register(validacion), '%P')
    
    entry = ctk.CTkEntry(
        parent,
        justify="center",
        validate="key" if validacion else "none",
        validatecommand=validate_cmd,
        width=width
    )
    entry.pack(side="left", padx=5)
    entry.insert(0, str(valor_defecto))
    return entry

# Campos de configuración
entry_fuente = crear_campo_config(format_frame, "Tamaño Fuente:", 60, validar_numero)
entry_interlineado = crear_campo_config(format_frame, "Interlineado:", 20, validar_numero)

# Checkboxes
def crear_checkbox(parent, texto, relx, rely, relwidth, comando=None):
    checkbox = ctk.CTkCheckBox(
        parent,
        text=texto,
        font=label_font,
        text_color=color_label,
        fg_color=COLORS["success"],
        hover_color=COLORS["success_hover"],
        checkbox_height=20,
        checkbox_width=20,
        command=comando
    )
    checkbox.place(relx=relx, rely=rely, relwidth=relwidth)
    return checkbox

checkbox_formato = crear_checkbox(Cuadro1, "Formato", 0.5, 0.2, 0.4)
checkbox_prosa = crear_checkbox(Cuadro1, "Prosa", 0.5, 0.26, 0.4, toggle_modo_prosa)

def vaciar_campos():
    """Función para vaciar todos los campos del formulario"""
    # Limpiar campos de texto
    for entry in [entry_nombre, entry_edad, entry_fecha, entry_peso, entry_talla, entry_ta]:
        entry.delete(0, 'end')
    
    # Limpiar textbox de prosa
    textbox_prosa.delete("1.0", "end")
    
    # Limpiar instrucciones
    for widget in instrucciones_widgets:
        widget.destroy()
    instrucciones_widgets.clear()
    
# Configurar generador de imágenes
generador = GeneradorImagen(
    entry_nombre, entry_edad, entry_fecha, entry_peso, entry_talla, entry_ta,
    textbox_prosa, instrucciones_widgets, checkbox_prosa,
    entry_fuente, entry_interlineado,
    logo_path=RUTA_LOGO
)

def crear_pdf(imagen):
    """Función para crear PDF a partir de imagen"""
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
        mostrar_mensaje(Receta, f"Error: {e}", 3000)

def generar_receta():
    """Generar la receta según el modo seleccionado"""
    if checkbox_formato.get():
        generador.generar_con_formato()
    else:
        generador.generar_sin_formato()

# Botones en el panel lateral
boton_imagen = crear_boton(
    Cuadro3, 
    "Generar Receta", 
    generar_receta, 
    COLORS["primary"],
    COLORS["primary_hover"]
)
boton_imagen.place(relx=0.1, rely=0.2, relwidth=0.8)

btn_vaciar = crear_boton(
    Cuadro3,
    "Vaciar Campos",
    vaciar_campos, 
    COLORS["danger"],
    COLORS["danger_hover"]
)
btn_vaciar.place(relx=0.1, rely=0.45, relwidth=0.8)

btn_copiar = crear_boton(
    Cuadro3,
    "Copiar Datos",
    copiar_al_portapapeles,
    "#2C85CC",
    "#23619C"
)
btn_copiar.place(relx=0.1, rely=0.7, relwidth=0.8)

Receta.mainloop()