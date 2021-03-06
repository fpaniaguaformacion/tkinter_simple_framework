import logging
import sys
import os
from tkinter import *
import tkinter.messagebox
import json
from ui.frame_creacion import FrameCreacion
from ui.frame_edicion import FrameEdicion

class GUIApp:
    CONFIG_FILE_NAME = "config.json"
    window_width = 0
    window_height = 0
    app_title = None
    app = Tk()
    frames = {}

    # Constructor
    def __init__(self) -> None:
        self.read_config()
        self.init_window()
        self.init_menu()
        self.init_frames()
        GUIApp.app.mainloop()

    # Lectura de la configuración de la APP
    def read_config(self):
        if(not os.path.exists(GUIApp.CONFIG_FILE_NAME)):
            logging.debug("Creando fichero de configuración")
            self.create_default_config_file()
        logging.debug("Leyendo fichero de configuración")
        with open(GUIApp.CONFIG_FILE_NAME,mode="r") as json_file:
            config = json.load(json_file)
        GUIApp.app_title = config["APP_TITLE"]
        GUIApp.window_width = int(config["WINDOW_WIDTH"])
        GUIApp.window_height = int(config["WINDOW_HEIGHT"])

    def create_default_config_file(self):
        config = {
            "APP_TITLE":"Default App Name",
            "WINDOW_WIDTH":1024,
            "WINDOW_HEIGHT":768
        }
        with open(GUIApp.CONFIG_FILE_NAME,mode="w") as json_file:
            json.dump(config, json_file)


    # Construcción de la ventana
    def init_window(self):
        logging.debug("Entrando en create_window")
        screen_width = GUIApp.app.winfo_screenwidth()
        screen_height = GUIApp.app.winfo_screenheight()
        OFFSET_X = int((screen_width - GUIApp.window_width) / 2)
        OFFSET_Y = int((screen_height - GUIApp.window_height) / 2)
        GUIApp.app.geometry(
            f"{GUIApp.window_width}x{GUIApp.window_height}+{OFFSET_X}+{OFFSET_Y}")
        GUIApp.app.resizable(False, False)
        GUIApp.app.title(GUIApp.app_title)

    # Construcción del menú
    def init_menu(self):
        logging.debug("Entrando en init_menu")
        menubar = Menu(GUIApp.app)
        menu_archivo = ("Archivo", (("Nuevo", ), ("Abrir",),
            ("Guardar",), ("Cerrar",), None, ("Salir", self.exit)))
        menu_editar = ("Editar", (("Cortar",), ("Copiar",), ("Pegar",)))
        menu_ventanas = ("Peliculas", 
            (
                ("Crear",self.mostrar_frame_creacion),
                ("Editar",self.mostrar_frame_edicion)
        ))
        menu_ayuda = ("Ayuda", (("Ayuda",), None, ("Acerca de...", self.about)))
        menus = (menu_archivo, menu_editar, menu_ventanas, menu_ayuda)
        GUIApp.app.config(menu=menubar)
        for menu in menus:
            nuevo_menu = Menu(menubar, tearoff=0)
            for opcion in menu[1]:
                if opcion == None:
                    nuevo_menu.add_separator()
                else:
                    if (len(opcion) == 1):
                        nuevo_menu.add_command(label=opcion[0], state=DISABLED)
                    else:
                        nuevo_menu.add_command(
                            label=opcion[0], command=opcion[1])
            menubar.add_cascade(label=menu[0], menu=nuevo_menu)

    #Inicialización de las "pantallas" (Frames) de la aplicación
    def init_frames(self):
        logging.debug("Entrando en init_frames")
        GUIApp.frames["FrameCreacion"]=FrameCreacion(GUIApp.app, GUIApp.window_width, GUIApp.window_height)
        GUIApp.frames["FrameEdicion"]=FrameEdicion(GUIApp.app, GUIApp.window_width, GUIApp.window_height)
        self.mostrar_frame_edicion()

    #Cambio de Frame 
    def showFrame(self, frameName):
        logging.debug("Entrando en mostrarFrame")
        for frame in GUIApp.frames.values():
            frame.pack_forget()
        GUIApp.frames[frameName].pack()
    
    def mostrar_frame_creacion(self):
        logging.debug("Entrando en mostrar_frame_creacion")
        self.showFrame("FrameCreacion")
    
    def mostrar_frame_edicion(self):
        logging.debug("Entrando en mostrar_frame_edicion")
        self.showFrame("FrameEdicion")
        
    def exit(self):
        logging.debug("Entrando en exit")
        sys.exit()

    def about(self):
        logging.debug("Entrando en About...")
        tkinter.messagebox.showinfo(title="Python Simple GUI Framework", message="Fernando Paniagua (2021)\nfernando.paniagua.formacion@gmail.com")

if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
    app = GUIApp()