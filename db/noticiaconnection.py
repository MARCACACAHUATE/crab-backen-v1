# MySQL
from mysql.connector import connect

class NoticiaConnect:


    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)


    def List_Noticias(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            row = x[1:]
            data.append({
                "id": x[0],
                "titulo": row[0],
                "contenido": row[1],
                "fecha": row[2],
                "categoria": row[6],
                "pagina": row[8],
            })
        cursor.close()
        return data
    
    def Select(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            data.append({
                "id": x[0],
                "titulo": x[1],
                "contenido": x[2],
                "fecha": x[3],
                "categoria_id": x[4],
                "pagina_id": x[5]
            })
        cursor.close()
        return data


    def Insert(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    def Delete(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    
    def Update(self, query: str):
        print("Esta madre no hace nada")