import sqlite3
import logging

from model.pelicula import Pelicula

class GestorBBDD:
    # Atributos estáticos
    DATABASE_NAME = "./datos/bbdd_peliculas.db"

    # Constructor
    def __init__(self):
        #Atributos
        self.connection = sqlite3.connect(GestorBBDD.DATABASE_NAME)
        self.crear_esquema_normal()

    # Destructor
    def __del__(self):
        self.connection.close()

    # Métodos
    def crear_esquema_normal(self):
        cursor = self.connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS peliculas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, director TEXT NOT NULL, anyo INTEGER NOT NULL)"
        sql = "CREATE TABLE IF NOT EXISTS generos (id INTEGER PRIMARY KEY AUTOINCREMENT, genero TEXT NOT NULL)"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def create(self, pelicula):
        cursor = self.connection.cursor()
        sql = f"INSERT INTO peliculas (titulo, director, anyo) VALUES ('{pelicula.titulo}', '{pelicula.director}', {pelicula.anyo})"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()
        
    def findAll(self):
        cursor = self.connection.cursor()
        sql = "SELECT * FROM peliculas"
        lista_peliculas = cursor.execute(sql).fetchall()
        cursor.close()
        return lista_peliculas

    def findById(self, id):
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM peliculas where id={id}"
        registro = cursor.execute(sql).fetchone()
        pelicula = Pelicula(registro[0],registro[1],registro[2],registro[3])
        cursor.close()
        return pelicula

    def delete(self, id):
        cursor = self.connection.cursor()
        sql = f"DELETE FROM peliculas where id={id}"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def update(self, pelicula):
        cursor = self.connection.cursor()
        sql = f"UPDATE peliculas SET titulo='{pelicula.titulo}', director='{pelicula.director}', anyo={pelicula.anyo} WHERE id={pelicula.id}"
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

    def getAllDirectors(self):
        cursor = self.connection.cursor()
        sql = "SELECT distinct(director) FROM peliculas ORDER BY director"
        lista_directores = cursor.execute(sql).fetchall()
        lista_directores = [director[0] for director in lista_directores]
        cursor.close()
        return lista_directores

    def getAllGeneros(self):
        cursor = self.connection.cursor()
        sql = "SELECT genero FROM generos ORDER BY genero"
        generos = cursor.execute(sql).fetchall()
        generos = [genero[0] for genero in generos]
        cursor.close()
        return generos