import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
from tkcalendar import Calendar
import os
import tempfile
import webbrowser
import pyperclip
from PIL import Image

from seleccionar_fecha import SeleccionarFecha
from gestionar_instrucciones import GestorInstrucciones
from generador_imagen import GeneradorImagen


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

gestor_inst = GestorInstrucciones(instrucciones_scrollable)

# Botones de control

btn_agregar = ctk.CTkButton(
    button_frame,
    text="➕ Añadir Instrucción",
    command=gestor_inst.agregar,
    width=120,
    fg_color="#2CC985",
    hover_color="#239561"
)
btn_agregar.pack(side="left", padx=10)

btn_eliminar = ctk.CTkButton(
    button_frame,
    text="➖ Eliminar Instrucción",
    command=gestor_inst.eliminar,
    width=120,
    fg_color="#FF4D4D",
    hover_color="#CC3E3E"
)
btn_eliminar.pack(side="right", padx=10)



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
    command=lambda: SeleccionarFecha(Receta, entry_fecha),
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
    
generador = GeneradorImagen(
    entry_nombre, entry_edad, entry_fecha, entry_peso, entry_talla, entry_ta,
    textbox_prosa, instrucciones_widgets, checkbox_prosa,
    entry_fuente, entry_interlineado,
    logo_path=os.path.join(os.path.dirname(__file__), "Logo.jpg")
)


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
    if checkbox_formato.get():
        generador.generar_con_formato()
    else:
        generador.generar_sin_formato()


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