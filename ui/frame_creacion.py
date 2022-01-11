import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import LEFT
from persistencia.gestor_peliculas import GestorBBDD
from ui_core.simple_gui_components import SuperFrame
from model.pelicula import Pelicula
import logging

class FrameCreacion(SuperFrame):
    #Botones
    BUTTONS_WIDTH=100
    BUTTONS_HEIGHT=50
    #Color de fondo
    BG_COLOR = None

    def __init__(self, parent, width, height):
        SuperFrame.__init__(self, parent, bg=FrameCreacion.BG_COLOR, width=width, height=height)

        #Botones para la toolbar
        buttons = (
            ("Guardar",self.guardar,"icons/save.png"),
        ) 
        self.createToolbar(buttons, FrameCreacion.BUTTONS_WIDTH, FrameCreacion.BUTTONS_HEIGHT)
        
        self.init_components()

        self.pack()

    def init_components(self):
        logging.debug("Inicializando componentes...")

        #Título
        self.label_titulo = tk.Label(self, text="Titulo:", background=FrameCreacion.BG_COLOR)
        self.label_titulo.place(x=300,y=200)
        self.entry_titulo = tk.Entry(self, width=50)
        self.entry_titulo.place(x=390, y=200)

        #Lista de géneros
        self.label_genero = tk.Label(self, text="Género:", background=FrameCreacion.BG_COLOR)
        self.label_genero.place(x=300, y=230)
        generos = self.get_generos()
        self.variable = tk.StringVar(self)
        self.variable.set(generos[0])
        self.menu_generos = tk.OptionMenu(self, self.variable, *generos)
        self.menu_generos.config(width=12)
        self.menu_generos.place(x=387, y=225)
        self.label_advertencia = tk.Label(self, text="(solo para demostración)", background=FrameCreacion.BG_COLOR,
                                          foreground="red")
        self.label_advertencia.place(x=510, y=230)

        #Director
        self.label_director = tk.Label(self, text="Director:", background=FrameCreacion.BG_COLOR)
        self.label_director.place(x=300,y=260)
        self.entry_director = tk.Entry(self, width=30)
        self.entry_director.place(x=390, y=260)

        #Año de estreno
        self.label_anyo = tk.Label(self, text="Año estreno:", background=FrameCreacion.BG_COLOR)
        self.label_anyo.place(x=300,y=290)
        self.entry_anyo = tk.Entry(self, width=4, justify=tk.RIGHT)
        self.entry_anyo.place(x=390, y=290)

    def guardar(self):
        logging.debug("Guardando...")
        titulo = self.entry_titulo.get() #Obtiene el texto que hay en la caja de texto del título
        director = self.entry_director.get()
        anyo = int(self.entry_anyo.get())
        genero = self.variable.get()
        pelicula = Pelicula(0, titulo, director, anyo, genero)
        try:
            gestor = GestorBBDD()
            gestor.create(pelicula)
            tk.messagebox.showinfo(title="Aviso", message="La película se ha creado satisfactoriamente") 
            self.entry_titulo.delete(0,"end")
            self.entry_director.delete(0,"end")
            self.entry_anyo.delete(0,"end")
        except Exception as e:
            logging.error(e)
            tk.messagebox.showerror(title="Error", message="Error al crear la película")

    def get_generos(self):
        gestor = GestorBBDD()
        generos = gestor.getAllGeneros()
        return generos