import sqlite3

class DB:

    def connect(self):
        db = sqlite3.connect('C:/Users/sumyt/PycharmProjects/TripadvisorParser/tripadvisorNew.db')
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
                            city_name VARCHAR(255), 
                            parsed BOOLEAN ) 
                            """
        cursor.execute(sql)
        cursor.close()
        db.commit()

    def add_cities_to_DB(self, city_urls, db):
        cursor = db.cursor()
        for url in city_urls:
            cursor.execute("INSERT INTO Cities(link, city_name, parsed) VALUES(:link, :city_name, :parsed)", url)
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



    def restaurant_record(self, rest_dict):
        self.createTableDataRestaraunts()
        db = self.connect()
        cursor = db.cursor()
        if not rest_dict:
            return
        try:
            for rest in rest_dict:
                cursor.execute("INSERT INTO DataRestaurants(restName, latitude, longitude, timeZone, restaurantID, phone,"
                               "website, email, street, city, state, country, postaLcode, description, priceLevel,"
                               "cuisine, photoParsed) VALUES(:restName, :latitude, :longitude, :timeZone, :restaurantID, :phone,"
                               ":website, :email, :street, :city, :state, :country, :postaLcode, :description,"
                               ":priceLevel, :cuisine, :photoParsed)",
                               rest)
            cursor.execute("UPDATE Restaurants SET parsed = 1 WHERE id = :restaurantID", rest)
            cursor.close()
            db.commit()
            db.close()
            print('Add restaurants from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")
            pass


    def createTableDataRestaraunts(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS DataRestaurants (
                                id                     INTEGER       PRIMARY KEY AUTOINCREMENT
                                                                     NOT NULL,
                                restName               VARCHAR (255),
                                latitude               VARCHAR (255),
                                longitude              VARCHAR (255),
                                timeZone               VARCHAR,
                                restaurantID           INTEGER       REFERENCES Restaurants (cityID),
                                phone                  VARCHAR (255),
                                website                VARCHAR (255),
                                email                  VARCHAR (255),
                                street                 VARCHAR (255),
                                city                   VARCHAR (255),
                                state                  VARCHAR (255),
                                country                VARCHAR (255),
                                postaLcode             VARCHAR (255),
                                description            VARCHAR (255),
                                priceLevel             VARCHAR (255),
                                cuisine                VARCHAR (255),
                                photoParsed            BOOLEAN
                                ) 
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()

    def work_time_restaurant_record(self, work_time):
        self.createTableWorkhours()
        db = self.connect()
        cursor = db.cursor()
        if not work_time:
            return
        try:
            for rest in work_time:
                cursor.execute("INSERT INTO Workhours (restaurantID, weekday, from_1, to_1, from_2, to_2"
                               ") VALUES(:restaurantID, :weekday, :from_1, :to_1, :from_2, :to_2)", rest)
            # cursor.execute("UPDATE Restaurants SET parsed = 1 WHERE id = :cityID", rest)
            cursor.close()
            db.commit()
            db.close()
            print('Add WORK_TIME from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")


    def createTableWorkhours(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS Workhours (
                                id                     INTEGER       PRIMARY KEY AUTOINCREMENT
                                                                     NOT NULL,
                                restaurantID INTEGER   REFERENCES Restaurants (id) 
                                                       NOT NULL,
                                weekday      CHAR (10),
                                from_1       DATETIME,
                                to_1         DATETIME,
                                from_2       DATETIME,
                                to_2         DATETIME
                                ) 
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