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



    def createTableRestaraunts(self):
        db = sqlite3.connect('C:/SQLLiteDB/tripadvisor_db.db')
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS restaurants")
        sql = """
                                CREATE TABLE restaurants(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,                     
                                link VARCHAR(255),
                                parsed BOOLEAN, 
                                cityID INTEGER,
                                FOREIGN KEY(cityID) REFERENCES Cities(id) ) 
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()