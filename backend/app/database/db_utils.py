import mysql.connector


from database.config import get_settings

settings = get_settings()

params = {
    'host': settings.host,
    'user': settings.user,
    'password': settings.password,
    'database': settings.database
}



class Database():
    def __init__(self):
        self.params = params
        self.connect = mysql.connector.connect(**params)
        self.cursor = self.connect.cursor()


    def fetch_data(self, request):
        """ Pour SELECT """
        try:
            self.cursor.execute(request)
            data = self.cursor.fetchall()
            return data
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}
        finally:
            self.close()

    def insert_data(self, request):
        """ POUR  UPDATE, INSERT, DELETE"""
        try:
            self.cursor.execute(request)
            self.connect.commit()
            return {"success": True}
        except mysql.connector.Error as err:
            return {"success": False, "error": str(err)}
        finally:
            self.close()

    def close(self):
        self.cursor.close()
        self.connect.close()
