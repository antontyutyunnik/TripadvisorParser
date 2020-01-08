import sqlite3

class DB:

    def connect(self):
        db = sqlite3.connect('C:/Users/sumyt/PycharmProjects/TripadvisorParser/tripadvisor.db')
        return db

    def createTableCities(self, db):
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS Cities")
        sql = """
                            CREATE TABLE Cities(
                            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,                     
                            link VARCHAR(255), 
                            parsed BOOLEAN ) 
                            """
        cursor.execute(sql)
        cursor.close()
        db.commit()

    def add_cities_to_DB(self, city_urls, db):
        cursor = db.cursor()
        for url in city_urls:
            cursor.execute("INSERT INTO Cities(link, parsed) VALUES(:link, :parsed)", url)
        cursor.close()
        db.commit()
        db.close()

    def write_cities(self, city_urls):
        db = self.connect()
        self.createTableCities(db)
        self.add_cities_to_DB(city_urls, db)


    def get_all_cities_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cities")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows

    # def write_restaurants(self, city_urls):
    #     db = self.connect()
    #     self.get_all_cities_from_DB(db)