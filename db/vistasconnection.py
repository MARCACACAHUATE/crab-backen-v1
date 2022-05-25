# Mysql
from mysql.connector import connect



class VistasConnection:
    """ Clase que crea la conección a la db y hacer las consultas a la 
        tabla de User.
    """


    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)


    def noticiasDia(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            row = x[1:]
            data.append({
                "categoria": x[0],
                "total_noticias": x[1],
                "fecha": x[2]
            })
        cursor.close()
        return data


    def noticiasDataset(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            data.append({
                "id": x[0],
                "titulo": x[1],
                "contendio": x[2],
                "fecha": x[3],
                "categorias_id": x[4],
                "paginas": x[5]
            })
        cursor.close()
        return data

    def noticiasPagina(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            data.append({
                "nombre": x[0],
                "total_noticias": x[1]
            })
        cursor.close()
        return data