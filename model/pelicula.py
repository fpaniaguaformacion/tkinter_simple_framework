class Pelicula:
    id = None
    titulo = None
    director = None
    anyo = 0
    productora = None
    def __init__(self, id, titulo, director, anyo, genero=None):
        self.id = id
        self.titulo = titulo
        self.director = director
        self.anyo = anyo
        self.genero = genero

