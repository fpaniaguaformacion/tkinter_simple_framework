import logging
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import DISABLED, END, LEFT
from ui_core.simple_gui_components import SimpleTable
from ui_core.simple_gui_components import SuperFrame
from persistencia.gestor_peliculas import GestorBBDD
from model.pelicula import Pelicula

class FrameEdicion(SuperFrame):
    #Botones
    BUTTONS_WIDTH=100
    BUTTONS_HEIGHT=50
    buttons_images=[]
    #Tabla
    TABLE_WIDTH = 1000 #Ancho de la tabla
    TABLE_HEIGHT = 330 #Alto de la tabla
    ROWS_HEIGHT = 25 #Altura de cada fila
    VISIBLE_ROWS = int(TABLE_HEIGHT/ROWS_HEIGHT) #Número de filas visibles
    
    TABLE_X_POS = 10
    TABLE_Y_POS = 80
    ODD_ROW_COLOR = "#FFDA8A" 
    EVEN_ROW_COLOR = "#FFF9EC"
    #Color de fondo
    BG_COLOR = None
    def __init__(self, parent, width, height):
        SuperFrame.__init__(self, parent, bg=self.BG_COLOR, width=width, height=height)
        #Botones para la toolbar
        buttons = (
            ("Actualizar",self.reload,"icons/refresh.png"),
            ("Borrar",self.delete,"icons/delete.png"),
            ("Save",self.save,"icons/save.png"),            
            ("",self.create_pdf,"icons/pdf.png")
        ) 
        self.createToolbar(buttons, self.BUTTONS_WIDTH, self.BUTTONS_HEIGHT)
        self.init_components()
        self.pack()      
    
    def init_components(self):
        logging.debug("Inicializando componentes...")
        #Tabla
        columns_ids = tuple(range(1,5))
        columns_names = ("ID","Título","Director","Año") 

        self.table = SimpleTable(self, 
            columns_ids=columns_ids, columns_names=columns_names, 
            table_with=self.TABLE_WIDTH, visible_rows=self.VISIBLE_ROWS, rows_height=self.ROWS_HEIGHT,
            odd_rows_bg_color=self.ODD_ROW_COLOR, even_rows_bg_color=self.EVEN_ROW_COLOR)
        self.table.place(x=self.TABLE_X_POS, y=self.TABLE_Y_POS)

        self.table.bind("<Double-1>", self.edit)
        self.table.bind("<<TreeviewSelect>>", self.edit)
        
        #Datos
        self.label_id = tk.Label(self, text="Id:", background=self.BG_COLOR)
        self.label_id.place(x=300,y=450)
        self.entry_id = tk.Entry(self, width=50, state="readonly")
        self.entry_id.place(x=390, y=450)

        self.label_titulo = tk.Label(self, text="Titulo:", background=self.BG_COLOR)
        self.label_titulo.place(x=300,y=480)
        self.entry_titulo = tk.Entry(self, width=50)
        self.entry_titulo.place(x=390, y=480)

        self.label_director = tk.Label(self, text="Director:", background=self.BG_COLOR)
        self.label_director.place(x=300,y=510)
        self.entry_director = tk.Entry(self, width=50)
        self.entry_director.place(x=390, y=510)

        self.label_anyo = tk.Label(self, text="Año estreno:", background=self.BG_COLOR)
        self.label_anyo.place(x=300,y=540)
        self.entry_anyo = tk.Entry(self, width=25)
        self.entry_anyo.place(x=390, y=540)

    def reload(self):
        print("Recargando...")
        #Borramos la tabla
        self.table.clear_all()
        #Instanciamos el gestor de persistencia
        gestor = GestorBBDD()

        #Obtenemos todas las películas
        lista_peliculas = gestor.findAll()
        #Pasamos las películas a la tabla        
        self.table.insert_rows(lista_peliculas, 0)    

    def delete(self):
        logging.debug("Borrando...")
        if (self.table.get_selected_row_index()==""):
            tk.messagebox.showerror(title="Error", message="Debe seleccionar una película")
        else:
            row_index = int(self.table.get_selected_row_index())
            reply = tk.messagebox.askyesno(message="¿Está seguro de que desea eliminar la película?", title="Aviso")
            if (reply==True):
                gestor=GestorBBDD()
                gestor.delete(row_index)
                self.reload()
                tk.messagebox.showinfo(title="Aviso", message="La película se ha eliminado correctamente") 

    def edit(self, event=None):
        logging.debug("Editando...")
        if (self.table.get_selected_row_values()==""):
            self.clear_entry_text()
        else:
            selected_row = self.table.get_selected_row_values()
            self.set_entry_text(self.entry_id, selected_row[0])
            self.set_entry_text(self.entry_titulo, selected_row[1])
            self.set_entry_text(self.entry_director, selected_row[2])
            self.set_entry_text(self.entry_anyo, selected_row[3])
            
    def save(self):
        logging.debug("Guardando...")
        id = self.entry_id.get()
        if (id==""):
            tk.messagebox.showerror(title="Error", message="Debe seleccionar una película")
        else:
            id = int(id)
            titulo = self.entry_titulo.get()
            director = self.entry_director.get()
            anyo = int(self.entry_anyo.get())
            pelicula = Pelicula(id, titulo, director, anyo, None)
            reply = tk.messagebox.askyesno(message="¿Está seguro de que desea modificar la película?", title="Aviso")
            if (reply==True):
                gestor=GestorBBDD()
                gestor.update(pelicula)
                tk.messagebox.showinfo(title="Aviso", message="La película se ha modificado correctamente") 
                self.reload()
                self.clear_entry_text()

    def clear_entry_text(self):
        self.set_entry_text(self.entry_id, "")
        self.set_entry_text(self.entry_titulo, "")
        self.set_entry_text(self.entry_director, "")
        self.set_entry_text(self.entry_anyo, "")

    def create_pdf(self):
        logging.debug("Creando pdf...")