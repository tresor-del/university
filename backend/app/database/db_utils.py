import mysql.connector


from app.database.config import get_settings

settings = get_settings()

params = {
    'host': settings.host,
    'user': settings.user,
    'password': settings.password,
    'database': settings.database
}


class Database:
    def __init__(self):
        self.connect = None

    def connect_db(self):
        if not self.connect or not self.connect.is_connected():
            self.connect = mysql.connector.connect(**params)

    def get_data(self, query, values=None):
        """Pour SELECT"""
        try:
            self.connect_db()
            with self.connect.cursor() as cursor:
                cursor.execute(query, values or ())
                return cursor.fetchall()
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}

    def execute(self, query, values=None):
        """Pour INSERT, UPDATE, DELETE"""
        try:
            self.connect_db()
            with self.connect.cursor() as cursor:
                cursor.execute(query, values or ())
                self.connect.commit()
                return {"success": True}
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}

    def close(self):
        if self.connect and self.connect.is_connected():
            self.connect.close()
