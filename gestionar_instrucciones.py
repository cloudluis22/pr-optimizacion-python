import customtkinter as ctk
import textwrap

class GestorInstrucciones:
    """
    Clase para gestionar la adición y eliminación de widgets de instrucciones
    dentro de un CTkScrollableFrame.
    """
    def __init__(self, scrollable_frame):
        self.scrollable_frame = scrollable_frame
        self.instrucciones_widgets = []
        self._agregar_widget()  # agrega la instrucción inicial

    def _agregar_widget(self):
        frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#61461F")

        num_inst = len(self.instrucciones_widgets) + 1
        label = ctk.CTkLabel(
            frame,
            text=f" INSTRUCCIÓN {num_inst}:",
            font=ctk.CTkFont(family="Arial", size=9, weight="bold"),
            text_color="white"
        )
        label.pack(side="left", padx=(0, 5))

        textbox = ctk.CTkTextbox(
            frame,
            height=50,
            wrap="word",
            fg_color="white",
            border_color="white",
            border_width=1,
            text_color="black"
        )
        textbox.pack(side="left", fill="both", expand=True, padx=(0, 5))

        # Ajuste dinámico de altura
        def ajustar_altura(event=None):
            contenido = textbox.get("1.0", "end-1c")
            lineas = contenido.count("\n") + 1
            ancho = textbox.winfo_width() or textbox.winfo_reqwidth()
            chars_por_linea = max(30, ancho // 8)
            for parrafo in contenido.split("\n"):
                if len(parrafo) > chars_por_linea:
                    lineas += len(parrafo) // chars_por_linea
            altura = max(50, min(300, lineas * 20 + 10))
            textbox.configure(height=altura)
            frame.update_idletasks()

        textbox.bind("<KeyRelease>", ajustar_altura)
        textbox.bind("<FocusOut>", ajustar_altura)
        textbox.after(100, ajustar_altura)

        frame.pack(fill="x", pady=3)
        self.instrucciones_widgets.append(frame)

    def agregar(self):
        self._agregar_widget()

    def eliminar(self):
        if len(self.instrucciones_widgets) > 1:
            self.instrucciones_widgets.pop().destroy()