from PIL import Image, ImageDraw, ImageFont
import textwrap
import tempfile
import webbrowser
import os
import customtkinter as ctk

class GeneradorImagen:
    def __init__(self, entry_nombre, entry_edad, entry_fecha, entry_peso, entry_talla, entry_ta,
                 textbox_prosa, instrucciones_widgets, checkbox_prosa,
                 entry_fuente, entry_interlineado,
                 logo_path, recursos_dir=None):
        self.entry_nombre = entry_nombre
        self.entry_edad = entry_edad
        self.entry_fecha = entry_fecha
        self.entry_peso = entry_peso
        self.entry_talla = entry_talla
        self.entry_ta = entry_ta
        self.textbox_prosa = textbox_prosa
        self.instrucciones_widgets = instrucciones_widgets
        self.checkbox_prosa = checkbox_prosa
        self.entry_fuente = entry_fuente
        self.entry_interlineado = entry_interlineado
        self.logo_path = logo_path
        self.recursos_dir = recursos_dir or os.path.dirname(__file__)

    def _obtener_ancho_maximo(self, tamano_fuente):
        tam = int(tamano_fuente)
        if tam <= 20: return 200
        elif tam <= 25: return 170
        elif tam <= 30: return 150
        elif tam <= 35: return 140
        elif tam <= 40: return 120
        elif tam <= 45: return 100
        elif tam <= 50: return 90
        elif tam <= 60: return 70
        elif tam <= 65: return 65
        elif tam <= 70: return 60
        elif tam <= 75: return 55
        else: return 60

    def _crear_pdf(self, imagen):
        temp = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        path = temp.name
        temp.close()
        imagen.save(path, "PDF", resolution=100.0)
        webbrowser.open(path)

    def generar_con_formato(self):
        imagen = Image.new("RGB", (2550, 3300), color="white")
        draw = ImageDraw.Draw(imagen)
        try:
            espacio = int(self.entry_interlineado.get())
            if espacio <= 0: espacio = 15
        except:
            espacio = 15

        # Datos paciente
        datos = {
            "Nombre": self.entry_nombre.get(),
            "Edad": self.entry_edad.get(),
            "Fecha": self.entry_fecha.get(),
            "Peso": self.entry_peso.get(),
            "Talla": self.entry_talla.get(),
            "TA": self.entry_ta.get()
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

        # Texto principal
        tam_fuente = int(self.entry_fuente.get()) if self.entry_fuente.get().isdigit() else 30
        max_chars = self._obtener_ancho_maximo(tam_fuente)
        fuente = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', tam_fuente)

        if self.checkbox_prosa.get():
            texto = self.textbox_prosa.get("1.0", "end-1c").strip()
            lineas = []
            for seg in texto.split('\n'):
                lineas.extend(textwrap.wrap(seg, width=max_chars) or [''])
            y = 1100
            for l in lineas:
                draw.text((200, y), l, font=fuente, fill=(50,50,50))
                bbox = draw.textbbox((0,0), l, font=fuente)
                y += (bbox[3]-bbox[1]) + espacio
        else:
            instrucciones = []
            for widget in self.instrucciones_widgets:
                # Buscar el textbox dentro del widget
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkTextbox):
                        texto = child.get("1.0", "end-1c").strip()
                        if texto:
                            instrucciones.append(texto)
                        break
            
            y = 1100
            for i, instr in enumerate(instrucciones, 1):
                segs = instr.split('\n')
                envs = []
                for s in segs:
                    envs.extend(textwrap.wrap(s, width=max_chars) or [''])
                for j, line in enumerate(envs):
                    txt = f"{i}. {line}" if j==0 else f"    {line}"
                    draw.text((200, y), txt, font=fuente, fill=(50,50,50))
                    bbox = draw.textbbox((0,0), txt, font=fuente)
                    y += (bbox[3]-bbox[1]) + espacio
                y += espacio*2
        self._crear_pdf(imagen)
    def generar_sin_formato(self):
        # Similar a generar_con_formato pero simplificado
        imagen = Image.new("RGB", (2550, 3300), color="white")
        draw = ImageDraw.Draw(imagen)
        try:
            espacio = int(self.entry_interlineado.get())
            if espacio <= 0: espacio = 15
        except:
            espacio = 15
        datos = {
            "Nombre": self.entry_nombre.get(),
            "Edad": self.entry_edad.get(),
            "Fecha": self.entry_fecha.get(),
            "Peso": self.entry_peso.get(),
            "Talla": self.entry_talla.get(),
            "TA": self.entry_ta.get()
        }
        Fuente1 = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 50)
        draw.text((200, 800), f"Nombre: {datos['Nombre']}", font=Fuente1, fill=(50, 50, 50))
        draw.text((2000, 800), f"Edad: {datos['Edad']}", font=Fuente1, fill=(50, 50, 50))
        draw.text((200, 900), f"Fecha: {datos['Fecha']}", font=Fuente1, fill=(50, 50, 50))
        draw.text((800, 900), f"Peso: {datos['Peso']} kg", font=Fuente1, fill=(50, 50, 50))
        draw.text((1400, 900), f"Talla: {datos['Talla']} cm", font=Fuente1, fill=(50, 50, 50))
        draw.text((2000, 900), f"TA: {datos['TA']} mmHg", font=Fuente1, fill=(50, 50, 50))

        tam_fuente = int(self.entry_fuente.get()) if self.entry_fuente.get().isdigit() else 30
        max_chars = self._obtener_ancho_maximo(tam_fuente)
        fuente = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', tam_fuente)

        if self.checkbox_prosa.get():
            texto = self.textbox_prosa.get("1.0", "end-1c").strip()
            lineas = []
            y = 1100
            for seg in texto.split('\n'):
                lineas.extend(textwrap.wrap(seg, width=max_chars) or [''])
            for l in lineas:
                draw.text((200, y), l, font=fuente, fill=(50,50,50))
                bbox = draw.textbbox((0,0), l, font=fuente)
                y += (bbox[3]-bbox[1]) + espacio
        else:
            instrucciones = []
            for widget in self.instrucciones_widgets:
                # Buscar el textbox dentro del widget
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkTextbox):
                        texto = child.get("1.0", "end-1c").strip()
                        if texto:
                            instrucciones.append(texto)
                        break
            
            y = 1100
            for i, instr in enumerate(instrucciones, 1):
                segs = instr.split('\n')
                envs = []
                for s in segs:
                    envs.extend(textwrap.wrap(s, width=max_chars) or [''])
                for j, line in enumerate(envs):
                    txt = f"{i}. {line}" if j==0 else f"    {line}"
                    draw.text((200, y), txt, font=fuente, fill=(50,50,50))
                    bbox = draw.textbbox((0,0), txt, font=fuente)
                    y += (bbox[3]-bbox[1]) + espacio
                y += espacio*2
                
        self._crear_pdf(imagen)