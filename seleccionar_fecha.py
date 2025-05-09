
import tkinter as tk
import customtkinter as ctk
from tkcalendar import Calendar
import datetime

class SeleccionarFecha:

    def __init__(self, parent, entry_fecha):
        self.parent = parent
        self.entry_fecha = entry_fecha
        self._open_calendar()

    def _open_calendar(self):
        top = ctk.CTkToplevel(self.parent)
        top.title("Seleccionar Fecha")
        top.geometry("300x200")
        top.resizable(0, 0)
        top.grab_set()

        try:
            fecha_existente = datetime.datetime.strptime(
                self.entry_fecha.get(), "%d/%m/%y"
            )
        except ValueError:
            fecha_existente = datetime.datetime.today()

        cal = Calendar(
            top,
            selectmode='day',
            year=fecha_existente.year,
            month=fecha_existente.month,
            day=fecha_existente.day,
            date_pattern='dd/mm/yyyy'
        )
        cal.pack(pady=10)

        btn_aceptar = ctk.CTkButton(
            top,
            text="Seleccionar",
            command=lambda: self._set_date(cal, top),
            fg_color="#2CC985",
            hover_color="#239561"
        )
        btn_aceptar.pack(pady=5)

    def _set_date(self, cal, top):
        fecha_seleccionada = cal.get_date()
        fecha_obj = datetime.datetime.strptime(fecha_seleccionada, "%d/%m/%Y")
        fecha_formateada = fecha_obj.strftime("%d/%m/%y")
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, fecha_formateada)
        top.destroy()