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
                for url in rest_url:
                    cursor.execute("INSERT INTO Restaurants(link, parsed, cityID) VALUES(:link, :parsed,  :cityID)", url)
            cursor.execute("UPDATE Cities SET parsed = 1 WHERE id = :cityID", url)
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
                                photo_parsed INTEGER (5),
                                FOREIGN KEY(cityID) REFERENCES cities(id) ) 
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()


    def get_all_restaurants_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Restaurants WHERE photo_parsed = 1")
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


    def get_all_data_restaurants_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM DataRestaurants")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows


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


    def get_all_workhours_restaurants_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Workhours")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows

    def photo_restaurant_record(self, photo_dict):
        self.createTablePhoto()
        db = self.connect()
        cursor = db.cursor()
        try:
            for photo in photo_dict:
                parsed = photo['parsed']
                if parsed == 2:
                    break
                else:
                    cursor.execute("INSERT INTO Photo (restaurantID, photo_url, parsed"
                                   ") VALUES(:restaurantID, :photo_url, :parsed)", photo)
                    cursor.execute("UPDATE Restaurants SET photo_parsed = 1 WHERE id = :restaurantID", photo)
            cursor.close()
            db.commit()
            db.close()
            print('Add PHOTO from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")

    def photo_restaurant_record_is_none(self, photo_dict):
        self.createTablePhoto()
        db = self.connect()
        cursor = db.cursor()
        try:
            for photo in photo_dict:
                continue
            cursor.execute("UPDATE Restaurants SET photo_parsed = 2 WHERE id = :restaurantID", photo)
            cursor.close()
            db.commit()
            db.close()
            print('Add PHOTO from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")

    def createTablePhoto(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS Photo(
                                id       INTEGER       PRIMARY KEY AUTOINCREMENT
                                                       NOT NULL,
                                restaurantID   INTEGER       REFERENCES DataRestaurants (id),
                                photo_url VARCHAR (255),
                                parsed VARCHAR (255))
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()

    def get_all_photo_from_DB(self):
        db = self.connect()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Photo WHERE parsed = 0")
        rows = cursor.fetchall()

        cursor.close()
        db.commit()
        db.close()
        return rows

    def photo_path_restaurant_record(self, photo_dict):
        self.createTableRelativePathPhoto()
        db = self.connect()
        cursor = db.cursor()
        try:
            for photo in photo_dict:
                cursor.execute("INSERT INTO RelativePathPhoto (restaurantID, path"
                               ") VALUES(:restaurantID, :path)", photo)
            cursor.execute("UPDATE Photo SET parsed = 1 WHERE restaurantID = :restaurantID", photo)
            cursor.execute("UPDATE Restaurants SET photo_parsed = 0 WHERE id = :restaurantID", photo)
            cursor.close()
            db.commit()
            db.close()
            print('Add PHOTO from to DB')
        except sqlite3.Error as e:
            print(e)
            db.rollback()
            db.close()
            print("Insert DB error")

    def createTableRelativePathPhoto(self):
        db = self.connect()
        cursor = db.cursor()
        sql = """
                                CREATE TABLE IF NOT EXISTS RelativePathPhoto(
                                id       INTEGER       PRIMARY KEY AUTOINCREMENT
                                                       NOT NULL,
                                restaurantID   INTEGER       REFERENCES DataRestaurants (id),
                                path VARCHAR (500))
                                """
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()



    def is_many_rows(self, rows):
        if len(rows) > 1:
            print("Error" + rows + "Restorants has many IDs")
            return


    def getAddressByRestaurant(self, restaurant, connection):
        id = restaurant[0]

        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()

        return rows[0][9]

    def getPhoneByRestaurant(self, restaurant, connection):
        id = restaurant[0]

        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()

        return rows[0][6]

    def getPostalCodeByRestaurant(self, restaurant, connection):
        id = restaurant[0]

        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()

        return rows[0][13]

    def get_all_data_restaurants_from_DB_for_photo(self, restaurants):
        list = []
        db = self.connect()
        for restaurant in restaurants:
            id = restaurant[0]

            cursor = db.cursor()
            rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
            self.is_many_rows(rows)
            list.append(rows[0][0][1])
            cursor.close()
        db.close()

        return list

    def get_country_from_db_data_rest(self, restaurant):
        id = restaurant[0]
        db = self.connect()
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()
        db.close()

        return rows[0][12]

    def get_city_from_db_data_rest(self, restaurant):
        id = restaurant[0]
        db = self.connect()
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()
        db.close()

        return rows[0][10]

    def get_rest_name_from_db_data_rest(self, restaurant):
        id = restaurant[0]
        db = self.connect()
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM DataRestaurants WHERE restaurantID = " + str(id)).fetchall()
        self.is_many_rows(rows)
        cursor.close()
        db.close()

        return rows[0][1]

    def get_photo_urls_from_db_data_rest(self, restaurant):
        list = []
        id = restaurant[0]
        db = self.connect()
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM Photo WHERE restaurantID = " + str(id)).fetchall()
        for urls in rows:
            url = urls[2]
            list.append(url)
        cursor.close()
        db.close()

        return list
