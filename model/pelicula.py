class Pelicula:
    id = None
    titulo = None
    director = None
    anyo = 0
    productora = None
    def __init__(self, id, titulo, director, anyo, productora):
        self.id = id
        self.titulo = titulo
        self.director = director
        self.anyo = anyo
        self.productora = productora