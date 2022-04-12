# Mysql
from mysql.connector import connect



class UserConnection:
    """ Clase que crea la conección a la db y hacer las consultas a la 
        tabla de User.
    """


    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)


    def Select(self, query: str):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            data.append({
                "username": x[1],
                "email": x[2],
                "full_name": x[3],
                "password": x[4]
            })
        cursor.close()
        return data


    def Insert(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    def Delete(self,query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    def Update(self,query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()