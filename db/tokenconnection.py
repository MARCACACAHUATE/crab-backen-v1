from mysql.connector import connect

class TokenConnection:


    def __init__(self, **kwargs):
        self.conn = connect(**kwargs)
