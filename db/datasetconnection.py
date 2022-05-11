from mysql.connector import connect

class DatasetConnection:
    """ Esta clase es de prueba en donde voy a usar
        otra forma de traer los datos de la base de datos.
    """

    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)

    
    def Select(self, query: str = None):
        data = []
        cursor = self.conn.cursor()
        
        if query == None:
            cursor.execute(f"SELECT * FROM datasets")
        else:
            cursor.execute(query)

        for row in cursor:
            data.append({
                "id": row[0],
                "fecha_inicio": row[1],
                "fecha_fin": row[2],
                "usuario_id": row[3]
            })
        cursor.close()
        return data


    def Insert(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    def Delete(self, id: int):
        """Recibe el id del elemento que se quiere eliminar y
        regresa ese elemento despues de ser eliminado"""
        cursor = self.conn.cursor()
        data = self.Select(query = f"SELECT * FROM datasets WHERE id={id}")
        cursor.execute(f"DELETE FROM datasets WHERE id={id}")
        self.conn.commit()
        cursor.close()
        return data


    def Update(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()