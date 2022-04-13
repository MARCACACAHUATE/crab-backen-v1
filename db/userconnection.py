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
            row = x[1:]
            data.append({
                "username": row[0],
                "email": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "password": row[4],
                "is_admin": bool(row[5]),
                "is_active": bool(row[6]),
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