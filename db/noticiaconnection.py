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
                "contenido": row[0],
                "fecha": row[1],
                "categoria": row[5],
                "pagina": row[7],
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
                "contenido": x[1],
                "fecha": x[2],
                "categoria_id": x[3],
                "pagina_id": x[4]
            })
        cursor.close()
        return data


    def Insert(self, query: str):
        print("Esta madre no hace nada")
    
    
    def Delete(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    
    def Update(self, query: str):
        print("Esta madre no hace nada")