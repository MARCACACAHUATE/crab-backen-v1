# Mysql
from mysql.connector import connect



class UserConnection:

    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)


    def Select(self, query):
        data = []
        cursor = self.conn.cursor()
        cursor.execute(query)
        for x in cursor:
            data.append({
                "username": x[1],
                "password": x[2]
            })
        cursor.close()
        return data


    def Insert(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    def Delete(self,query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()


    def Update(self,query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()