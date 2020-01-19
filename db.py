import sqlite3

class DB:

    def connect(self):
        db = sqlite3.connect('C:/Users/sumyt/PycharmProjects/TripadvisorParser/tripadvisor.db')
        return db

    def write_cities(self, city_urls):
        db = self.connect()
        self.createTableCities(db)
        self.add_cities_to_DB(city_urls, db)

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

    def get_all_cities_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Cities")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows


    def write_restaurants(self, rest_urls):
        self.createTableRestaraunts()
        db = self.connect()
        cursor = db.cursor()
        if not rest_urls:
            return
        try:
            for rest_url in rest_urls:
                cursor.execute("INSERT INTO Restaurants(link, parsed, cityID) VALUES(:link, :parsed,  :cityID)", rest_url)
            cursor.execute("UPDATE Cities SET parsed = 1 WHERE id = :cityID", rest_url)
            cursor.close()
            db.commit()
            db.close()
            print('Add restaurants from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")



    def createTableRestaraunts(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS Restaurants(
                                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,                     
                                link VARCHAR(255),
                                parsed BOOLEAN, 
                                cityID INTEGER,
                                FOREIGN KEY(cityID) REFERENCES cities(id) ) 
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()


    def get_all_restaurants_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Restaurants")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows

    def write_data_restaurants(self, rest_urls):
        self.createTableRestaraunts()
        db = self.connect()
        cursor = db.cursor()
        if not rest_urls:
            return
        try:
            for rest_url in rest_urls:
                cursor.execute("INSERT INTO Restaurants(link, parsed, cityID) VALUES(:link, :parsed,  :cityID)", rest_url)
            cursor.execute("UPDATE Cities SET parsed = 1 WHERE id = :cityID", rest_url)
            cursor.close()
            db.commit()
            db.close()
            print('Add restaurants from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")



    def createTableDataRestaraunts(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS DataRestaurants (
                                id       INTEGER       PRIMARY KEY AUTOINCREMENT
                                                       NOT NULL,
                                restName VARCHAR (255),
                                address  VARCHAR (255),
                                parsed   BOOLEAN,
                                cityID   INTEGER       REFERENCES Restaurants (cityID),
                                phone    VARCHAR (255),
                                siteLink VARCHAR (255),
                                workTime VARCHAR (255))
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()

    def createTableFoto(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS Foto(
                                id       INTEGER       PRIMARY KEY AUTOINCREMENT
                                                       NOT NULL,
                                nameFoto VARCHAR (255),
                                restaurantID   INTEGER       REFERENCES DataRestaurants (id),
                                parsed VARCHAR (255))
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()